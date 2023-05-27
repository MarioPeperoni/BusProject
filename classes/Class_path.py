import uuid


class Path:
    def __init__(self, stations, transport_type, custom_color=None):
        self.ID = uuid.uuid4().int
        self.stations = stations
        self.transport_type = transport_type
        self.custom_color = custom_color
