from typing import Optional
from typing import Any
from typing import Union

import bpy

import compas_blender
from compas.geometry import Cylinder
from compas.artists import ShapeArtist
from .artist import BlenderArtist


class CylinderArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing cylinder shapes.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`
        A COMPAS cylinder.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 cylinder: Cylinder,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):
        super().__init__(shape=cylinder, collection=collection or cylinder.name, **kwargs)

    def draw(self, u=None, v=None):
        """Draw the cylinder associated with the artist.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~CylinderArtist.u``.
        v : int, optional
            Number of faces in the "v" direction.
            Default is ``~CylinderArtist.v``.

        Returns
        -------
        list
            The objects created in Blender.
        """
        u = u or self.u
        v = v or self.v
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        objects = []
        obj = compas_blender.draw_mesh(vertices, faces, name=self.shape.name, color=self.color, collection=self.collection)
        objects.append(obj)
        self.objects += objects
        return objects
