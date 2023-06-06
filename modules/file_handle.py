import json
from datetime import datetime
from typing import List

import classes.Class_map_color as map_color
from classes.Class_station import Station
from classes.Class_transport_object import TransportObject
from classes.Class_map_detail import MapDetail
from classes.Class_city import City
from classes.Class_city_load_data import city_load_data

PROGRAM_VERSION = "0.1.0"
CITY_PATH = "data/city.json"

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

    with open(CITY_PATH, "r") as file:
        data = json.load(file)
    file.close()

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
    with open(CITY_PATH, "w") as file:
        json.dump(data, file, indent=4)
    file.close()

    # Reload the city
    load_city()


def write_new_station(station):
    """
    Adds a new station to the JSON file and reloads the city
    :param station: station to be added
    """

    with open(CITY_PATH, "r") as file:
        data = json.load(file)
    file.close()

    # Get the list of stations
    stations = data[0]["stations"]

    # Add the new station to the list
    stations.append(station.to_dict())

    # Add the new list to the data
    data[0]["stations"] = stations

    # Save the data
    with open(CITY_PATH, "w") as file:
        json.dump(data, file, indent=4)
    file.close()

    # Reload the city
    load_city()


def delete_station(station):
    """
    Deletes a station from the JSON file and reloads the city
    :param station: station to be deleted
    """

    with open(CITY_PATH, "r") as file:
        data = json.load(file)
    file.close()

    # Get the list of stations
    stations = data[0]["stations"]

    # Remove the station from the list
    stations.remove(station.to_dict())

    # Add the new list to the data
    data[0]["stations"] = stations

    # Save the data
    with open(CITY_PATH, "w") as file:
        json.dump(data, file, indent=4)
    file.close()

    print("Station deleted from database")

    # Reload the city
    load_city()


def delete_transport_object(transport_object):
    """
    Deletes a transport object from the JSON file and reloads the city
    :param transport_object:
    :return:
    """
    with open(CITY_PATH, "r") as file:
        data = json.load(file)
    file.close()

    # Get the list of transport objects
    transport_objects = data[0]["transport_objects"]

    # Remove the transport object from the list
    transport_objects.remove(transport_object.to_dict())

    # Add the new list to the data
    data[0]["transport_objects"] = transport_objects

    # Save the data
    with open(CITY_PATH, "w") as file:
        json.dump(data, file, indent=4)
    file.close()

    print("Transport object deleted from database")

    # Reload the city
    load_city()


def load_city(change_file_path=None):
    """
    Loads the city from a JSON file
    """
    global CITY_PATH

    # Check if file path is provided
    if change_file_path is not None:
        CITY_PATH = change_file_path

    # Load the city from a JSON file
    data = json.loads(open(CITY_PATH).read())

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


def create_empty_city(name, map_color_scheme=map_color.MapColorSchemeDefault):
    """
    Creates new empty city
    :param name: name of the city
    :param map_color_scheme: color scheme of the map
    :return:
    """
    global CITY_PATH

    # Set the path to the city file
    CITY_PATH = "data/cities/" + name + ".json"

    # Create a new city with empty lists
    new_city_city = City(name, [], [], [], map_color_scheme)

    # Create city load data
    new_city_entry = city_load_data(PROGRAM_VERSION, name, CITY_PATH, str(datetime.now()), False)

    # Save the city to a JSON file
    with open(CITY_PATH, "w") as file:
        json.dump([new_city_city.to_dict()], file, indent=4)
    file.close()

    # Save the city load data to a JSON file
    # Load the city load data from a JSON file
    try:
        with open("data/city_load_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
        # Create the file if it doesn't exist
        with open("data/city_load_data.json", "w") as file:
            json.dump(data, file, indent=4)
    file.close()

    # Add the new city load data to the list
    data.append(new_city_entry.to_dict())

    # Save the data
    with open("data/city_load_data.json", "w") as file:
        json.dump(data, file, indent=4)
    file.close()


def change_path(path):
    global CITY_PATH
    CITY_PATH = path


def get_station_by_id(station_id):
    """
    Gets the station object by the station ID
    :param station_id:
    :return:
    """
    for station in stations:
        if station.stationID == station_id:
            return station
    return None
