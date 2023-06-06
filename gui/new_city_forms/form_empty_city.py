import tkinter as tk

from gui.GUIInitial_window import load_main_program

from modules import file_handle


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

    def ok_button_clicked(self):
        # Create empty city
        file_handle.create_empty_city(map_name_entry.get())

        # Load city
        file_handle.load_city()

        # Close window
        window_new_map.destroy()

        # Load close init window and start main program
        load_main_program()
