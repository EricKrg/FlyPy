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
        try:
            port = fly.Airport(default=name)
            if port.lat != '':
                return port.__dict__, 200
            else:
                return {"message": "airport not found"}, 404
        except Exception:
            return {'message': 'oops something went wrong'}, 404


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
            t.getTraveltime()
            return t.serialize_to_json(), 200
        except Exception:
            return {'message': 'oops something went wrong'}, 404


class WorldTour(Resource):
    def get(self, start: str):
        try:
            t = fly.Trip()
            #t.getRoundTrip(start)
            t.getLiteRoundTrip(start)
            t.getTraveltime()
            return  t.serialize_to_json(), 200
        except Exception:
            return {'message': 'oops something went wrong'}, 404


class AllCon(Resource):
    def get(self, name: str):
        try:
            port = fly.Airport(IATA=name)
            is_in = request.args.get('goingin')
            trans = int(request.args.get('trans'))
            if is_in:
                res = port.all_in(heavy=True, trans=trans)
            else:
                res = port.all_out(heavy=True, trans=trans)
            return res.serialize_to_json(), 200
        except Exception:
            return {'message': 'oops something went wrong'}, 404

class AllConTo(Resource):
    def get(self, name: str):
        try:
            port = fly.Airport(IATA=name)
            to = request.args.get('to')
            res = port.all_out_to(to)
            res_json = {}
            for p in res:
                res_json[p.destinationAirport.IATA] = p.serialze_to_json()
            return res_json, 200
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
            if 'start' in request.args.keys():
                start = request.args.get('start')
                end = request.args.get('end')
                con = fly.Connection(start,end)
                tracker = fly.FlightTracker(connection=con)
            else:
                fNr = request.args.get('fnr')
                if len(fNr) < 4:
                    return  {'message': 'fnr too short'}, 201
                else:
                    tracker = fly.FlightTracker(fNr=fNr)
            return tracker.serialize_to_json(), 200
        except Exception:
            return {'message': 'oops something went wrong'}, 404


api.add_resource(Airport, '/airport/<string:name>')  # http://localhost:5000/item/Smartphone
api.add_resource(Connection, '/connect')
api.add_resource(AllCon, '/allcon/<string:name>')
api.add_resource(AllConTo, '/allconto/<string:name>')
api.add_resource(WorldTour, '/aroundtheworld/<string:start>')
api.add_resource(Airports,'/allairports')
api.add_resource(Longest,'/connect/longest/<string:name>')
api.add_resource(Shortest,'/connect/shortest/<string:name>')
api.add_resource(FlightTracker, '/tracker')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
