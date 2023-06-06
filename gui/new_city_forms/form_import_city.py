import tkinter as tk

from gui.GUIInitial_window import load_main_program

from modules import openMapsImporter, file_handle


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
    up_coordinate_entry = tk.Entry(coordinates_frame, width=7)
    up_coordinate_entry.grid(row=0, column=3)
    up_coordinate_label = tk.Label(coordinates_frame, text="⬆️")
    up_coordinate_label.grid(row=1, column=3)

    # Create entry for down coordinate
    down_coordinate_entry = tk.Entry(coordinates_frame, width=7)
    down_coordinate_entry.grid(row=4, column=3)
    down_coordinate_label = tk.Label(coordinates_frame, text="⬇️")
    down_coordinate_label.grid(row=3, column=3)

    # Create entry for left coordinate
    left_coordinate_entry = tk.Entry(coordinates_frame, width=7)
    left_coordinate_entry.grid(row=2, column=1)
    left_coordinate_label = tk.Label(coordinates_frame, text="⬅️")
    left_coordinate_label.grid(row=2, column=2)

    # Create entry for right coordinate
    right_coordinate_entry = tk.Entry(coordinates_frame, width=7)
    right_coordinate_entry.grid(row=2, column=5)
    right_coordinate_label = tk.Label(coordinates_frame, text="➡️")
    right_coordinate_label.grid(row=2, column=4)

    # Create ok button
    ok_button = tk.Button(window_new_map, text="Create",
                          command=lambda: ok_button_clicked())
    ok_button.grid(row=3, column=0, columnspan=2, pady=5)

    def ok_button_clicked():
        # Import city from coordinates
        openMapsImporter.create_city(map_name_entry.get(),
                                     float(left_coordinate_entry.get()), float(down_coordinate_entry.get()),
                                     float(right_coordinate_entry.get()), float(up_coordinate_entry.get()),
                                     500, True)
        # Load city
        file_handle.load_city()

        # Close window
        window_new_map.destroy()

        # Load close init window and start main program
        load_main_program()