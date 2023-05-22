import math
import time

from classes.Class_transport_object import TransportObject

import GUImap_canvas

SIMULATION_RUNNING = False

TRANSPORT_TYPE = 0

VEHICLE_SPEED = 50
NEXT_STOP = 0
FPS = 60
STOP_WAIT_TIME = 4

STOPS_X = []
STOPS_Y = []


def start_simulation(transport_object: TransportObject):
    """
    Starts the simulation
    :param transport_object:
    :return:
    """
    global VEHICLE_COLOR, VEHICLE_SPEED, NEXT_STOP, TRANSPORT_TYPE, SIMULATION_RUNNING

    # Set simulation running to true
    SIMULATION_RUNNING = True

    # Clear variables
    STOPS_X.clear()
    STOPS_Y.clear()
    NEXT_STOP = 0

    # Set the transport type
    TRANSPORT_TYPE = transport_object.transportType

    # Determine speed by transport type
    if TRANSPORT_TYPE == 0:
        VEHICLE_SPEED = 30
    elif TRANSPORT_TYPE == 1:
        VEHICLE_SPEED = 50
    elif TRANSPORT_TYPE == 2:
        VEHICLE_SPEED = 70
    elif TRANSPORT_TYPE == 3:
        VEHICLE_SPEED = 90

    # Set next stop to the first stop
    NEXT_STOP = 0

    # Read all coordinates of the stops
    for i in range(len(transport_object.stops)):
        STOPS_X.append(transport_object.stops[i].coordinateX)
        STOPS_Y.append(transport_object.stops[i].coordinateY)

    # Calculate the distance between stops
    distance_between_stops = []
    for i in range(len(STOPS_X) - 1):
        distance_between_stops.append((STOPS_X[i + 1] - STOPS_X[i]) ** 2 + (STOPS_Y[i + 1] - STOPS_Y[i]) ** 2)

    # Draw the vehicle
    print(distance_between_stops)

    # Move between stops
    for i in range(len(STOPS_X) - 1):
        print("Moving between stops", i, "and", i + 1)
        move_between(STOPS_X[i], STOPS_Y[i], STOPS_X[i + 1], STOPS_Y[i + 1])

        # Wait at the stop
        wait(STOP_WAIT_TIME)


def move_between(x1, y1, x2, y2):
    """
    Moves the vehicle between two points
    :param x1: x coordinate of the first point
    :param y1: y coordinate of the first point
    :param x2: x coordinate of the second point
    :param y2: y coordinate of the second point
    """

    # Check if the simulation is running
    global SIMULATION_RUNNING
    if not SIMULATION_RUNNING:
        return

    # Calculate the distance between the two points
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    # Calculate the time it takes to move between the two points
    time_to_move = distance / VEHICLE_SPEED

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

        # Print the time stamp, distance to move and angle
        print("Time Stamp:", time_stamp, "Distance to Move (X):", distance_to_move_x, "Distance to Move (Y):",
              distance_to_move_y, "Angle:", angle)

        # Update the time stamp
        time_stamp += 1

        # Draw the vehicle
        GUImap_canvas.draw_vehicle(x1 + distance_to_move_x, y1 + distance_to_move_y, 25, TRANSPORT_TYPE, angle)

        # Update the coordinates
        x1 += distance_to_move_x
        y1 += distance_to_move_y

        # Update the canvas
        GUImap_canvas.CANVAS.update()

        # Wait for 1/FPS seconds
        time.sleep(1 / FPS)


def wait(seconds):
    """
    Waits for given seconds
    """
    for i in range(seconds * FPS):
        GUImap_canvas.CANVAS.update()
        time.sleep(1 / FPS)


def stop_simulation():
    """
    Stops the simulation
    """
    global SIMULATION_RUNNING

    # Set simulation running to false
    SIMULATION_RUNNING = False
    GUImap_canvas.SIMULATION_RUNNING = False
    GUImap_canvas.refresh_canvas()
