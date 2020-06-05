from compas.geometry import Projection


def test_projection_orthogonal():
    point = [0, 0, 0]
    normal = [0, 0, 1]
    P = Projection.from_plane((point, normal))
    assert P.matrix == [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def test_projection_parallel():
    point = [0, 0, 0]
    normal = [0, 0, 1]
    direction = [1, 1, 1]
    P = Projection.from_plane_and_direction((point, normal), direction)
    assert P.matrix == [[1.0, 0.0, -1.0, 0.0], [0.0, 1.0, -1.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]]


def test_projection_perspective():
    point = [0, 0, 0]
    normal = [0, 0, 1]
    perspective = [1, 1, 0]
    P = Projection.from_plane_and_point((point, normal), perspective)
    assert P.matrix == [[0.0, 0.0, -1.0, 0.0], [0.0, 0.0, -1.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, -1.0, 0.0]]


def test_projection_entries():
    persp1 = [0.3, 0.1, 0.1, 1]
    P1 = Projection.from_entries(persp1)
    assert P1.matrix == [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.3, 0.1, 0.1, 1.0]]
