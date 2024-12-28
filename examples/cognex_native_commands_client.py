from RobotRaconteur.Client import *

url = 'rr+tcp://localhost:59901/?service=cognex'
# Connect to the object recognition sensor service
c = RRN.ConnectService(url)

# Get a cell value. Cell must have form "A001", "B025", etc.
cell_value = c.cognex_get_cell("B025")
print(f"Cell B025: {cell_value}")

# Set a cell value.
# Available functions include "cognex_set_cell_int", "cognex_set_cell_float", "cognex_set_cell_string"
# The cell must be type "EditInt", "EditFloat", "EditString" matching the function
c.cognex_set_cell_int("E003", 1)
c.cognex_set_cell_float("D003", 10.1)
# c.cognex_set_cell_string("C003", "Hello")

# Trigger frame capture. Image acquisition must be set to "External" in the Cognex In-Sight Explorer
c.cognex_trigger_acquisition()

# Trigger an event. This is for a custom event defined in the spreadsheet
c.cognex_trigger_event(2)
