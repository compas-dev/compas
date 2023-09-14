from typing import Union
from typing import Optional
from typing import Any

import bpy  # type: ignore
import compas_blender

from compas.colors import Color
from compas.artists import Artist
from compas_blender.conversions import color_to_blender_material


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

    def link_object(self, obj: bpy.types.Object):
        """Link an object to the collection of this artist.

        Parameters
        ----------
        obj : :class:`bpy.types.Object`
            The Blender object to link.

        """
        self.unlink_object(obj)
        self.collection.objects.link(obj)

    def unlink_object(self, obj: bpy.types.Object):
        """Unlink an object from the collection of this artist.

        Parameters
        ----------
        obj : :class:`bpy.types.Object`
            The Blender object to unlink.

        """
        for c in obj.users_collection:
            c.objects.unlink(obj)

    def assign_object_color(self, obj: bpy.types.Object, color: Color):
        """Assign a color to a Blender object.

        Parameters
        ----------
        obj : :class:`bpy.types.Object`
            The Blender object.
        color : str | tuple, optional
            The color specification.

        Returns
        -------
        :class:`bpy.types.Material`
            The Blender color material assigned to the object.

        """
        material = color_to_blender_material(color)
        obj.color = color.rgba
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
        obj.active_material = material
        return material
