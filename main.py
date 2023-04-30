import tkinter as tk
import create_transport_entry

# Create the main window
window = tk.Tk()
window.geometry("800x600")
window.title("App")

# Create a button to open the CreateTransportEntry window
create_transport_button = tk.Button(window, text="Create Transport Entry", command=create_transport_entry.create_window)
create_transport_button.pack()

# Start the main loop
window.mainloop()