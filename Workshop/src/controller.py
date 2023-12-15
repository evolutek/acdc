from detection import *
from utils import MemoryVideoProvider
from uart import SerialDevice


SCALEDOWN_LEVEL = 0

MIN_SHAPE_AREA = 300

RED_COLOR_RANGE = ColorRange(
    (350, 100, 100), (345, 45, 40), (10, 100, 100), (0, 0, 255)
)

GREEN_COLOR_RANGE = ColorRange(
    (150, 100, 100), (120, 20, 10), (170, 100, 100), (0, 255, 0)
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


def setup(input_video: MemoryVideoProvider, output_video: MemoryVideoProvider, serial: SerialDevice):
    pass # Ecrivez ici le code d'initialization (executer une unique fois au début)


def loop(input_video: MemoryVideoProvider, output_video: MemoryVideoProvider, serial: SerialDevice):
    # Le code ici est exécuté en boucle

    frame = input_video.read()
    if frame is None:
        return True

    splashs = detector.detect(frame)
    splashs.render(frame)

    # Chaque splash represente une "tache" de couleur détecter sur l'écran

    for splash in splashs.splashs:
        # splash.area : Nombre de pixel dans la tache
        # splash.centroid : Un tuple (x, y) qui est les coordonée du centre de la tache
        # splash.box : Un tuple (left, top, right, bottom) qui est la boite qui encadre la tache
        # splash.color : Qui est à soit RED_COLOR_RANGE ou à GREEN_COLOR_RANGE
        pass

    output_video.write(frame)

    return False
