from detection import *
from utils import MemoryVideoProvider
from uart import SerialDevice


SCALEDOWN_LEVEL = 0

MIN_SHAPE_AREA = 300

RED_COLOR_RANGE = ColorRange(
    (350, 100, 100), (340, 45, 40), (10, 100, 100), (0, 0, 255)
)

GREEN_COLOR_RANGE = ColorRange(
    (150, 100, 100), (120, 20, 15), (170, 100, 100), (0, 255, 0)
)


detector = ColorSplashDetection()
detector.colors.append(RED_COLOR_RANGE)
detector.colors.append(GREEN_COLOR_RANGE)
detector.scaledown_level = SCALEDOWN_LEVEL
detector.min_area = MIN_SHAPE_AREA


def find_best_splash(splashs: ColorSplashList, color: ColorRange) -> ColorSpash:
    best_splash = None
    for splash in splashs.splashs:
        if splash.color == color:
            if best_splash is None or splash.area > best_splash.area:
                best_splash = splash
    return best_splash


def float_point_to_int(point: tuple[float,float]) -> tuple[int,int]:
    return (int(point[0] + 0.5), int(point[1] + 0.5))


from driver import CarDriver

driver = None


def setup(input_video: MemoryVideoProvider, output_video: MemoryVideoProvider, serial: SerialDevice):
    pass


def loop(input_video: MemoryVideoProvider, output_video: MemoryVideoProvider, serial: SerialDevice):
    global driver
    if driver is None:
        driver = CarDriver(serial)

    frame = input_video.read()
    if frame is None:
        return True

    width = frame.shape[1]

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

        middle_x = (best_green_splash.centroid[0] + best_red_splash.centroid[0]) / 2

        if middle_x < width * 0.35:
            driver.turn(-1)
        elif middle_x > width * 0.65:
            driver.turn(1)
        else:
            driver.turn(0)

        driver.move(0.5)

    else:
        driver.brake()


    output_video.write(frame)

    return False
