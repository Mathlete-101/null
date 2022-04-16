import pygame

from engine.settings import settings

sounds = {}
musics = {}


def add_sound(sound, name):
    sounds[name] = sound


def add_music(music, name):
    musics[name] = music


def get(name):
    try:
        return sounds[name]
    except KeyError:
        try:
            return musics[name]
        except KeyError:
            raise KeyError("No sound or music named '{}'".format(name))


def update_volume():
    for sound in sounds.values():
        sound.set_volume(settings.get(["sound", "volume", "sfx"]) * settings.get(["sound", "volume", "master"]))
    pygame.mixer.music.set_volume(settings.get(["sound", "volume", "music"]) * settings.get(["sound", "volume", "master"]))

def play_sound(name):
    sound = get(name)
    sound.play()


def play_music(name):
    music = get(name)
    music.play()


def stop_music():
    pygame.mixer.music.stop()
