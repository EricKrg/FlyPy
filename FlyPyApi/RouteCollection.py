
from FlyPyApi import Airport, Connection

import requests
import json

conApi = 'http://es01:9200/routes/'

class RouteCollection:
    # an airport can have multiple connection going in out
    # todo
    #   - large connect collection
    #   - filter collection

    def __init__(self, iata: str, is_source: bool, heavy = False):

        #self.airport :Airport = Airport(IATA=iata)
        self.connectionSet = []  # light collection for searching
        self.connectionDict = {}
        self.heavy = heavy

        searchterm = "sourceAirport" if is_source else "destinationAirport"
        searchBody = {
              "size": 1000,
              "query": {
                "bool": {
                  "must": [
                    { "term": {"{}.keyword".format(searchterm): iata}}
                  ]
                }
              }
            }
        req = requests.get(conApi + '_search', json=searchBody)
        json_res = json.loads(req.content)
        hits = json_res.get('hits').get('hits')

        for con in hits:
            con_dict = con.get('_source')
            if is_source:
                if con_dict['destinationAirport'] in self.connectionSet: continue  # dont do double work
                self.connectionSet.append(con_dict['destinationAirport'])

            else:
                if con_dict['sourceAirport'] in self.connectionSet: continue
                self.connectionSet.append(con_dict['sourceAirport'])
        self.connectionSet = set(self.connectionSet)

        if self.heavy:
            for c in self.connectionSet:
                self.connectionDict[c] = Connection(iata,c)

    def search(self, searchIATA):
        try:
            match = searchIATA in self.connectionSet
            return match
        except KeyError:
            return False

    # shortest and longest direct flight
    def longestFlight(self):
        max_d = 0
        for k in self.connectionDict.keys():
            dist = self.connectionDict[k].distance
            if dist > max_d:
                max_d = dist
                flight = self.connectionDict[k]
        return flight

    def shortestFLight(self):
        min_d = float('inf')
        for k in self.connectionDict.keys():
            dist = self.connectionDict[k].distance
            if dist < min_d:
                min_d = dist
                flight = self.connectionDict[k]
        return flight

    def serialize_to_json(self):
        res_json = {}
        for el in self.connectionDict:
            res_json[el] = self.connectionDict[el].serialze_to_json()
        return res_json
    def __len__(self):
        return len(self.connectionSet)


if __name__ == "__main__":
    import time
    start = time.time()
    coll = RouteCollection("JFK", True)
    end = time.time()
    print(end - start)
    print(coll.longestFlight())
    print(coll.shortestFLight())
    coll.serialize_to_json()
    print(coll)





