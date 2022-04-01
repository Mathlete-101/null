import pygame
import pytest

from graphics.graphic_class.graphic import Graphic


@pytest.fixture
def render_surface():
    from pygame import Surface
    return Surface((100, 100))

@pytest.fixture
def sample_block_image():
    from pygame import Surface
    return Surface((10, 10))


@pytest.fixture
def block(sample_block_image, render_surface):
    from game_object.static.block import Block
    return Block((0, 0), render_surface, sample_block_image)

class TestBlock:
    def test_init(self, block, sample_block_image, render_surface):
        assert block.image == sample_block_image
        assert block.rect == pygame.Rect(0, 0, 42, 42)

    def test_init_error(self, render_surface):
        from game_object.static.block import Block
        with pytest.raises(Exception):
            Block((0, 0), Graphic(pygame.Surface(0, 0)), render_surface)

    def test_properties(self, block):
        """Test to see if the block is a ceiling, floor, or left or right wall"""
        assert block.is_ceiling is True
        assert block.is_floor is True
        assert block.is_left_wall is True
        assert block.is_right_wall is True

    def test_render(self, block, render_surface):
        """Test to see if the block renders to the render surface"""
        initial_render_surface = render_surface.copy()
        block.render()
        assert initial_render_surface != render_surface

    def test_alert(self, block, sample_block_image):
        initial_image = sample_block_image.copy()
        block.alert()
        assert initial_image != sample_block_image



