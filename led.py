import time
from neopixel import *
import multiprocessing as mp

LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_INVERT     = False
LED_BRIGHTNESS = 255
LED_CHANNEL    = 0

class Led:
    def __init__(self, pin, led_count):
        self.led_count = led_count
        self.pin = pin
        self.strip = Adafruit_NeoPixel(led_count, pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.output = mp.Queue()

    def colorWipe(self, color):
        for i in range(self.led_count):
            self.strip.setPixelColor(i, color)
        self.strip.show()
            # wait_ms=10
            # time.sleep(wait_ms/1000.0)

    def colorWipeMulti(self, strip_len, color, output):
        for i in range(strip_len):
            output.put((i,color))
            wait_ms=20
            time.sleep(wait_ms/1000.0)

    def clear(self):
        self.colorWipe(Color(0,0,0))

    def startAnimation(self, note, pitch):
        brightness = pitch * 2
        if note == 'snare':
            color = Color(brightness,brightness,brightness)
        elif note == 'kick':
            color = Color(0,brightness,0)
        elif note == 'hi-hat closed':
            color = Color(0,0,brightness)
        else:
            color = Color(brightness,0,0)
        process = mp.Process(target=self.colorWipeMulti, args=(self.led_count, color, self.output))
        process.start()

    def animate(self):
        if self.output.qsize():
            while self.output.qsize():
                i, color = self.output.get()
                self.strip.setPixelColor(i, color)
            self.strip.show()