from collections.abc import Sequence

import compas.geometry
from compas.typing import FloatSequenceLike
from compas.typing import NumericArray
from compas.typing import PointsLike
from compas.typing import RealInput

type LineType = compas.geometry.Line | PointsLike
type PlaneType = compas.geometry.Plane | PointsLike
CircleType = tuple[PlaneType, RealInput]
type PolygonType = compas.geometry.Polygon | PointsLike
type PolylineType = compas.geometry.Polyline | PointsLike
type QuaternionType = compas.geometry.Quaternion | FloatSequenceLike
type TriangleType = compas.geometry.Polygon | PointsLike
type TransformationType = compas.geometry.Transformation | Sequence[Sequence[RealInput]] | NumericArray
