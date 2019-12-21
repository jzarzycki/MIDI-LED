#!/usr/bin/env python3

import board
from threading import Thread

from src.led import Led
from src.midi import Midi, get_midi_file_name

from src.animation_settings import settings

from src.socket_server import Server

led_pin = board.D18
led_count = 60
led_strip = Led(led_pin, led_count, (127, 0, 0))

server = Server(led_strip, settings)
Thread(target=server.run_server, args=()).start()

def open_file():
    midi_file = ''
    while midi_file == '':
        midi_file = get_midi_file_name()
    print(f'Opening midi file : {midi_file}')
    return Midi(midi_file)
midi = open_file()

led_strip.show_animations()

def main():
    global midi, led_strip
    note_info = None
    while True:
        try:
            note_info = midi.read()
        except OSError as e:
            if e.strerror == "No such device":
                print('Midi file no longer available, searching for a new one')
                midi = open_file()
            else:
                raise e
        if note_info:
            led_strip.handle_input(note_info, settings)

if __name__ == '__main__':
    main()