import math

import numpy as np

from compas._typing import Coordinate
from compas._typing import Coordinates
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.linalg import length_vector


class DuckCoordinate:
    def __init__(self, x, y, z):
        self.values = (x, y, z)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __iter__(self):
        return iter(self.values)


class IndexCoordinate:
    def __init__(self, x, y, z):
        self.values = (x, y, z)

    def __getitem__(self, key):
        return self.values[key]


def test_runtime_coordinate_protocol_behavior_is_preserved():
    coordinate = DuckCoordinate(np.float32(1), np.float64(2), 3)

    assert isinstance(coordinate, Coordinate)
    assert isinstance([coordinate], Coordinates)
    assert Point(1, 2, 3) == coordinate


def test_indexing_only_coordinate_remains_usable_by_duck_typing():
    coordinate = IndexCoordinate(1, 2, 2)

    assert not isinstance(coordinate, Coordinate)
    assert math.isclose(length_vector(coordinate), 3.0)


def test_builtin_bool_remains_usable_where_an_operation_allows_it():
    assert math.isclose(length_vector((True, False, False)), 1.0)


def test_datastructure_coordinate_annotations_do_not_add_conversion():
    vertices = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)
    mesh = Mesh.from_vertices_and_faces(vertices, [[0, 1, 2]])

    assert mesh.number_of_vertices() == 3
    assert mesh.vertex_coordinates(1) == [1.0, 0.0, 0.0]
