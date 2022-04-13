import pygame


class Music:
    def __init__(self, filename, file_type="mid"):
        self.filename = filename
        self.file_type = file_type

    def load(self):
        pygame.mixer.music.load(self.filename, self.file_type)

    def play(self):
        self.load()
        pygame.mixer.music.play(-1)
