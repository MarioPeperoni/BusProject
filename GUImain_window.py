import tkinter as tk

import GUImap_canvas
import GUIform_create_tranport


def create_main_window():
    """
    Creates the main window of the application
    :return:
    """
    # Create the main window
    window = tk.Tk()
    window.geometry("980x600")
    window.title("Bus Project")

    # Create a button to open the CreateTransportEntry window
    create_transport_button = tk.Button(window, text="Create Transport Entry",
                                        command=GUIform_create_tranport.create_window)
    create_transport_button.pack(side="right", anchor="ne", pady=20)

    # Create a canvas for displaying the map
    GUImap_canvas.create_canvas(window).pack(side="left")

    window.mainloop()
