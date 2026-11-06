import numpy as np
from numpy.typing import NDArray
from collections.abc import Iterator

from compas.typing import PointLike
from compas.typing import Float64Array
from compas.typing import IndicesLike
from compas.typing import IntegralInput
from compas.typing import NumericArray
from compas.typing import PointsLike
from compas.typing import RealInput
from compas.typing import VerticesFaces
from compas.geometry import Tessellation
from compas.geometry import Transformation
from compas.geometry import delaunay_triangulation
from compas.geometry import is_polygon_in_polygon_xy


class IterableOnlyCoordinate:
    def __iter__(self) -> Iterator[float]:
        return iter((1.0, 2.0, 3.0))


class IterableOnlyPoints:
    def __iter__(self) -> Iterator[list[float]]:
        return iter(([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]))


real_input: RealInput = "1"  # expected-error: reportAssignmentType
integral_input: IntegralInput = 1.5  # expected-error: reportAssignmentType
numpy_bool_input: RealInput = np.bool_(True)  # expected-error: reportAssignmentType
coordinate_input: PointLike = ["0", "1", "2"]  # expected-error: reportAssignmentType
iterable_only_coordinate: PointLike = IterableOnlyCoordinate()  # expected-error: reportAssignmentType
iterable_only_points: PointsLike = IterableOnlyPoints()  # expected-error: reportAssignmentType
object_array_value: NDArray[np.object_] = np.asarray([1, 2, 3], dtype=np.object_)
object_array: NumericArray = object_array_value  # expected-error: reportAssignmentType
indices_input: IndicesLike = np.asarray([0, 1, 2], dtype=np.float64)  # expected-error: reportAssignmentType
float64_array: Float64Array = np.asarray([1, 2, 3], dtype=np.float32)  # expected-error: reportAssignmentType
Tessellation([["0", "0", "0"]], [[0, 0, 0]])  # expected-error: reportArgumentType
Tessellation([[0.0, 0.0, 0.0]], np.asarray([[0.0, 0.0, 0.0]]))  # expected-error: reportArgumentType
delaunay_triangulation(np.asarray([[0, 0, 0]], dtype=np.complex128))  # expected-error: reportArgumentType
is_polygon_in_polygon_xy(np.asarray([[0, 0, 0]], dtype=np.complex128), [[0, 0, 0]])  # expected-error: reportArgumentType
triangle_mesh_complex_vertices: VerticesFaces = (np.asarray([[0, 0, 0]], dtype=np.complex128), [[0, 0, 0]])  # expected-error: reportAssignmentType
triangle_mesh_float_indices: VerticesFaces = ([[0.0, 0.0, 0.0]], np.asarray([[0.0, 0.0, 0.0]]))  # expected-error: reportAssignmentType
narrow_int_matrix: list[list[int]] = [[1, 0], [0, 1]]
narrow_numpy_matrix: list[list[np.float64]] = [[np.float64(1), np.float64(0)], [np.float64(0), np.float64(1)]]
Transformation(narrow_int_matrix)  # expected-error: reportArgumentType
Transformation(narrow_numpy_matrix)  # expected-error: reportArgumentType
