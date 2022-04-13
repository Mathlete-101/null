sounds = {}


def add(sound, name):
    sounds[name] = sound


def get(name):
    try:
        return sounds[name]
    except KeyError:
        raise KeyError(f"Sound '{name}' not found")

def play_sound(name):
    sound = get(name)
    sound.play()
