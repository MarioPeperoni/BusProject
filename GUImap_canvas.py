from tkinter import Canvas

import file_handle

# Global variables
CANVAS = Canvas
MAX_ZOOM = 2
CANVAS_SCALE = 1
DRAG_OFFSET = [0, 0]
LIGHT_MODE = False

stations = file_handle.return_list_of_stations()
map_details = file_handle.return_list_of_map_details()
map_color_scheme = file_handle.return_map_color_scheme()


def create_canvas(tk):
    """
    Creates a canvas for displaying the map
    :param tk: tkinter
    :return:
    """
    global CANVAS
    global stations
    global map_color_scheme

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

    # Redraw the stations
    # UNCOMMENT FOR EXPERIMENTAL ZOOMING
    # draw_stations(stations)

    output_debug_data()


def start_drag(event):
    """
    Starts dragging the map with the mouse
    :param event:
    :return:
    """
    global CANVAS
    print("Start drag: " + str(event.x) + ", " + str(event.y))
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
    dx = event.x - CANVAS.drag_start_x
    dy = event.y - CANVAS.drag_start_y

    # Update the drag offset
    DRAG_OFFSET[0] += dx
    DRAG_OFFSET[1] += dy

    # Move the map
    CANVAS.move("all", dx, dy)
    CANVAS.drag_start_x = event.x
    CANVAS.drag_start_y = event.y

    print("Drag offset: " + str(DRAG_OFFSET[0]) + ", " + str(DRAG_OFFSET[1]))


def draw_map_details():
    """
    Draws the map details on the canvas
    :return:
    """
    global CANVAS
    global map_details

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
    global map_color_scheme

    CANVAS.delete("station_circle")
    CANVAS.delete("station_name")

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
                           width=5 * CANVAS_SCALE, tags=("station_circle", station.stationName, station.stationID))
        print("Station: " + station.stationName + ", " + str(station.stationID))

        # Set up the font
        font_size = int(12 * CANVAS_SCALE)
        font_color = map_color_scheme.get("colorLightText") if LIGHT_MODE else map_color_scheme.get("colorDarkText")
        font = ("Arial", font_size, "bold")

        # Draw the station name
        CANVAS.create_text((station.coordinateX + DRAG_OFFSET[0]) * CANVAS_SCALE,
                           (station.coordinateY + DRAG_OFFSET[1]) * CANVAS_SCALE + 20 * CANVAS_SCALE,
                           text=station.stationName,
                           font=font, fill=font_color,
                           tags=("station_text", station.stationName, station.stationID))


def output_debug_data():
    print("CANVAS_SCALE: " + str(CANVAS_SCALE))
    print("DRAG_OFFSET: " + str(DRAG_OFFSET))


def draw_transport_path(stations_selected):
    """
    Highlights stations and draw the path between them
    :param stations_selected:
    :return:
    """

    # Print the stations
    for station in stations_selected:
        print(station.stationName)

    # Find stations with the same ID
    for station in stations_selected:
        print("Station ID: " + str(station.stationID))
        station_circle = CANVAS.find_withtag(station.stationName)[0]
        station_text = CANVAS.find_withtag(station.stationName)[1]
        CANVAS.itemconfig(station_circle, fill="yellow")
