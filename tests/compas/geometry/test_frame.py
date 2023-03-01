from compas.geometry import Frame


def test_axes_are_orthonormal():
    pt = [1, 2, 3]
    vec1 = [1, 0, 0]
    vec2 = [0, 0.9, 0]

    frame = Frame(pt, vec1, vec2)
    assert frame == [[1, 2, 3], [1, 0, 0], [0, 1, 0]]
