from math import sin, pi
from threading import Thread
from time import sleep
import neopixel

class Led:
    def __init__(self, pin, led_count):
        self.pin = pin
        self.led_count = led_count
        self.strip = neopixel.NeoPixel(self.pin, self.led_count, auto_write=False)

    def color_wipe(self, color):
        for i in range(self.led_count):
            self.strip[i] = color
            wait_ms=10
            sleep(wait_ms/1000.0)

    def clear(self):
        self.color_wipe((0,0,0))

    def flash(self, brightness):
        steps = 20
        for i in range(steps):
            brightness = sin(float(i) / steps * pi)
            self.strip.brightness = brightness
            wait_ms=5
            sleep(wait_ms/1000.0)

    def start_animation(self, note, pitch):
        brightness = pitch * 2
        if note == 'snare':
            color = (brightness,brightness,brightness)
        elif note == 'kick':
            process = Thread(target=self.flash, args=(brightness,))
            process.start()
            return
        elif note == 'tom1':
            color = (brightness, 0, brightness)
            process = Thread(target=self.flash, args=(brightness,))
            process.start()
        elif note == 'tom2':
            color = (brightness // 2,0,brightness)
            process = Thread(target=self.flash, args=(brightness,))
            process.start()
        elif note == 'tom3':
            color = (0, 0, brightness)
            process = Thread(target=self.flash, args=(brightness,))
            process.start()
        else:
            color = (0,0,brightness)
        process = Thread(target=self.color_wipe, args=(color,))
        process.start()

    def animate(self):
        self.strip.show()