#!/usr/bin/env python3

from fps import *
from detection import *
from webrtc import *
from uart import *
from camera import *

import cv2 as cv
import sys
from threading import Thread


# General configurations
FPS = 24

WEBRTC_SERVER = True
OPENCV_WINDOW = False
DRY_RUN = True # Do not use serial and print instructions to console

SERIAL_BAUDRATE = 38400

SCALEDOWN_LEVEL = 0

MIN_SHAPE_AREA = 300

RED_COLOR_RANGE = ColorRange(
    (350, 100, 100), (340, 45, 40), (10, 100, 100), (0, 0, 255)
)

GREEN_COLOR_RANGE = ColorRange(
    (150, 100, 100), (120, 20, 15), (170, 100, 100), (0, 255, 0)
)


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


def find_best_splash(splashs: ColorSplashList, color: ColorRange) -> ColorSpash:
    best_splash = None
    for splash in splashs.splashs:
        if splash.color == color:
            if best_splash is None or splash.area > best_splash.area:
                best_splash = splash
    return best_splash


def float_point_to_int(point: tuple[float,float]) -> tuple[int,int]:
    return (int(point[0] + 0.5), int(point[1] + 0.5))


def processing(video_provider: VideoProvider, serial: SerialDevice) -> None:
    try:
        cap = get_best_camera(FPS)
        print("Camera stream successfuly opened (type: %s)" % cap.get_type())
    except Exception as e:
        error(str(e), code = 2)

    detector = ColorSplashDetection()
    detector.colors.append(RED_COLOR_RANGE)
    detector.colors.append(GREEN_COLOR_RANGE)
    detector.scaledown_level = SCALEDOWN_LEVEL
    detector.min_area = MIN_SHAPE_AREA

    fps_controler = FrameRateControler(FPS)

    try:
        last_fps = 0
        while not end:
            fps_controler.begin_frame()

            frame = cap.read()
            if frame is None:
                error("Failed to retreive frame")
                break

            splashs = detector.detect(frame)
            splashs.render(frame)

            best_green_splash = find_best_splash(splashs, GREEN_COLOR_RANGE)
            best_red_splash = find_best_splash(splashs, RED_COLOR_RANGE)

            if best_green_splash is not None and best_red_splash is not None:
                cv.line(
                    frame,
                    float_point_to_int(best_green_splash.centroid),
                    float_point_to_int(best_red_splash.centroid),
                    (255, 0, 0), 1
                )

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

    if not DRY_RUN:
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

    video_provider = MyVideoProvider()

    if WEBRTC_SERVER:
        webrtc_server = WebRTCServer()
        webrtc_server.set_video_provider(video_provider)

    processing_thr = Thread(target = processing, args = [video_provider, serial])
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
