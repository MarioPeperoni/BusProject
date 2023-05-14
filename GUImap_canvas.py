from tkinter import Canvas

import file_handle

canvas = Canvas
max_zoom = 10
canvas_scale = 1

stations = file_handle.return_list_of_stations()
map_details = file_handle.return_list_of_map_details()
map_color_scheme = file_handle.return_map_color_scheme()

lightMode = False

def create_canvas(tk):
    """
    Creates a canvas for displaying the map
    :param tk: tkinter
    :return:
    """
    global canvas
    global stations
    global map_color_scheme

    canvas = Canvas(tk, width=800, height=600)

    canvas.bind("<MouseWheel>", zoom)
    canvas.bind("<ButtonPress-1>", start_drag)
    canvas.bind("<B1-Motion>", drag)
    canvas.bind("<Motion>", update_mouse_position)

    # Set the background color
    canvas.configure(bg=map_color_scheme.get("colorLightBG") if lightMode else map_color_scheme.get("colorDarkBG"))

    # Draw the map details
    draw_map_details()

    # Draw the stations
    draw_stations(stations)

    # Draw text with coordinated of the mouse
    canvas.create_text(40, 580, text="(0, 0)", tags="mouse_position")
    return canvas


def zoom(event):
    """
    Zooms the map in and out
    :param event: event
    :return:
    """
    global canvas
    global max_zoom
    global canvas_scale

    # Get the mouse wheel delta
    if event.delta > 0:
        scale = 1.1
    elif event.delta < 0:
        scale = 0.9

    if canvas_scale * scale > max_zoom:
        return
    canvas_scale *= scale

    # Update the scale
    canvas.scale("all", event.x, event.y, scale, scale)


def start_drag(event):
    """
    Starts dragging the map with the mouse
    :param event:
    :return:
    """
    global canvas
    canvas.drag_start_x = event.x
    canvas.drag_start_y = event.y


def drag(event):
    """
    Drags the map with the mouse
    :param event: event
    :return:
    """
    global canvas
    canvas.move("all", event.x - canvas.drag_start_x, event.y - canvas.drag_start_y)
    canvas.drag_start_x = event.x
    canvas.drag_start_y = event.y


def update_mouse_position(event):
    """
    Updates the mouse position text
    :param event: event
    :return:
    """
    global canvas
    global canvas_scale

    # Get the mouse position
    mouse_x = int(event.x / canvas_scale)
    mouse_y = int(event.y / canvas_scale)

    # Update the text
    canvas.delete("mouse_position")
    canvas.create_text(40, 580, text="(" + str(mouse_x) + ", " + str(mouse_y) + ")", tags="mouse_position")


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
    global canvas_scale
    global map_color_scheme

    # Draw the stations
    for station in stations:
        if station.transportType == 0:
            color = map_color_scheme.get("colorLightBusStation") \
                if lightMode else map_color_scheme.get("colorDarkBusStation")
        elif station.transportType == 1:
            color = map_color_scheme.get("colorLightTramStation") \
                if lightMode else map_color_scheme.get("colorDarkTramStation")
        elif station.transportType == 2:
            color = map_color_scheme.get("colorLightTrainStation") \
                if lightMode else map_color_scheme.get("colorDarkTrainStation")
        else:
            color = "black"

        # Create the station circle
        canvas.create_oval(station.coordinateX - 10, station.coordinateY - 10,
                           station.coordinateX + 10, station.coordinateY + 10,
                           fill=color,
                           outline="black"
                           if lightMode else "white", width=5)

        # Draw the station name
        # For now it is not adaptive to the zoom level

        # Set up the font
        font_size = int(10)
        font_color = map_color_scheme.get("colorLightText") if lightMode else map_color_scheme.get("colorDarkText")
        font = ("Arial", font_size, "bold")

        canvas.create_text(station.coordinateX, station.coordinateY + 20, text=station.stationName,
                           font=font, fill=font_color,
                           tags="station")
