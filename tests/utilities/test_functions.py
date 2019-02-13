import functools

from compas.utilities import binomial


def test_binomial():
    assert binomial(3, 1) == 3
    assert binomial(21, 10) == 352716
