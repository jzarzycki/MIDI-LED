from math import sin, pi
from threading import Thread
from time import time
from threading import Semaphore
import neopixel
from animations import functions

class Led:
    def __init__(self, pin, led_count, default_color=(0,0,0)):
        self.led_count = led_count
        self.default_color = self.__dim_color__(default_color)
        self.default_brightness = sin(19.0/20.0*pi)

        self.colors = [self.default_color] * led_count
        self.ledMultipliers = [1] * led_count

        self.__strip__ = neopixel.NeoPixel(pin, self.led_count, auto_write=False)
        self.__strip__.brightness = self.default_brightness
        self.__update_strip__()

        self.refresh_strip = False
        self.__semaphore__ = Semaphore()

    def setLedColor(self, index, color, dim_color=True):
        self.__semaphore__.acquire()
        self.colors[index] = self.__dim_color__(color) if dim_color else color
        self.__semaphore__.release()

    def setBrightness(self, brightness):
        self.__semaphore__.acquire()
        self.__strip__.brightness = brightness
        self.__semaphore__.release()

    def setMultiplier(self, index, value):
        self.__semaphore__.acquire()
        self.ledMultipliers[index] = value
        self.__semaphore__.release()

    def __dim_color__(self, color):
        max_val = max(color)
        return tuple([int(127/max_val*val) for val in color])

    def __update_strip__(self):
        for i, [color, multiplier] in enumerate(zip(self.colors, self.ledMultipliers)):
            self.__strip__[i] = tuple([int(multiplier * val) for val in color])

    def __update_in_background__(self):
        t = time()
        wait_ms = 16
        while self.refresh_strip:
            self.__strip__.show()
            while t > time():
                self.__update_strip__()
            t += wait_ms / 1000.0

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