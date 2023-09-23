from enum import IntEnum


class CmdEnum(IntEnum):
    COMMAND_FLAG = 0x42
    NONE = -42

    # list command
    RESET = 0x00,
    SETUP = 0x01,
    PING = 0x02,
    SET_ACC = 0x03,
    SET_ANGLE = 0x04,
    BATTERY = 0x07,

    # all ANGLE
    CENTER = 0x00
    LEFT = 0x01
    RIGHT = 0x02




class Response:
    def __init__(self, data):
        self.data = data
        self.type_of_command: CmdEnum = CmdEnum.NONE

