from typing import Optional
from typing import Tuple
from typing import Union

import bpy

import compas_blender
from compas.geometry import Primitive
from compas_blender.artists import BaseArtist

__all__ = ['PrimitiveArtist']

Color = Union[Tuple[int, int, int], Tuple[float, float, float]]


class PrimitiveArtist(BaseArtist):
    """Base class for artists for geometry primitives.

    Parameters
    ----------
    primitive: :class:`compas.geometry.Primitive`
        The geometry of the primitive.
    color : 3-tuple
        The RGB components of the base color of the primitive.
    collection : str or bpy.types.Collection, optional
        The collection in which the primitive should be contained.

    Attributes
    ----------
    primitive: :class:`compas.geometry.Primitive`
        The geometry of the primitive.
    name : str
        The name of the primitive.
    color : tuple
        The RGB components of the base color of the primitive.
    collection : str or bpy.types.Collection
        The collection in which the primitive should be contained.

    """
    def __init__(self,
                 primitive: Primitive,
                 color: Color,
                 collection: Optional[Union[str, bpy.types.Collection]] = None):
        super().__init__()
        self.primitive = primitive
        self.color = color
        self.collection = collection or primitive.name

    @property
    def collection(self) -> bpy.types.Collection:
        return self._collection

    @collection.setter
    def collection(self, value):
        if isinstance(value, bpy.types.Collection):
            self._collection = value
        else:
            self._collection = compas_blender.create_collection(value)

    @property
    def name(self):
        """str : Reference to the name of the primitive."""
        return self.primitive.name

    @name.setter
    def name(self, name):
        self.primitive.name = name
