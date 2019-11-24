#!/usr/bin/env python3

import board
from threading import Thread

from led import Led
from midi import Midi, get_midi_file_name

from animation_manager import handle_input
from animation_settings import settings # get rid of it?

import socket_server
socket_server.init(settings)
Thread(target=socket_server.run_server, args=()).start()

led_pin = board.D18
led_count = 60
leds = Led(led_pin, led_count, (127,0,0))

midi_file = ''
while midi_file == '':
    midi_file = get_midi_file_name()
print(f'Opening file : {midi_file}')
midi = Midi(midi_file)

leds.show_animations()

if __name__ == '__main__':
    while True:
        note_info = midi.read()
        if note_info:
            print(note_info)
            handle_input(leds, note_info, settings)