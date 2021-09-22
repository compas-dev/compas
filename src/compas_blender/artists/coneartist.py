from typing import Optional
from typing import Any
from typing import Union

import bpy

import compas_blender
from compas.geometry import Cone
from compas.artists import ShapeArtist
from .artist import BlenderArtist


class ConeArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing cone shapes.

    Parameters
    ----------
    cone : :class:`compas.geometry.Cone`
        A COMPAS cone.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 cone: Cone,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):
        super().__init__(shape=cone, collection=collection or cone.name, **kwargs)

    def draw(self, u=None):
        """Draw the cone associated with the artist.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~ConeArtist.u``.

        Returns
        -------
        list
            The objects created in Blender.
        """
        u = u or self.u
        vertices, faces = self.shape.to_vertices_and_faces(u=u)
        objects = []
        obj = compas_blender.draw_mesh(vertices, faces, name=self.shape.name, color=self.color, collection=self.collection)
        objects.append(obj)
        self.objects += objects
        return objects
