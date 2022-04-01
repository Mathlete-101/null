import pygame
import pytest
from assembler import assembler

pygame.init()
pygame.display.set_mode((640, 480))
assembler.assemble()

@pytest.fixture
def ladder():
    from game_object.static.ladder import Ladder

    return Ladder((0, 0), pygame.Surface((100, 100)))

@pytest.fixture
def level(ladder):
    from level.level import Level
    l = Level((1, 1))
    l.set((0, 0), ladder)


@pytest.fixture
def player(level):
    from game_object.mobile.player import Player
    return Player(level)

class TestLadder:
    def test_init(self, ladder):
        assert ladder.rect.x == 0
        assert ladder.rect.y == 0
        assert ladder.rect.width == 42
        assert ladder.rect.height == 42
        assert ladder.opaque is False
        assert ladder.is_top_ladder is False

    def test_special_collision(self, ladder, player):
        assert ladder.special_collision is True
        ladder.collide_special(player)

