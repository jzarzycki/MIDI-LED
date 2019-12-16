import os
from src.accepted_inputs import accepted_inputs

def get_midi_file_name():
    directory = '/dev/snd/'
    output = os.popen(f'ls {directory} | grep -i midi').read()
    if output != '':
        name = ''
        for character in output:
            if character == '\n':
                return directory + name
            name += character
    return ''

class Midi:
    def __init__(self, file):
        self.f = open(file, mode='rb')

    def __del__(self):
        self.f.close()

    def check_for_note_event(self):
        try:
            byte = self.f.read(1)
        except KeyboardInterrupt:
            raise
        if byte == b'\x99':
            return True

    def read(self):
        if self.check_for_note_event():
            # read which type of drum was hit (pitch)
            # and with what strength (velocity)
            try:
                pitch, velocity = self.f.read(2)
            except KeyboardInterrupt:
                raise

            drum_name = None
            if pitch in accepted_inputs:
                drum_name = accepted_inputs[pitch]
            else:
                drum_name = 'undefined'
                # alarm user, that they need to add this input to accepted_inputs
                print('input not accepted: ', hex(pitch))
                return

            # handle note on event
            if velocity:
                return drum_name, velocity