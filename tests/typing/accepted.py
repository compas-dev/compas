from collections.abc import Iterator

import numpy as np

from compas._typing import CoordinateInput
from compas._typing import CoordinatesInput
from compas._typing import Float64Array
from compas._typing import FloatingArray
from compas._typing import IndicesInput
from compas._typing import Int32Array
from compas._typing import IntegerArray
from compas._typing import IntegralInput
from compas._typing import NumericArray
from compas._typing import RealInput
from compas.geometry import Point
from compas.geometry import Vector


class CustomCoordinate:
    def __init__(self, values: tuple[float, float, float]):
        self.values = values

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, key: int) -> float:
        return self.values[key]

    def __iter__(self) -> Iterator[float]:
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
indices_inputs: list[IndicesInput] = [[0, 1, 2], (np.int32(0), np.int64(1)), int32_array, int64_array]
