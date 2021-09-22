from typing import Optional
from typing import Any
from typing import Union

import bpy
import compas_blender
from compas.geometry import Box
from compas.artists import ShapeArtist
from .artist import BlenderArtist


class BoxArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing box shapes.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`
        A COMPAS box.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 box: Box,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):
        super().__init__(shape=box, collection=collection or box.name, **kwargs)

    def draw(self):
        """Draw the box associated with the artist.

        Returns
        -------
        list
            The objects created in Blender.
        """
        vertices, faces = self.shape.to_vertices_and_faces()
        objects = []
        obj = compas_blender.draw_mesh(vertices, faces, name=self.shape.name, color=self.color, collection=self.collection)
        objects.append(obj)
        self.objects += objects
        return objects
