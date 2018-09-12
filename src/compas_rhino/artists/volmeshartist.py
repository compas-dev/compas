from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time

import compas
import compas_rhino

from compas_rhino.artists.mixins import VertexArtist
from compas_rhino.artists.mixins import EdgeArtist
from compas_rhino.artists.mixins import FaceArtist

try:
    import rhinoscriptsyntax as rs

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['VolMeshArtist']


class VolMeshArtist(FaceArtist, EdgeArtist, VertexArtist):
    """A volmesh artist defines functionality for visualising COMPAS volmeshes in Rhino.

    Parameters
    ----------
    volmesh : compas.datastructures.VolMesh
        A COMPAS volmesh.
    layer : str, optional
        The name of the layer that will contain the volmesh.

    Attributes
    ----------
    defaults : dict
        Default settings for color, scale, tolerance, ...

    """

    def __init__(self, volmesh, layer=None):
        self.volmesh = volmesh
        self.layer = layer
        self.defaults = {
            'color.vertex' : (255, 0, 0),
            'color.face'   : (255, 255, 255),
            'color.edge'   : (0, 0, 0),
        }

    @property
    def layer(self):
        """str: The layer that contains the volmesh."""
        return self.datastructure.attributes.get('layer')

    @layer.setter
    def layer(self, value):
        self.datastructure.attributes['layer'] = value

    @property
    def volmesh(self):
        """compas.datastructures.VolMesh: The volmesh that should be painted."""
        return self.datastructure

    @volmesh.setter
    def volmesh(self, volmesh):
        self.datastructure = volmesh

    def redraw(self, timeout=None):
        """Redraw the Rhino view.

        Parameters
        ----------
        timeout : float, optional
            The amount of time the artist waits before updating the Rhino view.
            The time should be specified in seconds.
            Default is ``None``.

        """
        if timeout:
            time.sleep(timeout)
        rs.EnableRedraw(True)
        rs.Redraw()

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)

    def clear(self):
        """Clear the vertices, faces and edges of the volmesh, without clearing the
        other elements in the layer."""
        self.clear_vertices()
        self.clear_faces()
        self.clear_edges()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures import VolMesh
    from compas_rhino.artists.volmeshartist import VolMeshArtist

    volmesh = VolMesh.from_obj(compas.get('boxes.obj'))

    artist = VolMeshArtist(volmesh, layer='VolMeshArtist')

    artist.clear_layer()

    artist.draw_vertices()
    artist.redraw(0.0)

    artist.draw_vertexlabels()
    artist.redraw(1.0)

    artist.draw_faces()
    artist.redraw(1.0)

    artist.draw_facelabels()
    artist.redraw(1.0)

    artist.draw_edges()
    artist.redraw(1.0)

    artist.draw_edgelabels()
    artist.redraw(1.0)
