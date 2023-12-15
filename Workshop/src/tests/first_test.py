import cv2 as cv
import numpy as np
import time

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

WINDOW_NAME = "Camera"
MAX_FPS = 30

#def hsv(h, s, v):
#    return np.array([h // 2, s * 255 // 100, v * 255 // 100], dtype="uint8")

def hsv(h, s, v):
    return (h // 2, s * 255 // 100, v * 255 // 100)

def downscale_image(frame, level):
    for _ in range(level):
        frame = cv.pyrDown(frame)
    return frame

def upscale_contours(contours, level):
    scalar = 2 ** level
    for points in contours:
        for i in range(len(points)):
            points[i][0] *= scalar
    return contours

def decimate(image, radius, threshold=254):
    #cv.medianBlur(image, radius, image)
    cv.stackBlur(image, (radius, radius), image)
    #cv.GaussianBlur(image, (radius, radius), 0, image)
    cv.threshold(image, threshold, 255, cv.THRESH_BINARY, image)

SCALE_LEVEL = 0

COLORS_BOUNDS = [
    (
        (340, 40, 35), (-10, 100, 100),
        (330, 20, 20), (-30, 100, 100),
        (2, 2, 3), (2, 2, 3),
        (350, 100, 100)
    ),
    (
        (120, 40, 25), (170, 100, 100),
        (120, 16, 16), (180, 100, 100),
        (1, 2, 3), (1, 2, 3),
        (165, 100, 100)
    )
]

def my_inrange(image, lo, up):
    if up[0] < 0:
        lower = cv.inRange(image, (0, lo[1], lo[2]), (-up[0], up[1], up[2]))
        upper = cv.inRange(image, (lo[0], lo[1], lo[2]), (180, up[1], up[2]))
        return cv.bitwise_or(lower, upper)
    return cv.inRange(image, lo, up)

# Input must be in hsv
def find_shape_of_color(input, hsv):
    hsvdist = np.absolute(input - hsv)
    hdist = hsvdist[:,:,0].astype(np.uint8)
    sdist = hsvdist[:,:,1].astype(np.uint8)
    vdist = hsvdist[:,:,2].astype(np.uint8)
    hmask = cv.inRange(hdist, 0, 20)
    _, smask = cv.threshold(sdist, 25, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    _, vmask = cv.threshold(vdist, 25, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    return cv.bitwise_and(hmask, cv.bitwise_and(smask, vmask))

def process_frame_v1(input):
    frame = downscale_image(input, SCALE_LEVEL)
    scaled = frame
    frame = cv.stackBlur(frame, (5, 5))
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    red = find_shape_of_color(frame, hsv(*COLORS_BOUNDS[0][6]))
    green = find_shape_of_color(frame, hsv(*COLORS_BOUNDS[1][6]))

    """
    red = my_inrange(
        frame,
        hsv(*COLORS_BOUNDS[0][0]),
        hsv(*COLORS_BOUNDS[0][1])
    )

    green = my_inrange(
        frame,
        hsv(*COLORS_BOUNDS[1][0]),
        hsv(*COLORS_BOUNDS[1][1])
    )
    """

    #red_contours, _ = cv.findContours(red, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #green_contours, _ = cv.findContours(green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #result = cv.drawContours(input, upscale_contours(red_contours, SCALE_LEVEL), -1, (0, 0, 255), 1)
    #result = cv.drawContours(result, upscale_contours(green_contours, SCALE_LEVEL), -1, (0, 255, 0), 1)

    mask = cv.bitwise_or(red, green)
    decimate(mask, 9, 190)

    _, _, stats, centroids = cv.connectedComponentsWithStats(mask, connectivity=4)
    for i in range(1, len(stats)):
        stat = stats[i]
        if stat[cv.CC_STAT_AREA] > 1000:
            x1 = stat[cv.CC_STAT_LEFT]
            y1 = stat[cv.CC_STAT_TOP]
            x2 = x1 + stat[cv.CC_STAT_WIDTH]
            y2 = y1 + stat[cv.CC_STAT_HEIGHT]
            cv.rectangle(scaled, (x1, y1), (x2, y2), (255, 0, 0), 1)
            cx = int(centroids[i][0] + 0.5)
            cy = int(centroids[i][0] + 0.5)
            cv.circle(scaled, (cx, cy), 2, (0, 255, 0), -1)

    return scaled

def get_center(contour):
    cx, cy = 0, 0
    for pt in contour:
        cx += pt[0]
        cy += pt[1]
    cx //= len(contour)
    cy //= len(contour)
    return cx, cy

def process_frame_v2(input):
    frame = downscale_image(input, SCALE_LEVEL)
    #frame = cv.fastNlMeansDenoisingColored(frame, None, 6, 10)
    #frame = cv.equalizeHist(frame)
    #frame = cv.stackBlur(frame, (3, 3))
    #frame = cv.GaussianBlur(frame, (3, 3), 0)
    #frame = frame.astype(np.uint32, casting='safe')
    #frame = cv.cvtColor(frame, cv.CV_32SC1)
    #frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    c = 0

    restrictive_mask = my_inrange(
        frame,
        hsv(*COLORS_BOUNDS[c][0]),
        hsv(*COLORS_BOUNDS[c][1])
    )

    mild_mask = my_inrange(
        frame,
        hsv(*COLORS_BOUNDS[c][2]),
        hsv(*COLORS_BOUNDS[c][3])
    )
    cv.bitwise_or(restrictive_mask, mild_mask, mild_mask)

    decimate(restrictive_mask, 3)
    decimate(mild_mask, 9)

    mask = np.zeros([frame.shape[0]+2, frame.shape[1]+2], dtype=np.uint8)

    mask[1:-1,1:-1] = mild_mask
    cv.bitwise_not(mask, mask)
    np.clip(mask, 0, 1, mask)

    for y in range(0, frame.shape[0]):
        for x in range(0, frame.shape[1]):
            if mask[y+1,x+1] == 0 and restrictive_mask[y,x] != 0:
                _,   _, mask, _ = cv.floodFill(
                    frame,
                    mask,
                    (x, y),
                    None,
                    hsv(*COLORS_BOUNDS[c][4]), hsv(*COLORS_BOUNDS[c][5]),
                    4 | (255 << 8) | cv.FLOODFILL_MASK_ONLY
                )

    decimate(mask, 11, 200)
    return mask

process_frame = process_frame_v1

measure_start_time = time.time()
frame_start_time = measure_start_time
correction_delta_time = 0
frames = 0
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame. Exiting.")
        break

    # Our operations on the frame come here
    frame = process_frame(frame)

    # Display the resulting frame
    cv.imshow(WINDOW_NAME, frame)

    frame_end_time = time.time()
    frame_delta_time = frame_end_time - frame_start_time
    frame_start_time = frame_end_time
    frames += 1

    measure_delta_time = frame_end_time - measure_start_time
    if measure_delta_time >= 1:
        print("FPS: %i" % (frames / measure_delta_time + 0.5))
        measure_start_time = frame_end_time
        frames = 0

    correction_time = max(1, int(max(0, 1 / MAX_FPS - frame_delta_time + correction_delta_time) * 1000))

    if cv.waitKey(correction_time) == ord('q'):
        break

    if cv.getWindowProperty(WINDOW_NAME, cv.WND_PROP_VISIBLE) < 1:
        break

    correction_end_time = time.time()
    correction_delta_time = correction_time / 1000 - (correction_end_time - frame_end_time)
    frame_start_time = correction_end_time

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
