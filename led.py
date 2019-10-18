from math import sin, pi
from threading import Thread
from time import sleep
import neopixel

class Led:
    def __init__(self, pin, led_count, default_color=(0,0,0)):
        self.pin = pin
        self.led_count = led_count
        self.strip = neopixel.NeoPixel(self.pin, self.led_count, auto_write=False)
        self.default_color = default_color
        self.color_wipe(default_color)
        self.default_brightness = sin(19.0/20.0*pi)
        self.strip.brightness = self.default_brightness

        self.current_id1 = 0
        self.current_id2 = 0
        self.current_len1 = 0
        self.current_len2 = 0

    def color_wipe(self, color):
        for i in range(self.led_count):
            self.strip[i] = color
            wait_ms = 10
            sleep(wait_ms / 1000.0)

    def clear(self):
        self.color_wipe((0,0,0))

    def flash(self, velocity):
        steps = 20
        for i in range(steps):
            percent = sin(i / steps * pi)
            brightness = velocity/127 * (1 - self.default_brightness) + self.default_brightness
            self.strip.brightness = brightness * percent
            wait_ms=5
            sleep(wait_ms / 1000.0)
        brightness = self.default_brightness

    def color_from_middle(self, color, velocity, my_id, width=15, duration_ms = 100):
        middle = self.led_count // 2
        offset = self.led_count % 2
        length = int(velocity / 127 * width)
        self.current_len1 = length
        if offset:
            self.strip[middle] = color
            sleep(duration_ms/length/2 / 1000.0)
        for i in range(length):
            if my_id == self.current_id1:
                self.strip[middle + i + offset] = color
                self.strip[middle - i - 1] = color
                sleep(duration_ms/length/2 / 1000.0)
        start = middle - length
        for i in range(length):
            if my_id == self.current_id1:
                self.strip[start + i] = self.default_color
                self.strip[start + 2*length - i] = self.default_color
                sleep(duration_ms/length/2 / 1000.0)
            else:
                if(i != length-1):
                    self.strip[start + i] = self.default_color
                    self.strip[start + 2*length - i] = self.default_color
        if my_id == self.current_id1:
            self.strip[middle] = self.default_color

    def color_from_rear(self, color, velocity, my_id, width=15, duration_ms = 100):
        length = int(velocity / 127 * width)
        if length < 5:
            length = 5
        if length > 15:
            length = 15
        self.current_len2 = length
        for i in range(length):
            if my_id == self.current_id2:
                self.strip[i] = color
                self.strip[self.led_count - i - 1] = color
                sleep(duration_ms/length/2 / 1000.0)
        for i in range(length):
            if my_id == self.current_id2:
                self.strip[length - i - 1] = self.default_color
                self.strip[self.led_count - length + i] = self.default_color
                sleep(duration_ms/length/2 / 1000.0)
            else:
                if(i != length-1):
                    self.strip[i] = self.default_color
                    self.strip[self.led_count - i - 1] = self.default_color

    def start_animation(self, note, pitch):
        brightness = 2 * pitch
        if note == 'snare':
            color = (brightness,brightness,brightness)
            self.current_id1+=1
            Thread(target=self.color_from_middle, args=(color, pitch, self.current_id1)).start()
        elif note == 'kick':
            Thread(target=self.flash, args=(pitch,)).start()
            if self.default_color == (127, 0, 0):
                new_default_color = (0, 0, 127)
            elif self.default_color == (0, 0, 127):
                new_default_color = (127, 0, 0)
            for i, color in enumerate(self.strip):
                if color == self.default_color:
                    self.strip[i] = new_default_color
            self.default_color = new_default_color
            return
        elif note == 'tom1':
            #color = (brightness, brightness, 0)
            Thread(target=self.flash, args=(pitch,)).start()
            return
        elif note == 'tom2':
            #color = (brightness, brightness // 2, 0)
            Thread(target=self.flash, args=(pitch,)).start()
            return
        elif note == 'tom3':
            #color = (brightness, brightness // 3, 0)
            Thread(target=self.flash, args=(pitch,)).start()
            return
        else:
            if self.default_color == (127, 0, 0):
                color = (0, 0, 127)
            elif self.default_color == (0, 0, 127):
                color = (127, 0, 0)
            self.current_id2+=1
            Thread(target=self.color_from_rear, args=(color, pitch, self.current_id2)).start()

    def animate(self):
        self.strip.show()