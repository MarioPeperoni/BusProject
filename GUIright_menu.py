import tkinter as tk

import GUIform_create_transport
import GUImap_canvas

from file_handle import transport_objects
from file_handle import cityName

MENU_RIGHT = None
TRANSPORT_LISTBOX = None


def create_right_menu(root):
    """
    Creates menu on the right side of application
    :param root: window of the application
    :return:
    """
    global MENU_RIGHT
    MENU_RIGHT = tk.Frame(root)
    MENU_RIGHT.size = "200x600"

    # Create label for displaying the city name
    city_name = tk.Label(MENU_RIGHT, wraplength=200, text=cityName, font=("Arial", 20, "bold"))
    city_name.pack()

    # Create button in right frame for creating a new transport entry
    create_transport_button = tk.Button(MENU_RIGHT, text="Create new path",
                                        command=GUIform_create_transport.create_window)
    create_transport_button.pack()

    # Declare variable for transport type
    GUIform_create_transport.transportType = tk.IntVar(value=0)

    # Create radio buttons for transport types
    transportType_bus = tk.Radiobutton(MENU_RIGHT, text="Bus", variable=GUIform_create_transport.transportType,
                                       value=0, command=refresh_transport_paths)
    transportType_bus.pack()
    transportType_tram = tk.Radiobutton(MENU_RIGHT, text="Tram", variable=GUIform_create_transport.transportType,
                                        value=1, command=refresh_transport_paths)
    transportType_tram.pack()
    transportType_train = tk.Radiobutton(MENU_RIGHT, text="Train", variable=GUIform_create_transport.transportType,
                                         value=2, command=refresh_transport_paths)
    transportType_train.pack()

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
        TRANSPORT_LISTBOX.insert(tk.END, "#" + str(transport.number) + " " + transport.name)

    # Bind buttons to listbox
    TRANSPORT_LISTBOX.bind("<Button-3>", show_context_menu)
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
        transport_objects.append(newTransportObject)

    # Sort transport objects by number
    transport_objects.sort(key=lambda x: x.number)

    # Iterate over the transport objects and insert their names into the Listbox
    for transport in transport_objects:
        if transport.transportType == GUIform_create_transport.transportType.get():
            TRANSPORT_LISTBOX.insert(tk.END, "#" + str(transport.number) + " " + transport.name)

    TRANSPORT_LISTBOX.update()


def transport_highlight_path(event):
    """
    Highlights the selected transport path on the map
    :return:
    """
    selected_index = TRANSPORT_LISTBOX.curselection()[0]
    selected_transport = transport_objects[selected_index]

    # Draw selected transport path
    GUImap_canvas.draw_transport_path(selected_transport.stops, GUIform_create_transport.transportType.get())


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
    # context_menu.add_command(label="Delete", command=delete_transport)
    # context_menu.add_command(label="Edit", command=edit_transport)

    # Display context menu
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()
