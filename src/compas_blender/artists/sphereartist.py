from typing import Optional
from typing import Any
from typing import List
from typing import Union

import bpy

import compas_blender
from compas_blender.utilities import RGBColor
from compas.geometry import Sphere
from compas.artists import ShapeArtist
from .artist import BlenderArtist


class SphereArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing sphere shapes.

    Parameters
    ----------
    sphere : :class:`compas.geometry.Sphere`
        A COMPAS sphere.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 sphere: Sphere,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):

        super().__init__(shape=sphere, collection=collection or sphere.name, **kwargs)

    def draw(self, color: Optional[RGBColor] = None, u: int = None, v: int = None) -> List[bpy.types.Object]:
        """Draw the sphere associated with the artist.

        Parameters
        ----------
        color : tuple of float or tuple of int, optional
            The RGB color of the sphere.
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~SphereArtist.u``.
        v : int, optional
            Number of faces in the "v" direction.
            Default is ``~SphereArtist.v``.

        Returns
        -------
        list
            The objects created in Blender.
        """
        u = u or self.u
        v = v or self.v
        color = color or self.color
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        obj = compas_blender.draw_mesh(vertices, faces, name=self.shape.name, color=color, collection=self.collection)
        return [obj]
