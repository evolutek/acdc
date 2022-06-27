from enum import IntEnum

class CMD(IntEnum):
    COMMAND_FLAG = 0x42

    # list command
    RESET = 0x00,
    SETUP = 0x01,
    PING = 0x02,
    BATTERY = 0x07,


class Response:
    def __init__(self, data):
        self.data = data
