from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino.conversions import vertices_and_faces_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class PolyhedronArtist(RhinoArtist, GeometryObject):
    """Artist for drawing polyhedron shapes.

    Parameters
    ----------
    polyhedron : :class:`~compas.geometry.Polyhedron`
        A COMPAS polyhedron.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, polyhedron, **kwargs):
        super(PolyhedronArtist, self).__init__(geometry=polyhedron, **kwargs)

    def draw(self, color=None):
        """Draw the polyhedron associated with the artist.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the polyhedron.

        Returns
        -------
        System.Guid
            The GUID of the object created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        vertices = [list(vertex) for vertex in self.geometry.vertices]
        faces = self.geometry.faces

        return sc.doc.Objects.AddMesh(vertices_and_faces_to_rhino(vertices, faces), attr)
