#!/usr/bin/env python3

print("Begin imports ...")

from fps import *
from webrtc import *
from uart import *
from camera import *
from utils import *
from config import *
from controller import loop, setup

import cv2 as cv
import sys
from threading import Thread
import asyncio

print("Import finish")


def error(*args, code = None, **kargs):
    print(*args, **kargs, file = sys.stderr, flush = True)
    if code is not None:
        exit(code)


def webrtc_thr_func(video_provider: VideoProvider, stop_event: list[asyncio.Event]):
    print("Starting WebRTC server ...")
    webrtc_server = WebRTCServer()
    webrtc_server.set_video_provider(video_provider)
    webrtc_server.run(stop_event)


def main():
    if not SERIAL_DRY_RUN:
        print("Begin serials ports listing ...")
        serials = list_serials()
        if len(serials) == 0:
            error("No serial device found", code = 1)

        i = 1
        for serial in serials:
            print("{:3d} : {}".format(i, str(serial)))
            i += 1

        serial_device_index = int(input("On which serial devices do you want to communicate with the µC ?: ")) - 1
        serial = serials[serial_device_index].connect(SERIAL_BAUDRATE)

    else:
        serial = StreamSerialDevice()

    video_input  = MemoryVideoProvider()
    video_output = MemoryVideoProvider()

    webrtc_thr = None
    stop_event = [False]
    if WEBRTC_SERVER:
        webrtc_thr = Thread(target = webrtc_thr_func, args = [video_output, stop_event])
        webrtc_thr.start()

    try:
        print("Begin camera connection ...")
        cap = get_best_camera(FPS)
        print("Camera stream opened (type: %s)" % cap.get_type())
    except Exception as e:
        error(str(e), code = 2)

    try:
        fps_controler = FrameRateControler(FPS)
        frame_counter = 0

        setup(video_input, video_output, serial)

        while True:
            fps_controler.begin_frame()

            video_input.write(cap.read())

            if loop(video_input, video_output, serial):
                break

            if OPENCV_WINDOW:
                cv.imshow("Camera", video_output.read())

            frame_counter += 1
            if frame_counter >= FPS:
                print("FPS: %i" % int(fps_controler.get_fps() + 0.5))
                frame_counter = 0

            wait = fps_controler.get_time_to_wait()

            if OPENCV_WINDOW:
                if cv.waitKey(max(2, int(wait * 1000))) == ord('q'):
                    break
                if cv.getWindowProperty("Camera", cv.WND_PROP_VISIBLE) < 1:
                    break
            else:
                time.sleep(wait)

            fps_controler.end_frame()

    except KeyboardInterrupt:
        pass

    cap.close()

    if webrtc_thr is not None:
        stop_event[0] = True
        webrtc_thr.join()


if __name__ == "__main__":
    main()
