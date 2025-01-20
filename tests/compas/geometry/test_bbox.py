import pytest
import os
import compas
from random import random
from compas.tolerance import TOL
from compas.datastructures import Mesh
from compas.geometry import Box
from compas.geometry import bounding_box
from compas.geometry import bounding_box_xy

HERE = os.path.dirname(__file__)


@pytest.mark.parametrize(
    "coords,expected",
    [
        [
            [[0, 0], [1, 2], [-5, 6], [-3, 2], [0.5, -1]],
            [[-5, -1, 0.0], [1, -1, 0.0], [1, 6, 0.0], [-5, 6, 0.0]],
        ],
        [
            [
                [6.74219, -53.57835],
                [6.74952, -53.57241],
                [6.75652, -53.56289],
                [6.74756, -53.56598],
                [6.73462, -53.57518],
            ],
            [
                [6.73462, -53.57835, 0.0],
                [6.75652, -53.57835, 0.0],
                [6.75652, -53.56289, 0.0],
                [6.73462, -53.56289, 0.0],
            ],
        ],
    ],
)
def test_bounding_box_xy(coords, expected):
    assert expected == bounding_box_xy(coords)


@pytest.mark.parametrize(
    "coords,expected",
    [
        [
            [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [
                [0, 0, 0],
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 1],
                [1, 1, 1],
                [0, 1, 1],
            ],
        ]
    ],
)
def test_bounding_box(coords, expected):
    assert expected == bounding_box(coords)


@pytest.mark.parametrize(
    "coords,expected",
    [
        [
            [[0, 0], [1, 2], [-5, 6], [-3, 2], [0.5, -1]],
            [
                [-6.129411764705883, 4.682352941176471, 0.0],
                [0.5, -1.0, 0.0],
                [2.1941176470588237, 0.976470588235294, 0.0],
                [-4.435294117647059, 6.658823529411765, 0.0],
            ],
        ],
        [
            [
                [6.74219, -53.57835],
                [6.74952, -53.57241],
                [6.75652, -53.56289],
                [6.74756, -53.56598],
                [6.73462, -53.57518],
            ],
            [
                [6.754970846941253, -53.56071108254564, 0.0],
                [6.73462, -53.57518, 0.0],
                [6.738658767139154, -53.58086061378051, 0.0],
                [6.759009614080408, -53.56639169632614, 0.0],
            ],
        ],
    ],
)
def test_oriented_bounding_box_xy_numpy(coords, expected):
    if compas.IPY:
        return

    from compas.geometry import oriented_bounding_box_xy_numpy

    assert expected == oriented_bounding_box_xy_numpy(coords)


@pytest.mark.parametrize(
    "coords,expected",
    [
        [
            [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
            [
                [0.0, 0.0, 1.0],
                [0.0, 1.0, 0.0],
                [1.0, 0.5, -0.5],
                [1.0, -0.5, 0.5],
                [-0.3333333333333333, -0.3333333333333333, 0.6666666666666667],
                [-0.3333333333333333, 0.6666666666666667, -0.33333333333333326],
                [0.6666666666666667, 0.1666666666666667, -0.8333333333333333],
                [0.6666666666666667, -0.8333333333333333, 0.16666666666666674],
            ],
        ]
    ],
)
def test_oriented_bounding_box_numpy(coords, expected):
    if compas.IPY:
        return

    from compas.geometry import oriented_bounding_box_numpy

    results = oriented_bounding_box_numpy(coords)
    for result, expected_values in zip(results, expected):
        assert TOL.is_allclose(result, expected_values)


def test_oriented_bounding_box_numpy_from_fixtures():
    if compas.IPY:
        return

    coords = compas.json_load(os.path.join(HERE, "fixtures", "bbox_points_00.json"))
    expected = [
        [-16.324597659837302, 17.160372549942966, 3.56729],
        [-16.324597659837302, 17.160372549942966, 2.45],
        [-15.960798521686625, 13.229144025284555, 2.45],
        [-15.960798521686625, 13.229144025284555, 3.56729],
        [-18.2385089496689, 16.983257616692406, 3.56729],
        [-18.2385089496689, 16.983257616692406, 2.45],
        [-17.874709811518226, 13.052029092033992, 2.45],
        [-17.874709811518226, 13.052029092033992, 3.56729],
    ]

    from compas.geometry import oriented_bounding_box_numpy

    results = oriented_bounding_box_numpy(coords)
    for result, expected_values in zip(results, expected):
        assert TOL.is_allclose(result, expected_values)


def test_oriented_bounding_box_numpy_flat():
    if compas.IPY:
        return

    from compas.geometry import oriented_bounding_box_numpy

    points = [[10 * random(), 10 * random(), 0] for i in range(100)]
    box = Box.from_bounding_box(oriented_bounding_box_numpy(points))

    for point in points:
        assert box.contains_point(point)

    assert not box.contains_point([10 * random(), 10 * random(), 1])

    points = [[10 * random(), 10 * random(), 10] for i in range(100)]
    box = Box.from_bounding_box(oriented_bounding_box_numpy(points))

    for point in points:
        assert box.contains_point(point)

    assert not box.contains_point([10 * random(), 10 * random(), 11])


def test_minimum_area_rectangle_xy():
    if compas.IPY:
        return

    from compas.geometry import bbox_numpy
    import numpy as np

    mesh = Mesh.from_obj(os.path.join(HERE, "fixtures", "bbox_rect_bad.obj"))
    points, _ = mesh.to_vertices_and_faces()
    expected = [[359.481028, 229.73229169], [256.84043629, 120.92493596], [295.67358196, 84.29269706], [398.31417367, 193.10005279]]

    min_bbox = bbox_numpy.minimum_area_rectangle_xy(np.array(points))

    assert TOL.is_allclose([(x, y) for x, y in min_bbox], expected)


def test_minimum_area_rectangle_xy_translated():
    if compas.IPY:
        return

    from compas.geometry import bbox_numpy
    import numpy as np

    mesh = Mesh.from_obj(os.path.join(HERE, "fixtures", "bbox_rect_good.obj"))
    points, _ = mesh.to_vertices_and_faces()
    expected = [[307.39472429, 358.36965131], [204.75412877, 249.56229154], [243.58728967, 212.93003827], [346.22788519, 321.73739804]]

    min_bbox = bbox_numpy.minimum_area_rectangle_xy(np.array(points))

    assert TOL.is_allclose([(x, y) for x, y in min_bbox], expected)
