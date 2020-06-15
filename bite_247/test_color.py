from unittest.mock import patch

import pytest

import color


@pytest.fixture(scope="module")
def gen():
    return color.gen_hex_color()


def test_gen_hex_color(gen):
    min_ = 100
    for x in range(100):
        val = next(gen)

        assert len(val) == 7
        assert val[0] == "#"
        assert val.upper() == val

        r, g, b = [
            val[start: start + 2] for start in range(1, len(val[1:]), 2)
        ]

        assert 0 <= int(r, 16) <= 255
        min_ = min(min_, int(r, 16))
        assert 0 <= int(g, 16) <= 255
        min_ = min(min_, int(g, 16))
        assert 0 <= int(b, 16) <= 255
        min_ = min(min_, int(b, 16))

    assert min_ == 0