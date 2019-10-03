from midi import Midi

midi_file = '/dev/snd/midiC1D0'
midi = Midi(input_file)

while True:
    midi_input = midi.read()
    if midi_input:
        print(midi_input)