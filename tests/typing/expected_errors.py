import numpy as np
from numpy.typing import NDArray

from compas._typing import CoordinateInput
from compas._typing import Float64Array
from compas._typing import IndicesInput
from compas._typing import IntegralInput
from compas._typing import NumericArray
from compas._typing import RealInput
from compas._typing import TriangleMeshInput
from compas.geometry import Tessellation
from compas.geometry import Delaunay
from compas.geometry import triangulate_planar_points

real_input: RealInput = "1"  # expected-error: reportAssignmentType
integral_input: IntegralInput = 1.5  # expected-error: reportAssignmentType
numpy_bool_input: RealInput = np.bool_(True)  # expected-error: reportAssignmentType
coordinate_input: CoordinateInput = ["0", "1", "2"]  # expected-error: reportAssignmentType
object_array_value: NDArray[np.object_] = np.asarray([1, 2, 3], dtype=np.object_)
object_array: NumericArray = object_array_value  # expected-error: reportAssignmentType
indices_input: IndicesInput = np.asarray([0, 1, 2], dtype=np.float64)  # expected-error: reportAssignmentType
float64_array: Float64Array = np.asarray([1, 2, 3], dtype=np.float32)  # expected-error: reportAssignmentType
Tessellation([["0", "0", "0"]], [[0, 0, 0]])  # expected-error: reportArgumentType
Tessellation([[0.0, 0.0, 0.0]], np.asarray([[0.0, 0.0, 0.0]]))  # expected-error: reportArgumentType
triangulate_planar_points(np.asarray([[0, 0, 0]], dtype=np.complex128), strategy=Delaunay())  # expected-error: reportArgumentType
triangle_mesh_complex_vertices: TriangleMeshInput = (np.asarray([[0, 0, 0]], dtype=np.complex128), [[0, 0, 0]])  # expected-error: reportAssignmentType
triangle_mesh_float_indices: TriangleMeshInput = ([[0.0, 0.0, 0.0]], np.asarray([[0.0, 0.0, 0.0]]))  # expected-error: reportAssignmentType
