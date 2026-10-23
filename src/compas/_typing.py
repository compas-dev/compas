from collections.abc import Iterator
from collections.abc import Sequence
from os import PathLike
from typing import Protocol
from typing import runtime_checkable

FilePath = str | PathLike[str]


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


@runtime_checkable
class Coordinates(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, key: int) -> CoordinateType: ...

    def __iter__(self) -> Iterator[CoordinateType]: ...


CoordinatesType = Coordinates | Sequence[CoordinateType]

SphereType = tuple[CoordinateType, float]
MeshType = tuple[CoordinatesType, Sequence[Sequence[int]]]
RayType = tuple[CoordinateType, CoordinateType]
RayMeshHit = tuple[int, float, float, float]
