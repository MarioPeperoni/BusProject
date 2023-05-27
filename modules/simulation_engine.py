import math
import threading
import time
import datetime
import uuid

from classes.Class_transport_object import TransportObject
from classes.Class_path import Path

from gui import GUImap_canvas

from modules import file_handle

SIMULATION_RUNNING = False

TRANSPORT_TYPE = 0

VEHICLE_SPEED = 50
NEXT_STOP = 0
FPS = 60
STOP_WAIT_TIME = 4

GLOBAL_TIME_SECONDS = datetime.datetime.now().time().hour * 3600 \
                    + datetime.datetime.now().time().minute * 60 \
                    + datetime.datetime.now().time().second


GLOBAL_SIMULATION_SPEED = 10

STOPS_X = []
STOPS_Y = []


def start_simulation():
    """
    Starts the simulation
    :return:
    """
    global VEHICLE_COLOR, VEHICLE_SPEED, NEXT_STOP, TRANSPORT_TYPE, SIMULATION_RUNNING

    # Check if the simulation is already running
    if SIMULATION_RUNNING is True:
        return

    # Set simulation running to true
    SIMULATION_RUNNING = True

    # Start time
    threading.Thread(target=start_time).start()


def create_new_vehicle_simulation(transport_object: TransportObject):
    """
    Creates new vehicle simulation
    """
    sim_vehicle = SimVehicle()
    print("Starting simulation... Transport number: " + str(transport_object.number))

    # Start simulation
    threading.Thread(sim_vehicle.start_simulating(transport_object)).start()


def time_listener():
    """
    Listens for time and looks for time in transport objects timetable
    """
    if SIMULATION_RUNNING is False:
        return
    for transport_object in file_handle.transport_objects:
        # Check if the transport object has a time in table
        if GLOBAL_TIME_SECONDS in transport_object.departureTimes:
            # Create thread for simulation
            threading.Thread(target=create_new_vehicle_simulation, args=(transport_object,)).start()


def update_vehicle_speed():
    """
    Updates the vehicle speed
    """
    vehicle_speed = 0

    if TRANSPORT_TYPE == 0:
        vehicle_speed = 3 * GLOBAL_SIMULATION_SPEED
    elif TRANSPORT_TYPE == 1:
        vehicle_speed = 5 * GLOBAL_SIMULATION_SPEED
    elif TRANSPORT_TYPE == 2:
        vehicle_speed = 70 * GLOBAL_SIMULATION_SPEED
    elif TRANSPORT_TYPE == 3:
        vehicle_speed = 90 * GLOBAL_SIMULATION_SPEED

    return vehicle_speed


def start_time():
    """
    Starts counting the time
    """
    # Check if the simulation is running
    global SIMULATION_RUNNING, GLOBAL_TIME_SECONDS, GLOBAL_SIMULATION_SPEED

    while SIMULATION_RUNNING:
        # Wait for 1 second
        wait(1000 / GLOBAL_SIMULATION_SPEED, True)

        # Check if time is past 24 hours
        if GLOBAL_TIME_SECONDS >= 86400:
            # Reset the time
            GLOBAL_TIME_SECONDS = 0
        else:
            # Increment the time
            GLOBAL_TIME_SECONDS += 1

        # Check if minute passed
        if GLOBAL_TIME_SECONDS % 60 == 0:
            # Update the time
            time_listener()

        # Update the time
        GUImap_canvas.draw_timer_on_screen(GLOBAL_TIME_SECONDS)


def wait(seconds, ms=False):
    """
    Waits for given seconds
    """
    if ms:
        frames = int(seconds / (1000 / FPS))
    else:
        frames = int(seconds * FPS)

    for i in range(frames):
        GUImap_canvas.CANVAS.update()
        time.sleep(1 / FPS)


def stop_simulation():
    """
    Stops the simulation
    """
    global SIMULATION_RUNNING

    # Check if the simulation is already stopped
    if SIMULATION_RUNNING is False:
        return

    # Set simulation running to false
    SIMULATION_RUNNING = False
    GUImap_canvas.SIMULATION_RUNNING = False
    GUImap_canvas.refresh_canvas()


class SimVehicle:
    def __init__(self):
        self.ID = 0
        self.transport_type = 0
        self.vehicle_speed = update_vehicle_speed()
        self.stops_x = []
        self.stops_y = []
        self.path = 0

    def start_simulating(self, transport_object: TransportObject):
        # Set SIMULATION_RUNNING to true
        global SIMULATION_RUNNING
        SIMULATION_RUNNING = True

        # Set the vehicle ID
        self.ID = uuid.uuid4()

        # Set the transport type
        self.transport_type = transport_object.transportType

        # Read all coordinates of the stops
        for i in range(len(transport_object.stops)):
            self.stops_x.append(transport_object.stops[i].coordinateX)
            self.stops_y.append(transport_object.stops[i].coordinateY)

        # Create path for vehicle
        self.path = Path(transport_object.stops, transport_object.transportType)
        GUImap_canvas.draw_transport_path(self.path)

        # Move between stops
        for i in range(len(self.stops_x) - 1):
            self.move_between(self.stops_x[i], self.stops_y[i], self.stops_x[i + 1], self.stops_y[i + 1])

            # Wait at the stop
            wait(STOP_WAIT_TIME)

        # End of simulation - remove vehicle and path from canvas
        GUImap_canvas.clear_path(self.path)
        GUImap_canvas.CANVAS.delete(self.ID)

    def move_between(self, x1, y1, x2, y2):
        """
        Moves the vehicle between two points
        :return:
        """
        global SIMULATION_RUNNING
        if not SIMULATION_RUNNING:
            return

        # Calculate the distance between the two points
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        # Calculate the time it takes to move between the two points
        time_to_move = distance / self.vehicle_speed

        # Calculate the distance to move in each frame
        distance_to_move = distance / (time_to_move * FPS)

        # Calculate the angle between the two points
        angle = math.atan2(y2 - y1, x2 - x1)

        # Calculate the distance to move in each frame
        distance_to_move_x = distance_to_move * math.cos(angle)
        distance_to_move_y = distance_to_move * math.sin(angle)

        time_stamp = 0

        # Move the vehicle
        for i in range(int(time_to_move * FPS)):

            # Check if the simulation is running
            if not SIMULATION_RUNNING:
                return

            # Update the time stamp
            time_stamp += 1

            # Draw the vehicle
            GUImap_canvas.draw_vehicle(x1 + distance_to_move_x,
                                       y1 + distance_to_move_y,
                                       25,
                                       self.transport_type,
                                       angle,
                                       self.ID)

            # Update the coordinates
            x1 += distance_to_move_x
            y1 += distance_to_move_y

            # Update the canvas
            GUImap_canvas.CANVAS.update()

            # Wait for 1/FPS seconds
            time.sleep(1 / FPS)
