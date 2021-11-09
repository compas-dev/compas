from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas_blender.utilities import RGBColor
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

    def draw(self, color: Optional[RGBColor] = None, u: int = None) -> List[bpy.types.Object]:
        """Draw the cylinder associated with the artist.

        Parameters
        ----------
        color : tuple of float or tuple of int, optional
            The RGB color of the cylinder.
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~CylinderArtist.u``.

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
