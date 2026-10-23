from compas.geometry import distance_line_line
from compas.geometry import quadmesh_planarize


def test_quadmesh_planarize_has_default_implementation():
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0.2], [0, 1, 0]]
    faces = [[0, 1, 2, 3]]

    planarized = quadmesh_planarize((vertices, faces), kmax=10, maxdev=1e-6)

    diagonal_distance = distance_line_line(
        (planarized[0], planarized[2]),
        (planarized[1], planarized[3]),
    )
    assert diagonal_distance < 1e-6
    assert vertices == [[0, 0, 0], [1, 0, 0], [1, 1, 0.2], [0, 1, 0]]


def test_quadmesh_planarize_preserves_unused_vertices():
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [2, 2, 2]]

    planarized = quadmesh_planarize((vertices, [[0, 1, 2, 3]]), kmax=1)

    assert planarized[4] == [2, 2, 2]
