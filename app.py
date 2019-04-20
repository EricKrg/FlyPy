# FlyPyController
import FlyPyApi as fly
from flask import Flask, request, Response, jsonify
from flask_restful import Resource,Api
import json

app = Flask(__name__)
api = Api(app)

def serialize(obj):  # gen. serializer
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, Connection):
        serial = obj.__dict__
        return serial

    if isinstance(obj, Airport):
        serial = obj.__dict__
        return serial
    return obj.__dict__


class Airport(Resource):
    def get(self, name: str):
        port = fly.Airport(default=name)
        if port.lat != '':
            return port.__dict__, 200
        else:
            return {"message": "airport not found"}, 404


class Airports(Resource):
    def get(self):
        try:
            return jsonify({"all":fly.AirportCollection().port_dict})
        except Exception:
            return {'message': 'oops something went wrong'}, 404



class Connection(Resource):
    # todo
    #   - catch bad request, missing start or end...
    def get(self):
        try:
            start = request.args.get('start')
            end = request.args.get('end')
            steps = request.args.get('steps')
            print(len(steps))
            steps = [] if len(steps) == 0 else steps.split(',')
            t = fly.Trip()
            t.getFlightplan(start, end, steps)
            return t.serialize_to_json(), 200
        except Exception:
            return {'message': 'oops something went wrong'}, 404


class WorldTour(Resource):
    def get(self, start: str):
        try:
            t = fly.Trip()
            #t.getRoundTrip(start)
            t.getLiteRoundTrip(start)
            return  t.serialize_to_json(), 200
        except Exception:
            return {'message': 'oops something went wrong'}, 404


class AllCon(Resource):
    def get(self, name: str):
        try:
            port = fly.Airport(IATA=name)
            is_in = request.args.get('goingin')
            if is_in:
                res = port.all_in(heavy=True)
            else:
                res = port.all_out(heavy=True)
            return res.serialize_to_json()
        except Exception:
            return {'message': 'oops something went wrong'}, 404

class Longest(Resource):
    def get(self, name: str):
        try:
            port = fly.Airport(IATA=name)
            res = port.all_out(heavy=True).longestFlight()
            return res.serialze_to_json(),200
        except Exception:
            return {'message': 'oops something went wrong'}, 404

class Shortest(Resource):
    def get(self, name: str):
        try:
            port = fly.Airport(IATA=name)
            res = port.all_out(heavy=True).shortestFLight()
            return res.serialze_to_json(),200
        except Exception:
            return {'message': 'oops something went wrong'}, 404

class FlightTracker(Resource):
    def get(self):
        try:
            start = request.args.get('start')
            end = request.args.get('end')
            con = fly.Connection(start,end)
            tracker = fly.FlightTracker(con)
            return tracker.serialize_to_json(), 200
        except Exception:
            return {'message': 'oops something went wrong'}, 404




api.add_resource(Airport, '/airport/<string:name>')  # http://localhost:5000/item/Smartphone
api.add_resource(Connection, '/connect')
api.add_resource(AllCon, '/allcon/<string:name>')
api.add_resource(WorldTour, '/aroundtheworld/<string:start>')
api.add_resource(Airports,'/allairports')
api.add_resource(Longest,'/connect/longest/<string:name>')
api.add_resource(Shortest,'/connect/shortest/<string:name>')
api.add_resource(FlightTracker, '/tracker')

if __name__ == '__main__':
    app.run(debug=True)
