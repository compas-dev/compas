from compas.geometry import Plane


def test_from_point_and_two_vectors():
    pt = [1, 2, 3]
    vec1 = [1, 0, 0]
    vec2 = [0, 1, 0]

    result = Plane.from_point_and_two_vectors(pt, vec1, vec2)
    assert result == [[1, 2, 3], [0, 0, 1]]


def test_from_three_points():
    pt1 = [0, 0, 0]
    pt2 = [1, 0, 0]
    pt3 = [0, 1, 0]

    result = Plane.from_three_points(pt1, pt2, pt3)
    assert result == ([0, 0, 0], [0, 0, 1])
