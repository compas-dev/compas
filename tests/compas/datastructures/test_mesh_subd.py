import pytest

from compas.datastructures import Mesh
from compas.datastructures import mesh_subdivide


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
    subd = mesh_subdivide(mesh_quads)
    assert subd.number_of_faces() == 4 * mesh_quads.number_of_faces()
    assert subd.number_of_vertices() == (mesh_quads.number_of_vertices() +
                                         mesh_quads.number_of_edges() +
                                         mesh_quads.number_of_faces())


def test_tris_subdivide(mesh_tris):
    subd = mesh_subdivide(mesh_tris)
    assert subd.number_of_faces() == 3 * mesh_tris.number_of_faces()
    assert subd.number_of_vertices() == (mesh_tris.number_of_vertices() +
                                         mesh_tris.number_of_edges() +
                                         mesh_tris.number_of_faces())


def test_quads_subdivide_tri(mesh_quads):
    subd = mesh_subdivide(mesh_quads, scheme='tri')
    assert subd.number_of_faces() == 4 * mesh_quads.number_of_faces()
    assert subd.number_of_vertices() == mesh_quads.number_of_vertices() + mesh_quads.number_of_faces()


def test_tris_subdivide_tri(mesh_tris):
    subd = mesh_subdivide(mesh_tris, scheme='tri')
    assert subd.number_of_faces() == 3 * mesh_tris.number_of_faces()
    assert subd.number_of_vertices() == mesh_tris.number_of_vertices() + mesh_tris.number_of_faces()


def test_quads_subdivide_quad(mesh_quads):
    subd = mesh_subdivide(mesh_quads, scheme='quad')
    assert subd.number_of_faces() == 4 * mesh_quads.number_of_faces()
    assert subd.number_of_vertices() == (mesh_quads.number_of_vertices() +
                                         mesh_quads.number_of_edges() +
                                         mesh_quads.number_of_faces())


def test_tris_subdivide_quad(mesh_tris):
    subd = mesh_subdivide(mesh_tris, scheme='quad')
    assert subd.number_of_faces() == 3 * mesh_tris.number_of_faces()
    assert subd.number_of_vertices() == (mesh_tris.number_of_vertices() +
                                         mesh_tris.number_of_edges() +
                                         mesh_tris.number_of_faces())
