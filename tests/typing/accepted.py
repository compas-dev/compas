from collections.abc import Iterator
from collections.abc import Mapping
from decimal import Decimal
from typing import SupportsFloat
from typing import assert_type
from typing import overload

import numpy as np

from compas.typing import PointLike
from compas.typing import PointGroupsLike
from compas.typing import PointsLike
from compas.typing import Float64Array
from compas.typing import FloatSequenceLike
from compas.typing import FloatingArray
from compas.typing import IndicesLike
from compas.typing import Int32Array
from compas.typing import IntegerArray
from compas.typing import IntegralInput
from compas.typing import NumericArray
from compas.typing import RealInput
from compas.typing import VectorLike
from compas.typing import VerticesFaces
from compas.geometry import Point
from compas.geometry import Pointcloud
from compas.geometry import Polygon
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Quaternion
from compas.geometry import Transformation
from compas.geometry import Circle
from compas.geometry import Tessellation
from compas.geometry import Triangulator
from compas.geometry import Vector
from compas.geometry import boolean_union_mesh_mesh
from compas.geometry import closest_point_on_polygon_xy
from compas.geometry import closest_point_on_polyline_xy
from compas.geometry import intersection_mesh_mesh
from compas.geometry import intersection_line_plane
from compas.geometry import intersection_plane_circle
from compas.geometry import intersection_ray_mesh
from compas.geometry import is_polygon_in_polygon_xy
from compas.geometry import orthonormalize_axes
from compas.geometry import constrained_delaunay_triangulation
from compas.geometry import delaunay_triangulation
from compas.geometry import trimesh_remesh
from compas.geometry import trimesh_remesh_along_isoline
from compas.geometry import trimesh_remesh_constrained
from compas.geometry import trimesh_slice
from compas.geometry import trimesh_geodistance
from compas.geometry import trimesh_harmonic
from compas.geometry import trimesh_isolines
from compas.geometry import trimesh_lscm
from compas.geometry import trimesh_massmatrix
from compas.geometry import transform_points
from compas.geometry._core.predicates_2 import is_intersection_segment_segment_xy
from compas.geometry.triangulation import triangulate_polygon
from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.scene import SceneAttributeUpdate
from compas.scene import SceneObject
from compas.scene import SceneStateField


class CustomCoordinate:
    def __init__(self, values: tuple[float, float, float]):
        self.values = values

    def __len__(self) -> int:
        return len(self.values)

    @overload
    def __getitem__(self, key: int) -> float: ...

    @overload
    def __getitem__(self, key: slice) -> tuple[float, ...]: ...

    def __getitem__(self, key: int | slice) -> float | tuple[float, ...]:
        return self.values[key]

    def __iter__(self) -> Iterator[float]:
        return iter(self.values)


class CustomCoordinates:
    def __init__(self, values: list[CustomCoordinate]):
        self.values = values

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, key: int) -> CustomCoordinate:
        return self.values[key]

    def __iter__(self) -> Iterator[CustomCoordinate]:
        return iter(self.values)


class CustomIndices:
    def __init__(self, values: tuple[int, int, int]):
        self.values = values

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, key: int) -> int:
        return self.values[key]

    def __iter__(self) -> Iterator[int]:
        return iter(self.values)


class CustomTriangles:
    def __init__(self, values: list[CustomIndices]):
        self.values = values

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, key: int) -> CustomIndices:
        return self.values[key]

    def __iter__(self) -> Iterator[CustomIndices]:
        return iter(self.values)


class CustomPolylines:
    def __init__(self, values: list[CustomCoordinates]):
        self.values = values

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, key: int) -> CustomCoordinates:
        return self.values[key]

    def __iter__(self) -> Iterator[CustomCoordinates]:
        return iter(self.values)


real_inputs: list[RealInput] = [True, 1, 1.0, np.int32(1), np.int64(1), np.float32(1), np.float64(1)]
integral_inputs: list[IntegralInput] = [True, 1, np.int32(1), np.int64(1)]

float32_array: FloatingArray = np.asarray([1, 2, 3], dtype=np.float32)
float64_array: Float64Array = np.asarray([1, 2, 3], dtype=np.float64)
int32_array: Int32Array = np.asarray([1, 2, 3], dtype=np.int32)
int64_array: IntegerArray = np.asarray([1, 2, 3], dtype=np.int64)
numeric_arrays: list[NumericArray] = [float32_array, float64_array, int32_array, int64_array]
memoryview_input: PointLike = memoryview(np.asarray([1.0, 2.0, 3.0], dtype=np.float64))


