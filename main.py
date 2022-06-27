import struct

from Protocol.protocol import API, CmdEnum
from inputs import devices
from inputs import get_gamepad
from inputs import UnknownEventCode
from time import sleep

class Agent():
    def __init__(self):
        self.protocol = API()
        self.setup()

    def setup(self):
        response = self.protocol.write(CmdEnum.SETUP)

        try:
            print(f"[+] START OF INITIALIZATION")
            response.data = struct.unpack("b", response)
            gamepad = devices.gamepads[0]
            print(f"[+] END OF INITIALIZATION")
        except:
            print("No gamepad detected")
            exit(84)

    def btn_turn(self, value: int):
        # print(f"Turning {value}")
        if value > 0:
            print(f"[+] I MOVE RIGHT")
            self.protocol.write(CmdEnum.SET_ANGLE, CmdEnum.RIGHT)
        if value < 0:
            print(f"[+] I MOVE LEFT")
            self.protocol.write(CmdEnum.SET_ANGLE, CmdEnum.LEFT)
        if value == 0:
            print(f"[+] I MOVE CENTER")
            self.protocol.write(CmdEnum.SET_ANGLE, CmdEnum.CENTER)

    def btn_accelerate(self, value: int):
        print(f"Accelerating {value}")
        # TODO : Set motor to value

    def btn_mode(self, event):
        print("Exiting Program ...")
        exit(0)

    def ping_cars(self, state):
        print("I'M ALIVE")
        self.protocol.write(CmdEnum.PING)

    def analyse_input(self, event):
        func = {"BTN_MODE": self.btn_mode}
        #"ABS_HAT0Y": self.btn_accelerate}

        if event.code in func and event.state == 1:  # Exit the program if the HOME button is pressed
            func[event.code](event.state)
        if event.code == "ABS_HAT0X":
            self.btn_turn(event.state)
        if event.code == "ABS_RZ":
            self.ping_cars(event.state)

        elif event.ev_type != "Sync":  # Just to avoid the print of delimiter events
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

    def run(self):
        while True:
            try:
                # Get all the gamepad events
                events = get_gamepad()
            except UnknownEventCode:  # If the get_gamepad() func returns an error (wich he will), this prevents a useless crash
                events = []
            for event in events:
                self.analyse_input(event)

agent = Agent()
agent.run()