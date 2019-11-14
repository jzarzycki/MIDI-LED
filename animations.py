from time import time, sleep
from math import sin, pi, sqrt

def color_wipe(led, color):
    for i in range(led.led_count):
        led.strip[i] = color
        wait_ms = 10
        sleep(wait_ms / 1000.0)

def flash(led, velocity, wait_ms=10, steps = 10):
    t = time()
    for i in range(steps):
        percent = sin(i / steps * pi)
        brightness = velocity/127 * (1 - led.default_brightness) + led.default_brightness
        led.strip.brightness = brightness * percent

        while t > time():
            pass
        t += wait_ms / 1000.0
    led.strip.brightness = led.default_brightness

def __fade__(x, y, nr, out_of):
    li = []
    for i, j in zip(x, y):
        li.append(int(i - (i-j)*(nr/out_of)))
    return tuple(li)

def color_from_middle(led, velocity, color, width=15, duration_ms = 100):
    t = time()
    middle = led.led_count // 2
    offset = led.led_count % 2
    length = int(velocity / 127 * width)
    if length == 0:
        length = 3
    wait_ms = duration_ms / (2*length)
    if offset:
        led.strip[middle] = color
        while t > time():
            pass
        t += wait_ms / 1000.0
    for i in range(length):
        new_color = __fade__(color, led.default_color, i + 1, length)
        led.strip[middle + i + offset] = new_color
        led.strip[middle - i - 1] = new_color
        while t > time():
            pass
        t += wait_ms / 1000.0
    start = middle - length
    for i in range(length):
        led.strip[start + i] = led.default_color
        led.strip[start + 2*length - i] = led.default_color
        while t > time():
            pass
        t += wait_ms / 1000.0
    led.strip[middle] = led.default_color

def color_from_rear(led, velocity, color, width=15, duration_ms = 100):
    t = time()
    length = int(velocity / 127 * width)
    wait_ms = duration_ms / (2*length)
    if length < 5:
        length = 5
    if length > 15:
        length = 15
    for i in range(length):
        led.strip[i] = color
        led.strip[led.led_count - i - 1] = color
        while t > time():
            pass
        t += wait_ms / 1000.0
    for i in range(length):
        led.strip[length - i - 1] = led.default_color
        led.strip[led.led_count - length + i] = led.default_color
        while t > time():
            pass
        t += wait_ms / 1000.0

functions = {
    "flash": flash,
    "color_from_middle": color_from_middle,
    "color_from_rear": color_from_rear,
    "color_wipe": color_wipe,
}