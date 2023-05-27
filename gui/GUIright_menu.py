import tkinter as tk
from tkinter import messagebox

from gui import GUIform_create_transport
from gui import GUImap_canvas

from modules import file_handle
from modules import simulation_engine

MENU_RIGHT = tk.Frame
TRANSPORT_LISTBOX = tk.Listbox

transport_objects = file_handle.transport_objects
bus_objects = file_handle.bus_objects
tram_objects = file_handle.tram_objects
train_objects = file_handle.train_objects
metro_objects = file_handle.metro_objects


def create_right_menu(root):
    """
    Creates menu on the right side of application
    :param root: window of the application
    :return:
    """
    global MENU_RIGHT
    global TRANSPORT_TYPE_RADIO_SELECTION

    MENU_RIGHT = tk.Frame(root)
    MENU_RIGHT.size = "200x600"

    # Create label for displaying the city name
    city_name = tk.Label(MENU_RIGHT, wraplength=200, text=file_handle.cityName, font=("Arial", 20, "bold"))
    city_name.pack()

    # Create button in right frame for creating a new transport entry
    create_transport_button = tk.Button(MENU_RIGHT, text="Create new path",
                                        command=GUIform_create_transport.create_window)
    create_transport_button.pack()

    # Create variable for storing the selected transport type
    TRANSPORT_TYPE_RADIO_SELECTION = tk.IntVar()

    # Create radio buttons for transport types
    transportType_bus = tk.Radiobutton(MENU_RIGHT, text="Bus", variable=TRANSPORT_TYPE_RADIO_SELECTION,
                                       value=0, command=refresh_transport_paths)
    transportType_bus.pack()
    transportType_tram = tk.Radiobutton(MENU_RIGHT, text="Tram", variable=TRANSPORT_TYPE_RADIO_SELECTION,
                                        value=1, command=refresh_transport_paths)
    transportType_tram.pack()
    transportType_train = tk.Radiobutton(MENU_RIGHT, text="Train", variable=TRANSPORT_TYPE_RADIO_SELECTION,
                                         value=2, command=refresh_transport_paths)
    transportType_train.pack()
    transportType_metro = tk.Radiobutton(MENU_RIGHT, text="Metro", variable=TRANSPORT_TYPE_RADIO_SELECTION,
                                         value=3, command=refresh_transport_paths)
    transportType_metro.pack()

    # Create button for starting the simulation
    start_simulation_button = tk.Button(MENU_RIGHT, text="Start simulation",
                                        command=lambda: simulation_engine.start_simulation(
                                            get_selected_transport_object()))
    start_simulation_button.pack()

    # Create button for stopping the simulation
    stop_simulation_button = tk.Button(MENU_RIGHT, text="Stop simulation",
                                       command=lambda: simulation_engine.stop_simulation())
    stop_simulation_button.pack()

    # Create listbox for displaying all connections
    create_listbox(MENU_RIGHT).pack(pady=10, side=tk.TOP, fill=tk.BOTH, expand=True)

    return MENU_RIGHT


def create_listbox(root):
    """
    Creates a listbox for displaying all transports
    :param root: root of the listbox
    :return:
    """
    global TRANSPORT_LISTBOX

    # Create listbox for displaying all transports
    TRANSPORT_LISTBOX = tk.Listbox(MENU_RIGHT, height=1000)

    # Sort transport objects by number
    transport_objects.sort(key=lambda x: x.number)

    # Create a scrollbar for the listbox
    tk.Scrollbar(MENU_RIGHT, orient="vertical")

    # Iterate over the transport objects and insert their names into the Listbox
    for transport in transport_objects:
        if transport.transportType == TRANSPORT_TYPE_RADIO_SELECTION.get():
            TRANSPORT_LISTBOX.insert(tk.END, "#" + str(transport.number) + " " + transport.name)

    # Bind buttons to listbox
    TRANSPORT_LISTBOX.bind("<Button-2>", show_context_menu)
    TRANSPORT_LISTBOX.bind("<<ListboxSelect>>", transport_highlight_path)

    return TRANSPORT_LISTBOX


