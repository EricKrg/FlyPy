import FlyPyApi
import requests
import json
import re
import configparser

config = configparser.ConfigParser()
config.read('FlyPyConfig.ini')
if config['es']['local']:
    portApi = config['es']['esURL'] + "/airports/"
else:
    portApi = config['es']['esClusterURL'] + "/airports/"


class Airport:
    def __init__(self,default='', **kwargs):
        self.airportID= ''
        self.name=''
        self.city= ''
        self.country= ''
        self.IATA=''
        self.ICAO= ''
        self.lat = ''
        self.lon = ''
        self.timezone = ''
        self.altitude = ''
        self.dst = ''
        self.tz = ''

        # create airport instance
        self.createInstance(default=default, kwargs=kwargs)
        self.continent = self.getContinent()


    def createInstance(self, kwargs, default=''):
        if "IATA" in kwargs.keys():  # create Airport by iata, exact search
            self.IATA = kwargs.get('IATA')  # in case iata is not present, so this could still be used for trip searching
            self.requestInstance(key = 'IATA.keyword', value=self.IATA, isTerm=True)
        elif len(kwargs) > 0 :
            # take the best search result
            for k in kwargs.keys():
                key = k
            self.requestInstance(key=key, value=kwargs.get(key), isTerm=False)
        else:
            pos=["IATA","name","city","country"]
            for p in pos:
                self.requestInstance(key=p, value=default,isTerm=False)


    def requestInstance(self, key, value, isTerm):
         queryType = 'term' if isTerm else 'match'
         searchBody = {
             "query": {
                 queryType: {
                     key: value
                 }
             }
         }
         try:
             req = requests.get(portApi + "_search", json=searchBody)
             json_res = json.loads(req.content)
             hits = json_res.get('hits').get('hits')
             match = hits[0]['_source']
             try:
                 for key in match:
                     self.__setattr__(key, match[key])
             except AttributeError:
                 print("Attribute failed")
         except ConnectionError:
             print("no connection to elastic search")
         except IndexError:
             if len(hits) == 0:
                 print("Airport: not found {}:{}".format(key,value))


    def all_in(self, heavy=False) :
        return FlyPyApi.RouteCollection(self.IATA, is_source=False, heavy=heavy)

    def all_out(self,heavy=False):
        return FlyPyApi.RouteCollection(self.IATA,is_source=True, heavy=heavy)

    def all_out_to(self, to:str):
        all = self.all_out()
        port_list = []
        for a in all.connectionSet:
            port = Airport(IATA = a)
            if port.city == to or port.country == to:
                port_list.append(port)
        return port_list

    def getContinent(self):
        return re.sub('\/.*', '', self.tz)


    def getLocalTime(self):
        pass

    def getCoords(self):
        if self.lat == '':
            return 0,0
        return float(self.lat), float(self.lon)

    def __str__(self):
        pass


if __name__ == "__main__":
    d = Airport(default="Frankfurt")
    ld = d.all_out(heavy=True).longestFlight()
    #jsonLD=ld.serialze_to_json()
    #print(jsonLD)
    testPort = Airport(IATA="EWR")
    port2 = Airport(name="Madang Airport")
    port = Airport(country="Germany")

    all = testPort.all_in()
    testPort.all_out_to(to="Berlin")
    port2 = Airport(name="Madang Airport")


