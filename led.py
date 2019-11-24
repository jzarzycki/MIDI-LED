from math import sin, pi
from threading import Thread
from time import sleep
import neopixel
from animations import functions

class Led:
    def __init__(self, pin, led_count, default_color=(0,0,0)):
        self.pin = pin
        self.led_count = led_count
        self.strip = neopixel.NeoPixel(self.pin, self.led_count, auto_write=False)
        self.default_color = default_color
        self.clear()
        self.default_brightness = sin(19.0/20.0*pi)
        self.strip.brightness = self.default_brightness
        self.refresh_strip = False

    def clear(self):
        for i in range(len(self.strip)):
            self.strip[i] = self.default_color

    def __update_in_background__(self):
        while self.refresh_strip:
            self.strip.show()
            sleep(0.01)

    def show_animations(self):
        self.refresh_strip = True
        Thread(target=self.__update_in_background__, args=()).start()

    def handle_input(self, note_info, settings):
        note, strength = note_info
        if note in settings.keys():
            setting = settings[note]
            for animation_name, arg in setting.items():
                animation = functions[animation_name]
                args = (self, strength) + arg
                Thread(target=animation, args=args).start()