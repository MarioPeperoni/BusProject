from tkinter import Canvas

from file_handle import stations
from file_handle import map_details
from file_handle import map_color_scheme

import file_handle

# Global variables
CANVAS = Canvas
MAX_ZOOM = 2
CANVAS_SCALE = 1
DRAG_OFFSET = [0, 0]
LIGHT_MODE = False

# Path drawing variables
PATH_DRAWING = False
PATH_STATIONS = []
PATH_TYPE = 0


def create_canvas(tk):
    """
    Creates a canvas for displaying the map
    :param tk: tkinter
    :return:
    """
    global CANVAS

    CANVAS = Canvas(tk)

    # Bind events
    CANVAS.bind("<MouseWheel>", zoom)
    CANVAS.bind("<ButtonPress-1>", start_drag)
    CANVAS.bind("<B1-Motion>", drag)

    # Set the background color
    CANVAS.configure(bg=map_color_scheme.get("colorLightBG") if LIGHT_MODE else map_color_scheme.get("colorDarkBG"))

    # Draw the map details
    draw_map_details()

    # Draw the stations
    draw_stations(stations)

    return CANVAS


def zoom(event):
    """
    Zooms the map in and out
    :param event: event
    :return:
    """
    global CANVAS_SCALE

    # Get the mouse wheel delta
    if event.delta > 0:
        scale = 1.1
    elif event.delta < 0:
        scale = 0.9

    if CANVAS_SCALE * scale > MAX_ZOOM:
        return
    CANVAS_SCALE *= scale

    # Scale map to mouse position
    CANVAS.scale("all", event.x, event.y, scale, scale)

    # Refresh the canvas
    refresh_canvas()


def start_drag(event):
    """
    Starts dragging the map with the mouse
    :param event:
    :return:
    """
    global CANVAS
    CANVAS.drag_start_x = event.x
    CANVAS.drag_start_y = event.y


def drag(event):
    """
    Drags the map with the mouse
    :param event: event
    :return:
    """
    global CANVAS
    global DRAG_OFFSET
    global CANVAS_SCALE

    # Calculate the drag offset
    dx = (event.x - CANVAS.drag_start_x) / CANVAS_SCALE
    dy = (event.y - CANVAS.drag_start_y) / CANVAS_SCALE

    # Update the drag offset
    DRAG_OFFSET[0] += dx
    DRAG_OFFSET[1] += dy

    # Move the map
    CANVAS.drag_start_x = event.x
    CANVAS.drag_start_y = event.y

    # Refresh the canvas
    refresh_canvas()


def refresh_canvas():
    """
    Redraws the canvas
    :return:
    """
    CANVAS.delete("transport_path")
    CANVAS.delete("station_circle")
    CANVAS.delete("station_text")

    # Redraw the map details
    draw_map_details()

    # Redraw the stations
    draw_stations(stations)

    # Redraw paths
    if PATH_DRAWING:
        draw_transport_path(PATH_STATIONS, PATH_TYPE)


def draw_map_details():
    """
    Draws the map details on the canvas
    :return:
    """
    global CANVAS

    # Draw the map details
    for map_detail in map_details:
        CANVAS.create_polygon(map_detail.points, fill=map_detail.color)


