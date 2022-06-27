# ---------------
# Author(s) : Kapwiing
# ---------------
ScriptVersion = "0.3"
# ---------------
print(f"Version : {ScriptVersion}\n\n")
# ----[INFO]----
# This script is meant to read the inputs of the controller and possibly
# inpterpret them
# --------------

# -----TODO-----
# - Read inputs of the controller using the inputs library
# --------------

from inputs import devices
from inputs import get_gamepad
from inputs import UnknownEventCode
from time import sleep

for device in devices:
    print(device)

# Get the gamepad object
try:
    gamepad = devices.gamepads[0]
except:
    print("No gamepad detected")
    exit(84)

def btn_turn(value:int):
    # print(f"Turning {value}")
    print("heeeeelllllooo")
    # TODO : Set servo to value

def btn_accelerate(value:int):
    print(f"Accelerating {value}")
    # TODO : Set motor to value

def event_start(event):
    print("je vais me start")

def btn_mode(event):
    print("Exiting Program ...")
    exit(0)

def analyse_input(event):
    func = {"BTN_START": event_start, "BTN_MODE": btn_mode, "ABS_HAT0X": btn_turn, "ABS_HAT0Y": btn_accelerate}

    if event.code in func and event.state == 1: # Exit the program if the HOME button is pressed
        func[event.code]()
    elif event.ev_type != "Sync": # Just to avoid the print of delimiter events
        print(f"TYPE : {event.ev_type}")
        print(f"CODE : {event.code}")
        print(f"STATE : {event.state}")
    # REMOVED : Memory error on raspi0
    # if (event.code == "BTN_SOUTH" and event.state == 1): # A simple vibration test
    #     # First 2 parameters are the side of the controller.
    #     # The last one is the duration of the vibration in miliseconds.
    #     gamepad.set_vibration(1, 1, 300)
    # if event.code == "BTN_START":
    #     print("je suis start")
    # elif (event.code == "ABS_X"): # Turn the car
    #     btn_turn(event.state)
    # elif (event.code == "ABS_RZ"): # Accelerate the car
    #     accelerate(event.state)

if (__name__ == "__main__"):
    while True:
        try:
            # Get all the gamepad events
            events = get_gamepad()
        except UnknownEventCode: # If the get_gamepad() func returns an error (wich he will), this prevents a useless crash
            events = []
        for event in events:
            analyse_input(event)


# -------------------------
# ----BUTTON REFFERENCE----
# -------------------------
# A = BTN_SOUTH -> 0/1
# B = BTN_EAST  -> 0/1
# X = BTN_WEST  -> 0/1
# Y = BTN_NORTH -> 0/1
# --------------
# BOTTOM/TOP ARROW = ABS_HAT0Y -> -1/0/1
# LEFT/RIGHT ARROW = ABS_HAT0X -> -1/0/1
# --------------
# L1 = BTN_TL -> 0/1
# R1 = BTN_TR -> 0/1
# L2 = ABS_Z  -> 0/255
# R2 = ABS_RZ -> 0/255
# --------------
# LEFT JOYSTICK        = ABS_X / Y   -> -32768/32767
# RIGHT JOYSTICK       = ABS_RX / Y  -> -32768/32767
# LEFT JOYSTICK CLICK  = BTN_THUMBL  -> 0/1
# RIGHT JOYSTICK CLICK = BTN_THUMBR  -> 0/1
# --------------
# SELECT = BTN_SELECT   -> 0/1
# START  = BTN_START    -> 0/1
# HOME   = BTN_MODE     -> 0/1
# ----TYPES OF INPUTS----
# - Sync
# - Key
# - Absolute
