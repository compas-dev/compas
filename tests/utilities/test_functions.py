import pytest

from compas.utilities import binomial


@pytest.mark.parametrize(("n", "k", "result"),
	[
	pytest.param(3, 1, 3),
	pytest.param(21, 10, 352716),
	pytest.param(10, 0, 1),
	pytest.param(0, 0, 1),
	pytest.param(1, 2, 0, marks=pytest.mark.xfail(raises=ValueError)),
	pytest.param(2, -1, 0, marks=pytest.mark.xfail(raises=ValueError)),
	]
)
def test_binomial(n, k, result):
    assert binomial(n, k) == pytest.approx(result)
