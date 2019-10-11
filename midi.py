from data.accepted_inputs import accepted_inputs

class Midi:
    def __init__(self, file):
       self.f = open(file, mode='rb')

    def read(self):
        # wait for a note event
        b = self.f.read(1)
        if b == b'\x99':
            # read which type of drum was hit with what strength
            note, pitch = self.f.read(2)

            # define the kind of drum
            drumName = None
            if note in accepted_inputs:
                drumName = accepted_inputs[note]
            else:
                drumName = 'undefined'
                # debug
                print(hex(note))
                return

            # handle note on/off event
            # note on
            if pitch:
                return drumName, pitch
            #note off
            # else:
                # return 'note off', 0