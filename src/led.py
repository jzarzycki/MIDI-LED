from math import sin, pi
from threading import Thread
from time import time
from threading import Semaphore
import neopixel
from src.animations import functions

class Led:
    def __init__(self, pin, led_count, default_color=(0,0,0)):
        self.led_count = led_count

        self.color_cycle = [(255,255,0),(255,0,255),(0,255,255),(255,255,255)]
        self.current_index = 0
        self.default_color = self.__dim_color__(default_color)

        self.color_cycle_anim = [(0,255,255),(255,255,255),(255,255,0), (255,0,255)]
        self.current_index_anim = 0
        self.default_color_anim = self.__dim_color__(self.color_cycle_anim[0])

        self.default_brightness = sin(19.0/20.0*pi)

        self.colors = [self.default_color] * led_count
        self.ledMultipliers = [0] * led_count

        self.__strip__ = neopixel.NeoPixel(pin, self.led_count, auto_write=False)
        self.__strip__.brightness = self.default_brightness
        self.__update_strip__()

        self.__refresh_strip__ = False
        self.__color_semaphore__ = Semaphore()
        self.__brightness_semaphore__ = Semaphore()
        self.__multiplier_semaphore__ = Semaphore()

    def __del__(self):
        self.__refresh_strip__ = False

    def setLedColor(self, index, color, dim_color=True):
        self.__color_semaphore__.acquire()

        if  type(index) == list:
            for i, c in zip(index, color):
                val = self.__dim_color__(c) if dim_color else c
                self.colors[i] = val
                self.__update_strip__(i)
        else:
            val = self.__dim_color__(color) if dim_color else color
            self.colors[index] = val
            self.__update_strip__(index)

        self.__color_semaphore__.release()

    def setBrightness(self, brightness):
        self.__brightness_semaphore__.acquire()
        self.__strip__.brightness = brightness
        self.__brightness_semaphore__.release()

    def setMultiplier(self, index, multipier):
        self.__multiplier_semaphore__.acquire()

        if  type(index) == list:
            for i in index:
                self.ledMultipliers[i] = multipier
                self.__update_strip__(i)
        else:
            self.ledMultipliers[index] = multipier
            self.__update_strip__(index)

        self.__multiplier_semaphore__.release()

    def switchDefaultColor(self):
        self.current_index = (self.current_index + 1) % len(self.color_cycle)
        self.default_color = self.__dim_color__(self.color_cycle[self.current_index])
        self.current_index_anim = (self.current_index + 1) % len(self.color_cycle)
        self.default_color_anim = self.__dim_color__(self.color_cycle_anim[self.current_index_anim])

    def __dim_color__(self, color, threshold=64):
        max_val = max(color)
        if max_val <= 0:
            return (0, 0, 0)
        return tuple([int(threshold/max_val*val) for val in color])

    def __update_strip__(self, i=None):
        try:
            if i is None:
                for i, _ in enumerate(self.__strip__):
                    self.__update_strip__(i)
            elif 0 < i < self.led_count:
                color = self.colors[i]
                percent = self.ledMultipliers[i]
                max_color = max(color)
                if max_color == 0:
                    pass
                mul = 255 / max_color
                f = lambda val : int((mul-1)*val*percent + val)
                new_color = tuple([f(val) for val in color])
                self.__strip__[i] = new_color
        except KeyboardInterrupt:
                raise

    def __update_in_background__(self, wait_ms = 16):
        t = time()
        while self.__refresh_strip__:
            try:
                self.__strip__.show()
                while t > time():
                    pass
                t += wait_ms / 1000.0
            except KeyboardInterrupt:
                raise

    def show_animations(self):
        self.__refresh_strip__ = True
        Thread(target=self.__update_in_background__, args=()).start()

    def handle_input(self, note_info, settings):
        note, strength = note_info
        if note in settings.keys():
            setting = settings[note]
            for animation_name, arg in setting.items():
                animation = functions[animation_name]
                args = (self, strength) + arg
                Thread(target=animation, args=args).start()