"""Deterministic, seeded fixtures for the serialization benchmark.

Two subjects stand in for "large numeric payloads" (PRD 10.1):

* ``Mesh`` -- vertices (float64 x3) + integer face indices. Generated as a jittered
  grid so the vertex/face counts and coordinates are reproducible. A ``with_attributes``
  variant attaches a per-vertex float, exposing the hybrid-layout cost that a columnar
  format cannot flatten.
* ``Pointcloud`` -- N points (float64 x3). The COMPAS ``Pointcloud`` type has no
  per-point attribute slot, so only a points-only variant exists here; the Mesh
  attribute variant carries the "with per-element attributes" case.

All generators are seeded so runs are comparable and fixtures are reused across
every format under test.
"""

import math
import random

from compas.datastructures import Mesh
from compas.geometry import Pointcloud

DEFAULT_SEED = 42


def make_mesh(n_vertices, with_attributes=False, seed=DEFAULT_SEED):
    """Build a deterministic jittered-grid mesh with approximately ``n_vertices`` vertices.

    Parameters
    ----------
    n_vertices : int
        Target number of vertices. The mesh is a ``side x side`` grid with
        ``side = round(sqrt(n_vertices))``, so the actual count is the nearest square.
    with_attributes : bool, optional
        If True, attach a seeded per-vertex float attribute (``quality``).
    seed : int, optional
        Seed for the coordinate jitter and attributes.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
    """
    rng = random.Random(seed)
    side = max(2, int(round(math.sqrt(n_vertices))))

    vertices = []
    for y in range(side):
        for x in range(side):
            vertices.append([float(x), float(y), rng.uniform(-0.5, 0.5)])

    faces = []
    for y in range(side - 1):
        for x in range(side - 1):
            i = y * side + x
            faces.append([i, i + 1, i + 1 + side, i + side])

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    if with_attributes:
        for vertex in mesh.vertices():
            mesh.vertex_attribute(vertex, "quality", rng.uniform(0.0, 1.0))

    return mesh


def make_pointcloud(n_points, seed=DEFAULT_SEED):
    """Build a deterministic pointcloud of ``n_points`` float64 points.

    Parameters
    ----------
    n_points : int
        Number of points.
    seed : int, optional
        Seed for the point coordinates.

    Returns
    -------
    :class:`compas.geometry.Pointcloud`
    """
    rng = random.Random(seed)
    points = [[rng.uniform(-100.0, 100.0), rng.uniform(-100.0, 100.0), rng.uniform(-100.0, 100.0)] for _ in range(n_points)]
    return Pointcloud(points)


# Subject catalogue: (label, factory taking a size -> Data object).
# Sizes follow PRD 10.1 but are selected by the runner (see run.py --sizes / --quick).
SUBJECTS = {
    "mesh": lambda size, seed=DEFAULT_SEED: make_mesh(size, with_attributes=False, seed=seed),
    "mesh_attrs": lambda size, seed=DEFAULT_SEED: make_mesh(size, with_attributes=True, seed=seed),
    "pointcloud": lambda size, seed=DEFAULT_SEED: make_pointcloud(size, seed=seed),
}
