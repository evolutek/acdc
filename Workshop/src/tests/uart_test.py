from uart import *


SERIAL_BAUDRATE = 9600


def error(*args, code = None, **kargs):
    print(*args, **kargs, file = sys.stderr, flush = True)
    if code is not None:
        exit(code)


serials = list_serials()
if len(serials) == 0:
    error("No serial device found", code = 1)

i = 1
for serial in serials:
    print("{:3d} : {}".format(i, str(serial)))
    i += 1

serial_device_index = int(input("On which serial devices do you want to communicate with the µC ?: ")) - 1
serial = serials[serial_device_index].connect(SERIAL_BAUDRATE)

print("Serial connected")

while True:
    msg = serial.read(4096).decode(errors="ignore")
    print(msg)
