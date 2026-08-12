from typing import Any

import pytest

from compas.datastructures import Mesh
from compas.datastructures.mesh.subdivision import mesh_subdivide


@pytest.fixture
def mesh_tris():
    mesh = Mesh.from_polyhedron(6)
    mesh.quads_to_triangles()
    return mesh


@pytest.fixture
def mesh_quads():
    mesh = Mesh.from_polyhedron(6)
    return mesh


def test_quads_subdivide(mesh_quads):
    subd = mesh_quads.subdivided()
    assert subd.number_of_faces() == 4 * mesh_quads.number_of_faces()
    assert subd.number_of_vertices() == (mesh_quads.number_of_vertices() + mesh_quads.number_of_edges() + mesh_quads.number_of_faces())


def test_tris_subdivide(mesh_tris):
    subd = mesh_tris.subdivided()
    assert subd.number_of_faces() == 3 * mesh_tris.number_of_faces()
    assert subd.number_of_vertices() == (mesh_tris.number_of_vertices() + mesh_tris.number_of_edges() + mesh_tris.number_of_faces())


def test_quads_subdivide_tri(mesh_quads):
    subd = mesh_quads.subdivided(scheme="tri")
    assert subd.number_of_faces() == 4 * mesh_quads.number_of_faces()
    assert subd.number_of_vertices() == mesh_quads.number_of_vertices() + mesh_quads.number_of_faces()


def test_tris_subdivide_tri(mesh_tris):
    subd = mesh_tris.subdivided(scheme="tri")
    assert subd.number_of_faces() == 3 * mesh_tris.number_of_faces()
    assert subd.number_of_vertices() == mesh_tris.number_of_vertices() + mesh_tris.number_of_faces()


def test_quads_subdivide_quad(mesh_quads):
    subd = mesh_quads.subdivided(scheme="quad")
    assert subd.number_of_faces() == 4 * mesh_quads.number_of_faces()
    assert subd.number_of_vertices() == (mesh_quads.number_of_vertices() + mesh_quads.number_of_edges() + mesh_quads.number_of_faces())


def test_tris_subdivide_quad(mesh_tris):
    subd = mesh_tris.subdivided(scheme="quad")
    assert subd.number_of_faces() == 3 * mesh_tris.number_of_faces()
    assert subd.number_of_vertices() == (mesh_tris.number_of_vertices() + mesh_tris.number_of_edges() + mesh_tris.number_of_faces())


@pytest.mark.parametrize(
    ("scheme", "options", "vertices", "faces"),
    [
        ("tri", {}, 14, 24),
        ("quad", {}, 26, 24),
        ("corner", {}, 20, 30),
        ("catmullclark", {}, 26, 24),
        ("doosabin", {}, 24, 26),
        ("frames", {"offset": 0.1}, 32, 24),
        ("frames", {"offset": 0.1, "add_windows": True}, 32, 30),
    ],
)
def test_subdivision_schemes_have_expected_counts_and_preserve_source(mesh_quads, scheme, options, vertices, faces):
    source_data = mesh_quads.__data__

    subd = mesh_subdivide(mesh_quads, scheme=scheme, **options)

    assert subd.number_of_vertices() == vertices
    assert subd.number_of_faces() == faces
    assert subd.is_valid()
    assert mesh_quads.__data__ == source_data


def test_loop_subdivision_has_expected_counts_and_preserves_source(mesh_tris):
    source_data = mesh_tris.__data__

    subd = mesh_subdivide(mesh_tris, scheme="loop")

    assert subd.number_of_vertices() == 26
    assert subd.number_of_faces() == 48
    assert subd.is_valid()
    assert mesh_tris.__data__ == source_data


@pytest.mark.parametrize("scheme", ["tri", "quad", "corner", "catmullclark", "doosabin"])
def test_zero_subdivision_levels_returns_independent_copy(mesh_quads, scheme):
    subd = mesh_subdivide(mesh_quads, scheme=scheme, k=0)

    assert subd is not mesh_quads
    assert type(subd) is type(mesh_quads)
    assert subd.__data__ == mesh_quads.__data__


def test_zero_loop_subdivision_levels_returns_independent_copy(mesh_tris):
    subd = mesh_subdivide(mesh_tris, scheme="loop", k=0)

    assert subd is not mesh_tris
    assert type(subd) is type(mesh_tris)
    assert subd.__data__ == mesh_tris.__data__


def test_subdivision_preserves_mesh_type(mesh_quads):
    class CustomMesh(Mesh):
        pass

    mesh = CustomMesh.__from_data__(mesh_quads.__data__)

    assert type(mesh_subdivide(mesh, scheme="quad")) is CustomMesh


def test_subdivision_rejects_unsupported_scheme(mesh_quads):
    scheme: Any = "invalid"
    with pytest.raises(ValueError, match="not supported: invalid"):
        mesh_subdivide(mesh_quads, scheme=scheme)
