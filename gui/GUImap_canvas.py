import math
from tkinter import Canvas

from classes import Class_path

from gui import GUIform_create_station
from gui import GUIStation_menu

from modules import simulation_engine

from modules.file_handle import map_details
from modules.file_handle import map_color_scheme

from gui import GUIform_set_time

from modules import file_handle

# Global variables
CANVAS = Canvas
MAX_ZOOM = 2
CANVAS_SCALE = 1
DRAG_OFFSET = [0, 0]
LIGHT_MODE = False
MOUSE_X = 0
MOUSE_Y = 0
STATIONS = file_handle.stations

# Path drawing variables
PATHS_DRAWN = []

# Simulation variables
LAST_SIMULATION_TIME = 0
SIMULATION_RUNNING = False
VEHICLE_ID_LIST = []


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
    CANVAS.bind("<Button-2>", lambda event: GUIform_create_station.create_window(round(MOUSE_X), round(MOUSE_Y)))
    CANVAS.bind("<Motion>", get_mouse_coordinates)
    CANVAS.tag_bind("station_circle", "<Button-1>", station_clicked)
    CANVAS.tag_bind("sim_timer", "<Button-1>", lambda event: GUIform_set_time.create())

    # Set the background color
    CANVAS.configure(bg=map_color_scheme.get("colorLightBG") if LIGHT_MODE else map_color_scheme.get("colorDarkBG"))

    # Draw the map details
    draw_map_details()

    # Draw the stations
    draw_stations(file_handle.stations)

    # Start simulation
    simulation_engine.start_simulation()

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


def get_mouse_coordinates(event):
    """
    Gets the mouse coordinates
    :param event:
    :return:
    """
    global MOUSE_X
    global MOUSE_Y

    MOUSE_X = (event.x - DRAG_OFFSET[0]) / CANVAS_SCALE
    MOUSE_Y = (event.y - DRAG_OFFSET[1]) / CANVAS_SCALE

    # Round the coordinates
    MOUSE_X = round(MOUSE_X, 2)
    MOUSE_Y = round(MOUSE_Y, 2)

    CANVAS.delete("cursor_pos")
    CANVAS.create_text(10, CANVAS.winfo_height() - 10, anchor="sw", text="X: " + str(MOUSE_X) + " Y: " + str(MOUSE_Y),
                       tags="cursor_pos")


def refresh_stations(station, mode="add"):
    """
    Refreshes the stations on the map
    :param station: station structure
    :param mode: mode (add)
    :return:
    """
    global STATIONS

    # Mode switch
    if mode == "add":
        # Add the station to the list
        STATIONS.append(station)
    elif mode == "remove":
        # Remove the station from the list
        try:
            STATIONS.remove(station)
        except ValueError:
            # If value error try to delete the station by id (it happens if station has been added in this session)
            for s in STATIONS:
                if s.stationID == station.stationID:
                    STATIONS.remove(s)

    # Redraw the stations
    refresh_canvas()


def refresh_canvas():
    """
    Redraws the canvas
    :return:
    """
    CANVAS.delete("transport_path")
    CANVAS.delete("station_circle")
    CANVAS.delete("station_text")
    CANVAS.delete("sim_timer")

    # Delete sim vehicles
    for vehicle_id in VEHICLE_ID_LIST:
        CANVAS.delete(vehicle_id)

    # Redraw the map details
    draw_map_details()

    # Redraw the stations
    draw_stations(STATIONS)

    # Redraw paths
    for path in PATHS_DRAWN:
        draw_transport_path(path)

    # Draw the timer
    draw_timer_on_screen(LAST_SIMULATION_TIME)


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
    for station in STATIONS:
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


def draw_transport_path(path: Class_path, manual=False):
    """
    Highlights stations and draw the path between them
    :param path: path object
    :return:
    """

    # Add the path to the list of drawn paths
    if path not in PATHS_DRAWN:
        PATHS_DRAWN.append(path)

    # Check for manual selection
    if manual:
        PATHS_DRAWN.clear()
        PATHS_DRAWN.append(path)
        CANVAS.delete("transport_path")

    # Delete previous path and clear the highlight
    CANVAS.delete(path.ID)

    # Draw the path between the stations
    for i in range(len(path.stations) - 1):
        station1 = path.stations[i]
        station2 = path.stations[i + 1]

        # Get the coordinates of the stations
        x1 = (station1.coordinateX + DRAG_OFFSET[0]) * CANVAS_SCALE
        y1 = (station1.coordinateY + DRAG_OFFSET[1]) * CANVAS_SCALE
        x2 = (station2.coordinateX + DRAG_OFFSET[0]) * CANVAS_SCALE
        y2 = (station2.coordinateY + DRAG_OFFSET[1]) * CANVAS_SCALE

        # Check for custom color
        if path.custom_color is None:

            # Set color based on transport type
            if path.transport_type == 0:
                COLOR = map_color_scheme.get("colorLightBusStation") \
                    if LIGHT_MODE else map_color_scheme.get("colorDarkBusStation")
            elif path.transport_type == 1:
                COLOR = map_color_scheme.get("colorLightTramStation") \
                    if LIGHT_MODE else map_color_scheme.get("colorDarkTramStation")
            elif path.transport_type == 2:
                COLOR = map_color_scheme.get("colorLightTrainStation") \
                    if LIGHT_MODE else map_color_scheme.get("colorDarkTrainStation")
            elif path.transport_type == 3:
                COLOR = map_color_scheme.get("colorLightMetroStation") \
                    if LIGHT_MODE else map_color_scheme.get("colorDarkMetroStation")
        else:
            # Set the color to the custom color
            COLOR = path.custom_color

        CANVAS.create_line(x1, y1, x2, y2,
                           fill=COLOR,
                           width=5 * CANVAS_SCALE,
                           tags=("transport_path", station1.stationName, station2.stationName, path.ID))
        # Move the path to the back
        CANVAS.tag_lower("transport_path")


