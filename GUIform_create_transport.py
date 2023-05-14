import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import GUIright_menu
import file_handle
from file_handle import stations

from classes.Enum_transport_type import TransportType
from classes.Class_transport_object import TransportObject
from classes.Class_station import Station


def create_window():
    """
    Creates a window for creating a new transport entry
    :return:
    """

    # Read the existing stations from the JSON file
    station_names = [station.stationName for station in stations]

    # Create the main window
    print(station_names)
    form = tk.Toplevel(pady=20, padx=20)
    form.title("Create new transport entry")
    form.resizable(False, False)

    # Create variables for form
    transportType = tk.IntVar(value=TransportType.Bus.value)
    number = tk.StringVar(value="")
    name = tk.StringVar(value="")
    selectedStop = tk.StringVar()
    stops = []
    inserted_departureTime = tk.StringVar(value="")
    departureTimes = []

    # Create selection for transport type
    transportType_label = tk.Label(form, text="Transport Type:")
    transportType_label.grid(row=0, column=0, sticky="w")
    # Create radio buttons for transport types
    transportType_bus = tk.Radiobutton(form, text="Bus", variable=transportType, value=TransportType.Bus.value)
    transportType_bus.grid(row=0, column=1, sticky="w")
    transportType_tram = tk.Radiobutton(form, text="Tram", variable=transportType, value=TransportType.Tram.value)
    transportType_tram.grid(row=0, column=2, sticky="w")
    transportType_train = tk.Radiobutton(form, text="Train", variable=transportType, value=TransportType.Train.value)
    transportType_train.grid(row=0, column=3, sticky="w")

    def check_for_number(entry):
        """
        Checks if input is a number
        """
        if entry.isdigit() or entry == "":
            return True
        else:
            return False

    # Create entry for transport number
    number_label = tk.Label(form, text="Route Number:")
    number_label.grid(row=1, column=0, sticky="w")
    number_entry = tk.Entry(form, textvariable=number, validate="key", validatecommand=(form.register(check_for_number),
                                                                                        "%P"))
    number_entry.grid(row=1, column=1, sticky="w")

    # Create entry for transport name
    name_label = tk.Label(form, text="Route name:")
    name_label.grid(row=2, column=0, sticky="w")
    name_entry = tk.Entry(form, textvariable=name)
    name_entry.grid(row=2, column=1, sticky="w")

    # Create a separator
    seperator1 = ttk.Separator(form, orient="horizontal")
    seperator1.grid(row=3, column=0, columnspan=4, sticky="ew", pady=10, padx=10)

    # Create a function to add a selected station
    def add_stop():
        """
        Adds a selected station to the list of selected stations
        """
        # Get selected station from dropdown menu
        station = selectedStop.get()

        if station == "                                        ":  # Check if any station is selected
            return

        # Delete station from dropdown menu
        availableStops_dropdown["menu"].delete(station_names.index(station))
        station_names.remove(station)

        # Add station to selected stations list
        selectedStops_listbox.insert(tk.END, str(len(stops)) + " " + station)
        stops.append(station)
        selectedStop.set("                                        ")
        selectedStops_listbox.update()

        # Change size of listbox
        selectedStops_listbox.config(height=len(stops))

    # Create dropdown menu for available stops
    availableStops_label = tk.Label(form, text="Available stops:")
    availableStops_label.grid(row=4, column=0, sticky="w")
    selectedStop.set("                                        ")
    availableStops_dropdown = tk.OptionMenu(form, selectedStop, *station_names)
    availableStops_dropdown.grid(row=4, column=1, columnspan=3, sticky="w")

    # Create a button to add a selected station
    add_station_button = tk.Button(form, text="➕", command=add_stop)
    add_station_button.grid(row=4, column=2, sticky="w")

    # Create a listbox for selected stations
    selectedStops_listbox = tk.Listbox(form, height=len(stops))
    selectedStops_listbox.grid(row=5, column=1)

    # Create a separator
    seperator2 = ttk.Separator(form, orient="horizontal")
    seperator2.grid(row=6, column=0, columnspan=4, sticky="ew", pady=10, padx=10)

    def check_for_length(entry):
        """
        Checks if the entry is longer than 5 characters
        :param entry:  entry to check
        :return:
        """
        if len(entry) > 5:
            return False
        else:
            return True

    def add_colon(entry):
        """
        Adds a colon to the entry time if it is 2 characters long
        :param entry: time entry
        """
        if len(entry.get()) == 2 and ":" not in entry.get():
            entry.insert(tk.END, ":")

    def add_departure_time():
        """
        Adds a selected station to the list of selected stations
        """
        # Get selected station from dropdown menu
        time = inserted_departureTime.get()

        # Add station to selected stations list
        inserted_departureTime_listbox.insert(tk.END, time)
        departureTimes.append(time)
        departureTime_entry.insert(0, "00:00")
        inserted_departureTime_listbox.update()

        # Change size of listbox
        inserted_departureTime_listbox.config(height=len(departureTimes))

    # Create input for time
    departureTime_label = tk.Label(form, text="Departure Time (hh:mm):")
    departureTime_label.grid(row=8, column=0, sticky="w")
    departureTime_entry = tk.Entry(form, width=10, validate="key",
                                   validatecommand=(departureTime_label.register(check_for_length), '%P'),
                                   textvariable=inserted_departureTime)
    departureTime_entry.grid(row=8, column=1, sticky="w")
    departureTime_entry.insert(0, "00:00")

    # Add a colon to the time input
    departureTime_entry.bind("<KeyRelease>", lambda event: add_colon(departureTime_entry))

    # Create a button to add a departure time
    add_station_button = tk.Button(form, text="➕", command=add_departure_time)
    add_station_button.grid(row=8, column=2, sticky="w")

    # Create a listbox for inputted times
    inserted_departureTime_listbox = tk.Listbox(form, height=len(departureTimes))
    inserted_departureTime_listbox.grid(row=9, column=1)

    # Create a separator
    seperator3 = ttk.Separator(form, orient="horizontal")
    seperator3.grid(row=10, column=0, columnspan=4, sticky="ew", pady=10, padx=10)

    def submit_form():
        """
        Adds a new transport entry to the json file and closes the form
        :return:
        """
        # Check if all fields are filled
        if not number.get() or not name.get() or not stops or not departureTimes:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # Convert stops to station objects
        stops_object = Station.get_stations_by_names(stops, stations)
        # Add new transport entry to json file
        file_handle.add_new_transport_entry_to_json(transportType.get(), int(number.get()), name.get(), stops_object,
                                                    departureTimes)

        # Refresh the transport paths
        file_handle.load_city()
        newTransportEntry = TransportObject(
            transportType.get(), int(number.get()), name.get(), stops_object, departureTimes)
        GUIright_menu.refresh_transport_paths(newTransportEntry)

        # Close the form
        form.destroy()

    # Create a button to add new transport entry
    submit_button = tk.Button(form, text="Add new entry", command=submit_form)
    submit_button.grid(row=11, column=0, columnspan=4)

    # Start the main loop
    form.mainloop()
