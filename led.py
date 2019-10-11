import time
import neopixel
import threading
from math import sin, pi

class Led:
    def __init__(self, pin, led_count):
        self.led_count = led_count
        self.pin = pin
        self.strip = neopixel.NeoPixel(self.pin, self.led_count, auto_write=False)

    def colorWipe(self, color):
        for i in range(self.led_count):
            self.strip[i] = color
            wait_ms=10
            time.sleep(wait_ms/1000.0)

    def clear(self):
        self.colorWipe((0,0,0))

    def flash(self, brightness):
        steps = 20
        for i in range(steps):
            brightness = sin(float(i) / steps * pi)
            self.strip.brightness = brightness
            wait_ms=5
            time.sleep(wait_ms/1000.0)


    def startAnimation(self, note, pitch):
        # color is in GRB format
        brightness = pitch * 2
        if note == 'snare':
            color = (brightness,brightness,brightness)
        elif note == 'kick':
            process = threading.Thread(target=self.flash, args=(brightness,))
            process.start()
            return
        elif note == 'tom1':
            color = (brightness, 0, brightness)
            process = threading.Thread(target=self.flash, args=(brightness,))
            process.start()
        elif note == 'tom2':
            color = (brightness // 2,0,brightness)
            process = threading.Thread(target=self.flash, args=(brightness,))
            process.start()
        elif note == 'tom3':
            color = (0, 0, brightness)
            process = threading.Thread(target=self.flash, args=(brightness,))
            process.start()
        else:
            color = (0,0,brightness)
        process = threading.Thread(target=self.colorWipe, args=(color,))
        process.start()

    def animate(self):
        self.strip.show()