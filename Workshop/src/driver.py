from uart import *
from threading import Thread

import struct
import time


"""
Commands arguments read timeout: 8 ms
Minimum delay between commands: 12 ms
Protocols description (for communication with the µC):

Frame format:
    | Command code (1 bytes) | Command arguments (... bytes) |

Raspberry Pi to µC commands:
    Ready status:
        Code: 'O'
        Args: [heartbeat max interval (2 bytes)]

    Ready response:
        Code: 'A'
        Args: [heartbeat max interval (2 bytes)]

    Forward:
        Code: 'F'
        Args: [speed (1 byte)]

    Backward:
        Code: 'K'
        Args: [speed (1 byte)]

    Turn left:
        Code: 'L'
        Args: [angle (1 byte)]

    Turn right:
        Code: 'R'
        Args: [angle (1 byte)]

    Stop/Freewheel:
        Code: 'S'
        Args: []

    Brake:
        Code: 'B'
        Args: []

    Heartbeat:
        Code: 'H'
        Args: []

    Get battery voltage:
        Code: 'V'
        Args: []

µC to Raspberry Pi commands:
    Ready status:
        Code: 'O'
        Args: []

    Ready response:
        Code: 'A'
        Args: []

    Battery voltate:
        Code: 'V'
        Args: [voltage (2 bytes)]

If one device receive a ready status command it must anwser with a ready response command.
"""


class SerialProtocol:
    def __init__(self, serial: SerialDevice) -> None:
        self.serial = serial
        self.cmd_args_len = {}
        self.cmd_queue = []
        self.min_cmd_interval = 12

    def register_cmd(self, cmd: int, args_len: int):
        self.cmd_args_len[cmd] = args_len

    def send_cmd(self, cmd: int, args: bytes = None) -> None:
        data = struct.pack("B", cmd)
        if args is not None:
            data += args
        self.serial.write(data)

    def recv_cmd(self) -> tuple[int, bytes]:
        while True:
            code = struct.unpack("B", self.serial.read(1))
            if code not in self.cmd_args_len:
                continue
            length = self.cmd_args_len[code]
            args = None
            if length > 0:
                args = self.serial.read(length)
            return code, args


class CarDriver:
    def __init__(self, serial: SerialDevice) -> None:
        self.serial = SerialProtocol(serial)
        self.end = False
        self.heartbeats_thr = Thread(target = self.heartbeats_loop)

        self.serial.register_cmd(ord('O'), 0)
        self.serial.register_cmd(ord('A'), 0)
        self.serial.register_cmd(ord('F'), 1)
        self.serial.register_cmd(ord('K'), 1)
        self.serial.register_cmd(ord('B'), 0)
        self.serial.register_cmd(ord('L'), 1)
        self.serial.register_cmd(ord('R'), 1)
        self.serial.register_cmd(ord('S'), 0)
        self.serial.register_cmd(ord('H'), 0)
        self.serial.register_cmd(ord('V'), 0)

    def heartbeats_loop(self) -> None:
        while not self.end:
            self.hearbeat()
            time.sleep(0.1)

    def hearbeat(self) -> None:
        self.serial.send_cmd(ord('H'))

    def connect(self, retry: int = 2) -> bool:
        self.serial.send_cmd(ord('O'))
        #cmd, args = self.serial.recv()
        #if cmd == ord('O'):
        #    self.serial.send_cmd(ord('A'))
        #elif cmd != ord('A'):
        #    return False
        self.heartbeats_thr.start()
        return True

    def get_battery(self) -> float:
        self.serial.send_cmd(ord('V'))
        cmd, args = self.serial.recv_cmd()
        if cmd == ord('V'):
            voltage = struct.unpack("H", args)
            return voltage / 1000.0
        return None

    def turn(self, angle: float):
        raw_angle = int(max(0, min(1, abs(angle))) * 0xFF)
        if angle > 0:
            self.serial.send_cmd(ord('L'), struct.pack("B", raw_angle))
        else:
            self.serial.send_cmd(ord('R'), struct.pack("B", raw_angle))

    def move(self, speed: float):
        raw_speed = int(max(0, min(1, abs(speed))) * 0xFF)
        if speed < 0:
            self.serial.send_cmd(ord('K'), struct.pack("B", raw_speed))
        else:
            self.serial.send_cmd(ord('F'), struct.pack("B", raw_speed))

    def brake(self):
        self.serial.send_cmd(ord('B'))

    def freewheel(self):
        self.serial.send_cmd(ord('S'))

    def close(self):
        self.end = True
        self.freewheel()
        self.turn(0)
        self.heartbeats_thr.join()
