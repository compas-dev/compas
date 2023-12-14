from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color

from compas_rhino import conversions

from compas.scene import GeometryObject
from .sceneobject import GHSceneObject


class PolygonObject(GHSceneObject, GeometryObject):
    """Scene object for drawing polygons.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon`
        A COMPAS polygon.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, polygon, **kwargs):
        super(PolygonObject, self).__init__(geometry=polygon, **kwargs)

    def draw(self, color=None, show_vertices=False, show_edges=False):
        """Draw the polygon.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The RGB color of the polygon.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        color = Color.coerce(color) or self.color
        vertices = self.geometry.vertices
        faces = self.geometry.faces

        geometry = conversions.vertices_and_faces_to_rhino(vertices, faces, color=color)

        if self.transformation:
            geometry.Transform(conversions.transformation_to_rhino(self.transformation))

        self._guids = [geometry]
        return self.guids