def accepts_supports_float(value: SupportsFloat) -> None:
    pass


for real_input_value in real_inputs:
    accepts_supports_float(real_input_value)

coordinate_inputs: list[PointLike] = [
    [1, 2, 3],
    (1.0, 2.0, 3.0),
    Point(1, 2, 3),
    Vector(1, 2, 3),
    CustomCoordinate((1, 2, 3)),
    float32_array,
    int64_array,
]
vector_inputs: list[VectorLike] = coordinate_inputs
real_vector: list[RealInput] = [np.float32(1), np.float64(2), 3]

Point(0, 0, 0).translate(real_vector)
assert_type(Point(0, 0, 0).translated(float32_array), Point)


def coordinate_arithmetic(coordinate: PointLike) -> RealInput:
    subsection: FloatSequenceLike = coordinate[:2]
    return subsection[0] + coordinate[2]


def assign_structural_components(point: PointLike, vector: VectorLike) -> None:
    target_point = Point(0, 0, 0)
    target_vector = Vector(0, 0, 0)
    target_point.x = point[0]
    target_vector.x = vector[0]


Plane(float32_array, int64_array)
Line(float32_array, float64_array)
Frame(float32_array, float64_array, int64_array)
Circle(np.float32(1.0))
Transformation.from_euler_angles(float32_array)
Transformation.from_euler_angles([Decimal("0"), Decimal("0"), Decimal("0")])
quaternion = Quaternion(1, 0, 0, 0)
quaternion_input: FloatSequenceLike = quaternion
assert_type(quaternion[:2], list[float])
intersection_line_plane(np.asarray([[0, 0, -1], [0, 0, 1]], dtype=np.float32), np.asarray([[0, 0, 0], [0, 0, 1]], dtype=np.int64))
intersection_plane_circle(
    np.asarray([[0, 0, 0], [0, 0, 1]], dtype=np.float32),
    (np.asarray([[0, 0, 0], [0, 0, 1]], dtype=np.float64), np.float32(1.0)),
)
assert_type(
    closest_point_on_polyline_xy(float32_array, np.asarray([[0, 0, 0], [1, 0, 0]], dtype=np.float32)),
    list[RealInput],
)
assert_type(
    closest_point_on_polygon_xy(float32_array, np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)),
    list[RealInput],
)
assert_type(orthonormalize_axes(float32_array, int64_array), tuple[list[RealInput], list[RealInput]])
transform_points(np.asarray([[1, 2, 3]], dtype=np.float32), np.eye(4, dtype=np.float64))
Point(1, 2, 3).transform(np.eye(4, dtype=np.float64))
Transformation([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
Transformation(
    [
        [np.float64(1), np.float64(0), np.float64(0), np.float64(0)],
        [np.float64(0), np.float64(1), np.float64(0), np.float64(0)],
        [np.float64(0), np.float64(0), np.float64(1), np.float64(0)],
        [np.float64(0), np.float64(0), np.float64(0), np.float64(1)],
    ]
)
coordinates_inputs: list[PointsLike] = [coordinate_inputs, np.asarray([[0, 0, 0], [1, 1, 1]], dtype=np.float64)]
Graph.from_pointcloud(Pointcloud(coordinates_inputs[1]))
Graph.from_pointcloud((point for point in coordinates_inputs[1]))
outer_polygon = Polygon([[0, 0, 0], [2, 0, 0], [2, 2, 0], [0, 2, 0]])
inner_polygon = Polygon([[0.5, 0.5, 0], [1.5, 0.5, 0], [1, 1.5, 0]])
is_polygon_in_polygon_xy(outer_polygon, inner_polygon)
assert_type(
    is_intersection_segment_segment_xy([[0, 0, 0], [1, 1, 0]], [[0, 1, 0], [1, 0, 0]]),
    bool | np.bool_,
)
assert_type(
    is_intersection_segment_segment_xy(
        np.asarray([[0, 0, 0], [1, 1, 0]], dtype=np.float32),
        np.asarray([[0, 1, 0], [1, 0, 0]], dtype=np.float64),
    ),
    bool | np.bool_,
)
coordinates_collection_inputs: list[PointGroupsLike] = [
    [coordinates_inputs[1]],
    np.asarray([[[0, 0, 0], [1, 0, 0], [0, 1, 0]]], dtype=np.float32),
]
indices_inputs: list[IndicesLike] = [[0, 1, 2], (np.int32(0), np.int64(1)), int32_array, int64_array]

vertices32 = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)
triangles32 = np.asarray([[0, 1, 2]], dtype=np.int32)
vertices64 = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float64)
triangles64 = np.asarray([[0, 1, 2]], dtype=np.int64)
triangle_mesh_inputs: list[VerticesFaces] = [
    ([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], [[0, 1, 2]]),
    (((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)), ((0, 1, 2),)),
    (vertices32, triangles32),
    (vertices64, triangles64),
]
boolean_union_mesh_mesh(triangle_mesh_inputs[0], triangle_mesh_inputs[1])
boolean_union_mesh_mesh((vertices32, triangles32), (vertices64, triangles64))
trimesh_remesh((vertices32, triangles32), 0.5)
trimesh_remesh_constrained((vertices32, triangles32), 0.5, [[0, 1]])
trimesh_remesh_along_isoline((vertices32, triangles32), np.asarray([0.0, 1.0, 0.0], dtype=np.float32), 0.5)
intersection_mesh_mesh((vertices32, triangles32), (vertices64, triangles64))
trimesh_slice((vertices32, triangles32), [([0.0, 0.0, 0.0], [0.0, 0.0, 1.0])])
intersection_ray_mesh(([0.0, 0.0, -1.0], [0.0, 0.0, 1.0]), (vertices32, triangles32))
trimesh_geodistance((vertices32, triangles32), 0)
trimesh_isolines((vertices32, triangles32), np.asarray([0, 1, 0], dtype=np.int64))
trimesh_massmatrix((vertices32, triangles32))
trimesh_harmonic((vertices32, triangles32))
trimesh_lscm((vertices32, triangles32))
normals64 = np.asarray([[0, 0, 1]] * 3, dtype=np.float64)
uvs32 = np.asarray([[0, 0], [1, 0], [0, 1]], dtype=np.float32)
polylines64 = np.asarray([[[0, 0, 0], [1, 0, 0]]], dtype=np.float64)
tessellation = Tessellation(vertices32, triangles32, normals64, uvs32, polylines64)
assert_type(tessellation.vertices, np.ndarray[tuple[int, int], np.dtype[np.float32]])
assert_type(tessellation.triangles, np.ndarray[tuple[int, int], np.dtype[np.int32]])
assert_type(
    tessellation.to_vertices_and_triangles(),
    tuple[
        np.ndarray[tuple[int, int], np.dtype[np.float32]],
        np.ndarray[tuple[int, int], np.dtype[np.int32]],
    ],
)
custom_vertices = CustomCoordinates([CustomCoordinate((0.0, 0.0, 0.0))])
custom_triangles = CustomTriangles([CustomIndices((0, 0, 0))])
custom_polylines = CustomPolylines([custom_vertices])
custom_tessellation = Tessellation(custom_vertices, custom_triangles, polylines=custom_polylines)
assert_type(custom_tessellation.vertices, CustomCoordinates)
assert_type(custom_tessellation.triangles, CustomTriangles)
Mesh.from_vertices_and_faces(vertices32, triangles32)

