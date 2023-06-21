import tkinter as tk
import tkinter.messagebox as messagebox

from modules import simulation_engine


def create():
    """
    Creates window with prompts for setting time
    """
    window_set_time = tk.Toplevel()
    window_set_time.title("Set time (HH:MM)")
    window_set_time.resizable(False, False)

    # Prompt user to enter a name for the map
    time_label = tk.Label(window_set_time, text="Time:")
    time_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    time_entry = tk.Entry(window_set_time)
    time_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)
    time_entry.insert(0, '12:00')

    # Create ok button
    ok_button = tk.Button(window_set_time, text="Set",
                          command=lambda: ok_button_clicked())
    ok_button.grid(row=1, column=0, columnspan=2, pady=5)

    def ok_button_clicked():
        # Check for correct time format
        if len(time_entry.get()) != 5:
            messagebox.showerror("Error", "Incorrect time format")
            return
        if time_entry.get()[2] != ":":
            messagebox.showerror("Error", "Incorrect time format")
            return
        if not time_entry.get()[0:2].isdigit():
            messagebox.showerror("Error", "Incorrect time format")
            return
        if not time_entry.get()[3:5].isdigit():
            messagebox.showerror("Error", "Incorrect time format")
            return

        simulation_engine.set_time(time_entry.get())
        window_set_time.destroy()
