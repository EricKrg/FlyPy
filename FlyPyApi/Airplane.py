
class Airplane:
    def __init__(self, status, lat, lon, alt, flightNr, airline):
        self.status = status
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.flightNr = flightNr
        self.airline = airline


    def serialize_to_json(self):
        return self.__dict__