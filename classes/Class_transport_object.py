from classes.Class_station import Station


class TransportObject:
    """
    Representation of a transport object
    :param transportType: type of transport (0 - bus, 1 - tram, 2 - train, 3 - metro)
    :param number: number of object
    :param name: name of object
    :param stops: list of stops
    :param departureTimes: list of departure times
    """
    transportType = 0
    number = 0
    name = ""
    stops: list[Station] = []
    departureTimes = []

    def __init__(self, transportType, number, name, stops, departureTimes):
        self.transportType = transportType
        self.number = number
        self.name = name
        self.stops = stops
        self.departureTimes = departureTimes

    def to_dict(self):
        """
        Converts a transport_object object to a dictionary
        """
        return {
            'transportType': self.transportType,
            'number': self.number,
            'name': self.name,
            'stops': [stop.to_dict() for stop in self.stops],
            'departureTimes': self.departureTimes
        }
