
import pytest

from game_object.static.air import Air


@pytest.fixture
def air():
    return Air((0, 0))

class TestAir:
    def test_tags(self, air):
        assert 'air' in air.tags

    def test_is_air(self, air):
        assert air.is_floor is False
        assert air.is_left_wall is False
        assert air.is_right_wall is False
        assert air.is_ceiling is False
        assert air.opaque is False
