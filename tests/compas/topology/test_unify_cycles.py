import math
import os
import random

import compas
from compas.datastructures import Mesh
from compas.geometry import volume_polyhedron
from compas.tolerance import TOL
from compas.topology import unify_cycles

HERE = os.path.dirname(__file__)


def test_unify_cycles():
    if compas.IPY:
        return

    test_data = compas.json_load(os.path.join(HERE, "..", "fixtures", "topology", "vertices_faces.json"))
    vertices = test_data["vertices"]
    faces = test_data["faces"]

    max_edge_length = 22.386
    max_nbrs = 29
    volume = 1121.146165  # only correct if cycles are unified

    # no parameters
    unify_cycles(vertices, faces)
    assert TOL.is_close(volume, volume_polyhedron((vertices, faces)))

    # only max_nbrs
    unify_cycles(vertices, faces, nmax=max_nbrs)
    assert TOL.is_close(volume, volume_polyhedron((vertices, faces)))

    # only max_distance
    unify_cycles(vertices, faces, max_distance=max_edge_length)
    assert TOL.is_close(volume, volume_polyhedron((vertices, faces)))

    # both parameters
    unify_cycles(vertices, faces, nmax=max_nbrs, max_distance=max_edge_length)
    assert TOL.is_close(volume, volume_polyhedron((vertices, faces)))


def test_face_adjacency_and_unify_cycles():
    if compas.IPY:
        return
    for _ in range(10):
        nx = random.randint(5, 20)
        ny = random.randint(5, 20)
        dx = 10
        dy = 10
        mesh = Mesh.from_meshgrid(dx, nx, dy, ny)
        vertices, faces = mesh.to_vertices_and_faces()
        max_distance = math.sqrt((dx / nx) ** 2 + (dy / ny) ** 2) + TOL.absolute
        unify_cycles(vertices, faces, max_distance=max_distance)
        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        for face in mesh.faces():
            assert TOL.is_allclose(mesh.face_normal(face), [0, 0, 1])
