from typing import Optional
from typing import Any
from typing import Union

import bpy

import compas_blender
from compas.geometry import Capsule
from compas.artists import ShapeArtist
from .artist import BlenderArtist


class CapsuleArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing capsule shapes.

    Parameters
    ----------
    capsule : :class:`compas.geometry.Capsule`
        A COMPAS capsule.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 capsule: Capsule,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):

        super().__init__(shape=capsule, collection=collection or capsule.name, **kwargs)

    def draw(self, u=None, v=None):
        """Draw the capsule associated with the artist.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~CapsuleArtist.u``.
        v : int, optional
            Number of faces in the "v" direction.
            Default is ``~CapsuleArtist.v``.

        Returns
        -------
        list
            The objects created in Blender.
        """
        u = u or self.u
        v = v or self.v
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        obj = compas_blender.draw_mesh(vertices, faces, name=self.shape.name, color=self.color, collection=self.collection)
        return [obj]
