from threading import Thread
from animations import functions

def handle_input(led, note_info, settings):
    note, strength = note_info
    if note in settings.keys():
        setting = settings[note]
        for animation_name, arg in setting.items():
            animation = functions[animation_name]
            args = (led, strength) + arg
            Thread(target=animation, args=args).start()