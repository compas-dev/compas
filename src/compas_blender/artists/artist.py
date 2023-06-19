from typing import Union
from typing import Optional
from typing import Any

import bpy
import compas_blender

from compas.artists import Artist


class BlenderArtist(Artist):
    """Base class for all Blender artists.

    Parameters
    ----------
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection the object(s) created by the artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas.artists.Artist` for more info.

    Attributes
    ----------
    collection : :blender:`bpy.types.Collection`
        The collection containing the object(s) created by this artist.

    """

    def __init__(self, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):
        # Initialize collection before even calling super because other classes depend on that
        self._collection = None
        self.collection = collection
        super().__init__(**kwargs)

    @property
    def collection(self) -> bpy.types.Collection:
        return self._collection

    @collection.setter
    def collection(self, value: Union[str, bpy.types.Collection]):
        if isinstance(value, bpy.types.Collection):
            self._collection = value
        elif isinstance(value, str):
            self._collection = compas_blender.create_collection(value)
        else:
            raise Exception("Collection must be of type `str` or `bpy.types.Collection`.")
