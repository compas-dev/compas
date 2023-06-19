from compas.geometry import Vector


def test_cross_vectors():
    vec_list1 = [[1, 2, 3], [7, 8, 9]]
    vec_list2 = [[2, 3, 4], [5, 6, 7]]

    result = Vector.cross_vectors(vec_list1, vec_list2)
    assert result == [[-1, 2, -1], [2, -4, 2]]


def test_cross():
    vec1 = Vector(1, 2, 3)
    vec2 = [5, 6, 7]

    result = vec1.cross(vec2)
    assert result == (-4, 8, -4)
    assert result == Vector(-4, 8, -4)
