import tkinter as tk

import GUImap_canvas
import file_handle

from tkinter import messagebox


def create_station_menu(station):
    global WINDOW

    WINDOW = tk.Tk()
    WINDOW.title("Station Menu")
    WINDOW.geometry("300x300")
    WINDOW.resizable(False, False)

    # Create title label
    title_label = tk.Label(WINDOW, text=station.stationName, font=("Arial", 20))
    title_label.pack(pady=10, padx=10)

    # Create delete button
    delete_button = tk.Button(WINDOW, text="Delete", command=lambda: delete_station(station))
    delete_button.pack(pady=10, padx=10)


def delete_station(station):
    """
    Deletes station from canvas and database
    :return:
    """

    # Create message box with confirmation
    if not messagebox.askyesno("Delete station", "Are you sure you want to delete this station?", icon="warning"):
        return

    # Delete station from database
    file_handle.delete_station(station)

    # Delete station from canvas
    GUImap_canvas.refresh_stations(station, "remove")

    # Close window
    WINDOW.destroy()
