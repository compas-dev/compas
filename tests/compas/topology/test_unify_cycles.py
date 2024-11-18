import math
import os
import random

import compas
from compas.datastructures import Mesh
from compas.tolerance import TOL
from compas.topology import unify_cycles

HERE = os.path.dirname(__file__)


def test_unify_cycles():
    if compas.IPY:
        return
    test_data = compas.json_load(os.path.join(HERE, "..", "fixtures", "topology", "vertices_faces.json"))
    vertices = test_data["vertices"]
    faces = test_data["faces"]
    unify_cycles(vertices, faces)
    unify_cycles(vertices, faces, nmax=29, max_distance=22.4)  # anything below won't work


def test_face_adjacency():
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
