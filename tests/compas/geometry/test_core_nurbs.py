import pytest

from compas.geometry import compute_basisfuncs
from compas.geometry import compute_basisfuncsderivs
from compas.geometry import construct_knotvector
from compas.geometry import find_span
from compas.geometry import knots_and_mults_to_knotvector
from compas.geometry import knotvector_to_knots_and_mults


def test_construct_knotvector():
    knotvector = construct_knotvector(degree=2, pointcount=5)

    assert knotvector == pytest.approx([0, 0, 0, 1 / 3, 2 / 3, 1, 1, 1])

    with pytest.raises(ValueError):
        construct_knotvector(degree=3, pointcount=3)


def test_convert_knotvector_representation():
    knotvector = [0, 0, 0, 0.5, 1, 1, 1]

    knots, multiplicities = knotvector_to_knots_and_mults(knotvector)

    assert knots == [0, 0.5, 1]
    assert multiplicities == [3, 1, 3]
    assert knots_and_mults_to_knotvector(knots, multiplicities) == knotvector


def test_find_span_at_domain_boundaries():
    knotvector = construct_knotvector(degree=2, pointcount=5)

    assert find_span(4, 2, knotvector, 0.0) == 2
    assert find_span(4, 2, knotvector, 0.5) == 3
    assert find_span(4, 2, knotvector, 1.0) == 4

    with pytest.raises(ValueError):
        find_span(4, 2, knotvector, -0.1)

    with pytest.raises(ValueError):
        find_span(4, 2, knotvector, 1.1)


def test_compute_basis_functions_and_derivatives():
    knotvector = construct_knotvector(degree=2, pointcount=5)
    span = find_span(4, 2, knotvector, 0.5)

    basis = compute_basisfuncs(2, knotvector, span, 0.5)
    derivatives = compute_basisfuncsderivs(2, knotvector, span, 0.5, 2)

    assert basis == pytest.approx([0.125, 0.75, 0.125])
    assert sum(basis) == pytest.approx(1.0)
    assert derivatives[0] == pytest.approx(basis)
    assert derivatives[1] == pytest.approx([-1.5, 0.0, 1.5])
    assert derivatives[2] == pytest.approx([9.0, -18.0, 9.0])
