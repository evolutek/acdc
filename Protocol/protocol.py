import serial
from time import sleep
from Response import Response


class API:
    def __init__(self, baud_rate=115200, port="/dev/ttySO"):
        self.serial = serial.Serial(port=port, baudrate=baud_rate)

    def write(self, msg) -> Response:
        response = Response(self.serial.readlines())
        return response

