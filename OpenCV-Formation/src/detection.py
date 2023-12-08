import time

def detect(input, output):
    while True:
        # Read frame from camera
        frame = input.read()

        # Write frame on output
        if output.write(frame):
            return # You should exit when it return true
