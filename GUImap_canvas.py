from tkinter import Canvas

from file_handle import stations, map_details

import file_handle

canvas = None

globals()["stations"] = file_handle.return_list_of_stations()
globals()["map_details"] = file_handle.return_list_of_map_details()


def create_canvas(tk):
    """
    Creates a canvas for displaying the map
    :param tk: tkinter
    :return:
    """
    global canvas
    global stations
    canvas = Canvas(tk, width=800, height=600)
    draw_map_details()
    draw_stations(stations)
    return canvas


def draw_map_details():
    """
    Draws the map details on the canvas
    :return:
    """
    global canvas
    global map_details

    # Draw the map details
    for map_detail in map_details:
        canvas.create_polygon(map_detail.points, fill=map_detail.color)


def draw_stations(stations):
    """
    Draws the map on the canvas
    :param stations: list of Station objects
    :return:
    """
    global canvas

    # Set the background color
    canvas.configure(bg="#1b7300")

    # Draw the stations
    for station in stations:
        if station.transportType == 0:
            color = "blue"
        elif station.transportType == 1:
            color = "red"
        elif station.transportType == 2:
            color = "yellow"
        else:
            color = "black"
        canvas.create_oval(station.coordinateX - 5, station.coordinateY - 5, station.coordinateX + 5,
                           station.coordinateY + 5, fill=color)
        canvas.create_text(station.coordinateX + 10, station.coordinateY + 10, text=station.stationName)
