from typing import Iterator
from typing import Protocol
from typing import Sequence
from typing import Union


class Coordinate(Protocol):
    def __getitem__(self, key: int) -> float: ...

    def __iter__(self) -> Iterator[float]: ...


CoordinateType = Union[Coordinate, Sequence[float]]


class Coordinates(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, key: int) -> CoordinateType: ...

    def __iter__(self) -> Iterator[CoordinateType]: ...


CoordinatesType = Union[Coordinates, Sequence[CoordinateType]]