def draw_stations(stations):
    """
    Draws the map on the canvas
    :param stations: list of Station objects
    :return:
    """
    global CANVAS_SCALE

    CANVAS.delete("station_circle")
    CANVAS.delete("station_text")

    # Draw the stations
    for station in stations:
        if station.transportType == 0:
            color = map_color_scheme.get("colorLightBusStation") \
                if LIGHT_MODE else map_color_scheme.get("colorDarkBusStation")
        elif station.transportType == 1:
            color = map_color_scheme.get("colorLightTramStation") \
                if LIGHT_MODE else map_color_scheme.get("colorDarkTramStation")
        elif station.transportType == 2:
            color = map_color_scheme.get("colorLightTrainStation") \
                if LIGHT_MODE else map_color_scheme.get("colorDarkTrainStation")
        elif station.transportType == 3:
            color = map_color_scheme.get("colorLightMetroStation") \
                if LIGHT_MODE else map_color_scheme.get("colorDarkMetroStation")
        else:
            color = "black"

        # Calculate the updated coordinates and size of the station circle
        r = 10 * CANVAS_SCALE  # radius of circle
        x1 = (station.coordinateX + DRAG_OFFSET[0]) * CANVAS_SCALE - r
        y1 = (station.coordinateY + DRAG_OFFSET[1]) * CANVAS_SCALE - r
        x2 = (station.coordinateX + DRAG_OFFSET[0]) * CANVAS_SCALE + r
        y2 = (station.coordinateY + DRAG_OFFSET[1]) * CANVAS_SCALE + r

        # Create the station circle
        CANVAS.create_oval(x1, y1, x2, y2,
                           fill=color,
                           outline="black" if LIGHT_MODE else "white",
                           width=4 * CANVAS_SCALE, tags=("station_circle",
                                                         station.stationName, station.stationID, station.transportType))

        # Set up the font
        font_size = int(12 * CANVAS_SCALE)
        font_color = map_color_scheme.get("colorLightText") if LIGHT_MODE else map_color_scheme.get("colorDarkText")
        font = ("Arial", font_size, "bold")

        # Draw the station name
        CANVAS.create_text((station.coordinateX + DRAG_OFFSET[0]) * CANVAS_SCALE,
                           (station.coordinateY + DRAG_OFFSET[1]) * CANVAS_SCALE + 20 * CANVAS_SCALE,
                           text=station.stationName,
                           font=font, fill=font_color,
                           tags=("station_text", station.stationName, station.stationID, station.transportType))


def draw_transport_path(stations_selected, type, custom_color=None):
    """
    Highlights stations and draw the path between them
    :param stations_selected:
    :return:
    """
    global PATH_DRAWING
    global PATH_TYPE
    global PATH_STATIONS
    global COLOR

    # Set the path drawing variables
    PATH_DRAWING = True
    PATH_TYPE = type
    PATH_STATIONS = stations_selected

    # Delete previous path and clear the highlight
    CANVAS.delete("transport_path")

    # Draw the path between the stations
    for i in range(len(stations_selected) - 1):
        station1 = stations_selected[i]
        station2 = stations_selected[i + 1]

        # Get the coordinates of the stations
        x1 = (station1.coordinateX + DRAG_OFFSET[0]) * CANVAS_SCALE
        y1 = (station1.coordinateY + DRAG_OFFSET[1]) * CANVAS_SCALE
        x2 = (station2.coordinateX + DRAG_OFFSET[0]) * CANVAS_SCALE
        y2 = (station2.coordinateY + DRAG_OFFSET[1]) * CANVAS_SCALE

        # Check for custom color
        if custom_color is None:

            # Set color based on transport type
            if type == 0:
                COLOR = map_color_scheme.get("colorLightBusStation") \
                    if LIGHT_MODE else map_color_scheme.get("colorDarkBusStation")
            elif type == 1:
                COLOR = map_color_scheme.get("colorLightTramStation") \
                    if LIGHT_MODE else map_color_scheme.get("colorDarkTramStation")
            elif type == 2:
                COLOR = map_color_scheme.get("colorLightTrainStation") \
                    if LIGHT_MODE else map_color_scheme.get("colorDarkTrainStation")
            elif type == 3:
                COLOR = map_color_scheme.get("colorLightMetroStation") \
                    if LIGHT_MODE else map_color_scheme.get("colorDarkMetroStation")
        else:
            # Set the color to the custom color
            COLOR = custom_color

        CANVAS.create_line(x1, y1, x2, y2,
                           fill=COLOR,
                           width=5 * CANVAS_SCALE,
                           tags=("transport_path", station1.stationName, station2.stationName))
        # Move the path to the back
        CANVAS.tag_lower("transport_path")
