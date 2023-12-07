import serial
import serial.tools.list_ports
import sys
import glob
import time


class SerialDevice:
    def write(self, data: bytes) -> None:
        raise NotImplementedError("SerialDevice.write")

    def read(self, size: int) -> bytes:
        raise NotImplementedError("SerialDevice.read")


class StreamSerialDevice(SerialDevice):
    def __init__(self, file = sys.stdout, binary = False) -> None:
        self.file = file
        self.binary = binary

    def write(self, data: bytes) -> None:
        if not self.binary:
            data = data.hex() + "\r\n"
        self.file.write(data)
        self.file.flush()

    def read(self, size: int) -> bytes:
        data = self.file.read(size)
        if not self.binary:
            data = data.encode("utf8")
        return data


class HardwareSerialDeviceInfo:
    def __init__(self, device: str, name: str) -> None:
        self.device = device
        self.name = name

    def connect(self, baudrate: int):
        return HardwareSerialDevice(self, baudrate)

    def __str__(self) -> str:
        return "%s (%s)" % (self.name, self.device)


class HardwareSerialDevice(SerialDevice):
    def __init__(self, info: HardwareSerialDeviceInfo, baudrate: int) -> None:
        self.device = serial.Serial(info.device, baudrate=baudrate, stopbits=1, parity=serial.PARITY_NONE, bytesize=8)
        self.info = info
        self.baudrate = baudrate

    def write(self, data: bytes) -> None:
        for c in data:
            self.device.write(bytes([c]))
            self.device.flush()
            time.sleep(0.01)
        print(data.hex(), end='\r\n', flush=True)

    def read(self, size: int) -> bytes:
        return self.device.read(size)

    def __del__(self) -> None:
        self.device.close()


def _list_serials():
    if sys.platform.startswith('win'):
        ports = []
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise Exception('Unsupported platform')
    return ports


def get_port_name(port: str) -> str:
    pos = port.rfind('/')
    if pos == -1:
        pos = port.rfind('\\')
    if pos == -1:
        return port
    return port[pos+1:]


def list_serials() -> list[HardwareSerialDeviceInfo]:
    ports = set(_list_serials())
    devices = serial.tools.list_ports.comports()
    for device in devices:
        ports.add(device.device)
    r = []
    for port in ports:
        r.append(HardwareSerialDeviceInfo(port, get_port_name(port)))
    return r
