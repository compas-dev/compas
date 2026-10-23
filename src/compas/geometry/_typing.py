from collections.abc import Sequence

import compas.geometry
from compas._typing import CoordinateType

type LineType = compas.geometry.Line | Sequence[CoordinateType]
type PlaneType = compas.geometry.Plane | Sequence[CoordinateType]
CircleType = tuple[PlaneType, float]
type PolygonType = compas.geometry.Polygon | Sequence[CoordinateType]
type PolylineType = compas.geometry.Polyline | Sequence[CoordinateType]
type QuaternionType = compas.geometry.Quaternion | Sequence[float]
type TriangleType = compas.geometry.Polygon | Sequence[CoordinateType]
type TransformationType = compas.geometry.Transformation | Sequence[Sequence[float]]
