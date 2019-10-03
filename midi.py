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
            drum, pitch = self.f.read(2)

            # define the kind of drum
            drumName = ''
            if drum in drums:
                drumName = drums[drum]
            elif drum in cymbals:
                drumName = cymbals[drum]
            else:
                drumName = 'undefined'

            # handle note on/off event
            # note on
            if ord(pitch):
                return drumName, ord(pitch)
            #note off
            # else:
                # return 'note off', 0