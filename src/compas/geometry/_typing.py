from typing import TYPE_CHECKING
from typing import Sequence
from typing import Union

from compas._typing import CoordinateType

if TYPE_CHECKING:
    from compas.geometry import Line
    from compas.geometry import Plane
    from compas.geometry import Polygon
    from compas.geometry import Polyline
    from compas.geometry import Transformation


LineType = Union["Line", Sequence[CoordinateType]]
PlaneType = Union["Plane", Sequence[CoordinateType]]
PolygonType = Union["Polygon", Sequence[CoordinateType]]
PolylineType = Union["Polyline", Sequence[CoordinateType]]
TriangleType = Union["Polygon", Sequence[CoordinateType]]
TransformationType = Union["Transformation", Sequence[Sequence[float]]]
