from time import time, sleep
from math import sin, pi, sqrt
from threading import Semaphore

semaphore = Semaphore()

def instant_color(led, velocity, *color):
    led.switchDefaultColor()
    i = list(range(led.led_count))
    led.setLedColor(i, [led.default_color] * led.led_count)

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
    f = lambda x : sqrt((2*(x-0.5))) if x > 0.5 else 0
    li = []
    for i, j in zip(x, y):
        li.append(int(i - (i-j)*f(nr/out_of)))
    return tuple(li)

def color_from_middle(led, velocity, width=20, duration_ms = 150):
    t = time()
    color = led.default_color_anim
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

def bright_wave(led, velocity, wait_ms=10, wave_len=6):
    t = time()
    length = led.led_count
    offset = (length+1) % 2
    mid = length // 2
    num_iter = mid + length%2

    left_start = mid - offset + wave_len
    left_end = left_start - wave_len if left_start - wave_len > 0 else 0
    right_start = mid - wave_len
    right_end = (right_start + wave_len) % length

    for i in range(num_iter + wave_len):
        if i < length:
            led.setMultiplier([left_end, right_end], 1)
        if i > wave_len - 1:
            led.setMultiplier([left_start, right_start], 0)
        while t > time():
            pass
        t += wait_ms / 1000.0
        left_start -= 1
        left_end = left_end - 1 if left_end - 1 > 0 else 0
        right_start += 1
        right_end = (right_end + 1) % length

functions = {
    "flash": flash,
    "color-from-middle": color_from_middle,
    "instant": instant_color,
    "bright-wave": bright_wave,
}