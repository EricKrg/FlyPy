
import requests
import json
import FlyPyApi as fly

apiKey = 'da5a06-bc08c7'
baseUrl = 'http://aviation-edge.com/v2/public/flights?key='
#apiUrl = 'http://aviation-edge.com/v2/public/flights?key={}'.format(apiKey)

class FlightTracker:
    def __init__(self, connection: fly.Connection):
        self.con = connection
        self.apiUrl =  '{}{}'.format(baseUrl,apiKey)
        self.planeList = []
        self.requestFlight()

    def requestFlight(self):

        self.apiUrl += '&depIata={}&arrIata={}'.format(self.con.sourceAirport.IATA, self.con.destinationAirport.IATA)
        response = requests.get(self.apiUrl).json()
        ''' mockdata lhr to jfk
        response = [
        {
            "geography": {
                "latitude": 51.8109,
                "longitude": -3.2298,
                "altitude": 8915.4,
                "direction": 279.57
            },
            "speed": {
                "horizontal": 824.508,
                "isGround": 0,
                "vertical": 28.08
            },
            "departure": {
                "iataCode": "LHR",
                "icaoCode": "LHR"
            },
            "arrival": {
                "iataCode": "JFK",
                "icaoCode": "JFK"
            },
            "aircraft": {
                "regNumber": "GCIVW",
                "icaoCode": "B744",
                "icao24": "4006AD",
                "iataCode": "B744"
            },
            "airline": {
                "iataCode": "BA",
                "icaoCode": "BAW"
            },
            "flight": {
                "iataNumber": "BA175",
                "icaoNumber": "BAW175",
                "number": "175"
            },
            "system": {
                "updated": "1555493039",
                "squawk": "4441"
            },
            "status": "en-route"
        },
        {
            "geography": {
                "latitude": 53.4884,
                "longitude": -11.6316,
                "altitude": 10972.8,
                "direction": 285.79
            },
            "speed": {
                "horizontal": 864.18,
                "isGround": 0,
                "vertical": -1.188
            },
            "departure": {
                "iataCode": "LHR",
                "icaoCode": "EGLL"
            },
            "arrival": {
                "iataCode": "JFK",
                "icaoCode": "KJFK"
            },
            "aircraft": {
                "regNumber": "GVFIT",
                "icaoCode": "A346",
                "icao24": "",
                "iataCode": "A346"
            },
            "airline": {
                "iataCode": "VS",
                "icaoCode": "VIR"
            },
            "flight": {
                "iataNumber": "VS3N",
                "icaoNumber": "VIR3N",
                "number": "3N"
            },
            "system": {
                "updated": "1555493039",
                "squawk": "6236"
            },
            "status": "en-route"
        },
        {
            "geography": {
                "latitude": 51.7946,
                "longitude": -2.8339,
                "altitude": 8709.66,
                "direction": 290
            },
            "speed": {
                "horizontal": 833.688,
                "isGround": 0,
                "vertical": 28.08
            },
            "departure": {
                "iataCode": "LHR",
                "icaoCode": "LHR"
            },
            "arrival": {
                "iataCode": "JFK",
                "icaoCode": "JFK"
            },
            "aircraft": {
                "regNumber": "N777AN",
                "icaoCode": "B772",
                "icao24": "AA8315",
                "iataCode": "B772"
            },
            "airline": {
                "iataCode": "AA",
                "icaoCode": "AAL"
            },
            "flight": {
                "iataNumber": "AA101",
                "icaoNumber": "AAL101",
                "number": "101"
            },
            "system": {
                "updated": "1555493039",
                "squawk": "2045"
            },
            "status": "en-route"
        },
        {
            "geography": {
                "latitude": 40.4576,
                "longitude": -3.5636,
                "altitude": 0,
                "direction": 45
            },
            "speed": {
                "horizontal": 44.46,
                "isGround": 0,
                "vertical": 0
            },
            "departure": {
                "iataCode": "LHR",
                "icaoCode": "LHR"
            },
            "arrival": {
                "iataCode": "JFK",
                "icaoCode": "JFK"
            },
            "aircraft": {
                "regNumber": "GVFIT",
                "icaoCode": "A346",
                "icao24": "400E09",
                "iataCode": "A346"
            },
            "airline": {
                "iataCode": "VS",
                "icaoCode": "VIR"
            },
            "flight": {
                "iataNumber": "VS3",
                "icaoNumber": "VIR3",
                "number": "3"
            },
            "system": {
                "updated": "1555492892",
                "squawk": "0"
            },
            "status": "en-route"
        }
        ]
        '''
        if "error" in response: self.planeList = []
        else:
            for i in response:
                status = i.get('status')
                lat = i.get('geography').get('latitude')
                lon = i.get('geography').get('longitude')
                alt = i.get('geography').get('altitude')
                fnr = i.get('flight').get('iataNumber')
                airline = i.get('airline').get('iataCode')
                self.planeList.append(fly.Airplane(status, lat, lon, alt, fnr, airline))

    def serialize_to_json(self):
        res_json = {}
        for p in self.planeList:
            res_json[p.flightNr] = p.__dict__
        return res_json



if __name__ == "__main__":
    con = fly.Connection("JFK","LAX")
    t = FlightTracker(con)

