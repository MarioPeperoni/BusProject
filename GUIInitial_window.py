import json
import tkinter as tk

import file_handle

WINDOW = tk.Tk()


def create_window():
    """
    Create initial window for the program to run
    :return:
    """
    global WINDOW
    WINDOW.title("Bus Project Setup")
    WINDOW.resizable(False, False)
    WINDOW.bind("<<ListboxSelect>>", option_select)

    # Create title label
    title_label = tk.Label(WINDOW, text="Bus Project", font=("Arial", 50))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Create listbox for selecting a map
    global MAP_LISTBOX
    MAP_LISTBOX = tk.Listbox(WINDOW, width=50, height=10)
    MAP_LISTBOX.grid(row=2, column=0, columnspan=2, padx=20)

    # Append "create new map" to the listbox
    MAP_LISTBOX.insert(tk.END, "Create new empty map...")
    MAP_LISTBOX.insert(tk.END, "Create new map from coordinates...")

    # Load all the cities from the json file
    load_cities_data()

    # Create separator
    separator = tk.Frame(WINDOW)
    separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10, padx=10)

    WINDOW.mainloop()


def load_cities_data():
    """
    Loads all the cities saves from the file
    :return:
    """
    # Get all the cities from the json file
    with open("data/city_load_data.json", "r") as file:
        data = json.load(file)
    file.close()

    # Append cities name to the listbox
    index = 0
    for city in data:
        index += 1
        MAP_LISTBOX.insert(tk.END, "#" + str(index) + " " + city["name"])


def option_select(event):
    """
    Listbox selection event
    :return:
    """
    # Check if "create new map" is selected
    if MAP_LISTBOX.curselection()[0] == 0:
        # Create a new window for creating a new map
        create_new_map_window()

    # Check if "create new map from coordinates" is selected
    elif MAP_LISTBOX.curselection()[0] == 1:
        # Create a new window for creating a new map
        create_new_map_from_coordinates_window()

    # Check if existing map is selected
    else:
        # Get the selected map name
        selected_map_name = MAP_LISTBOX.get(MAP_LISTBOX.curselection()[0])

        # Remove the "#" and the number from the beginning of the string
        selected_map_name = selected_map_name.split(" ", 1)[1]

        # Load json file with all the cities
        with open("data/city_load_data.json", "r") as file:
            data = json.load(file)
        file.close()

        # Get city path by subtracting 2 from the index
        selected_map_name = data[MAP_LISTBOX.curselection()[0] - 2]["file_path"]
        file_handle.load_city(selected_map_name)
        file.close()
        load_main_program()


def create_new_map_window():
    """
    Creates window with prompts for creating new empty map
    :return:
    """
    window_new_map = tk.Toplevel()
    window_new_map.title("Create new map")
    window_new_map.resizable(False, False)

    # Prompt user to enter a name for the map
    map_name_label = tk.Label(window_new_map, text="Map name:")
    map_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
    map_name_entry = tk.Entry(window_new_map)
    map_name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)

    # Create ok button
    ok_button = tk.Button(window_new_map, text="Create",
                          command=lambda: ok_button_clicked())
    ok_button.grid(row=1, column=0, columnspan=2, pady=5)

    def ok_button_clicked():
        # Create empty city
        file_handle.create_empty_city(map_name_entry.get())

        # Load city
        file_handle.load_city()

        # Load close init window and start main program
        load_main_program()


def create_new_map_from_coordinates_window():
    """
    Creates window with prompts for creating new maps from coordinates
    """
    window_new_map = tk.Toplevel()
    window_new_map.title("Create new map from coordinates")
    window_new_map.resizable(False, False)

    # Prompt user to enter a name for the map
    map_name_label = tk.Label(window_new_map, text="Map name:")
    map_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
    map_name_entry = tk.Entry(window_new_map)
    map_name_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)

    # Prompt user to enter coordinates
    coordinates_label = tk.Label(window_new_map, text="Coordinates:")
    coordinates_label.grid(row=1, column=0, sticky="w", padx=10)

    # Create frame for inputting coordinates
    coordinates_frame = tk.Frame(window_new_map)
    coordinates_frame.grid(row=2, column=0, columnspan=2)

    # Create entry for up coordinate
    up_coordinate_entry = tk.Entry(coordinates_frame, width=4)
    up_coordinate_entry.grid(row=0, column=3)
    up_coordinate_label = tk.Label(coordinates_frame, text="⬆️")
    up_coordinate_label.grid(row=1, column=3)

    # Create entry for down coordinate
    down_coordinate_entry = tk.Entry(coordinates_frame, width=4)
    down_coordinate_entry.grid(row=4, column=3)
    down_coordinate_label = tk.Label(coordinates_frame, text="⬇️")
    down_coordinate_label.grid(row=3, column=3)

    # Create entry for left coordinate
    left_coordinate_entry = tk.Entry(coordinates_frame, width=4)
    left_coordinate_entry.grid(row=2, column=1)
    left_coordinate_label = tk.Label(coordinates_frame, text="⬅️")
    left_coordinate_label.grid(row=2, column=2)

    # Create entry for right coordinate
    right_coordinate_entry = tk.Entry(coordinates_frame, width=4)
    right_coordinate_entry.grid(row=2, column=5)
    right_coordinate_label = tk.Label(coordinates_frame, text="➡️")
    right_coordinate_label.grid(row=2, column=4)

    # Create ok button
    ok_button = tk.Button(window_new_map, text="Create",
                          command=lambda: ok_button_clicked())
    ok_button.grid(row=3, column=0, columnspan=2, pady=5)

    def ok_button_clicked():
        pass


def load_main_program():
    """
    Close init window and start main program
    """
    # Close init window
    WINDOW.withdraw()
    # Start main program
    import GUImain_window
    GUImain_window.create_main_window()