delaunay_triangulation(vertices32)
triangulate_polygon(vertices32)


def numpy_triangulator(vertices: PointsLike) -> np.ndarray[tuple[int, int], np.dtype[np.int64]]:
    return np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64)


triangulator: Triangulator = numpy_triangulator
Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]).triangulated(triangulator)
constrained_delaunay_triangulation(
    vertices32,
    holes=np.asarray([vertices32], dtype=np.float32),
    constraints=np.asarray([vertices32[:2]], dtype=np.float64),
    points=np.asarray([[0.25, 0.25, 0]], dtype=np.int64),
)


def update_sceneobject(owner: "CustomSceneObject", value: object) -> None:
    if not isinstance(value, (int, float)):
        raise TypeError
    owner.value = float(value)


class CustomSceneObject(SceneObject):
    __scene_state_namespace__ = "test.typing.CustomSceneObject"
    __scene_state_fields__ = (SceneStateField("value", (int, float), required=False, editable=True, update=update_sceneobject),)

    def __init__(self) -> None:
        super().__init__()
        self.value = 1.0


custom_sceneobject = CustomSceneObject()
custom_update: SceneAttributeUpdate[CustomSceneObject] = update_sceneobject
assert_type(
    custom_sceneobject.editable_attributes(),
    Mapping[str, SceneAttributeUpdate[CustomSceneObject] | None],
)
custom_sceneobject.update_editable_attribute("value", 2.0)
