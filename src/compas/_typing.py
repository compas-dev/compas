from typing import Iterator
from typing import Protocol
from typing import Sequence
from typing import Union
from typing import runtime_checkable


class FloatSequence(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, key: int) -> float: ...

    def __iter__(self) -> Iterator[float]: ...


FloatSequenceType = Union[FloatSequence, Sequence[float]]
RawCoordinateType = Union[list[float], tuple[float, float, float]]


class Coordinate(FloatSequence, Protocol):
    pass


CoordinateType = Union[Coordinate, Sequence[float]]


@runtime_checkable
class Coordinates(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, key: int) -> CoordinateType: ...

    def __iter__(self) -> Iterator[CoordinateType]: ...


CoordinatesType = Union[Coordinates, Sequence[CoordinateType]]
