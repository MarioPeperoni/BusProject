import file_handle
import openMapsImporter

# openMapsImporter.read_mapping_table()
openMapsImporter.import_area(18.4914, 54.4884, 18.5242, 54.5055, 1000) # Map of Witomino
openMapsImporter.create_city("Witomino")
file_handle.load_city()

import GUImain_window

GUImain_window.create_main_window()
