
import requests
import json
import re
import configparser

config = configparser.ConfigParser()
config.read('FlyPyConfig.ini')
if config['es']['local'] == 'y':
    portApi = config['es']['esURL'] + "/airports/_search?size=10000"
else:
    portApi = config['es']['esClusterURL'] + "/airports/_search?size=10000"


class AirportCollection:
    def __init__(self):
        self.port_dict = {}
        self.iata_dict = []
        req = requests.get(portApi)
        json_res = json.loads(req.content)
        hits = json_res.get('hits').get('hits')

        for hit in hits:
            hit = hit.get('_source')
            self.port_dict[hit['name']] = (hit['lat'],hit['lon'], hit['IATA'])
            self.iata_dict.append({hit['IATA']: (hit['lat'],hit['lon'], hit['name'], re.sub('\/.*', '',hit['tz']))})
if __name__ == "__main__":
    a = AirportCollection()
    print(a.iata_dict['CGN'])
    print(a.iata_dict['RYG'])
