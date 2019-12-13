from time import time, sleep
from math import sin, pi, sqrt
from threading import Semaphore

semaphore = Semaphore()

def color_wipe(led, color):
    for i in range(led.led_count):
        setLedColor(i, color)
        wait_ms = 10
        sleep(wait_ms / 1000.0)

def flash(led, velocity, wait_ms=10, steps = 10):
    t = time()
    for i in range(steps):
        percent = sin(i / steps * pi)
        brightness = velocity/127 * (1 - led.default_brightness) + led.default_brightness
        led.setBrightness(brightness * percent)
        while t > time():
            pass
        t += wait_ms / 1000.0
    semaphore.acquire()
    led.__strip__.brightness = led.default_brightness
    semaphore.release()

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
        led.setLedColor(middle, color)
        while t > time():
            pass
        t += wait_ms / 1000.0
    for i in range(length):
        new_color = __fade__(color, led.default_color, i + 1, length)
        led.setLedColor(middle + i + offset, new_color)
        led.setLedColor(middle - i - 1, new_color)
        while t > time():
            pass
        t += wait_ms / 1000.0
    start = middle - length
    for i in range(length):
        led.setLedColor(start + i, led.default_color)
        led.setLedColor(start + 2*length - i, led.default_color)
        while t > time():
            pass
        t += wait_ms / 1000.0
    led.setLedColor(middle, led.default_color)

def color_from_rear(led, velocity, color, width=15, duration_ms = 100):
    t = time()
    length = int(velocity / 127 * width)
    wait_ms = duration_ms / (2*length)
    if length < 5:
        length = 5
    if length > 15:
        length = 15
    for i in range(length):
        led.setLedColor(i, color)
        led.setLedColor(led.led_count - i - 1, color)
        while t > time():
            pass
        t += wait_ms / 1000.0
    for i in range(length):
        led.setLedColor(length - i - 1, led.default_color)
        led.setLedColor(led.led_count - length + i, led.default_color)
        while t > time():
            pass
        t += wait_ms / 1000.0

def bright_wave(led, velocity, wait_ms=5, wave_len=6):
    t = time()
    for start_index, _ in enumerate(led.ledMultipliers):
        waveMultipliers = led.ledMultipliers[start_index : start_index + wave_len]
        end_index = led.led_count if start_index + wave_len > led.led_count else start_index + wave_len
        indices = list(range(start_index, end_index))
        led.setMultiplier(indices, [2]*wave_len)
        while t > time():
            pass
        t += wait_ms / 1000.0
        for i, mul in enumerate(waveMultipliers):
            led.setMultiplier(start_index + i, 1)


functions = {
    "flash": flash,
    "color_from_middle": color_from_middle,
    "color_from_rear": color_from_rear,
    "color_wipe": color_wipe,
    "bright_wave": bright_wave,
}