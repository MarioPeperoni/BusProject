from enum import Enum


class TransportType(Enum):
    """
    Enumeration of transport types
    :param Bus: 0
    :param Tram: 1
    :param Train: 2
    """
    Bus = 0
    Tram = 1
    Train = 2

    def return_transport_type(self):
        """
        Converts from enum to int
        :return: transport type
        """
        return self.value
