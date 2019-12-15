#!/usr/bin/env python3

import board
from threading import Thread

from src.led import Led
from src.midi import Midi, get_midi_file_name

from src.animation_settings import settings

from src.socket_server import Server

led_pin = board.D18
led_count = 60
leds = Led(led_pin, led_count, (127,0,0))

server = Server(leds, settings)
Thread(target=server.run_server, args=()).start()

def open_file():
    midi_file = ''
    while midi_file == '':
        midi_file = get_midi_file_name()
    print(f'Opening midi file : {midi_file}')
    return Midi(midi_file)
midi = open_file()

leds.show_animations()

def main():
    global midi, leds
    try:
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
                leds.handle_input(note_info, settings)
    except KeyboardInterrupt:
        global socket_server
        del server
        del leds
        del midi
        return

if __name__ == '__main__':
    main()