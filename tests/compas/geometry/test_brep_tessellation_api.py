from math import degrees
from types import SimpleNamespace

import pytest  # pyright: ignore[reportMissingImports]

import compas.plugins
from compas.geometry import Brep
from compas.geometry import BrepFace
from compas.geometry import Box
from compas.geometry import Tessellation
from compas.geometry import Translation
from compas.geometry.brep.operations import brep_to_tessellation
from compas.tolerance import TOL


def _install_fake_brep_plugin(monkeypatch):
    calls = []
    tessellation = Tessellation([[0.0, 0.0, 0.0]], [])

    def tessellate(brep, *, linear_deflection, angular_deflection):
        calls.append((brep, linear_deflection, angular_deflection))
        return tessellation

    implementations = {
        "brep_to_tessellation": tessellate,
    }

    def select(extension_point):
        method = implementations.get(extension_point.name)
        if method is None:
            return None
        return SimpleNamespace(id="tests.fake_brep", method=method)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)
    return calls, tessellation


def test_brep_tessellation_dispatches_concrete_values(monkeypatch):
    calls, tessellation = _install_fake_brep_plugin(monkeypatch)
    brep = Brep()

    assert brep.to_tessellation(linear_deflection=0.1, angular_deflection=15.0) is tessellation
    assert calls == [(brep, 0.1, 15.0)]


def test_brep_resolves_defaults_and_validates_before_dispatch(monkeypatch):
    calls, _ = _install_fake_brep_plugin(monkeypatch)
    brep = Brep()

    brep.to_tessellation()
    assert calls[-1] == (brep, TOL.lineardeflection, degrees(TOL.angulardeflection))

    for value in (True, "0.1"):
        with pytest.raises(TypeError):
            brep.to_tessellation(linear_deflection=value)  # pyright: ignore[reportArgumentType]
    for value in (0.0, float("inf")):
        with pytest.raises(ValueError):
            brep.to_tessellation(linear_deflection=value)
    with pytest.raises(ValueError):
        brep.to_tessellation(angular_deflection=181.0)


def test_brep_resolves_independently_omitted_controls(monkeypatch):
    calls, _ = _install_fake_brep_plugin(monkeypatch)
    brep = Brep()

    brep.to_tessellation(linear_deflection=0.1)
    assert calls[-1] == (brep, 0.1, degrees(TOL.angulardeflection))

    brep.to_tessellation(angular_deflection=15.0)
    assert calls[-1] == (brep, TOL.lineardeflection, 15.0)


def test_brep_resolves_scoped_tolerance_defaults(monkeypatch):
    calls, _ = _install_fake_brep_plugin(monkeypatch)
    brep = Brep()

    with TOL.temporary(lineardeflection=0.025, angulardeflection=0.125):
        brep.to_tessellation()

    assert calls == [(brep, 0.025, degrees(0.125))]


def test_direct_brep_tessellation_hook_rejects_none(monkeypatch):
    calls, _ = _install_fake_brep_plugin(monkeypatch)
    brep = Brep()

    with pytest.raises(TypeError):
        brep_to_tessellation(
            brep,
            linear_deflection=None,  # pyright: ignore[reportArgumentType]
            angular_deflection=15.0,
        )
    with pytest.raises(TypeError):
        brep_to_tessellation(
            brep,
            linear_deflection=0.1,
            angular_deflection=None,  # pyright: ignore[reportArgumentType]
        )

    assert calls == []


def test_brep_face_reuses_brep_plugin_boundary(monkeypatch):
    calls, tessellation = _install_fake_brep_plugin(monkeypatch)
    brep = Brep()

    class TestFace(BrepFace):
        def as_brep(self):
            return brep

    face = TestFace()
    assert face.to_tessellation(linear_deflection=0.1, angular_deflection=15.0) is tessellation
    assert calls == [(brep, 0.1, 15.0)]


def test_legacy_brep_tessellation_entry_points_are_removed():
    brep = Brep()

    assert not hasattr(brep, "tessellate")
    assert not hasattr(brep, "polygonize")
    assert not hasattr(brep, "to_polygonal_surface")
    assert not hasattr(brep, "to_meshes")
    assert not hasattr(brep, "to_tesselation")
    assert not hasattr(brep, "to_viewmesh")


def test_brep_copy_and_transform_dispatch(monkeypatch):
    calls = []

    def copy(brep):
        calls.append(("copy", brep))
        return Brep(native_brep=object())

    def transform(brep, transformation):
        calls.append(("transform", brep, transformation))

    implementations = {
        "brep_copy": copy,
        "brep_transform": transform,
    }

    def select(extension_point):
        method = implementations.get(extension_point.name)
        if method is None:
            return None
        return SimpleNamespace(id="tests.fake_brep", method=method)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)

    brep = Brep(native_brep=object(), name="source")
    copied = brep.copy(copy_guid=True)
    transformation = Translation.from_vector([1.0, 2.0, 3.0])
    brep.transform(transformation)

    assert type(copied) is Brep
    assert copied.native_brep is not brep.native_brep
    assert copied.name == brep.name
    assert copied.guid == brep.guid
    assert calls == [("copy", brep), ("transform", brep, transformation)]


def test_brep_bounds_dispatch(monkeypatch):
    calls = []
    aabb = Box(1.0)
    obb = Box(2.0)

    def axis_aligned_bounds(brep):
        calls.append(("aabb", brep))
        return aabb

    def oriented_bounds(brep):
        calls.append(("obb", brep))
        return obb

    implementations = {
        "brep_aabb": axis_aligned_bounds,
        "brep_obb": oriented_bounds,
    }

    def select(extension_point):
        method = implementations.get(extension_point.name)
        if method is None:
            return None
        return SimpleNamespace(id="tests.fake_brep", method=method)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)

    brep = Brep()

    assert brep.aabb is aabb
    assert brep.obb is obb
    assert calls == [("aabb", brep), ("obb", brep)]
