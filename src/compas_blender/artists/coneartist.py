from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas_blender.utilities import RGBColor
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

    def draw(self, color: Optional[RGBColor] = None, u: int = None) -> List[bpy.types.Object]:
        """Draw the cone associated with the artist.

        Parameters
        ----------
        color : tuple of float or tuple of int, optional
            The RGB color of the cone.
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~ConeArtist.u``.

        Returns
        -------
        list
            The objects created in Blender.
        """
        u = u or self.u
        color = color or self.color
        vertices, faces = self.shape.to_vertices_and_faces(u=u)
        obj = compas_blender.draw_mesh(vertices, faces, name=self.shape.name, color=color, collection=self.collection)
        return [obj]
