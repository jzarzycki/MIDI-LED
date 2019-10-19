from math import sin, pi
from threading import Thread
from time import sleep
import neopixel
import animations

class Led:
    def __init__(self, pin, led_count, default_color=(0,0,0)):
        self.pin = pin
        self.led_count = led_count
        self.strip = neopixel.NeoPixel(self.pin, self.led_count, auto_write=False)
        self.default_color = default_color
        animations.color_wipe(self, default_color)
        self.default_brightness = sin(19.0/20.0*pi)
        self.strip.brightness = self.default_brightness

        self.current_id1 = 0
        self.current_id2 = 0
        self.current_len1 = 0
        self.current_len2 = 0

    def start_animation(self, note, pitch):
        brightness = 2 * pitch
        if note == 'snare':
            color = (brightness,brightness,brightness)
            self.current_id1+=1
            Thread(target=animations.color_from_middle, args=(self, color, pitch, self.current_id1)).start()
        elif note == 'kick':
            Thread(target=animations.flash, args=(self, pitch,)).start()
            #if self.default_color == (127, 0, 0):
            #    new_default_color = (0, 0, 127)
            #elif self.default_color == (0, 0, 127):
            #    new_default_color = (127, 0, 0)
            #for i, color in enumerate(self.strip):
            #    if color == self.default_color:
            #        self.strip[i] = new_default_color
            #self.default_color = new_default_color
            return
        else:
            if self.default_color == (127, 0, 0):
                color = (0, 0, 127)
            elif self.default_color == (0, 0, 127):
                color = (127, 0, 0)
            self.current_id2+=1
            Thread(target=animations.color_from_rear, args=(self, color, pitch, self.current_id2)).start()

    def animate(self):
        self.strip.show()