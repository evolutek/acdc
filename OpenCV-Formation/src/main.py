#!/usr/bin/env python3

from camera import *
from detection import detect

import cv2 as cv

import sys
from threading import Thread
import traceback


# General configurations
FPS = 24
RESOLUTION = (640, 480)

OPENCV_WINDOW = True


def error(*args, code = None, **kargs):
    print(*args, **kargs, file = sys.stderr, flush = True)
    if code is not None:
        exit(code)


class MyVideoProvider():
    def init(self):
        self.frame = None

    def write(self, frame) -> bool:
        self.frame = frame

        if OPENCV_WINDOW:
            cv.imshow("Camera", frame)

        wait = 0.5 / FPS
        if OPENCV_WINDOW:
            if cv.waitKey(int(1000 * wait)) == ord('q'):
                return True
            if cv.getWindowProperty("Camera", cv.WND_PROP_VISIBLE) < 1:
                return True
        else:
            time.sleep(wait)

        return False

    def read(self):
        return self.frame


end = False


def main():
    global end
    end = False

    video_provider = MyVideoProvider()

    try:
        capture = get_best_camera(FPS, RESOLUTION)
        print("Camera stream successfuly opened (type: %s)" % capture.get_type())
    except Exception as e:
        error(str(e), code = 2)

    try:
        detect(capture, video_provider)
    except KeyboardInterrupt:
        print("Interrupted with Ctrl-C, exiting cleanly ...")
    except Exception:
        traceback.print_exc()

    capture.close()

    end = True


if __name__ == "__main__":
    main()
