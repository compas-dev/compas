from typing import Any

import pytest

from compas.datastructures import Mesh
from compas.datastructures.mesh.smoothing import mesh_smooth_area
from compas.datastructures.mesh.smoothing import mesh_smooth_centerofmass
from compas.datastructures.mesh.smoothing import mesh_smooth_centroid
from compas.tolerance import TOL


SMOOTHING_FUNCTIONS = [
    mesh_smooth_centroid,
    mesh_smooth_centerofmass,
    mesh_smooth_area,
]


@pytest.fixture
def fan():
    return Mesh.from_vertices_and_faces(
        [[0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0], [1, 1, 1]],
        [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]],
    )


@pytest.mark.parametrize(
    ("smooth", "expected"),
    [
        (mesh_smooth_centroid, [1, 1, 0]),
        (mesh_smooth_centerofmass, [1, 1, 0]),
        (mesh_smooth_area, [1, 1, 1.0 / 3.0]),
    ],
)
def test_smoothing_moves_free_vertex_and_preserves_fixed_vertices(fan, smooth, expected):
    fixed = [0, 1, 2, 3]
    before = {vertex: fan.vertex_coordinates(vertex) for vertex in fixed}

    smooth(fan, fixed=fixed, kmax=1, damping=1.0)

    assert TOL.is_allclose(fan.vertex_coordinates(4), expected)
    assert all(TOL.is_allclose(fan.vertex_coordinates(vertex), before[vertex]) for vertex in fixed)


@pytest.mark.parametrize("smooth", SMOOTHING_FUNCTIONS)
def test_smoothing_calls_callback_after_each_iteration(fan, smooth):
    events = []
    callback_args = {"name": "smoothing"}

    smooth(
        fan,
        fixed=list(fan.vertices()),
        kmax=2,
        callback=lambda iteration, args: events.append((iteration, args)),
        callback_args=callback_args,
    )

    assert events == [(0, callback_args), (1, callback_args)]


@pytest.mark.parametrize("smooth", SMOOTHING_FUNCTIONS)
def test_smoothing_rejects_noncallable_callback(fan, smooth):
    callback: Any = 1
    with pytest.raises(TypeError, match="Callback is not callable"):
        smooth(fan, callback=callback)
