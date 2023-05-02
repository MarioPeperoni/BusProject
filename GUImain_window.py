import tkinter as tk

import GUImap_canvas
import GUIright_menu


def create_main_window():
    """
    Creates the main window of the application
    :return:
    """
    # Create the main window
    window = tk.Tk()
    window.geometry("980x600")
    window.title("Bus Project")
    window.resizable(False, False)

    # Create a canvas for displaying the map
    GUImap_canvas.create_canvas(window).pack(side="left", fill="both", expand=True, pady=5)

    # Create right side frame
    GUIright_menu.create_right_menu(window).pack(side="right", pady=5, padx=10)

    window.mainloop()
