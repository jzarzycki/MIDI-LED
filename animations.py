from time import sleep
from math import sin, pi

def color_wipe(led, color):
    for i in range(led.led_count):
        led.strip[i] = color
        wait_ms = 10
        sleep(wait_ms / 1000.0)

def flash(led, velocity):
    steps = 20
    for i in range(steps):
        percent = sin(i / steps * pi)
        brightness = velocity/127 * (1 - led.default_brightness) + led.default_brightness
        led.strip.brightness = brightness * percent
        wait_ms=5
        sleep(wait_ms / 1000.0)
    brightness = led.default_brightness

def color_from_middle(led, velocity, color, width=15, duration_ms = 100):
    middle = led.led_count // 2
    offset = led.led_count % 2
    length = int(velocity / 127 * width)
    led.current_len1 = length
    if offset:
        led.strip[middle] = color
        sleep(duration_ms/length/2 / 1000.0)
    for i in range(length):
        led.strip[middle + i + offset] = color
        led.strip[middle - i - 1] = color
        sleep(duration_ms/length/2 / 1000.0)
    start = middle - length
    for i in range(length):
        led.strip[start + i] = led.default_color
        led.strip[start + 2*length - i] = led.default_color
        sleep(duration_ms/length/2 / 1000.0)
    led.strip[middle] = led.default_color

def color_from_rear(led, velocity, color, width=15, duration_ms = 100):
    length = int(velocity / 127 * width)
    if length < 5:
        length = 5
    if length > 15:
        length = 15
    led.current_len2 = length
    for i in range(length):
        led.strip[i] = color
        led.strip[led.led_count - i - 1] = color
        sleep(duration_ms/length/2 / 1000.0)
    for i in range(length):
        led.strip[length - i - 1] = led.default_color
        led.strip[led.led_count - length + i] = led.default_color
        sleep(duration_ms/length/2 / 1000.0)