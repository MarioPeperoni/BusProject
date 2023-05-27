import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from gui import GUIright_menu
from modules import file_handle

from classes.Class_station import Station
from classes.Class_transport_object import TransportObject

from modules.file_handle import stations


def create_window():
    """
    Create a window for creating new transport path
    :return:
    """

    global WINDOW, \
        TRANSPORT_TYPE, NUMBER, NAME, \
        SELECTED_STOP, STOPS_ADDED, STOP_NAMES, \
        DEPARTURE_TIME_INPUT, DEPARTURE_TIMES

    # Create window
    WINDOW = tk.Toplevel(pady=20, padx=20)
    WINDOW.title("Create new transport path")
    WINDOW.resizable(False, False)

    # Create variables for form
    TRANSPORT_TYPE = tk.IntVar(value=0)
    NUMBER = tk.StringVar(value="")
    NAME = tk.StringVar(value="")
    SELECTED_STOP = tk.StringVar(value="")
    STOPS_ADDED = []
    STOP_NAMES = []
    DEPARTURE_TIME_INPUT = tk.StringVar(value="")
    DEPARTURE_TIMES = []

    # Populate the stop names
    populate_stop_names(0, True)

    # Layout the form
    transport_type_selection_frame()  # (0, 0) - (0, 1)
    basic_info_frame()  # (1, 0) - (2, 1)
    ttk.Separator(WINDOW, orient="horizontal").grid(row=3, column=0, columnspan=3, sticky="ew", pady=10, padx=10)
    stops_frame()  # (4, 0) - (5, 1)
    ttk.Separator(WINDOW, orient="horizontal").grid(row=6, column=0, columnspan=3, sticky="ew", pady=10, padx=10)
    departure_times_frame()  # (7, 0) - (8, 1)
    ttk.Separator(WINDOW, orient="horizontal").grid(row=9, column=0, columnspan=3, sticky="ew", pady=10, padx=10)
    tk.Button(WINDOW, text="Create path", command=submit_form).grid(row=10, column=0, columnspan=3)


def transport_type_selection_frame():
    """
    Creates the frame for the transport type selection
    :param x: x coordinate in WINDOW frame
    :param y: y coordinate in WINDOW frame
    """

    # Create label for selection
    transportType_label = tk.Label(WINDOW, text="Transport Type:")
    transportType_label.grid(row=0, column=0, sticky="w")

    # Create frame for selection
    transportType_frame = tk.Frame(WINDOW)

    # Create radio buttons for transport types in frame
    transportType_bus = tk.Radiobutton(transportType_frame, text="Bus", variable=TRANSPORT_TYPE, value=0,
                                       command=lambda: populate_stop_names(0))
    transportType_bus.grid(row=0, column=1, sticky="w")
    transportType_tram = tk.Radiobutton(transportType_frame, text="Tram", variable=TRANSPORT_TYPE, value=1,
                                        command=lambda: populate_stop_names(1))
    transportType_tram.grid(row=0, column=2, sticky="w")
    transportType_train = tk.Radiobutton(transportType_frame, text="Train", variable=TRANSPORT_TYPE, value=2,
                                         command=lambda: populate_stop_names(2))
    transportType_train.grid(row=0, column=3, sticky="w")
    transportType_metro = tk.Radiobutton(transportType_frame, text="Metro", variable=TRANSPORT_TYPE, value=3,
                                         command=lambda: populate_stop_names(3))
    transportType_metro.grid(row=0, column=4, sticky="w")

    # Align frame
    transportType_frame.grid(row=0, column=1, sticky="w")


def basic_info_frame():
    """
    Creates the frame for the basic information input
    :return: frame
    """

    # Create labels for basic info
    number_label = tk.Label(WINDOW, text="Route ID:")
    number_label.grid(row=1, column=0, sticky="w")

    number_entry = tk.Entry(WINDOW, textvariable=NUMBER)
    number_entry.grid(row=1, column=1, sticky="w")

    name_label = tk.Label(WINDOW, text="Route Name:")
    name_label.grid(row=2, column=0, sticky="w")

    name_entry = tk.Entry(WINDOW, textvariable=NAME)
    name_entry.grid(row=2, column=1, sticky="w")


def populate_stop_names(transport_type, init=False):
    """
    Populates the stop names for the dropdown menu for corresponding transport type
    :param transport_type: 0 = bus, 1 = tram, 2 = train, 3 = metro
    :param init: True if called on initialization
    """

    global AVAILABLE_STOPS_DROPDOWN

    # Clear stop names and stops added
    STOP_NAMES.clear()
    SELECTED_STOP.set("                                        ")
    STOPS_ADDED.clear()

    # Populate stop names with corresponding transport type
    for station in stations:
        if station.transportType == transport_type:
            STOP_NAMES.append(station.stationName)

    # Check if called on initialization
    if init is not True:

        # Refresh the dropdown menu
        menu = AVAILABLE_STOPS_DROPDOWN['menu']
        menu.delete(0, tk.END)  # Delete all existing menu items

        # Add new menu items
        for stop_name in STOP_NAMES:
            menu.add_command(label=stop_name, command=tk._setit(SELECTED_STOP, stop_name))

        # Reset listbox
        ADDED_STOPS_LISTBOX.delete(0, tk.END)
        ADDED_STOPS_LISTBOX.config(height=len(STOPS_ADDED))