def refresh_transport_paths(newTransportObject=None):
    """
    Refreshes the listbox with transport paths
    """
    global TRANSPORT_LISTBOX

    # Delete all items from listbox
    TRANSPORT_LISTBOX.delete(0, tk.END)

    # Add new transport object to list of transport objects if it is not None
    if newTransportObject is not None:
        global transport_objects, bus_objects, tram_objects, train_objects, metro_objects
        transport_objects.append(newTransportObject)

        # Split transport objects into separate lists
        bus_objects = [transport for transport in transport_objects if transport.transportType == 0]
        tram_objects = [transport for transport in transport_objects if transport.transportType == 1]
        train_objects = [transport for transport in transport_objects if transport.transportType == 2]
        metro_objects = [transport for transport in transport_objects if transport.transportType == 3]

    # Sort transport objects by number
    transport_objects.sort(key=lambda x: x.number)

    # Iterate over the transport objects and insert their names into the Listbox
    for transport in transport_objects:
        if transport.transportType == TRANSPORT_TYPE_RADIO_SELECTION.get():
            TRANSPORT_LISTBOX.insert(tk.END, "#" + str(transport.number) + " " + transport.name)

    TRANSPORT_LISTBOX.update()


def get_selected_transport_object():
    # Get selected transport object
    if TRANSPORT_TYPE_RADIO_SELECTION.get() == 0:
        selected_transport = bus_objects[TRANSPORT_LISTBOX.curselection()[0]]
    elif TRANSPORT_TYPE_RADIO_SELECTION.get() == 1:
        selected_transport = tram_objects[TRANSPORT_LISTBOX.curselection()[0]]
    elif TRANSPORT_TYPE_RADIO_SELECTION.get() == 2:
        selected_transport = train_objects[TRANSPORT_LISTBOX.curselection()[0]]
    elif TRANSPORT_TYPE_RADIO_SELECTION.get() == 3:
        selected_transport = metro_objects[TRANSPORT_LISTBOX.curselection()[0]]

    return selected_transport


def transport_highlight_path(event):
    """
    Highlights the selected transport path on the map
    :return:
    """

    selected_transport = get_selected_transport_object()

    # Cancel any running simulation
    simulation_engine.stop_simulation()

    # Draw selected transport path
    GUImap_canvas.draw_transport_path(selected_transport.stops, TRANSPORT_TYPE_RADIO_SELECTION.get())


def show_context_menu(event):
    """
    Shows context menu for the listbox
    :param event: event that triggered the function
    :return:
    """
    global TRANSPORT_LISTBOX

    # Create context menu
    context_menu = tk.Menu(TRANSPORT_LISTBOX, tearoff=0)

    # TODO: Add context menu options
    context_menu.add_command(label="Delete", command=delete_transport)
    # context_menu.add_command(label="Edit", command=edit_transport)

    # Display context menu
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()


def delete_transport():
    """
    Deletes transport path from dataset and listbox
    :return:
    """

    # Show confirmation popup
    if not messagebox.askokcancel("Delete transport path",
                                  "Are you sure you want to delete this transport path?",
                                  icon="warning"):
        return

    # Get selected transport object and delete from dataset
    if TRANSPORT_TYPE_RADIO_SELECTION.get() == 0:
        selected_transport = bus_objects[TRANSPORT_LISTBOX.curselection()[0]]
        bus_objects.remove(selected_transport)
    elif TRANSPORT_TYPE_RADIO_SELECTION.get() == 1:
        selected_transport = tram_objects[TRANSPORT_LISTBOX.curselection()[0]]
        tram_objects.remove(selected_transport)
    elif TRANSPORT_TYPE_RADIO_SELECTION.get() == 2:
        selected_transport = train_objects[TRANSPORT_LISTBOX.curselection()[0]]
        train_objects.remove(selected_transport)
    elif TRANSPORT_TYPE_RADIO_SELECTION.get() == 3:
        selected_transport = metro_objects[TRANSPORT_LISTBOX.curselection()[0]]
        metro_objects.remove(selected_transport)

    # Delete transport object from list of all transport objects
    transport_objects.remove(selected_transport)

    # Delete transport object from listbox
    TRANSPORT_LISTBOX.delete(TRANSPORT_LISTBOX.curselection()[0])

    # Delete from database
    file_handle.delete_transport_object(selected_transport)
