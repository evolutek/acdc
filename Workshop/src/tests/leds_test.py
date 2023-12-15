import board
import neopixel
import time

NB_LEDS = 9
FPS = 30
STEPS = 3

leds = neopixel.NeoPixel(board.D12, NB_LEDS, auto_write=False)

leds.fill((0, 0, 0))

# Hue is between 0 and 1
def hue_rgb(hue):
    if hue <= 1/3:
        v = int(hue * 3 * 0xFF + 0.5)
        return (255 - v, v, 0)
    elif hue <= 2/3:
        v = int((hue - 1/3) * 3 * 0xFF + 0.5)
        return (0, 255 - v, v)
    elif hue <= 1:
        v = int((hue - 2/3) * 3 * 0xFF + 0.5)
        return (v, 0, 255 - v)
    else:
        return (255, 255, 255)

offset = 0

try:
    while True:
        for j in range(STEPS):
            x = (1 / NB_LEDS) - ((j / NB_LEDS) / STEPS)
            for i in range(NB_LEDS):
                leds[(i + offset) % NB_LEDS] = hue_rgb(i / NB_LEDS + x)
            leds.show()
            time.sleep(1 / FPS)
        offset = (offset + 1) % NB_LEDS
except KeyboardInterrupt:
    pass