def clear_path(path):
    """
    Clears the path drawing
    :return:
    """
    global PATHS_DRAWN

    # Delete the path
    CANVAS.delete(path.ID)

    # Remove the path from the list of drawn paths
    PATHS_DRAWN.remove(path)

    # Refresh the canvas
    refresh_canvas()


def station_clicked(event):
    """
    Handles the station click event
    :return:
    """
    # Get the station clicked
    station = CANVAS.find_closest(event.x, event.y)[0]

    # Get the station ID
    id = CANVAS.gettags(station)[2]

    # Get the station object
    station = file_handle.get_station_by_id(id)

    # Open menu window
    GUIStation_menu.create_station_menu(station)
    print(station.stationName, station.stationID, station.transportType)


def draw_vehicle(x, y, size, transport_type, angle, vehicle_id=None, custom_color=None):
    global SIMULATION_RUNNING

    # Set the simulation running variable
    SIMULATION_RUNNING = True

    # Delete previous vehicle
    CANVAS.delete(str(vehicle_id))

    # Add vehicle id to the vehicle list if it is not already there
    if vehicle_id not in VEHICLE_ID_LIST:
        VEHICLE_ID_LIST.append(vehicle_id)

    # Calculate the size
    size = size * CANVAS_SCALE

    # Apply the drag offset and scale
    x = (x + DRAG_OFFSET[0]) * CANVAS_SCALE
    y = (y + DRAG_OFFSET[1]) * CANVAS_SCALE

    # Check for custom color
    if custom_color is None:

        # Set color based on transport type
        if transport_type == 0:
            vehicle_color = map_color_scheme.get("colorLightBusStation") \
                if LIGHT_MODE else map_color_scheme.get("colorDarkBusStation")
        elif transport_type == 1:
            vehicle_color = map_color_scheme.get("colorLightTramStation") \
                if LIGHT_MODE else map_color_scheme.get("colorDarkTramStation")
        elif transport_type == 2:
            vehicle_color = map_color_scheme.get("colorLightTrainStation") \
                if LIGHT_MODE else map_color_scheme.get("colorDarkTrainStation")
        elif transport_type == 3:
            vehicle_color = map_color_scheme.get("colorLightMetroStation") \
                if LIGHT_MODE else map_color_scheme.get("colorDarkMetroStation")
    else:
        # Set the color to the custom color
        vehicle_color = custom_color

    # Offset for rendering to the center vehicle
    offset = 7 * CANVAS_SCALE

    # Vertices of the vehicle
    vertices = [
        (x - offset, y - offset),
        (x + size - offset, y - offset),
        (x + size - offset, y + size / 2 - offset),
        (x - offset, y + size / 2 - offset)
    ]

    # Rotate the polygon vertices
    rotated_vertices = []
    for vertex in vertices:
        vertex_x, vertex_y = vertex
        rotated_x = (vertex_x - x) * math.cos(angle) - (vertex_y - y) * math.sin(angle) + x
        rotated_y = (vertex_x - x) * math.sin(angle) + (vertex_y - y) * math.cos(angle) + y
        rotated_vertices.append((rotated_x, rotated_y))

    CANVAS.create_polygon(*rotated_vertices,
                          fill=vehicle_color,
                          width=2 * CANVAS_SCALE, tags=("sim_vehicle", str(vehicle_id)))

    # Move the vehicle to the back
    CANVAS.tag_lower(str(vehicle_id))


def draw_timer_on_screen(time):
    """
    Draws the timer on the screen
    """
    global LAST_SIMULATION_TIME

    # Delete previous timer
    CANVAS.delete("sim_timer")

    LAST_SIMULATION_TIME = time

    # Calculate the time
    seconds = time % 60
    minutes = time // 60 % 60
    hours = time // 3600

    # Format the time
    time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

    # Draw box for the timer
    CANVAS.create_rectangle(0, 0, 100, 50,
                            fill="black",
                            outline="black",
                            tags="sim_timer",
                            stipple="gray50")

    # Draw the timer text
    CANVAS.create_text(50, 25,
                       text=time_string,
                       font=("Helvetica", 20),
                       fill=map_color_scheme.get(
                           "colorLightText") if LIGHT_MODE else map_color_scheme.get(
                           "colorDarkText"),
                       tags="sim_timer")

    # Move the timer to the front
    CANVAS.tag_raise("sim_timer")
