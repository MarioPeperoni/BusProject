import requests
import json

import xml.etree.ElementTree as ET

import classes.Class_map_color as map_color
from classes.Class_station import Station

config = {
    'left': 0,
    'bottom': 0,
    'right': 0,
    'top': 0,
    'map_size': 0,
    'offset_x': 0,
    'offset_y': 0,
}


def import_area(left, bottom, right, top, map_size=2000, offset_x=0, offset_y=0):
    """
    Imports stations from OpenStreetMap area
    :param left: left longitude
    :param bottom: bottom latitude
    :param right: right longitude
    :param top: top latitude
    :param map_size: size of the map
    :param offset_x: offset of the map for generating in chunks
    :param offset_y: offset of the map for generating in chunks
    :return:
    """

    global config
    config['left'] = left
    config['bottom'] = bottom
    config['right'] = right
    config['top'] = top
    config['map_size'] = map_size
    config['offset_x'] = offset_x
    config['offset_y'] = offset_y

    # Download data from OpenStreetMap
    coordinates = f'{left},{bottom},{right},{top}'
    response = requests.get('https://api.openstreetmap.org/api/0.6/map?bbox=' + coordinates)

    # Check for error code
    if response.status_code != 200:
        print('Error while downloading data:', response.text)
        exit(1)

    # Print response content to data.xml
    with open('data/data.xml', 'wb') as file:
        file.write(response.content)

    # Parse the XML file containing the OpenStreetMap data
    tree = ET.parse('data/data.xml')
    root = tree.getroot()

    # Declare variables
    stations_list = []
    seen_stations = set()
    map_size = 2000

    def scale(axis, value):
        """
        Scales the value to the given factor of a map
        :param axis: X or Y
        :param value: value to scale
        :return:
        """
        global config
        global map_size
        if axis.upper() == 'X':
            return int((float(value) - config['left']) * (config['map_size'] / (config['right'] - config['left']))
                       - config['offset_x'])
        if axis.upper() == 'Y':
            return int((float(value) - config['bottom']) * (-config['map_size'] / (config['top'] - config['bottom']))
                       + config['map_size'] - config['offset_y'])

    # Loop over all the nodes in the XML file
    for node in root.findall('node'):

        # Check if the node has a name and is a public transport station
        if node.find("tag[@k='name']") is None or node.find("tag[@k='public_transport']") is None:
            continue

        # Check for bus station
        if node.find("tag[@k='bus']") is not None \
                and node.find("tag[@k='bus']").get('v') == 'yes' \
                and node.find("tag[@k='public_transport']").get('v') == 'stop_position':

            # Check if the station is already in the list
            name = node.find("tag[@k='name']").get('v')
            transport_type = 0
            if (name, transport_type) not in seen_stations:
                seen_stations.add((name, transport_type))
                stations_list.append(
                    Station(node.find(
                        "tag[@k='name']").get('v'),
                            node.get('id'),
                            0,
                            scale('X', node.get('lon')),
                            scale('Y', node.get('lat'))
                            ))
                print(f'Bus {stations_list[-1].stationName} at {node.get("lon")}, {node.get("lat")} created')

        # Check for tram station
        if node.find("tag[@k='tram']") is not None \
                and node.find("tag[@k='tram']").get('v') == 'yes' \
                and node.find("tag[@k='public_transport']").get('v') == 'stop_position':

            # Check if the station is already in the list
            name = node.find("tag[@k='name']").get('v')
            transport_type = 1
            if (name, transport_type) not in seen_stations:
                seen_stations.add((name, transport_type))
                stations_list.append(
                    Station(node.find(
                        "tag[@k='name']").get('v'),
                            node.get('id'),
                            1,
                            scale('X', node.get('lon')),
                            scale('Y', node.get('lat'))
                            ))
                print(f'Tram {stations_list[-1].stationName} at {node.get("lon")}, {node.get("lat")} created')

        # Check for train station
        if node.find("tag[@k='train']") is not None \
                and node.find("tag[@k='train']").get('v') == 'yes' \
                and node.find("tag[@k='public_transport']").get('v') == 'stop_position':

            # Check if the station is already in the list
            name = node.find("tag[@k='name']").get('v')
            transport_type = 2
            if (name, transport_type) not in seen_stations:
                seen_stations.add((name, transport_type))
                stations_list.append(
                    Station(node.find(
                        "tag[@k='name']").get('v'),
                            node.get('id'),
                            2,
                            scale('X', node.get('lon')),
                            scale('Y', node.get('lat'))
                            ))
                print(f'Train {stations_list[-1].stationName} at {node.get("lon")}, {node.get("lat")} created')

        # Check for subway station
        if node.find("tag[@k='subway']") is not None \
            and node.find("tag[@k='subway']").get('v') == 'yes' \
            and node.find("tag[@k='public_transport']").get('v') == 'stop_position':

            # Check if the station is already in the list
            name = node.find("tag[@k='name']").get('v')
            transport_type = 3
            if (name, transport_type) not in seen_stations:
                seen_stations.add((name, transport_type))
                stations_list.append(
                    Station(node.find(
                        "tag[@k='name']").get('v'),
                            node.get('id'),
                            3,
                            scale('X', node.get('lon')),
                            scale('Y', node.get('lat'))
                            ))
                print(f'Subway {stations_list[-1].stationName} at {node.get("lon")}, {node.get("lat")} created')

    try:
        # Open json file with stations
        with open('data/stations.json', 'r') as file:
            stations = json.load(file)
    except FileNotFoundError:
        stations = []

    # Add new stations to the list
    for station in stations_list:
        if station.to_dict() not in stations:
            stations.append(station.to_dict())
            print(f'Station {station.stationName} added to the list')

    # Save stations to json file
    with open('data/stations.json', 'w') as file:
        json.dump(stations, file, indent=4)


def create_city(city_name, left, bottom, right, top, size=2000, map_color_scheme=map_color.MapColorSchemeDefault):
    """
    Creates a new city
    """

    print("Creating a new city " + city_name + " with coordinates: "
          + str(left) + ", " + str(bottom) + ", " + str(right) + ", " + str(top) + "...")

    # Clear stations.json file
    with open('data/stations.json', 'w') as file:
        file.write('[]')

    # Clear city.json file
    with open('data/city.json', 'w') as file:
        file.write('[]')

    # Import area
    import_area(left, bottom, right, top, size)

    # Load stations from JSON file
    with open('data/stations.json', 'r') as file:
        stations = json.load(file)

    # Create a new city
    city = {
        "cityName": city_name,
        "stations": stations,
        "transport_objects": [],
        "map_details": [],
        "map_color_scheme": map_color_scheme.to_dict(),
    }

    # Save the city to a JSON file
    with open("data/cities/" + city_name + ".json", "w") as file:
        json.dump([city], file, indent=4)

    # Print a message
    print(f'City {city_name} created successfully!')
