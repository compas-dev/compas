from types import SimpleNamespace

import pytest  # pyright: ignore[reportMissingImports]

import compas.plugins
from compas.geometry import Brep


QUERY_PROPERTIES = {
    "orientation": "brep_orientation",
    "type": "brep_type",
    "is_valid": "brep_is_valid",
    "is_orientable": "brep_is_orientable",
    "is_closed": "brep_is_closed",
    "is_infinite": "brep_is_infinite",
    "is_convex": "brep_is_convex",
    "is_manifold": "brep_is_manifold",
    "is_surface": "brep_is_surface",
    "is_compound": "brep_is_compound",
    "is_compoundsolid": "brep_is_compoundsolid",
    "is_shell": "brep_is_shell",
    "is_solid": "brep_is_solid",
    "vertices": "brep_vertices",
    "edges": "brep_edges",
    "trims": "brep_trims",
    "loops": "brep_loops",
    "faces": "brep_faces",
    "shells": "brep_shells",
    "solids": "brep_solids",
}


@pytest.mark.parametrize(("property_name", "plugin_name"), QUERY_PROPERTIES.items())
def test_brep_query_properties_dispatch_independently(monkeypatch, property_name, plugin_name):
    calls = []
    expected = object()

    def query(brep):
        calls.append(brep)
        return expected

    def select(extension_point):
        if extension_point.name == plugin_name:
            return SimpleNamespace(id="tests.fake_brep_query", method=query)
        return None

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)
    brep = Brep()

    assert getattr(brep, property_name) is expected
    assert calls == [brep]


def test_unsupported_brep_query_does_not_disable_supported_queries(monkeypatch):
    def vertices(brep):
        return [brep]

    def trims(brep):
        raise NotImplementedError("The backend does not provide Brep trims.")

    implementations = {
        "brep_vertices": vertices,
        "brep_trims": trims,
    }

    def select(extension_point):
        method = implementations.get(extension_point.name)
        if method is None:
            return None
        return SimpleNamespace(id="tests.fake_brep_query", method=method)

    monkeypatch.setattr(compas.plugins.plugin_manager, "select", select)
    brep = Brep()

    assert brep.vertices == [brep]
    with pytest.raises(NotImplementedError, match="does not provide Brep trims"):
        brep.trims
