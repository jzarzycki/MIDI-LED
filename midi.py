from data.drums import drums
from data.cymbals import cymbals

class Midi:
    def __init__(self, file):
       self.f = open(file)

    def read(self):
        # wait for a note event
        b = self.f.read(1)
        if b == '\x99':
            # read which type of drum was hit with what strength
            note, pitch = self.f.read(2)

            # define the kind of drum
            drumName = None
            if note in drums:
                drumName = drums[note]
            elif note in cymbals:
                drumName = cymbals[note]
            else:
                drumName = 'undefined'
                # debug
                print(hex(ord(note)))
                return

            # handle note on/off event
            # note on
            if ord(pitch):
                return drumName, ord(pitch)
            #note off
            # else:
                # return 'note off', 0