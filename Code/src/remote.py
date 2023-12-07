#!/usr/bin/env python3

from uart import *
from driver import *

import asyncio
import json
from websockets.server import serve
from websockets import ConnectionClosedOK

import socket


def get_local_ip():
    return socket.gethostbyname(socket.gethostname())


DRY_RUN = False
SERIAL_BAUDRATE = 38400


def error(*args, code = None, **kargs):
    print(*args, **kargs, file = sys.stderr, flush = True)
    if code is not None:
        exit(code)


driver = None


async def ws_server_handler(ws):
    while True:
        try:
            msg = await ws.recv()
        except ConnectionClosedOK:
            break

        try:
            data = json.loads(msg)
        except json.JSONDecodeError as e:
            error(str(e))
            continue

        op = data['op']
        if op == "b":
            driver.brake()
        elif op == "f":
            driver.freewheel()
        elif op == "m":
            move_data = data["data"]
            turn = move_data["turn"]
            speed = move_data["speed"]
            driver.turn(turn)
            driver.move(speed)
        else:
            error("Unknown operator code: " + op)


async def main():
    server = await serve(ws_server_handler, host = None, port = 8005)
    print("IP: %s" % get_local_ip())
    try:
        await server.serve_forever()
    except KeyboardInterrupt:
        pass
    #await server.close()


if __name__ == "__main__":
    if not DRY_RUN:
        serials = list_serials()
        if len(serials) == 0:
            error("No serial device found", code = 1)

        serial_device_index = 0

        if len(serials) > 1:
            print("Serial devices:")
            i = 1
            for serial in serials:
                print("{:3d} : {}".format(i, str(serial)))
                i += 1
            serial_device_index = int(input("On which serial devices do you want to communicate with the µC ?: ")) - 1

        serial = serials[serial_device_index].connect(SERIAL_BAUDRATE)

    else:
        serial = StreamSerialDevice()

    driver = CarDriver(serial)

    asyncio.run(main())
