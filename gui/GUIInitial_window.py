import json
import tkinter as tk

from gui.new_city_forms.form_empty_city import create_new_map_window
from gui.new_city_forms.form_import_city import create_new_map_from_coordinates_window
from modules import file_handle

WINDOW = tk.Tk()


def create_window():
    """
    Create initial window for the program to run
    :return:
    """
    global WINDOW
    WINDOW.title("Bus Project Setup")
    WINDOW.resizable(False, False)
    WINDOW.iconbitmap("data/icon/icon.ico")
    WINDOW.iconphoto(True, tk.PhotoImage(file="data/icon/icon.png"))
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
    try:
        with open("data/city_load_data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
        # Create the file if it doesn't exist
        with open("data/city_load_data.json", "w") as file:
            json.dump(data, file, indent=4)
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
        # Load json file with all the cities
        with open("data/city_load_data.json", "r") as file:
            data = json.load(file)
        file.close()

        # Get city path by subtracting 2 from the index
        selected_map_path = data[MAP_LISTBOX.curselection()[0] - 2]["file_path"]
        file_handle.load_city(selected_map_path)
        load_main_program()


def load_main_program():
    """
    Close init window and start main program
    """
    # Close init window
    WINDOW.withdraw()
    # Start main program
    from gui import GUImain_window
    GUImain_window.create_main_window()
