import json
from typing import List, Any

from Class_station import Station

existing_stations: list[Station] = []


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

    with open("data/transport_data.json", "r") as file:
        data = json.load(file)

    stops = Station.get_stations_by_names(stops_names, existing_stations)
    stops = [stop.to_dict() for stop in stops]
    # Create a new entry
    new_entry = {
        "transport_type": transportType,
        "number": number,
        "name": name,
        "stops": stops,
        "departure_times": departureTimes
    }

    # Add the new entry to the data
    data.append(new_entry)

    # Open the JSON file for writing
    with open("data/transport_data.json", "w") as file:
        json.dump(data, file, indent=4)


def read_stations_from_json() -> List[Station]:
    """
    Reads stations from a JSON file and returns a list of Station objects
    """
    global existing_stations
    with open('data/stations.json', 'r') as f:
        data = json.load(f)

    stations = []
    for station_data in data:
        station = Station()
        station.stationName = station_data['stationName']
        station.stationID = station_data['stationID']
        station.transportType = station_data['transportType']
        station.coordinateX = station_data['coordinateX']
        station.coordinateY = station_data['coordinateY']
        stations.append(station)
    existing_stations = stations
    print(existing_stations)
    return stations
