from threading import Thread
from animation_settings import settings

def handle_input(led, note_info):
    pitch, velocity = note_info
    if pitch in settings.keys():
        setting = settings[pitch]
        animation = setting['animation']
        args = (led, velocity)

        keys = setting.keys()
        if "args" in keys:
            args += setting["args"]
        elif "multipier" in keys:
            pass

        Thread(target=animation, args=args).start()