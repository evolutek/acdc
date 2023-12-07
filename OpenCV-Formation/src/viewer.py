#!/usr/bin/env python3

from fps import *
from webrtc import *
from camera import *

import cv2 as cv
import sys
from threading import Thread


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

    def set_frame(self, frame):
        self.frame = frame

    def read(self):
        return self.frame


end = False


def processing(video_provider: VideoProvider) -> None:
    try:
        cap = get_best_camera(FPS, RESOLUTION)
        print("Camera stream successfuly opened (type: %s)" % cap.get_type())
    except Exception as e:
        error(str(e), code = 2)

    fps_controler = FrameRateControler(FPS)

    try:
        last_fps = 0
        while not end:
            fps_controler.begin_frame()

            frame = cap.read()
            if frame is None:
                error("Failed to retreive frame")
                break

            video_provider.set_frame(frame)

            if OPENCV_WINDOW:
                cv.imshow("Camera", frame)

            fps = fps_controler.get_fps()
            if fps != last_fps:
                last_fps = fps
                print("FPS: %i" % int(fps + 0.5))

            wait = fps_controler.get_time_to_wait()

            if OPENCV_WINDOW:
                if cv.waitKey(max(2, int(wait * 1000))) == ord('q'):
                    break
                #if cv.getWindowProperty("Camera", cv.WND_PROP_VISIBLE) < 1:
                #    break
            else:
                time.sleep(wait)

            fps_controler.end_frame()
    except KeyboardInterrupt:
        pass

    cap.close()


def main():
    global end
    end = False

    video_provider = MyVideoProvider()

    if WEBRTC_SERVER:
        webrtc_server = WebRTCServer()
        webrtc_server.set_video_provider(video_provider)

    processing_thr = Thread(target = processing, args = [video_provider])
    processing_thr.start()

    if WEBRTC_SERVER:
        webrtc_server.run()
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    end = True
    processing_thr.join()


if __name__ == "__main__":
    main()
