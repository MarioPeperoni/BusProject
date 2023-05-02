import tkinter as tk

import GUIform_create_transport

from file_handle import transport_objects

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

    # Create button in right frame for creating a new transport entry
    create_transport_button = tk.Button(menu_right, text="Create new path",
                                        command=GUIform_create_transport.create_window)
    create_transport_button.pack()

    # Create listbox for displaying all connections
    create_listbox(menu_right)

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
    scrollbar = tk.Scrollbar(menu_right, orient="vertical")

    # Iterate over the transport objects and insert their names into the Listbox
    for transport in transport_objects:
        transport_listbox.insert(tk.END, "#" + str(transport.number) + " " + transport.name)

    transport_listbox.pack(pady=10)

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
