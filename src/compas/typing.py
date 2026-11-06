from collections.abc import Iterator
from collections.abc import Sequence
from os import PathLike
from typing import Any
from typing import Protocol
from typing import SupportsIndex
from typing import TypeVar
from typing import overload
from typing import runtime_checkable

import numpy as np
from numpy.typing import NDArray

__all__ = [
    "CoordinateProtocol",
    "FilePath",
    "Float64Array",
    "FloatingArray",
    "FloatSequenceLike",
    "IndexGroupsLike",
    "IndexGroupsProtocol",
    "IndicesLike",
    "IndicesProtocol",
    "Int32Array",
    "IntegerArray",
    "IntegralInput",
    "NumericArray",
    "PointGroupsLike",
    "PointGroupsProtocol",
    "PointLike",
    "PointsLike",
    "PointsProtocol",
    "RayData",
    "RayMeshHit",
    "RealInput",
    "SphereData",
    "VectorLike",
    "VerticesFaces",
]


type FilePath = str | PathLike[str]

type RealInput = int | float | np.integer[Any] | np.floating[Any]
type IntegralInput = int | np.integer[Any]

type NumericArray = NDArray[np.integer[Any] | np.floating[Any]]
type FloatingArray = NDArray[np.floating[Any]]
type IntegerArray = NDArray[np.integer[Any]]
type Float64Array = NDArray[np.float64]
type Int32Array = NDArray[np.int32]


T_co = TypeVar("T_co", bound=RealInput, covariant=True)


@runtime_checkable
class CoordinateProtocol(Protocol[T_co]):
    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[T_co]: ...

    @overload
    def __getitem__(self, key: int) -> T_co: ...

    @overload
    def __getitem__(self, key: slice) -> Sequence[T_co]: ...


type FloatSequenceLike = CoordinateProtocol[RealInput] | Sequence[RealInput] | NumericArray
type PointLike = FloatSequenceLike
type VectorLike = FloatSequenceLike


@runtime_checkable
class PointsProtocol(Protocol):
    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[PointLike]: ...

    def __getitem__(self, key: int) -> PointLike: ...


class IndicesProtocol(Protocol):
    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[SupportsIndex]: ...

    def __getitem__(self, key: int) -> SupportsIndex: ...


type PointsLike = PointsProtocol | Sequence[PointLike] | NumericArray
type IndicesLike = IndicesProtocol | Sequence[SupportsIndex] | IntegerArray


class IndexGroupsProtocol(Protocol):
    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[IndicesLike]: ...

    def __getitem__(self, key: int) -> IndicesLike: ...


class PointGroupsProtocol(Protocol):
    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[PointsLike]: ...

    def __getitem__(self, key: int) -> PointsLike: ...


type IndexGroupsLike = IndexGroupsProtocol | Sequence[IndicesLike] | IntegerArray
type PointGroupsLike = PointGroupsProtocol | Sequence[PointsLike] | NumericArray

type VerticesFaces = tuple[PointsLike, IndexGroupsLike]
type SphereData = tuple[PointLike, RealInput]
type RayData = tuple[PointLike, VectorLike]
type RayMeshHit = tuple[int, float, float, float]
