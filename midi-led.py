#!/usr/bin/env python3

import board
from threading import Thread

from led import Led
from midi import Midi

from animation_manager import handle_input
from animation_settings import settings # get rid of it?

import socket_server
socket_server.init(settings)
Thread(target=socket_server.run_server, args=()).start()

led_pin = board.D18
led_count = 60
leds = Led(led_pin, led_count, (127,0,0))

midi_file = '/dev/snd/midiC1D0'
midi = Midi(midi_file)
leds.show_animations()

if __name__ == '__main__':
    while True:
        note_info = midi.read()
        if note_info:
            print(note_info)
            handle_input(leds, note_info, settings)