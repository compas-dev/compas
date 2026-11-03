from types import SimpleNamespace

import pytest  # pyright: ignore[reportMissingImports]

import compas.plugins
from compas.geometry import Brep
from compas.geometry import BrepFace
from compas.geometry import Deflection
from compas.geometry import Native
from compas.geometry import PolygonalSurface
from compas.geometry import Tessellation


def _install_fake_brep_plugin(monkeypatch):
    calls = []
    tessellation = Tessellation([[0.0, 0.0, 0.0]], [])
    polygonal = PolygonalSurface([[0.0, 0.0, 0.0]], [])

    def tessellate(brep, strategy):
        calls.append(("tessellate", brep, strategy))
        return tessellation

    def polygonize(brep, strategy):
        calls.append(("polygonize", brep, strategy))
        return polygonal

    implementations = {
        "brep_tessellate": tessellate,
        "brep_polygonize": polygonize,
    }

    def select(extension_point):
        method = implementations.get(extension_point.name)
        if method is None:
            return None
        return SimpleNamespace(id="tests.fake_brep", method=method)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)
    return calls, tessellation, polygonal


def test_brep_tessellation_operations_dispatch_exact_strategy(monkeypatch):
    calls, tessellation, polygonal = _install_fake_brep_plugin(monkeypatch)
    brep = Brep()
    strategy = Deflection(0.1, 15.0)

    assert brep.tessellate(strategy) is tessellation
    assert brep.polygonize(strategy) is polygonal
    assert calls == [
        ("tessellate", brep, strategy),
        ("polygonize", brep, strategy),
    ]


def test_brep_rejects_non_deflection_strategies_before_dispatch(monkeypatch):
    calls, _, _ = _install_fake_brep_plugin(monkeypatch)
    brep = Brep()

    with pytest.raises(TypeError, match="Deflection"):
        brep.tessellate(Native())  # pyright: ignore[reportArgumentType]
    with pytest.raises(TypeError, match="Deflection"):
        brep.polygonize(Native())  # pyright: ignore[reportArgumentType]

    assert calls == []


def test_brep_face_reuses_brep_plugin_boundary(monkeypatch):
    calls, tessellation, polygonal = _install_fake_brep_plugin(monkeypatch)
    brep = Brep()

    class TestFace(BrepFace):
        def as_brep(self):
            return brep

    face = TestFace()
    strategy = Deflection(0.1, 15.0)

    assert face.tessellate(strategy) is tessellation
    assert face.polygonize(strategy) is polygonal
    assert [call[1] for call in calls] == [brep, brep]


def test_legacy_brep_tessellation_entry_points_are_removed():
    brep = Brep()

    assert not hasattr(brep, "to_meshes")
    assert not hasattr(brep, "to_tessellation")
    assert not hasattr(brep, "to_tesselation")
    assert not hasattr(brep, "to_viewmesh")
