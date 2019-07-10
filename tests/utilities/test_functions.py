import pytest

from compas.utilities import binomial_coefficient


@pytest.mark.parametrize(("n", "k", "result"), [
    (3, 1, 3),
    (21, 10, 352716),
    (10, 0, 1),
    (0, 0, 1),
])
def test_binomial(n, k, result):
    assert binomial_coefficient(n, k) == pytest.approx(result)


@pytest.mark.parametrize(("n", "k"), [
    (1, 2),
    (2, -1),
])
def test_binomial_raises_when_input_is_invalid(n, k):
    with pytest.raises(ValueError):
        binomial_coefficient(n, k)
