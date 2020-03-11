from compas.geometry import Reflection
from compas.geometry import Transformation
from compas.geometry import Frame


def test_reflection():
    point = [1, 1, 1]
    normal = [0, 0, 1]
    R1 = Reflection(point, normal)
    R2 = Transformation.from_matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 2], [0, 0, 0, 1]])
    assert R1 == R2


def test_reflection_from_frame():
    point = [1, 1, 1]
    x = [1, 0, 0]
    y = [0, 1, 0]

    f = Frame(point, x, y)
    R1 = Reflection.from_frame(f)
    R2 = Transformation.from_matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 2], [0, 0, 0, 1]])
    assert R1 == R2
