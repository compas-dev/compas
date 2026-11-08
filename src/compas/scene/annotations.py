from math import isfinite
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import Self
from typing import cast
from uuid import UUID

from compas.data import Data
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Transformation
from compas.geometry import distance_point_point
from compas.typing import PointLike

from .exceptions import SceneItemNotBoundError

__all__ = [
    "PointAnchor",
    "ComponentAnchor",
    "TextAnnotation",
    "ArrowAnnotation",
    "DistanceDimension",
]

if TYPE_CHECKING:
    from .scene import Scene


type HorizontalAlignment = Literal["left", "center", "right"]
type VerticalAlignment = Literal["bottom", "center", "top"]
type HeightMode = Literal["screen", "world"]
type ComponentType = Literal["point", "vertex", "node", "line", "edge"]
type ComponentKey = int | str | tuple[ComponentKey, ...]
type EdgeKey = tuple[ComponentKey, ComponentKey]


class PointAnchor(Data):
    """A fixed dimension anchor in the dimension's local coordinates.

    Parameters
    ----------
    point
        The fixed anchor point.
    name
        The anchor name.

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the fixed-anchor data.

        Returns
        -------
        dict[str, Any]
            The serializable fixed-anchor data.

        """
        return {"point": self.point}

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct a fixed anchor from its serialized data.

        Returns
        -------
        PointAnchor
            The reconstructed fixed anchor.

        """
        _validate_schema(data, {"point"}, "point-anchor")
        return cls(data["point"])

    def __init__(self, point: PointLike, name: str | None = None) -> None:
        super().__init__(name=name)
        self.point = _copy_point(point)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PointAnchor) and self.point == other.point

    def resolve(self, transformation: Transformation | None = None) -> Point:
        """Return the fixed point, optionally transformed to world coordinates.

        Parameters
        ----------
        transformation
            Transformation from the owning dimension's local coordinates to
            world coordinates.

        Returns
        -------
        Point
            A new point. The stored anchor is never modified.

        """
        point = _copy_point(self.point)
        if transformation is not None:
            point.transform(transformation)
        return point


class ComponentAnchor(Data):
    """An associative anchor that resolves a scene component's current point.

    Parameters
    ----------
    object_guid
        GUID of the scene object containing the component.
    component_type
        Component selector type. Supported values are `"point"`, `"vertex"`,
        `"node"`, `"line"`, and `"edge"`.
    component
        Stable vertex or node key, or a pair of edge endpoint keys. Stable keys
        may be integers, strings, or recursively nested tuples of those values.
        Point and line anchors have no component key.
    parameter
        Normalized line or edge parameter in the closed interval from zero to
        one. Point, vertex, and node anchors have no parameter.
    name
        The anchor name.

    Notes
    -----
    Resolution reads the referenced item every time. An unavailable object,
    item, or component returns `None`; no fallback point is stored or reused.

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the associative-anchor data.

        Returns
        -------
        dict[str, Any]
            The serializable associative-anchor data.

        """
        return {
            "object_guid": str(self.object_guid),
            "component_type": self.component_type,
            "component": self.component,
            "parameter": self.parameter,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct an associative anchor from its serialized data.

        Returns
        -------
        ComponentAnchor
            The reconstructed associative anchor.

        """
        _validate_schema(data, {"object_guid", "component_type", "component", "parameter"}, "component-anchor")
        component = cast(ComponentKey | EdgeKey | None, _restore_component_key(data["component"]))
        return cls(
            UUID(data["object_guid"]),
            data["component_type"],
            component=component,
            parameter=data["parameter"],
        )

    def __init__(
        self,
        object_guid: UUID,
        component_type: ComponentType,
        component: ComponentKey | EdgeKey | None = None,
        parameter: float | None = None,
        *,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        if not isinstance(object_guid, UUID):
            raise TypeError("Component-anchor object_guid should be a UUID.")
        if component_type not in {"point", "vertex", "node", "line", "edge"}:
            raise ValueError(f"Unsupported component-anchor type: {component_type!r}.")
        if component_type in {"point", "line"}:
            if component is not None:
                raise ValueError(f"A {component_type} anchor should not have a component key.")
        elif component_type in {"vertex", "node"}:
            if not _is_component_key(component):
                raise TypeError(f"A {component_type} anchor should have a stable serializable component key.")
        else:
            if not isinstance(component, tuple) or len(component) != 2 or not all(_is_component_key(key) for key in component):
                raise TypeError("An edge anchor should have a pair of stable serializable endpoint keys.")
        if component_type in {"line", "edge"}:
            if isinstance(parameter, bool) or not isinstance(parameter, (int, float)):
                raise TypeError(f"A {component_type} anchor should have a numeric parameter.")
            if not 0.0 <= parameter <= 1.0:
                raise ValueError(f"A {component_type} anchor parameter should be between 0.0 and 1.0.")
        elif parameter is not None:
            raise ValueError(f"A {component_type} anchor should not have a parameter.")
        self.object_guid = object_guid
        self.component_type = component_type
        self.component = component
        self.parameter = float(parameter) if parameter is not None else None

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ComponentAnchor)
            and self.object_guid == other.object_guid
            and self.component_type == other.component_type
            and self.component == other.component
            and self.parameter == other.parameter
        )

    def resolve(self, scene: "Scene") -> Point | None:
        """Resolve the component to its current world-coordinate point.

        Parameters
        ----------
        scene
            Scene containing the referenced scene object and its bound item.

        Returns
        -------
        Point | None
            The current world-coordinate point, or `None` when the reference
            cannot be resolved.

        """
        try:
            sceneobject = scene.object(self.object_guid)
            item = sceneobject.item
        except (KeyError, SceneItemNotBoundError):
            return None
        if item is None:
            return None
        try:
            if self.component_type == "point":
                if not isinstance(item, Point):
                    return None
                point: object = item
            elif self.component_type == "line":
                if not isinstance(item, Line):
                    return None
                parameter = cast(float, self.parameter)
                point = item.point_at(parameter)
            elif self.component_type == "vertex":
                vertex_point = getattr(item, "vertex_point", None)
                if not callable(vertex_point):
                    return None
                point = vertex_point(self.component)
            elif self.component_type == "node":
                node_point = getattr(item, "node_point", None)
                if not callable(node_point):
                    return None
                point = node_point(self.component)
            else:
                has_edge = getattr(item, "has_edge", None)
                edge_point = getattr(item, "edge_point", None)
                if not callable(has_edge) or not callable(edge_point):
                    return None
                edge = cast(EdgeKey, self.component)
                reverse = (edge[1], edge[0])
                if not has_edge(edge) and not has_edge(reverse):
                    return None
                point = edge_point(self.component, self.parameter)
        except (KeyError, IndexError):
            return None
        resolved = _copy_point(cast(PointLike, point))
        resolved.transform(sceneobject.worldtransformation)
        return resolved


