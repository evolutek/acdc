import numpy as np
import time


SUPPORT_RPI_CAMERA = True
SUPPORT_CV_CAMERA = True


if SUPPORT_CV_CAMERA:
    import cv2 as cv

if SUPPORT_RPI_CAMERA:
    try:
        from picamera2 import Picamera2
    except ImportError:
        print("Can't found picamera2 library")
        SUPPORT_RPI_CAMERA = False


class Camera:
    def read(self) -> np.ndarray:
        raise NotImplementedError("Camera.read")

    def close(self) -> None:
        raise NotImplementedError("Camera.close")

    def get_type(self) -> str:
        raise NotImplementedError("Camera.get_type")


class CvCamera(Camera):
    def __init__(self, framerate: int, resolution: tuple[int,int] = None) -> None:
        if not SUPPORT_CV_CAMERA:
            raise Exception("OpenCV camera not supported")

        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Cannot open camera")

        self.cap.set(cv.CAP_PROP_FPS, framerate)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])

        time.sleep(1)

        ret, _ = self.cap.read()
        if not ret:
            raise Exception("Failed to retreive first frame: %i" % ret)

    def read(self) -> np.ndarray:
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def close(self) -> None:
        self.cap.release()

    def get_type(self) -> str:
        return "CvCamera"


class RpiCamera(Camera):
    def __init__(self, framerate, resolution = (640, 480)) -> None:
        if not SUPPORT_RPI_CAMERA:
            raise Exception("Rpi camera not supported")
        self.framerate = framerate
        self.cap = Picamera2()
        self.cap.configure(self.cap.create_preview_configuration(main={"format": 'RGB888', "size": resolution}))
        self.cap.start()
        time.sleep(1)

    def read(self) -> np.ndarray:
        return self.cap.capture_array()

    def close(self) -> None:
        self.cap.close()

    def get_type(self) -> str:
        return "RpiCamera"


def get_best_camera(framerate: int, resolution: tuple[int,int] = (640, 480)) -> Camera:
    if SUPPORT_RPI_CAMERA:
        return RpiCamera(framerate, resolution)
    if SUPPORT_CV_CAMERA:
        return CvCamera(framerate, resolution)
    return None
