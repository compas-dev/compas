import compas
import pytest

from compas.datastructures import Mesh
from compas.utilities import iterable_like


# ==============================================================================
# iterable_like
# ==============================================================================

@pytest.mark.parametrize(("target", "base", "fillvalue"),
                         [("hello", [0.5], 0.5)])
def test_iterable_like_string_and_float(target, base, fillvalue):
    a = list(iterable_like(target, base, fillvalue))
    assert a == [0.5, 0.5, 0.5, 0.5, 0.5]

@pytest.mark.parametrize(("target", "base", "fillvalue"),
                         [(['foo', 'bar', 'baz'], {'key_1': 'a', 'key_2': 'b'}, 'key_3')])
def test_iterable_like_list_and_dict(target, base, fillvalue):
    a = list(iterable_like(target, base, fillvalue))
    assert sorted(a) == ['key_1', 'key_2', 'key_3']


@pytest.mark.parametrize(("target", "base", "fillvalue"),
                         [(range(2), ['a', 'b'], 0)])
def test_iterable_like_generator_and_list(target, base, fillvalue):
    a = list(iterable_like(target, base, fillvalue))
    assert a == ['a', 'b']


@pytest.mark.parametrize(("mesh_a", "mesh_b"),
                         [("faces.obj", "hypar.obj"),
                         ("hypar.obj", "faces.obj")])
def test_iterable_cap_generator(mesh_a, mesh_b):
    ma = Mesh.from_obj(compas.get(mesh_a))
    mb = Mesh.from_obj(compas.get(mesh_b))
    a = list(iterable_like(ma.faces(), mb.faces()))
    assert len(a) == len(list(ma.faces()))
