from typing import TYPE_CHECKING
from typing import Iterator
from typing import Protocol
from typing import Sequence
from typing import Union

if TYPE_CHECKING:
    from compas.geometry import Line
    from compas.geometry import Plane
    from compas.geometry import Polygon
    from compas.geometry import Polyline
    from compas.geometry import Transformation


class Coordinate(Protocol):
    def __getitem__(self, key: int) -> float: ...

    def __iter__(self) -> Iterator[float]: ...


CoordinateType = Union[Coordinate, Sequence[float]]


class Coordinates(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, key: int) -> CoordinateType: ...

    def __iter__(self) -> Iterator[CoordinateType]: ...


CoordinatesType = Union[Coordinates, Sequence[CoordinateType]]

LineType = Union["Line", Sequence[CoordinateType]]
PlaneType = Union["Plane", Sequence[CoordinateType]]
PolygonType = Union["Polygon", Sequence[CoordinateType]]
PolylineType = Union["Polyline", Sequence[CoordinateType]]
TriangleType = Union["Polygon", Sequence[CoordinateType]]
TransformationType = Union["Transformation", Sequence[Sequence[float]]]
