#!/usr/bin/env python3

import board
from led import Led
from midi import Midi
from animation_manager import handle_input

led_pin = board.D18
led_count = 60
leds = Led(led_pin, led_count, (127,0,0))

midi_file = '/dev/snd/midiC1D0'
midi = Midi(midi_file)
leds.show_animations()

if __name__ == '__main__':
    while True:
        note_info = midi.read()
        if note:
            print(note_info)
            handle_input(leds, note_info)