import time
from neopixel import *
import threading
from math import sin, pi

LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_INVERT     = False
LED_BRIGHTNESS = 10
LED_CHANNEL    = 0

class Led:
    def __init__(self, pin, led_count):
        self.led_count = led_count
        self.pin = pin
        self.strip = Adafruit_NeoPixel(led_count, pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

    def colorWipe(self, color):
        for i in range(self.led_count):
            self.strip.setPixelColor(i, color)
            wait_ms=10
            time.sleep(wait_ms/1000.0)

    def clear(self):
        self.colorWipe(Color(0,0,0))

    def flash(self, brightness):
        steps = 20
        for i in range(steps):
            var = sin(float(i) / steps * pi)
            brightness = int(255 * var)
            self.strip.setBrightness(brightness)
            wait_ms=5
            time.sleep(wait_ms/1000.0)


    def startAnimation(self, note, pitch):
        # color is in GRB format
        brightness = pitch * 2
        if note == 'snare':
            color = Color(brightness,brightness,brightness)
        elif note == 'kick':
            process = threading.Thread(target=self.flash, args=(brightness,))
            process.start()
            return
        elif note == 'tom1':
            color = Color(brightness,0,brightness)
        elif note == 'tom2':
            color = Color(brightness/2,0,brightness)
        elif note == 'tom3':
            color = Color(0,0,brightness)
        else:
            color = Color(0,0,brightness)
        process = threading.Thread(target=self.colorWipe, args=(color,))
        process.start()

    def animate(self):
        self.strip.show()