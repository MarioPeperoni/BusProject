import file_handle
import openMapsImporter

# openMapsImporter.create_city("Witomino", 18.4927, 54.4900, 18.5205, 54.5040, 1000)
# openMapsImporter.create_city("Warszawa Metro Test", 21.00847, 52.22935, 21.01422, 52.23239, 1000)
file_handle.load_city()

import GUImain_window

GUImain_window.create_main_window()
