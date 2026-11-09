from __future__ import annotations

from math import isfinite
from typing import TYPE_CHECKING
from typing import Any
from typing import Self
from typing import cast
from uuid import UUID

from compas.colors import Color
from compas.data import Data

from .annotations import ArrowAnnotation
from .annotations import DistanceDimension
from .annotations import TextAnnotation
from .exceptions import SceneItemNotBoundError

if TYPE_CHECKING:
    from .scene import Scene


type AnnotationItem = TextAnnotation | ArrowAnnotation | DistanceDimension


class DimensionStyle(Data):
    """Durable presentation style for a distance dimension.

    All sizes are expressed in logical screen pixels. `label_offset` follows
    the screen-space normal on the left side of the projected dimension from
    start to end.

    Parameters
    ----------
    color
        Line and label color.
    line_width
        Positive dimension-line width.
    text_size
        Positive label height.
    arrow_size
        Positive arrow-head width. The head length retains a 4:3 proportion.
    label_offset
        Finite signed label offset.
    name
        Style name.

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the serializable dimension-style data.

        Returns
        -------
        dict[str, Any]
            The closed dimension-style payload.

        """
        return {
            "color": self.color,
            "line_width": self.line_width,
            "text_size": self.text_size,
            "arrow_size": self.arrow_size,
            "label_offset": self.label_offset,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct a style from its closed serialized schema.

        Returns
        -------
        DimensionStyle
            The reconstructed style.

        """
        expected = {"color", "line_width", "text_size", "arrow_size", "label_offset"}
        unknown = set(data) - expected
        if unknown:
            raise ValueError("Unknown dimension-style fields: {}.".format(", ".join(sorted(unknown))))
        missing = expected - set(data)
        if missing:
            raise ValueError("Missing dimension-style fields: {}.".format(", ".join(sorted(missing))))
        return cls(**data)

    def __init__(
        self,
        color: Color | None = None,
        line_width: float = 3.0,
        text_size: float = 12.0,
        arrow_size: float = 12.0,
        label_offset: float = 0.0,
        *,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        self.color = Color.white() if color is None else color
        self.line_width = line_width
        self.text_size = text_size
        self.arrow_size = arrow_size
        self.label_offset = label_offset

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DimensionStyle) and self.__data__ == other.__data__

    @property
    def color(self) -> Color:
        """Return the dimension line and label color."""
        return self._color

    @color.setter
    def color(self, value: Color) -> None:
        if not isinstance(value, Color):
            raise TypeError("Dimension-style color should be a Color.")
        self._color = value

    @property
    def line_width(self) -> float:
        """Return the positive line width in logical pixels."""
        return self._line_width

    @line_width.setter
    def line_width(self, value: float) -> None:
        self._line_width = _positive_float(value, "line width")

    @property
    def text_size(self) -> float:
        """Return the positive label height in logical pixels."""
        return self._text_size

    @text_size.setter
    def text_size(self, value: float) -> None:
        self._text_size = _positive_float(value, "text size")

    @property
    def arrow_size(self) -> float:
        """Return the positive arrow-head width in logical pixels."""
        return self._arrow_size

    @arrow_size.setter
    def arrow_size(self, value: float) -> None:
        self._arrow_size = _positive_float(value, "arrow size")

    @property
    def label_offset(self) -> float:
        """Return the signed label offset in logical pixels."""
        return self._label_offset

    @label_offset.setter
    def label_offset(self, value: float) -> None:
        self._label_offset = _finite_float(value, "label offset")


class SceneAnnotation(Data):
    """Stable scene-scoped placement of one annotation item.

    Annotation entries belong to a flat ordered collection rather than the
    spatial hierarchy. They have no node, parent, children, or transformation.

    Parameters
    ----------
    item
        Independently serializable annotation item.
    item_guid
        GUID of an unresolved annotation item.
    name
        Entry name.
    show
        Whether the annotation is visible.
    style
        Optional distance-dimension presentation style.

    """

    @property
    def __data__(self) -> dict[str, Any]:
        """Return the durable annotation-entry data.

        Returns
        -------
        dict[str, Any]
            The closed annotation-entry payload.

        """
        return {
            "item": str(self.item_guid),
            "show": self.show,
            "style": self.style,
        }

    @classmethod
    def __from_data__(cls, data: dict[str, Any]) -> Self:
        """Construct an unresolved annotation entry from serialized data.

        Returns
        -------
        SceneAnnotation
            The reconstructed entry.

        """
        expected = {"item", "show", "style"}
        unknown = set(data) - expected
        if unknown:
            raise ValueError("Unknown scene-annotation fields: {}.".format(", ".join(sorted(unknown))))
        missing = expected - set(data)
        if missing:
            raise ValueError("Missing scene-annotation fields: {}.".format(", ".join(sorted(missing))))
        try:
            item_guid = UUID(data["item"])
        except (AttributeError, TypeError, ValueError):
            raise ValueError("Scene-annotation item should be a UUID string.") from None
        return cls(item_guid=item_guid, show=data["show"], style=data["style"])

    def __init__(
        self,
        item: AnnotationItem | None = None,
        *,
        item_guid: UUID | None = None,
        name: str | None = None,
        show: bool = True,
        style: DimensionStyle | None = None,
    ) -> None:
        if item is None and item_guid is None:
            raise ValueError("A scene annotation requires an item or item GUID.")
        if item is not None and not isinstance(item, (TextAnnotation, ArrowAnnotation, DistanceDimension)):
            raise TypeError("A scene-annotation item should be a TextAnnotation, ArrowAnnotation, or DistanceDimension.")
        if item is not None and item_guid is not None and item.guid != item_guid:
            raise ValueError("The supplied annotation item and item GUID do not match.")
        if item_guid is not None and not isinstance(item_guid, UUID):
            raise TypeError("Scene-annotation item_guid should be a UUID.")
        if not isinstance(show, bool):
            raise TypeError("Scene-annotation show should be a boolean.")
        if style is not None and not isinstance(style, DimensionStyle):
            raise TypeError("Scene-annotation style should be a DimensionStyle or None.")
        if isinstance(item, DistanceDimension) and style is None:
            style = DimensionStyle()
        if item is not None:
            _validate_item_style(item, style)
        super().__init__(name=name or getattr(item, "name", None))
        self._item_guid = item.guid if item is not None else cast(UUID, item_guid)
        self._item = item
        self._scene: Scene | None = None
        self.show = show
        self.style = style

    @property
    def item_guid(self) -> UUID:
        """Return the GUID of the represented annotation item."""
        return self._item_guid

    @property
    def item(self) -> AnnotationItem:
        """Return the bound annotation item.

        Raises
        ------
        SceneItemNotBoundError
            If the annotation item is unresolved.

        """
        if self.scene is not None:
            item = self.scene.item(self.item_guid, object_guid=self.guid)
            return cast(AnnotationItem, item)
        if self._item is None:
            raise SceneItemNotBoundError(self.guid, self.item_guid)
        return self._item

    @property
    def scene(self) -> Scene | None:
        """Return the owning scene, or `None` while detached."""
        return self._scene

    @property
    def show(self) -> bool:
        """Return whether the annotation is visible."""
        return self._show

    @show.setter
    def show(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("Scene-annotation show should be a boolean.")
        self._show = value

    @property
    def style(self) -> DimensionStyle | None:
        """Return the optional distance-dimension style."""
        return self._style

    @style.setter
    def style(self, value: DimensionStyle | None) -> None:
        if value is not None and not isinstance(value, DimensionStyle):
            raise TypeError("Scene-annotation style should be a DimensionStyle or None.")
        item = self._item
        if item is None and self.scene is not None:
            item = cast(AnnotationItem | None, self.scene.item_store.get(self.item_guid))
        if item is not None:
            if isinstance(item, DistanceDimension) and value is None:
                value = DimensionStyle()
            _validate_item_style(item, value)
        self._style = value

    def draw(self, context: str | None = None, runtime: object | None = None) -> list[object]:
        """Draw this entry through its owning scene context.

        Parameters
        ----------
        context
            Visualization context. The owning scene default is used when
            omitted.
        runtime
            Optional context-specific runtime object.

        Returns
        -------
        list[object]
            Backend-specific runtime handles.

        Raises
        ------
        ValueError
            If the entry is detached.

        """
        if self.scene is None:
            raise ValueError("The scene annotation does not belong to a scene.")
        return self.scene.draw_annotation(self, context=context, runtime=runtime)

    def clear(self, context: str | None = None, runtime: object | None = None) -> None:
        """Clear this entry's transient resources through its owning scene.

        Parameters
        ----------
        context
            Visualization context. The owning scene default is used when
            omitted.
        runtime
            Optional context-specific runtime object overriding the stored
            runtime.

        Raises
        ------
        ValueError
            If the entry is detached.

        """
        if self.scene is None:
            raise ValueError("The scene annotation does not belong to a scene.")
        self.scene.clear_annotation(self, context=context, runtime=runtime)


def _finite_float(value: float, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"Dimension-style {field} should be a number.")
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"Dimension-style {field} should be finite.")
    return result


def _positive_float(value: float, field: str) -> float:
    result = _finite_float(value, field)
    if result <= 0.0:
        raise ValueError(f"Dimension-style {field} should be positive.")
    return result


def _validate_item_style(item: AnnotationItem, style: DimensionStyle | None) -> None:
    if style is not None and not isinstance(item, DistanceDimension):
        raise ValueError("DimensionStyle is supported only for DistanceDimension entries.")


__all__ = ["DimensionStyle", "SceneAnnotation"]
