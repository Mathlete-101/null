import json
import os

import pygame.sprite

from engine import keys
from externals.leaderboard.leader import Leader
from misc.wrapped_sprite import WrappedSprite
from tools.text import render_font_cool as Text

# In theory, I could use ascii codes, but this is just easier
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Leaders(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        from engine.game import engine

        self.letter_on = 0

        # Initialize the leaderboard -- gotten from storage
        self.path = os.path.join(os.path.join("resources", "misc", "leaders" + str(engine.difficulty) + ".json"))
        if os.path.exists(self.path):
            with open(self.path, "r") as file:
                leaders_dict = json.load(file)
        else:
            leaders_dict = {
                "leaders": []
            }

        self.leaders = []

        def sort_leaders():
            self.leaders.sort(key=lambda x: x.score, reverse=True)

        for leader in leaders_dict["leaders"]:
            self.leaders.append(Leader(leader["name"], leader["score"]))

        for i in range(10 - len(self.leaders)):
            self.leaders.append(Leader("***", 0, True))

        sort_leaders()

        if engine.score > self.leaders[9].score:
            self.leaders.pop()
            self.new_score = Leader("AAA", engine.score)
            self.leaders.append(self.new_score)
            sort_leaders()
        else:
            self.new_score = None

        for i in range(len(self.leaders)):
            self.add(self.leaders[i].position((engine.screen.get_size()[0] * 5 / 8, 150 + 60 * i), str(i + 1) + "."))

        if self.new_score:
            self.set_new_score_name_sprite(0, (60, 60, 255))


        # This prevents the time you clicked a to end the game from also skipping the first letter selection
        keys.a_down = False


    def set_new_score_name_sprite(self, index, color=(60, 60, 255)):
        self.remove(self.new_score.name_sprites[index])
        self.new_score.name_sprites[index] = WrappedSprite(Text(self.new_score.name[index], zoom=3, color1=color),
                                                           (self.new_score.name_sprites[index].rect[0],
                                                            self.new_score.name_sprites[index].rect[1]))
        self.add(self.new_score.name_sprites[index])

    def update(self):
        if keys.a_down:
            if self.new_score:
                if self.letter_on < 3:
                    self.set_new_score_name_sprite(self.letter_on, (254, 255, 255))
                self.letter_on += 1
                if self.letter_on < 3:
                    self.set_new_score_name_sprite(self.letter_on, (60, 60, 255))
                elif self.letter_on == 3:
                    # save the leaderboard
                    leaderboard_dict = {}
                    leaderboard_dict["leaders"] = []
                    for leader in self.leaders:
                        if not leader.placeholder:
                            leaderboard_dict["leaders"].append({
                                "name": leader.name,
                                "score": leader.score
                            })
                        with open(self.path, "w") as file:
                            json.dump(leaderboard_dict, file)
                else:
                    # it should restart the game
                    # this doesn't work yet
                    # from engine.engine import engine
                    # engine.state = 0
                    # engine.score = 0

                    #instead, I'll just casually
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q))

            else:
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q))

        elif self.new_score and self.letter_on < 3:
            if keys.up_down:
                self.new_score.name = self.new_score.name[:self.letter_on] + LETTERS[(LETTERS.find(self.new_score.name[self.letter_on]) + 1) % 26] + self.new_score.name[self.letter_on + 1:]
                self.set_new_score_name_sprite(self.letter_on)
            elif keys.down_down:
                self.new_score.name = self.new_score.name[:self.letter_on] + LETTERS[(LETTERS.find(self.new_score.name[self.letter_on]) - 1) % 26] + self.new_score.name[self.letter_on + 1:]
                self.set_new_score_name_sprite(self.letter_on)
