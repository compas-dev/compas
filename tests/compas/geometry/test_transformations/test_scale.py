from compas.geometry import Scale
from compas.geometry import Frame


def test_scale():
    S = Scale.from_factors([1, 2, 3])
    assert S.matrix == [[1.0, 0.0, 0.0, 0.0], [0.0, 2.0, 0.0, 0.0], [0.0, 0.0, 3.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

    S = Scale.from_factors([2.] * 3, Frame((2, 5, 0), (1, 0, 0), (0, 1, 0)))
    assert S.matrix == [[2.0, 0.0, 0.0, -2.0], [0.0, 2.0, 0.0, -5.0], [0.0, 0.0, 2.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
