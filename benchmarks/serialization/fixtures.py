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

from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.geometry import Bezier
from compas.geometry import Box
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Pointcloud
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Sphere
from compas.geometry import Transformation
from compas.geometry import Vector

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


def make_graph(n_nodes, seed=DEFAULT_SEED):
    """Build a deterministic jittered-grid graph with approximately ``n_nodes`` nodes.

    Nodes carry ``x``, ``y``, ``z`` coordinates; edges connect grid neighbours.

    Parameters
    ----------
    n_nodes : int
        Target number of nodes (nearest square of a ``side x side`` grid).
    seed : int, optional

    Returns
    -------
    :class:`compas.datastructures.Graph`
    """
    rng = random.Random(seed)
    side = max(2, int(round(math.sqrt(n_nodes))))
    graph = Graph()
    keys = {}
    for y in range(side):
        for x in range(side):
            keys[(x, y)] = graph.add_node(x=float(x), y=float(y), z=rng.uniform(-0.5, 0.5))
    for y in range(side):
        for x in range(side):
            if x < side - 1:
                graph.add_edge(keys[(x, y)], keys[(x + 1, y)])
            if y < side - 1:
                graph.add_edge(keys[(x, y)], keys[(x, y + 1)])
    return graph


def _make_primitive(kind, rng):
    def coord():
        return [rng.uniform(-100.0, 100.0) for _ in range(3)]

    if kind == "point":
        return Point(*coord())
    if kind == "vector":
        return Vector(*coord())
    if kind == "line":
        return Line(coord(), coord())
    if kind == "frame":
        # near-orthonormal axes with jitter so the frame is well-conditioned
        j = rng.uniform(-0.1, 0.1)
        return Frame(coord(), [1.0, j, j], [j, 1.0, j])
    if kind == "plane":
        return Plane(coord(), coord())
    if kind == "box":
        f = Frame(coord(), [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        return Box(rng.uniform(1.0, 10.0), rng.uniform(1.0, 10.0), rng.uniform(1.0, 10.0), frame=f)
    if kind == "sphere":
        return Sphere(rng.uniform(1.0, 10.0), point=Point(*coord()))
    if kind == "circle":
        f = Frame(coord(), [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        return Circle(rng.uniform(1.0, 10.0), frame=f)
    # Compound geometry — exercises the flat `repeated double` point arrays in compas_pb.
    if kind == "polyline":
        return Polyline([coord() for _ in range(8)])
    if kind == "polygon":
        return Polygon([coord() for _ in range(6)])
    if kind == "bezier":
        return Bezier([coord() for _ in range(4)])
    if kind == "polyhedron":
        return Polyhedron([coord() for _ in range(4)], [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])
    if kind == "transformation":
        return Transformation.from_frame(Frame(coord(), [1.0, 0.1, 0.0], [0.0, 1.0, 0.1]))
    raise ValueError("Unknown primitive kind: {}".format(kind))


def make_primitives(kind, count, seed=DEFAULT_SEED):
    """Build a deterministic list of ``count`` primitives of the given ``kind``.

    Collections of primitives (e.g. a list of frames as robot targets) are a common
    real-world payload; the harness measures the list as a whole.

    Parameters
    ----------
    kind : str
        One of point, vector, line, frame, plane, box, sphere, circle.
    count : int
    seed : int, optional

    Returns
    -------
    list[:class:`compas.data.Data`]
    """
    rng = random.Random(seed)
    return [_make_primitive(kind, rng) for _ in range(count)]


_PRIMITIVE_KINDS = [
    "point", "vector", "line", "frame", "plane", "box", "sphere", "circle",
    "polyline", "polygon", "bezier", "polyhedron", "transformation",
]


# Subject catalogue: label -> factory(size, seed) returning a Data object (or list of them).
# Sizes are selected by the runner (see run.py PRESETS / DEFAULT_SIZES).
SUBJECTS = {
    "mesh": lambda size, seed=DEFAULT_SEED: make_mesh(size, with_attributes=False, seed=seed),
    "mesh_attrs": lambda size, seed=DEFAULT_SEED: make_mesh(size, with_attributes=True, seed=seed),
    "pointcloud": lambda size, seed=DEFAULT_SEED: make_pointcloud(size, seed=seed),
    "graph": lambda size, seed=DEFAULT_SEED: make_graph(size, seed=seed),
}
# One subject per primitive kind (pluralized label), each a list of `size` primitives.
for _kind in _PRIMITIVE_KINDS:
    _label = _kind + ("es" if _kind.endswith("x") else "s")
    SUBJECTS[_label] = (lambda k: lambda size, seed=DEFAULT_SEED: make_primitives(k, size, seed=seed))(_kind)
