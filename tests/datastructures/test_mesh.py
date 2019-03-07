import pytest

import compas

from compas.datastructures import Mesh

@pytest.fixture
def polylines():
    boundary_polylines = [
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
        [[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
        [[2.0, 0.0, 0.0], [2.0, 1.0, 0.0]],
        [[2.0, 1.0, 0.0], [1.0, 1.0, 0.0]],
        [[1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
        [[0.0, 1.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    other_polylines = [
        [[1.0, 0.0, 0.0], [1.0, 0.25.0, 0.0], [1.0, 0.5, 0.0], [1.0, 0.75.0, 0.0], [1.0, 1.0, 0.0]]
    ]
    
    return boundary_polylines, other_polylines


def test_from_polylines():
    boundary_polylines, other_polylines = polylines
    mesh = Mesh.from_polylines(boundary_polylines, other_polylines)
    assert mesh.number_of_vertices() == 6
    assert mesh.number_of_faces() == 2
    assert network.number_of_edges() == 7
