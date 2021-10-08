from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.artists import ShapeArtist
from .artist import RhinoArtist


class BoxArtist(RhinoArtist, ShapeArtist):
    """Artist for drawing box shapes.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`
        A COMPAS box.
    layer : str, optional
        The layer that should contain the drawing.
    """

    def __init__(self, box, layer=None, **kwargs):
        super(BoxArtist, self).__init__(shape=box, layer=layer, **kwargs)

    def draw(self, color=None):
        """Draw the box associated with the artist.

        Parameters
        ----------
        color : tuple of float, optional
            The RGB color of the box.

        Returns
        -------
        list
            The GUIDs of the objects created in Rhino.
        """
        color = color or self.color
        vertices = [list(vertex) for vertex in self.shape.vertices]
        polygons = [{'points': [vertices[index] for index in face]} for face in self.shape.faces]
        guids = compas_rhino.draw_faces(polygons, clear=False, redraw=False)
        guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
        compas_rhino.rs.ObjectLayer(guid, self.layer)
        compas_rhino.rs.ObjectName(guid, self.shape.name)
        compas_rhino.rs.ObjectColor(guid, color)
        return [guid]
