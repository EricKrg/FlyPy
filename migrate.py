import requests
from tqdm import tqdm

# static vars

esApiUrl = 'http://172.17.0.2:9200'


# ROUTES
routesFile = 'data/routes.dat'
routesMapping = {
    "settings" : {
        "number_of_shards" : 3
    },
    "mappings" : {
        "type_name":{
            "properties" : {
                "airline" : { "type" : "text" },
                "airlineID" : { "type" : "integer" },
                "sourceAirport" : { "type" : "string",
                                    "index": "not_analyzed"},
                "sourceAirportID" : { "type" : "integer" },
                "destinationAirport" : { "type" : "string",
                                         "index": "not_analyzed"},
                "destinationAirportID" : { "type" : "integer" },
                "codeShare" : { "type" : "text" },
                "stops" : { "type" : "integer" },
                "equipment" : { "type" : "text" },
            }
        }
    }
}
routesFillMapping = {
                "airline" : "",
                "airlineID" : "",
                "sourceAirport" : "",
                "sourceAirportID" : "",
                "destinationAirport" : "",
                "destinationAirportID" : "",
                "codeShare" : "",
                "stops" : "",
                "equipment" : "",
            }
# AIRPORTS
airportFile = 'data/airports.dat'
airportMapping = {
    "settings" : {
        "number_of_shards" : 3
    },
    "mappings" : {
        "type_name":{
            "properties" : {
                "airportID" : { "type" : "text" },
                "name" : { "type" : "text" },
                "city" : { "type" : "text" },
                "country" : { "type" : "text" },
                "IATA" : { "type" : "string",
                           "index": "not_analyzed"},
                "ICAO" : { "type" : "string",
                           "index": "not_analyzed" },
                "lat" : { "type" : "float" },
                "lon" : { "type" : "float" },
                "altitude" : { "type" : "float" },
                "timezone" : { "type" : "text" },
                "dst" : { "type" : "text" },
                "tz" : { "type" : "text" },
                "type" : { "type" : "text" },
                "source" : { "type" : "text" }
            }
        }
    }
}
airportFillMapping = {
                "airportID" : "",
                "name" : "",
                "city" : "",
                "country" : "",
                "IATA" : "",
                "ICAO" : "",
                "lat" : "",
                "lon" : "",
                "timezone" : "",
                "altitude": "",
                "dst" : "",
                "tz" : "",
                "type" :"",
                "source" : ""
            }

# -----------------------------------------
def resetIndex(route: str, Mapping: dict):
    if requests.get(esApiUrl + "/{}".format(route)).status_code == 200:
        requests.delete(esApiUrl + "/{}".format(route))
    requests.put(esApiUrl + "/{}".format(route), json=Mapping)

def fillIndex(filePath: str, fillMapping: dict, indexName: str ):
    with open(filePath) as routes:
        for e in tqdm(routes):
            e_split = e.split(sep=',')
            remove = r"\N"
            if e_split[4] == remove:
                continue
            else:
                fillMap = {i: str(e_split[k]).replace('"','') for k, i in enumerate(fillMapping.keys())}
                res = requests.post(esApiUrl + "/{}/_doc/".format(indexName), json=fillMap)


if __name__ == "__main__":
    # AIRPORTS
    resetIndex('airports', airportMapping)
    fillIndex(airportFile,airportFillMapping,'airports')
    # ROUTES
    resetIndex('routes', routesMapping)
    fillIndex(routesFile,routesFillMapping,'routes')