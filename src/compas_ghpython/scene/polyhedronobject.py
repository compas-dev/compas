from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class PolyhedronObject(GHSceneObject, GeometryObject):
    """Scene object for drawing polyhedron shapes.

    Parameters
    ----------
    polyhedron : :class:`compas.geometry.Polyhedron`
        A COMPAS polyhedron.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, polyhedron, **kwargs):
        super(PolyhedronObject, self).__init__(geometry=polyhedron, **kwargs)

    def draw(self, color=None):
        """Draw the polyhedron associated with the scene object.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The RGB color of the line.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]
            List of created Rhino mesh.

        """
        color = Color.coerce(color) or self.color
        vertices, faces = self.geometry.to_vertices_and_faces()

        geometry = conversions.vertices_and_faces_to_rhino(vertices, faces, color=color)
        geometry.Transform(conversions.transformation_to_rhino(self.transformation_world))

        self._guids = [geometry]
        return self.guids
