import cv2 as cv
import numpy as np


# Convert a hsv common hsv format to the opencv hsv format
def opencv_hsv(h, s, v):
    return (h // 2, s * 255 // 100, v * 255 // 100)


# Downscale an image by a factor of 2^level
# (make a copy even if level is 0)
def downscale(frame, level):
    for _ in range(level):
        frame = cv.pyrDown(frame)
    if level == 0:
        frame = frame.copy()
    return frame


# Fast method to blur an image
def fast_blur(image, radius):
    try:
        cv.stackBlur(image, (radius, radius), image)
    except AttributeError:
        cv.GaussianBlur(image, (radius, radius), 0, image)


# Decimate a binary image (i.e. reduce level of details by removing too small white or black areas)
def decimate(image, radius, threshold=254):
    fast_blur(image, radius)
    cv.threshold(image, threshold, 255, cv.THRESH_BINARY, image)


# Generate a mask image by filtering all pixel with a color inside the specified range
# (this function take in account the modulus range for the hue value)
def hsv_inrange(image, lo, up):
    if up[0] < lo[0]:
        lower = cv.inRange(image, (0, lo[1], lo[2]), (up[0], up[1], up[2]))
        upper = cv.inRange(image, (lo[0], lo[1], lo[2]), (180, up[1], up[2]))
        cv.bitwise_or(lower, upper, lower)
        return lower
    return cv.inRange(image, lo, up)


class ColorRange:
    def __init__(self, color, min, max, render) -> None:
        self.min: tuple[int,int,int] = min
        self.max: tuple[int,int,int] = max
        self.color: tuple[int,int,int] = color
        self.render: tuple[int,int,int] = render


class ColorSpash:
    def __init__(self, centroid, box, area, color) -> None:
        self.centroid: tuple[float,float] = centroid
        self.box: tuple[int,int,int,int] = box
        self.area: int = area
        self.color: ColorRange = color

    def render(self, input: np.ndarray) -> None:
        cv.rectangle(input, self.box[:2], self.box[2:], self.color.render, 1)
        cv.circle(input, (int(self.centroid[0] + 0.5), int(self.centroid[1] + 0.5)), 2, self.color.render, -1)


class ColorSplashList:
    def __init__(self) -> None:
        self.splashs: list[ColorSpash] = []

    def add(self, splash: ColorSpash) -> None:
        self.splashs.append(splash)

    def render(self, input: np.ndarray) -> None:
        for splash in self.splashs:
            splash.render(input)


class ColorSplashDetection:
    def __init__(self) -> None:
        self.scaledown_level: int = 0
        self.colors: list[ColorRange] = []
        self.min_area = 1000
        self.remove_nested_splashs = True

    def detect(self, input: np.ndarray) -> ColorSplashList:
        frame = downscale(input, self.scaledown_level)
        fast_blur(frame, 5)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        splashs = ColorSplashList()
        scaleup_factor = 2**self.scaledown_level

        for color in self.colors:
            mask = hsv_inrange(
                frame,
                opencv_hsv(*color.min),
                opencv_hsv(*color.max)
            )
            decimate(mask, 9, 190)

            _, _, stats, centroids = cv.connectedComponentsWithStats(mask, connectivity=4)
            for i in range(1, len(stats)):
                stat = stats[i]
                area = stat[cv.CC_STAT_AREA] * (scaleup_factor**2)
                if area > self.min_area:
                    x1 = stat[cv.CC_STAT_LEFT] * scaleup_factor
                    y1 = stat[cv.CC_STAT_TOP] * scaleup_factor
                    x2 = x1 + stat[cv.CC_STAT_WIDTH] * scaleup_factor
                    y2 = y1 + stat[cv.CC_STAT_HEIGHT] * scaleup_factor
                    cx = centroids[i][0] * scaleup_factor
                    cy = centroids[i][1] * scaleup_factor
                    splash = ColorSpash((cx, cy), (x1, y1, x2, y2), area, color)
                    splashs.add(splash)

        return splashs
