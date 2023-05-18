import json
from typing import List

from classes.Class_station import Station
from classes.Class_transport_object import TransportObject
from classes.Class_map_detail import MapDetail

cityName = ""
map_color_scheme = None
stations: list[Station] = []
map_details: list[MapDetail] = []

# Transport objects
transport_objects: list[TransportObject] = []  # For legacy use
bus_objects: list[TransportObject] = []
tram_objects: list[TransportObject] = []
train_objects: list[TransportObject] = []
metro_objects: list[TransportObject] = []


def write_new_transport_path(transportType, number, name, stops, departureTimes):
    """
    Adds a new transport entry to the JSON file
    :param transportType: type of transport
    :param number: number of the transport
    :param name: name of the transport
    :param stops: list of stops
    :param departureTimes: list of departure times
    :return:
    """

    with open("data/city.json", "r") as file:
        data = json.load(file)

    # Get the list of stations
    stops = [stop.to_dict() for stop in stops]

    # Create a new entry
    new_entry = {
        "transportType": transportType,
        "number": number,
        "name": name,
        "stops": stops,
        "departureTimes": departureTimes
    }

    # Add the new entry to the data
    data[0]["transport_objects"].append(new_entry)

    # Save the data
    with open("data/city.json", "w") as file:
        json.dump(data, file, indent=4)

    # Reload the city
    load_city()


def write_new_station(station):
    """
    Adds a new station to the JSON file and reloads the city
    :param station: station to be added
    """

    with open("data/city.json", "r") as file:
        data = json.load(file)

    # Get the list of stations
    stations = data[0]["stations"]

    # Add the new station to the list
    stations.append(station.to_dict())

    # Add the new list to the data
    data[0]["stations"] = stations

    # Save the data
    with open("data/city.json", "w") as file:
        json.dump(data, file, indent=4)

    # Reload the city
    load_city()


def load_city():
    """
    Loads the city from a JSON file
    """

    # Load the city from a JSON file
    data = json.loads(open('data/city.json').read())

    global cityName
    global stations
    global transport_objects
    global map_details
    global map_color_scheme
    global bus_objects
    global tram_objects
    global train_objects
    global metro_objects

    # Load all variables data from the JSON file
    cityName = data[0]['cityName']
    stations = [Station(s['stationName'], s['stationID'], s['transportType'], s['coordinateX'], s['coordinateY']) for s
                in data[0]['stations']]
    transport_objects = [TransportObject(t['transportType'], t['number'], t['name'], [
        Station(s['stationName'], s['stationID'], s['transportType'], s['coordinateX'], s['coordinateY']) for s in
        t['stops']], t['departureTimes']) for t in data[0]['transport_objects']]
    map_details = [MapDetail(m['points'], m['color']) for m in data[0]['map_details']]
    map_color_scheme = data[0]['map_color_scheme']

    # Split transport objects into separate lists
    bus_objects = [transport for transport in transport_objects if transport.transportType == 0]
    tram_objects = [transport for transport in transport_objects if transport.transportType == 1]
    train_objects = [transport for transport in transport_objects if transport.transportType == 2]
    metro_objects = [transport for transport in transport_objects if transport.transportType == 3]
