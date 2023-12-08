#!/usr/bin/env python3

from webrtc import *
from camera import *
from detection import detect

import cv2 as cv
import sys
from threading import Thread
import asyncio
import traceback


# General configurations
FPS = 24
RESOLUTION = (640, 480)

WEBRTC_SERVER = True
OPENCV_WINDOW = False


def error(*args, code = None, **kargs):
    print(*args, **kargs, file = sys.stderr, flush = True)
    if code is not None:
        exit(code)


class MyVideoProvider(VideoProvider):
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


def webrtc_thr_func(video_provider: VideoProvider, stop_event: list[asyncio.Event]):
    webrtc_server = WebRTCServer()
    webrtc_server.set_video_provider(video_provider)
    webrtc_server.run(None)


def main():
    global end
    end = False
    stop_event = [None]

    video_provider = MyVideoProvider()

    if WEBRTC_SERVER:
        webrtc_thr = Thread(target = webrtc_thr_func, args = [video_provider, stop_event])
        webrtc_thr.start()

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

    if WEBRTC_SERVER:
        if stop_event[0] is not None:
            stop_event[0].set()
        webrtc_thr.join()


if __name__ == "__main__":
    main()
