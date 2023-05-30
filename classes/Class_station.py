
class Station:
    """
    Representation of a station
    :param stationName: name of the station
    :param stationID: ID of the station
    :param transportType: type of transport
    :param coordinateX: X coordinate of the station
    :param coordinateY: Y coordinate of the station
    """
    stationName = ""
    stationID = 0
    transportType = 0
    coordinateX = 0
    coordinateY = 0

    @classmethod
    def get_stations_by_names(cls, names, stations_list, transport_type):
        """
        Converts a list of station names to a list of Station objects
        :param names: list of names of stations to search for
        :param stations_list: list of Station objects to search through
        :param transport_type: type of transport (0 - bus, 1 - tram, 2 - train, 3 - metro)
        :return: list of Station objects if found, None otherwise
        """
        stations = []
        for name in names:
            for station in stations_list:
                if station.stationName == name and station.transportType == transport_type:
                    stations.append(station)
                    break
        if len(stations) > 0:
            return stations
        return None

    def __init__(self, stationName, stationID, transportType, coordinateX, coordinateY):
        self.stationName = stationName
        self.stationID = stationID
        self.transportType = transportType
        self.coordinateX = coordinateX
        self.coordinateY = coordinateY

    def to_dict(self):
        """
        Converts a Station object to a dictionary
        """
        return {
            'stationName': self.stationName,
            'stationID': self.stationID,
            'transportType': self.transportType,
            'coordinateX': self.coordinateX,
            'coordinateY': self.coordinateY
        }
