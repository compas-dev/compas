import compas
import pytest

from compas.datastructures import Mesh
from compas.itertools import flatten
from compas.itertools import grouper
from compas.itertools import iterable_like
from compas.itertools import linspace
from compas.itertools import meshgrid
from compas.itertools import normalize_values
from compas.itertools import nth
from compas.itertools import padnone
from compas.itertools import pairwise
from compas.itertools import remap_values
from compas.itertools import reshape
from compas.itertools import take
from compas.itertools import window
from compas.tolerance import TOL


# ==============================================================================
# iterable_like
# ==============================================================================


@pytest.mark.parametrize(("target", "base", "fillvalue"), [("hello", [0.5], 0.5)])
def test_iterable_like_string_and_float(target, base, fillvalue):
    a = list(iterable_like(target, base, fillvalue))
    assert a == [0.5, 0.5, 0.5, 0.5, 0.5]


@pytest.mark.parametrize(
    ("target", "base", "fillvalue"),
    [(["foo", "bar", "baz"], {"key_1": "a", "key_2": "b"}, "key_3")],
)
def test_iterable_like_list_and_dict(target, base, fillvalue):
    a = list(iterable_like(target, base, fillvalue))
    assert sorted(a) == ["key_1", "key_2", "key_3"]


@pytest.mark.parametrize(("target", "base", "fillvalue"), [(range(2), ["a", "b"], 0)])
def test_iterable_like_generator_and_list(target, base, fillvalue):
    a = list(iterable_like(target, base, fillvalue))
    assert a == ["a", "b"]


@pytest.mark.parametrize(("mesh_a", "mesh_b"), [("faces.obj", "hypar.obj"), ("hypar.obj", "faces.obj")])
def test_iterable_cap_generator(mesh_a, mesh_b):
    ma = Mesh.from_obj(compas.get(mesh_a))
    mb = Mesh.from_obj(compas.get(mesh_b))
    a = list(iterable_like(ma.faces(), mb.faces()))
    assert len(a) == len(list(ma.faces()))


def test_reshape():
    a = [1, 2, 3, 4, 5, 6]
    assert TOL.is_allclose(reshape(a, (2, 3)), [[1, 2, 3], [4, 5, 6]])
    assert TOL.is_allclose(reshape(a, (3, 2)), [[1, 2], [3, 4], [5, 6]])
    a = [[1, 2], [3, 4], [5, 6]]
    assert TOL.is_allclose(reshape(a, (2, 3)), [[1, 2, 3], [4, 5, 6]])
    a = [1, 2, 3, 4]
    assert TOL.is_allclose(reshape(a, (4, 1)), [[1], [2], [3], [4]])


def test_flatten():
    a = [[1, 2, 3], [4, 5, 6]]
    assert TOL.is_allclose(flatten(a), [1, 2, 3, 4, 5, 6])
    a = [[1], [2], [3], [4]]
    assert TOL.is_allclose(flatten(a), [1, 2, 3, 4])


def test_normalize_values():
    assert normalize_values([2, 4, 6], -1, 1) == [-1.0, 0.0, 1.0]


def test_remap_values_with_explicit_domain():
    assert remap_values([5, 10], 0, 100, 0, 10) == [50.0, 100.0]


def test_meshgrid_accepts_iterators():
    x, y = meshgrid(iter([1, 2]), iter([3, 4, 5]))
    assert x == [[1, 2], [1, 2], [1, 2]]
    assert y == [[3, 3], [4, 4], [5, 5]]


def test_linspace_boundaries():
    assert list(linspace(2, 4, 2)) == [2.0, 4.0]
    with pytest.raises(ValueError):
        list(linspace(0, 1, 1))


def test_pairwise_and_window_are_lazy_and_accept_generators():
    assert list(pairwise(value for value in range(4))) == [(0, 1), (1, 2), (2, 3)]
    assert list(window((value for value in range(4)), 3)) == [(0, 1, 2), (1, 2, 3)]
    assert list(window([], 3)) == []


def test_iterable_like_is_lazy():
    consumed = []

    def values():
        consumed.append(1)
        yield "a"
        consumed.append(2)
        yield "b"

    result = iterable_like(range(2), values())
    assert consumed == []
    assert next(result) == "a"
    assert consumed == [1]


def test_take_and_nth():
    assert take(2, iter([1, 2, 3])) == [1, 2]
    assert nth(iter([1, 2, 3]), 1) == 2
    assert nth(iter([1]), 2) is None
    assert nth(iter([1]), 2, "missing") == "missing"


def test_padnone():
    padded = padnone(iter([1, 2]))
    assert take(5, padded) == [1, 2, None, None, None]


def test_grouper():
    assert list(grouper(iter([1, 2, 3]), 2, 0)) == [(1, 2), (3, 0)]
