import json
from typing import List

from classes.Class_station import Station
from classes.Class_tranport_object import TransportObject
from classes.Class_map_detail import MapDetail

cityName = ""
stations: list[Station] = []
transport_objects: list[TransportObject] = []
map_details: list[MapDetail] = []


def add_new_transport_entry_to_json(transportType, number, name, stops_names, departureTimes):
    """
    Adds a new transport entry to the JSON file
    :param transportType: type of transport
    :param number: number of the transport
    :param name: name of the transport
    :param stops_names: list of stops names
    :param departureTimes: list of departure times
    :return:
    """

    with open("data/city.json", "r") as file:
        data = json.load(file)

    # Get the list of stations
    stops = Station.get_stations_by_names(stops_names, stations)
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

    # Open the JSON file for writing
    with open("data/city.json", "w") as file:
        json.dump(data, file, indent=4)


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

    # Load all variables data from the JSON file
    cityName = data[0]['cityName']
    stations = [Station(s['stationName'], s['stationID'], s['transportType'], s['coordinateX'], s['coordinateY']) for s
                in data[0]['stations']]
    transport_objects = [TransportObject(t['transportType'], t['number'], t['name'], [
        Station(s['stationName'], s['stationID'], s['transportType'], s['coordinateX'], s['coordinateY']) for s in
        t['stops']], t['departureTimes']) for t in data[0]['transport_objects']]
    map_details = [MapDetail(m['points'], m['color']) for m in data[0]['map_details']]


def return_list_of_stations() -> List[Station]:
    """
    Returns a list of stations
    """
    load_city()
    global stations
    print(stations)
    return stations


def return_list_of_transport_objects() -> List[TransportObject]:
    """
    Returns a list of transport objects
    """
    load_city()
    global transport_objects
    print(transport_objects)
    return transport_objects


def return_list_of_map_details() -> List[MapDetail]:
    """
    Returns a list of map details
    """
    load_city()
    global map_details
    print(map_details)
    return map_details