class TextAnnotation(Data):
    """Backend-neutral world text anchored in local coordinates.

    Parameters
    ----------
    text
        Annotation text.
    anchor
        Local anchor point.
    height
        Positive text height in screen pixels or world units, according to
        `height_mode`.
    height_mode
        `"screen"` for constant screen size or `"world"` for world-space size.
    horizontal_alignment
        Horizontal alignment relative to the anchor.
    vertical_alignment
        Vertical alignment relative to the anchor.
    name
        The annotation name.

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the text-annotation data.

        Returns
        -------
        dict[str, Any]
            The serializable text-annotation data.

        """
        return {
            "text": self.text,
            "anchor": self.anchor,
            "height": self.height,
            "height_mode": self.height_mode,
            "horizontal_alignment": self.horizontal_alignment,
            "vertical_alignment": self.vertical_alignment,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct a text annotation from its serialized data.

        Returns
        -------
        TextAnnotation
            The reconstructed text annotation.

        """
        _validate_schema(
            data,
            {"text", "anchor", "height", "height_mode", "horizontal_alignment", "vertical_alignment"},
            "text-annotation",
        )
        return cls(**data)

    def __init__(
        self,
        text: str,
        anchor: PointLike,
        height: float = 12.0,
        height_mode: HeightMode = "screen",
        horizontal_alignment: HorizontalAlignment = "left",
        vertical_alignment: VerticalAlignment = "bottom",
        *,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        if not isinstance(text, str):
            raise TypeError("Text-annotation text should be a string.")
        if isinstance(height, bool) or not isinstance(height, (int, float)):
            raise TypeError("Text-annotation height should be a number.")
        if not isfinite(height) or height <= 0:
            raise ValueError("Text-annotation height should be finite and positive.")
        if height_mode not in {"screen", "world"}:
            raise ValueError(f"Unsupported text-annotation height mode: {height_mode!r}.")
        if horizontal_alignment not in {"left", "center", "right"}:
            raise ValueError(f"Unsupported horizontal alignment: {horizontal_alignment!r}.")
        if vertical_alignment not in {"bottom", "center", "top"}:
            raise ValueError(f"Unsupported vertical alignment: {vertical_alignment!r}.")
        self.text = text
        self.anchor = _copy_point(anchor)
        self.height = float(height)
        self.height_mode = height_mode
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TextAnnotation) and self.__data__ == other.__data__


class ArrowAnnotation(Data):
    """Backend-neutral world arrow between two local-coordinate points.

    Parameters
    ----------
    start
        Local arrow start point.
    end
        Local arrow end point.
    name
        The annotation name.

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the arrow-annotation data.

        Returns
        -------
        dict[str, Any]
            The serializable arrow-annotation data.

        """
        return {"start": self.start, "end": self.end}

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct an arrow annotation from its serialized data.

        Returns
        -------
        ArrowAnnotation
            The reconstructed arrow annotation.

        """
        _validate_schema(data, {"start", "end"}, "arrow-annotation")
        return cls(**data)

    def __init__(self, start: PointLike, end: PointLike, *, name: str | None = None) -> None:
        super().__init__(name=name)
        start_point = _copy_point(start)
        end_point = _copy_point(end)
        if start_point == end_point:
            raise ValueError("Arrow-annotation start and end points should be different.")
        self.start = start_point
        self.end = end_point

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ArrowAnnotation) and self.start == other.start and self.end == other.end


