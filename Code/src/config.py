import os
import sys

def has_graphic():
    if sys.platform == "win32":
        return True
    return "DISPLAY" in os.environ

# General configurations
FPS = 12

WEBRTC_SERVER = True
OPENCV_WINDOW = has_graphic()

SERIAL_DRY_RUN = True # Do not use serial and print instructions to console
SERIAL_BAUDRATE = 115200
