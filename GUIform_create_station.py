import tkinter as tk
import uuid

import file_handle
import GUImap_canvas
from classes.Class_station import Station


def create_window(x, y):
    """
    Creates a window for creating a new station
    :param x: x coordinate of the station
    :param y: y coordinate of the station
    """

    form = tk.Toplevel(pady=20, padx=20)
    form.title("Create new station")
    form.resizable(False, False)

    # Create variables for form
    name = tk.StringVar(value="")
    coordinates = tk.StringVar(value="{}, {}".format(x, y))
    transportType = tk.IntVar(value=0)

    # Create frame for transport type
    transportType_frame = tk.Frame(form)
    transportType_frame.grid(row=0, column=1, sticky="w")

    # Create selection for transport type
    transportType_label = tk.Label(form, text="Transport Type:")
    transportType_label.grid(row=0, column=0, sticky="w")

    # Create radio buttons for transport types
    transportType_bus = tk.Radiobutton(transportType_frame, text="Bus", variable=transportType, value=0)
    transportType_bus.grid(row=0, column=0, sticky="w")
    transportType_tram = tk.Radiobutton(transportType_frame, text="Tram", variable=transportType, value=1)
    transportType_tram.grid(row=0, column=1, sticky="w")
    transportType_train = tk.Radiobutton(transportType_frame, text="Train", variable=transportType, value=2)
    transportType_train.grid(row=0, column=2, sticky="w")
    transportType_metro = tk.Radiobutton(transportType_frame, text="Metro", variable=transportType, value=3)
    transportType_metro.grid(row=0, column=3, sticky="w")

    # Create entry for station name
    name_label = tk.Label(form, text="Station Name:")
    name_label.grid(row=2, column=0, sticky="w")
    name_entry = tk.Entry(form, textvariable=name)
    name_entry.grid(row=2, column=1, sticky="w")

    # Create entry for station coordinates
    coordinates_label = tk.Label(form, text="Coordinates:")
    coordinates_label.grid(row=3, column=0, sticky="w")
    coordinates_entry = tk.Entry(form, textvariable=coordinates)
    coordinates_entry.grid(row=3, column=1, sticky="w")

    # Create button for submitting the form
    submit_button = tk.Button(form, text="Create station",
                              command=lambda: submit_form(name, x, y, transportType))
    submit_button.grid(row=4, column=1, columnspan=2, sticky="w")

    def submit_form(name, coordinateX, coordinateY, transportType):
        """
        Submits the form and creates a new station entry
        :param name: station name
        :param coordinateX: x coordinate of the station
        :param coordinateY: y coordinate of the station
        :param transportType: transport type of the station (0 = bus, 1 = tram, 2 = train, 3 = metro)
        """
        # Create a new station entry
        new_station = Station(name.get(), str(uuid.uuid4().int), transportType.get(),
                              round(coordinateX),
                              round(coordinateY))

        print(new_station.to_dict())

        # Write the new station to the JSON file
        file_handle.write_new_station(new_station)
        GUImap_canvas.refresh_stations(new_station)

        # Close the window
        form.destroy()
