from collections.abc import Iterator
from typing import assert_type

import numpy as np

from compas._typing import CoordinateInput
from compas._typing import CoordinatesCollectionInput
from compas._typing import CoordinatesInput
from compas._typing import Float64Array
from compas._typing import FloatingArray
from compas._typing import IndicesInput
from compas._typing import Int32Array
from compas._typing import IntegerArray
from compas._typing import IntegralInput
from compas._typing import NumericArray
from compas._typing import RealInput
from compas._typing import TriangleMeshInput
from compas.geometry import Point
from compas.geometry import ConstrainedDelaunay
from compas.geometry import Delaunay
from compas.geometry import FaceTriangulation
from compas.geometry import Tessellation
from compas.geometry import Vector
from compas.geometry import triangulate_planar_domain
from compas.geometry import triangulate_planar_points
from compas.geometry.triangulation import triangulate_polygon
from compas.datastructures import Mesh


class CustomCoordinate:
    def __init__(self, values: tuple[float, float, float]):
        self.values = values

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, key: int) -> float:
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

coordinate_inputs: list[CoordinateInput] = [
    [1, 2, 3],
    (1.0, 2.0, 3.0),
    Point(1, 2, 3),
    Vector(1, 2, 3),
    CustomCoordinate((1, 2, 3)),
    float32_array,
    int64_array,
]
coordinates_inputs: list[CoordinatesInput] = [coordinate_inputs, np.asarray([[0, 0, 0], [1, 1, 1]], dtype=np.float64)]
coordinates_collection_inputs: list[CoordinatesCollectionInput] = [
    [coordinates_inputs[1]],
    np.asarray([[[0, 0, 0], [1, 0, 0], [0, 1, 0]]], dtype=np.float32),
]
indices_inputs: list[IndicesInput] = [[0, 1, 2], (np.int32(0), np.int64(1)), int32_array, int64_array]

vertices32 = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)
triangles32 = np.asarray([[0, 1, 2]], dtype=np.int32)
vertices64 = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float64)
triangles64 = np.asarray([[0, 1, 2]], dtype=np.int64)
triangle_mesh_inputs: list[TriangleMeshInput] = [
    ([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], [[0, 1, 2]]),
    (((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)), ((0, 1, 2),)),
    (vertices32, triangles32),
    (vertices64, triangles64),
]
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

triangulate_planar_points(vertices32, strategy=Delaunay())
triangulate_polygon(vertices32, FaceTriangulation())
triangulate_planar_domain(
    vertices32,
    holes=np.asarray([vertices32], dtype=np.float32),
    constraints=np.asarray([vertices32[:2]], dtype=np.float64),
    points=np.asarray([[0.25, 0.25, 0]], dtype=np.int64),
    strategy=ConstrainedDelaunay(),
)
