from midi import Midi
from led import Led
import board

midi_file = '/dev/snd/midiC1D0'
midi = Midi(midi_file)

led_pin = board.D18
led_count = 60

led = Led(led_pin, led_count)
led.clear()

while True:
    midi_input = midi.read()
    led.animate()

    if midi_input:
        note, pitch = midi_input
        print(note, pitch)
        led.startAnimation(note, pitch)