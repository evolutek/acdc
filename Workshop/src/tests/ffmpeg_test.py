#from image import *
from fps import *

import cv2 as cv
import subprocess as sp
import sys
from threading import Thread


FPS = 10
FFMPEG_PATH = 'ffmpeg'


def print_stderr(proc):
    for line in proc.stderr:
        print(line.decode(errors="ignore"), end='', file=sys.stderr)

def print_stdout(proc):
    for line in proc.stdout:
        print(line.decode(errors="ignore"), end='')


def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit(2)
    print("Camera stream successfuly opened")
    ret, frame = cap.read()
    if not ret:
        print("Failed to retreive first frame: %i" % ret)
        exit(2)
    height, width, channels = frame.shape

    dimension = '{}x{}'.format(width, height)
    #fps = str(cap.get(cv.CAP_PROP_FPS))

    command = [
        FFMPEG_PATH,
        '-y',
        '-f', 'rawvideo',
        '-video_size', dimension,
        '-pixel_format', 'bgr24',
        '-framerate', str(FPS),
        '-i', '-',
        '-preset', 'ultrafast',
        '-c:v', 'libx264',
        '-f', 'mpegts',
        '-tune', 'zerolatency',
        '-b:v', '800k',
        'udp://10.10.42.102:5000?pkt_size=1316'
    ]

    proc = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE)

    stderr_thread = Thread(target = print_stderr, args=[proc])
    stdout_thread = Thread(target = print_stdout, args=[proc])

    stderr_thread.start()
    stdout_thread.start()

    fps_controler = FrameRateControler(FPS)

    last_fps = 0
    while True:
        fps_controler.begin_frame()

        ret, frame = cap.read()
        if not ret:
            print("Failed to retreive frame")
            break

        proc.stdin.write(frame.tobytes())

        cv.imshow('Camera', frame)

        fps = fps_controler.get_fps()
        if fps != last_fps:
            last_fps = fps
            print("FPS: %i" % int(fps + 0.5))

        wait = fps_controler.get_time_to_wait()

        if cv.waitKey(max(3, wait)) == ord('q'):
            break

        if cv.getWindowProperty("Camera", cv.WND_PROP_VISIBLE) < 1:
            break

        fps_controler.end_frame()

    cap.release()

    print(proc.stderr.read().decode(errors="ignore"))
    print(proc.stdout.read().decode(errors="ignore"))

    proc.stdin.close()
    proc.stderr.close()
    proc.stdout.close()
    proc.wait()


if __name__ == "__main__":
    main()
