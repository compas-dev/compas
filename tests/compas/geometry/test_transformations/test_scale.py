from compas.geometry.transformations import Scale


def test_scale():
    S = Scale([1, 2, 3])
    assert S.matrix == [[1.0, 0.0, 0.0, 0.0], [0.0, 2.0, 0.0, 0.0], [0.0, 0.0, 3.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