class DistanceDimension(Data):
    """A distance annotation with independently fixed or associative anchors.

    Parameters
    ----------
    start
        First fixed or associative anchor.
    end
        Second fixed or associative anchor.
    unit
        Optional informational unit suffix. No coordinate conversion is
        performed.
    precision
        Non-negative number of fixed-point decimal places.
    label
        Optional verbatim label overriding derived distance formatting.
    name
        The dimension name.

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the distance-dimension data.

        Returns
        -------
        dict[str, Any]
            The serializable distance-dimension data.

        """
        return {
            "start": self.start,
            "end": self.end,
            "unit": self.unit,
            "precision": self.precision,
            "label": self.label,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct a distance dimension from its serialized data.

        Returns
        -------
        DistanceDimension
            The reconstructed distance dimension.

        """
        _validate_schema(data, {"start", "end", "unit", "precision", "label"}, "distance-dimension")
        return cls(**data)

    def __init__(
        self,
        start: PointAnchor | ComponentAnchor,
        end: PointAnchor | ComponentAnchor,
        unit: str | None = None,
        precision: int = 2,
        label: str | None = None,
        *,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        if not isinstance(start, (PointAnchor, ComponentAnchor)):
            raise TypeError("Distance-dimension start should be a PointAnchor or ComponentAnchor.")
        if not isinstance(end, (PointAnchor, ComponentAnchor)):
            raise TypeError("Distance-dimension end should be a PointAnchor or ComponentAnchor.")
        if unit is not None and not isinstance(unit, str):
            raise TypeError("Distance-dimension unit should be a string or None.")
        if unit is not None and not unit.strip():
            raise ValueError("Distance-dimension unit should be non-empty or None.")
        if isinstance(precision, bool) or not isinstance(precision, int):
            raise TypeError("Distance-dimension precision should be an integer.")
        if precision < 0:
            raise ValueError("Distance-dimension precision should be non-negative.")
        if label is not None and not isinstance(label, str):
            raise TypeError("Distance-dimension label should be a string or None.")
        self.start = start
        self.end = end
        self.unit = unit
        self.precision = precision
        self.label = label

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DistanceDimension) and self.__data__ == other.__data__

    def resolve(
        self,
        scene: "Scene | None" = None,
        transformation: Transformation | None = None,
    ) -> tuple[Point, Point] | None:
        """Resolve both anchors to world-coordinate points.

        Parameters
        ----------
        scene
            Scene used to resolve associative anchors.
        transformation
            Transformation from this dimension's local coordinates to world
            coordinates. It applies only to fixed anchors.

        Returns
        -------
        tuple[Point, Point] | None
            Resolved start and end points, or `None` if either associative
            anchor is unresolved.

        """
        start = self._resolve_anchor(self.start, scene, transformation)
        end = self._resolve_anchor(self.end, scene, transformation)
        if start is None or end is None:
            return None
        return start, end

    def distance(
        self,
        scene: "Scene | None" = None,
        transformation: Transformation | None = None,
    ) -> float | None:
        """Return the current resolved distance, or `None` if unresolved.

        Returns
        -------
        float | None
            The resolved distance, or `None`.

        """
        points = self.resolve(scene, transformation)
        if points is None:
            return None
        return distance_point_point(*points)

    def formatted_label(
        self,
        scene: "Scene | None" = None,
        transformation: Transformation | None = None,
    ) -> str | None:
        """Return the verbatim override or current formatted distance label.

        Returns
        -------
        str | None
            The label override, derived label, or `None` if unresolved.

        """
        if self.label is not None:
            return self.label
        distance = self.distance(scene, transformation)
        if distance is None:
            return None
        value = f"{distance:.{self.precision}f}"
        return f"{value} {self.unit}" if self.unit else value

    @staticmethod
    def _resolve_anchor(
        anchor: PointAnchor | ComponentAnchor,
        scene: "Scene | None",
        transformation: Transformation | None,
    ) -> Point | None:
        if isinstance(anchor, PointAnchor):
            return anchor.resolve(transformation)
        if scene is None:
            return None
        return anchor.resolve(scene)


def _validate_schema(data: dict[str, Any], expected: set[str], label: str) -> None:
    unknown = set(data) - expected
    if unknown:
        raise ValueError(f"Unknown {label} fields: {', '.join(sorted(unknown))}.")
    missing = expected - set(data)
    if missing:
        raise ValueError(f"Missing {label} fields: {', '.join(sorted(missing))}.")


def _copy_point(point: PointLike) -> Point:
    return Point(point[0], point[1], point[2])


def _is_component_key(value: object) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, str)):
        return True
    return isinstance(value, tuple) and all(_is_component_key(item) for item in value)


def _restore_component_key(value: object) -> object:
    if isinstance(value, list):
        return tuple(_restore_component_key(item) for item in value)
    return value
