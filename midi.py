import os
from data.accepted_inputs import accepted_inputs

def get_midi_file_name():
    output = os.popen('ls /dev/snd | grep -i midi').read()
    if output != '':
        name = ''
        for character in output:
            if character == '\n':
                return '/dev/snd/' + name
            name += character
    return ''

class Midi:
    def __init__(self, file):
       self.f = open(file, mode='rb')

    def check_for_note_event(self):
        byte = self.f.read(1)
        if byte == b'\x99':
            return True

    def read(self):
        if self.check_for_note_event():
            # read which type of drum was hit (pitch)
            # and with what strength (velocity)
            pitch, velocity = self.f.read(2)

            drumName = None
            if pitch in accepted_inputs:
                drumName = accepted_inputs[pitch]
            else:
                drumName = 'undefined'
                # debug
                print(hex(pitch))
                return

            # handle note on/off event
            # note on
            if velocity:
                return drumName, velocity
            # note off
            # else:
                # return 'pitch off', 0