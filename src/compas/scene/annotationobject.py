from typing import cast

from .annotations import ArrowAnnotation
from .annotations import DistanceDimension
from .annotations import TextAnnotation
from .sceneobject import SceneObject

__all__ = [
    "TextAnnotationObject",
    "ArrowAnnotationObject",
    "DistanceDimensionObject",
]


class TextAnnotationObject(SceneObject):
    """Stable scene object representing a text annotation."""

    @property
    def annotation(self) -> TextAnnotation:
        """Return the represented text annotation.

        Returns
        -------
        TextAnnotation

        """
        return cast(TextAnnotation, self.item)


class ArrowAnnotationObject(SceneObject):
    """Stable scene object representing an arrow annotation."""

    @property
    def annotation(self) -> ArrowAnnotation:
        """Return the represented arrow annotation.

        Returns
        -------
        ArrowAnnotation

        """
        return cast(ArrowAnnotation, self.item)


class DistanceDimensionObject(SceneObject):
    """Stable scene object representing a distance dimension."""

    @property
    def dimension(self) -> DistanceDimension:
        """Return the represented distance dimension.

        Returns
        -------
        DistanceDimension

        """
        return cast(DistanceDimension, self.item)
