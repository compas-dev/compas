from compas.geometry.transformations import Translation


def test_translation():
    T = Translation([1, 2, 3])
    assert T.matrix == [[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 2.0], [0.0, 0.0, 1.0, 3.0], [0.0, 0.0, 0.0, 1.0]]
