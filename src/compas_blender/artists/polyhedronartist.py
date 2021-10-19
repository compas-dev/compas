from typing import Optional
from typing import Any
from typing import Union

import bpy
import compas_blender
from compas.geometry import Polyhedron
from compas.artists import ShapeArtist
from .artist import BlenderArtist


class PolyhedronArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing polyhedron shapes.

    Parameters
    ----------
    polyhedron : :class:`compas.geometry.Polyhedron`
        A COMPAS polyhedron.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 polyhedron: Polyhedron,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):

        super().__init__(shape=polyhedron, collection=collection or polyhedron.name, **kwargs)

    def draw(self, color=None):
        """Draw the polyhedron associated with the artist.

        Parameters
        ----------
        color : tuple of float, optional
            The RGB color of the polyhedron.

        Returns
        -------
        list
            The objects created in Blender.
        """
        color = color or self.color
        vertices, faces = self.shape.to_vertices_and_faces()
        obj = compas_blender.draw_mesh(vertices, faces, name=self.shape.name, color=color, collection=self.collection)
        return [obj]
