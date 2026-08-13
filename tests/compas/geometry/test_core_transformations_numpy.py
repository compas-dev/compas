import numpy as np

from compas.geometry import dehomogenize_and_unflatten_frames_numpy
from compas.geometry import dehomogenize_numpy
from compas.geometry import homogenize_and_flatten_frames_numpy
from compas.geometry import homogenize_numpy
from compas.geometry import local_to_world_coordinates_numpy
from compas.geometry import transform_frames_numpy
from compas.geometry import transform_points_numpy
from compas.geometry import transform_vectors_numpy
from compas.geometry import world_to_local_coordinates_numpy


TRANSLATION = [
    [1.0, 0.0, 0.0, 4.0],
    [0.0, 1.0, 0.0, 5.0],
    [0.0, 0.0, 1.0, 6.0],
    [0.0, 0.0, 0.0, 1.0],
]


def test_transform_points_and_vectors_numpy():
    data = [[1.0, 2.0, 3.0], [-1.0, -2.0, -3.0]]

    assert np.allclose(transform_points_numpy(data, TRANSLATION), [[5, 7, 9], [3, 3, 3]])
    assert np.allclose(transform_vectors_numpy(data, TRANSLATION), data)


def test_transform_frames_numpy():
    frames = [[[1.0, 2.0, 3.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]]

    transformed = transform_frames_numpy(frames, TRANSLATION)

    assert transformed.shape == (1, 3, 3)
    assert np.allclose(transformed, [[[5, 7, 9], [1, 0, 0], [0, 1, 0]]])


def test_homogenize_and_dehomogenize_numpy():
    data = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]

    points = homogenize_numpy(data)
    vectors = homogenize_numpy(data, w=0.0)

    assert np.allclose(points, [[1, 2, 3, 1], [4, 5, 6, 1]])
    assert np.allclose(vectors, [[1, 2, 3, 0], [4, 5, 6, 0]])
    assert np.allclose(dehomogenize_numpy(points), data)
    assert np.allclose(dehomogenize_numpy(vectors), data)


def test_flatten_and_unflatten_frames_numpy():
    frames = [
        [[1.0, 2.0, 3.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        [[4.0, 5.0, 6.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    ]

    flattened = homogenize_and_flatten_frames_numpy(frames)
    unflattened = dehomogenize_and_unflatten_frames_numpy(flattened)

    assert flattened.shape == (6, 4)
    assert np.allclose(unflattened, frames)


def test_local_and_world_coordinates_numpy_roundtrip():
    frame = [[1.0, 2.0, 3.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    world = [[2.0, 4.0, 6.0], [-1.0, -2.0, -3.0]]

    local = world_to_local_coordinates_numpy(frame, world)

    assert np.allclose(local, [[1, 2, 3], [-2, -4, -6]])
    assert np.allclose(local_to_world_coordinates_numpy(frame, local), world)
