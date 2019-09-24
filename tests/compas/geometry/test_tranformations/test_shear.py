from compas.geometry.transformations import Shear


def test_shear():
    S = Shear(1)
    assert S.matrix == [[1.0, 0.0, 1.557407724654902, -1.557407724654902], [0.0, 1.0, 0.0, -0.0], [0.0, 0.0, 1.0, -0.0], [0.0, 0.0, 0.0, 1.0]]


def test_from_entries():
    shear1 = [-0.41, -0.14, -0.35]
    S = Shear.from_entries(shear1)
    assert S.matrix == [[1.0, -0.41, -0.14, 0.0], [0.0, 1.0, -0.35, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
