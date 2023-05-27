from modules import file_handle

import uuid

from classes.Class_station import Station
from classes.Class_transport_object import TransportObject

ALL_STATIONS = []
ALL_PATHS = []


def test_create_station():
    """
    Tests for creating a station
    """
    # Create 3 bus stations
    for i in range(3):
        station = Station("Bus Test" + str(i), uuid.uuid4().int, 0, i, 0)
        ALL_STATIONS.append(station)
        file_handle.write_new_station(station)

    # Create 3 tram stations
    for i in range(3):
        station = Station("Tram Test" + str(i), uuid.uuid4().int, 1, i, 1)
        ALL_STATIONS.append(station)
        file_handle.write_new_station(station)

    # Create 3 train stations
    for i in range(3):
        station = Station("Train Test" + str(i), uuid.uuid4().int, 2, i, 2)
        ALL_STATIONS.append(station)
        file_handle.write_new_station(station)

    # Create 3 metro stations
    for i in range(3):
        station = Station("Metro Test" + str(i), uuid.uuid4().int, 3, i, 3)
        ALL_STATIONS.append(station)
        file_handle.write_new_station(station)


def test_path_creating():
    """
    Tests for creating a path
    """

    # Creates transport path for every type
    for i in range(4):
        # Split the stations into 4 lists based on their transport type
        stations = [station for station in ALL_STATIONS if station.transportType == i]
        ALL_PATHS.append(TransportObject(i, i, "Test Path" + str(i), stations, ['12:00']))
        file_handle.write_new_transport_path(i, i, "Test Path" + str(i), stations, ['12:00'])


def delete_paths():
    """
    Test for deleting paths
    """
    if len(ALL_PATHS) == 0:
        raise Exception("No paths to delete")
    for paths in ALL_PATHS:
        file_handle.delete_transport_object(paths)


def delete_stations():
    """
    Test for deleting stations
    """
    if len(ALL_STATIONS) == 0:
        raise Exception("No stations to delete")
    for station in ALL_STATIONS:
        file_handle.delete_station(station)
