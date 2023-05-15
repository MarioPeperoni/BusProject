import tkinter as tk

import GUIform_create_transport
import GUImap_canvas

from file_handle import transport_objects
from file_handle import cityName

menu_right = None
transport_listbox = None


def create_right_menu(root):
    """
    Creates menu on the right side of application
    :param root: window of the application
    :return:
    """
    global menu_right
    menu_right = tk.Frame(root)
    menu_right.size = "200x600"

    # Create label for displaying the city name
    city_name = tk.Label(menu_right, wraplength=200, text=cityName, font=("Arial", 20, "bold"))
    city_name.pack()

    # Create button in right frame for creating a new transport entry
    create_transport_button = tk.Button(menu_right, text="Create new path",
                                        command=GUIform_create_transport.create_window)
    create_transport_button.pack()

    # Declare variable for transport type
    GUIform_create_transport.transportType = tk.IntVar(value=1)
    # Create radio buttons for transport types
    transportType_bus = tk.Radiobutton(menu_right, text="Bus", variable=GUIform_create_transport.transportType, value=1)
    transportType_bus.pack()
    transportType_tram = tk.Radiobutton(menu_right, text="Tram", variable=GUIform_create_transport.transportType,
                                        value=2)
    transportType_tram.pack()
    transportType_train = tk.Radiobutton(menu_right, text="Train", variable=GUIform_create_transport.transportType,
                                         value=3)
    transportType_train.pack()

    # Create listbox for displaying all connections
    create_listbox(menu_right).pack(pady=10, side=tk.TOP, fill=tk.BOTH, expand=True)

    return menu_right


def create_listbox(root):
    """
    Creates a listbox for displaying all transports
    :param root: root of the listbox
    :return:
    """
    global transport_listbox

    # Create listbox for displaying all transports
    transport_listbox = tk.Listbox(menu_right, height=1000)

    # Sort transport objects by number
    transport_objects.sort(key=lambda x: x.number)

    # Create a scrollbar for the listbox
    tk.Scrollbar(menu_right, orient="vertical")

    # Iterate over the transport objects and insert their names into the Listbox
    for transport in transport_objects:
        transport_listbox.insert(tk.END, "#" + str(transport.number) + " " + transport.name)

    # Bind buttons to listbox
    transport_listbox.bind("<Button-3>", show_context_menu)
    transport_listbox.bind("<<ListboxSelect>>", transport_highlight_path)

    return transport_listbox


def refresh_transport_paths(newTransportObject):
    """
    Refreshes the listbox with transport paths
    """
    global transport_listbox
    # Delete all items from listbox
    transport_listbox.delete(0, tk.END)

    # Add new transport object to list of transport objects
    transport_objects.append(newTransportObject)

    # Sort transport objects by number
    transport_objects.sort(key=lambda x: x.number)

    # Iterate over the transport objects and insert their names into the Listbox
    for transport in transport_objects:
        transport_listbox.insert(tk.END, "#" + str(transport.number) + " " + transport.name)

    transport_listbox.update()


def transport_highlight_path(event):
    """
    Highlights the selected transport path on the map
    :return:
    """
    selected_index = transport_listbox.curselection()[0]
    selected_transport = transport_objects[selected_index]

    # Print selected transport path
    GUImap_canvas.draw_transport_path(selected_transport.stops, 0)


def show_context_menu(event):
    """
    Shows context menu for the listbox
    :param event: event that triggered the function
    :return:
    """
    global transport_listbox

    # Create context menu
    context_menu = tk.Menu(transport_listbox, tearoff=0)

    # TODO: Add context menu options
    # context_menu.add_command(label="Delete", command=delete_transport)
    # context_menu.add_command(label="Edit", command=edit_transport)

    # Display context menu
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()
