from collections.abc import Iterator
from collections.abc import Sequence
from os import PathLike
from typing import Any
from typing import Protocol
from typing import TypeAlias
from typing import runtime_checkable

import numpy as np
from numpy.typing import NDArray

FilePath = str | PathLike[str]

RealInput: TypeAlias = int | float | np.integer[Any] | np.floating[Any]
IntegralInput: TypeAlias = int | np.integer[Any]

NumericArray: TypeAlias = NDArray[np.integer[Any] | np.floating[Any]]
FloatingArray: TypeAlias = NDArray[np.floating[Any]]
IntegerArray: TypeAlias = NDArray[np.integer[Any]]
Float64Array: TypeAlias = NDArray[np.float64]
Int32Array: TypeAlias = NDArray[np.int32]


class FloatSequence(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, key: int) -> float: ...

    def __iter__(self) -> Iterator[float]: ...


FloatSequenceType = FloatSequence | Sequence[float]
RawCoordinateType = list[float] | tuple[float, float, float]


@runtime_checkable
class Coordinate(FloatSequence, Protocol):
    pass


CoordinateType = Coordinate | Sequence[float]
PointCoordinates: TypeAlias = Sequence[float]


@runtime_checkable
class Coordinates(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, key: int) -> CoordinateType: ...

    def __iter__(self) -> Iterator[CoordinateType]: ...


CoordinatesType = Coordinates | Sequence[CoordinateType]

CoordinateInput: TypeAlias = Coordinate | Sequence[RealInput] | NumericArray
CoordinatesInput: TypeAlias = Coordinates | Sequence[CoordinateInput] | NumericArray


@runtime_checkable
class Indices(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, key: int) -> IntegralInput: ...

    def __iter__(self) -> Iterator[IntegralInput]: ...


IndicesInput: TypeAlias = Indices | Sequence[IntegralInput] | IntegerArray


@runtime_checkable
class IndicesCollection(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, key: int) -> IndicesInput: ...

    def __iter__(self) -> Iterator[IndicesInput]: ...


IndicesCollectionInput: TypeAlias = IndicesCollection | Sequence[IndicesInput] | IntegerArray


@runtime_checkable
class CoordinatesCollection(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, key: int) -> CoordinatesInput: ...

    def __iter__(self) -> Iterator[CoordinatesInput]: ...


CoordinatesCollectionInput: TypeAlias = CoordinatesCollection | Sequence[CoordinatesInput] | NumericArray

TriangleMeshInput: TypeAlias = tuple[CoordinatesInput, IndicesCollectionInput]

SphereType = tuple[CoordinateType, float]
MeshType = tuple[CoordinatesType, Sequence[Sequence[int]]]
RayType = tuple[CoordinateType, CoordinateType]
RayMeshHit = tuple[int, float, float, float]
