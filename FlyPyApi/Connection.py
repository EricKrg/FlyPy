
import FlyPyApi
import requests
import json
import math
import configparser

config = configparser.ConfigParser()
config.read('FlyPyConfig.ini')
if config['es']['local'] == 'y':
    conApi = config['es']['esURL'] + "/routes/"
else:
    conApi = config['es']['esClusterURL'] + "/routes/"

class Connection:
    def __init__(self, start: str, end: str):
        # a connection route could be flown by multiple airlines with diffrent equip
        self.airline = []
        self.sourceAirport = ''  # FlyPyApi.Airport(IATA=start)
        self.destinationAirport = ''  # FlyPyApi.Airport(IATA=end)
        self.equipment = []

        try:
            searchBody = {
                      "size": 1000,
                      "query": {
                        "bool": {
                          "must": [
                            { "term": { "sourceAirport.keyword":start }},
                            { "term": { "destinationAirport.keyword": end }}
                          ]
                        }
                      }
                    }
            req = requests.post(conApi + '_search', json=searchBody)
            json_res = json.loads(req.content)
            hits = json_res.get('hits').get('hits')
            for connect in hits:
                con_dict = connect.get('_source')
                self.sourceAirport = con_dict['sourceAirport']
                self.destinationAirport = con_dict['destinationAirport']
                self.airline.append(con_dict['airline'])
                self.equipment.append(con_dict['equipment'])
        except ConnectionError:
            print("no connection to elastic search")
        self.sourceAirport = FlyPyApi.Airport(IATA=self.sourceAirport)
        self.destinationAirport = FlyPyApi.Airport(IATA=self.destinationAirport)
        self.distance = self.getDistance()
        self.direction = self.getDirection()

    def getGeom(self):
        return self.sourceAirport.getCoords(), self.destinationAirport.getCoords()

    def getDistance(self):
        R = 6371000

        coord1 = self.sourceAirport.getCoords()
        coord2 = self.destinationAirport.getCoords()

        rad1 = math.radians(coord1[0])
        rad2 = math.radians(coord2[0])

        y = math.radians(coord2[0] - coord1[0])
        gam = math.radians(coord2[1] - coord1[1])

        a = math.sin(y / 2) * math.sin(y / 2) + \
            math.cos(rad1) * math.cos(rad2) * \
            math.sin(gam / 2) * math.sin(gam / 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round((R * c)/1000, 2)

    def getDirection(self):  # from source between 0-360deg

        coord1 = self.sourceAirport.getCoords()
        coord2 = self.destinationAirport.getCoords()

        lat1 = math.radians(coord1[0])
        lat2 = math.radians(coord2[0])

        diffLong = math.radians(coord2[1] - coord1[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                               * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing

    def serialze_to_json(self):
        res_json = {}
        for el in self.__dict__:
            if isinstance(self.__getattribute__(el), FlyPyApi.Airport):
                res_json[el] = self.__getattribute__(el).__dict__
            else:
                res_json[el] = self.__getattribute__(el)
        return res_json
    def __str__(self):
        return 'FROM: {} \t TO: {} \t FLOWN_BY: {} \t DISTANCE: {}'.format(self.sourceAirport.IATA,
                                                                           self.destinationAirport.IATA,
                                                                           self.airline, self.distance)

if __name__ == "__main__":
    con = Connection(start="FRA", end="JFK")
    con.serialze_to_json()
    brg = con.getDirection()
    print(con)