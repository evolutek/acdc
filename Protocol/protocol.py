import serial
from time import sleep
from Response import Response, CmdEnum

class API:
    def __init__(self, baud_rate=115200, port="/dev/ttyAMA0"):
        self.serial = serial.Serial(port=port, baudrate=baud_rate)
        self.packet = bytearray()

    def reset(self):
        self.packet.append(CmdEnum.COMMAND_FLAG)
        self.packet.append(CmdEnum.RESET) # id command
        self.packet.append(0x00)
        self.serial.write(self.packet)
        self.packet = bytearray()

    def get_battery(self):
        self.packet.append(CmdEnum.COMMAND_FLAG)
        self.packet.append(CmdEnum.BATTERY) # id command
        self.packet.append(0x00)  # 0x00 == 0 parametre
        self.serial.write(self.packet)
        self.packet = bytearray()

    def setup(self):
        self.packet.append(CmdEnum.COMMAND_FLAG)
        self.packet.append(CmdEnum.SETUP)  # id command
        self.packet.append(0x04)  # 0x00 == 0 parametre
        self.packet.append(0x00)  # set R
        self.packet.append(0x00)  # set G
        self.packet.append(0x00)  # set B
        self.packet.append(0x46)  # set vitesse
        self.serial.write(self.packet)
        self.packet = bytearray()

    def ping(self):
        self.packet.append(CmdEnum.COMMAND_FLAG)
        self.packet.append(CmdEnum.SETUP)  # id command
        self.packet.append(0x00)  # 0x00 == 0 parametre
        self.serial.write(self.packet)
        self.packet = bytearray()

    def write(self, msg : CmdEnum, param=None) -> Response:
        response = None
        if msg == CmdEnum.RESET:
            self.reset()
            response = Response(self.serial.readline())
        elif msg == CmdEnum.SETUP:
            self.setup()
            response = Response(self.serial.readline())
        elif msg == CmdEnum.BATTERIE:
            self.get_battery()
            response = Response(self.serial.readline())
        elif msg == CmdEnum.PING:
            self.ping()
        elif msg == CmdEnum.SET_ANGLE:
            self.set_angle(param)
        return response

    def set_angle(self, param):
        self.packet.append(CmdEnum.COMMAND_FLAG)
        self.packet.append(CmdEnum.SET_ANGLE)  # id command
        self.packet.append(0x01)  # 0x00 == 0 parametre
        self.packet.append(0x00)  # set R
        self.serial.write(self.packet)
        self.packet = bytearray()