def stops_frame():
    """
    Creates dropdown menu for selecting stops of current transportType
    and listbox for showing added stops
    :return: frame
    """
    global AVAILABLE_STOPS_DROPDOWN
    global ADDED_STOPS_LISTBOX

    def add_stop():
        """
        Adds selected stop to listbox
        """

        # Check if any stop is selected
        if SELECTED_STOP.get() == "                                        ":
            messagebox.showerror("Error", "Please select a stop")
            return

        # Delete stop from dropdown menu
        AVAILABLE_STOPS_DROPDOWN["menu"].delete(STOP_NAMES.index(SELECTED_STOP.get()))
        STOP_NAMES.remove(SELECTED_STOP.get())

        # Insert stop to listbox and add to STOPS_ADDED
        ADDED_STOPS_LISTBOX.insert(tk.END, str(len(STOPS_ADDED)) + " " + SELECTED_STOP.get())
        STOPS_ADDED.append(SELECTED_STOP.get())
        SELECTED_STOP.set("                                        ")

        # Change size of listbox
        ADDED_STOPS_LISTBOX.config(height=len(STOPS_ADDED))

    def remove_stop():
        pass

    # Create frame for stops
    stops_frame = tk.Frame(WINDOW)

    # Create dropdown menu for stops
    available_stops_label = tk.Label(WINDOW, text="Available stops:")
    available_stops_label.grid(row=4, column=0, sticky="w")
    SELECTED_STOP.set("                                        ")

    AVAILABLE_STOPS_DROPDOWN = tk.OptionMenu(WINDOW, SELECTED_STOP, *STOP_NAMES)
    AVAILABLE_STOPS_DROPDOWN.grid(row=4, column=1, sticky="w")

    # Create button to add stop to listbox
    add_stop_button = tk.Button(stops_frame, text="➕", command=add_stop)
    add_stop_button.grid(row=0, column=0, sticky="w")

    # Create button to remove stop from listbox
    # remove_stop_button = tk.Button(stops_frame, text="➖", command=remove_stop)
    # remove_stop_button.grid(row=1, column=0, sticky="w")

    # Create listbox for added stops
    ADDED_STOPS_LISTBOX = tk.Listbox(WINDOW, height=len(STOPS_ADDED))
    ADDED_STOPS_LISTBOX.grid(row=5, column=1, columnspan=4, sticky="w")

    stops_frame.grid(row=4, column=2, sticky="w")


def departure_times_frame():
    """
    Creates the frame for the time input
    :return:
    """

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
        Adds departure time to listbox
        """
        # Check if correct time format is entered
        if DEPARTURE_TIME_INPUT.get() == "":
            messagebox.showerror("Error", "Please enter a departure time")
            return
        if int(DEPARTURE_TIME_INPUT.get().split(":")[0]) > 23 or int(DEPARTURE_TIME_INPUT.get().split(":")[1]) > 59:
            messagebox.showerror("Error", "Please enter a valid departure time")
            return

        # Insert time to listbox and add to DEPARTURE_TIMES
        DEPARTURE_TIMES_LISTBOX.insert(tk.END, DEPARTURE_TIME_INPUT.get())
        DEPARTURE_TIMES.append(DEPARTURE_TIME_INPUT.get())
        DEPARTURE_TIME_INPUT.set("12:00")

        # Change size of listbox
        DEPARTURE_TIMES_LISTBOX.config(height=len(DEPARTURE_TIMES))

    # Create input for departure times
    departure_times_label = tk.Label(WINDOW, text="Departure times:")
    departure_times_label.grid(row=7, column=0, sticky="w")

    # Create entry for departure times
    departure_times_entry = tk.Entry(WINDOW, textvariable=DEPARTURE_TIME_INPUT, width=10,
                                     validate="key", validatecommand=(WINDOW.register(check_for_length), "%P"))
    DEPARTURE_TIME_INPUT.set("12:00")
    departure_times_entry.grid(row=7, column=1, sticky="w")

    # Add a colon to the time input
    departure_times_entry.bind("<KeyRelease>", lambda event: add_colon(departure_times_entry))

    # Create button to add departure time to listbox
    add_departure_time_button = tk.Button(WINDOW, text="➕", command=add_departure_time)
    add_departure_time_button.grid(row=7, column=2, sticky="w")

    # Create listbox for added departure times
    DEPARTURE_TIMES_LISTBOX = tk.Listbox(WINDOW, height=len(DEPARTURE_TIMES))
    DEPARTURE_TIMES_LISTBOX.grid(row=8, column=1, columnspan=4, sticky="w")


def time_to_seconds(time):
    """
    Converts a time in the format HH:MM to seconds
    :param time: time in the format HH:MM
    :return: time in seconds
    """
    return int(time.split(":")[0]) * 3600 + int(time.split(":")[1]) * 60


def submit_form():
    """
    Adds a new transport entry to the json file and closes the form
    """

    # Check if all fields are filled
    if TRANSPORT_TYPE.get() == "" \
            or NUMBER.get() == "" \
            or NAME.get() == "" \
            or len(STOPS_ADDED) == 0 \
            or len(DEPARTURE_TIMES) == 0:
        messagebox.showerror("Error", "Please fill out all fields")
        return

    # Convert stops names to station objects
    stops = Station.get_stations_by_names(STOPS_ADDED, stations)

    # Convert times to seconds
    for i in range(len(DEPARTURE_TIMES)):
        DEPARTURE_TIMES[i] = time_to_seconds(DEPARTURE_TIMES[i])

    # Add new transport entry to json file
    file_handle.write_new_transport_path(TRANSPORT_TYPE.get(), int(NUMBER.get()), NAME.get(), stops, DEPARTURE_TIMES)

    # Refresh transport list
    newTransportEntry = TransportObject(
        TRANSPORT_TYPE.get(), int(NUMBER.get()), NAME.get(), stops, DEPARTURE_TIMES)
    GUIright_menu.refresh_transport_paths(newTransportEntry)

    # Close form
    WINDOW.destroy()
