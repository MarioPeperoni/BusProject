from classes.Class_station import Station
from classes.Class_transport_object import TransportObject
from classes.Class_map_detail import MapDetail
from classes.Class_map_color import MapColorScheme


class City:
    """
    Full map info
    """
    cityName = ""
    stations: list[Station] = []
    transport_objects: list[TransportObject] = []
    map_details: list[MapDetail] = []
    map_color_scheme = MapColorScheme()

    def __init__(self, cityName, stations, transport_objects, map_details, map_color_scheme):
        self.cityName = cityName
        self.stations = stations
        self.transport_objects = transport_objects
        self.map_details = map_details
        self.map_color_scheme = map_color_scheme

    def to_dict(self):
        """
        Converts a map_info object to a dictionary
        """
        return {
            'cityName': self.cityName,
            'stations': [station.to_dict() for station in self.stations],
            'transport_objects': [transport_object.to_dict() for transport_object in self.transport_objects],
            'map_details': [map_detail.to_dict() for map_detail in self.map_details],
            'map_color_scheme': self.map_color_scheme.to_dict()
        }
