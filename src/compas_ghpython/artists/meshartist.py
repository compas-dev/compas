from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time

import compas
import compas_ghpython

from compas_ghpython.artists.mixins import VertexArtist
from compas_ghpython.artists.mixins import EdgeArtist
from compas_ghpython.artists.mixins import FaceArtist

__all__ = ['MeshArtist']


class MeshArtist(FaceArtist, EdgeArtist, VertexArtist):
    """A mesh artist defines functionality for visualising COMPAS meshes in Grasshopper.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A COMPAS mesh.
    layer : str, optional
        Layer is ignored.

    Attributes
    ----------
    defaults : dict
        Default settings for color, scale, tolerance, ...

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas_ghpython.artists import MeshArtist

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        artist = MeshArtist(mesh)
        artist.clear_layer()
        artist.draw_faces()
        artist.draw_vertices()
        artist.draw_edges()
        artist.redraw()

    """

    def __init__(self, mesh, layer=None):
        self.objects = dict(faces={}, edges={}, vertices={})
        self.mesh = mesh
        self.layer = layer
        self.defaults = {
            'color.vertex': (255, 0, 0),
            'color.face': (255, 255, 255),
            'color.edge': (0, 0, 0),
        }

    @property
    def layer(self):
        """str: The layer that contains the mesh."""
        return self.datastructure.attributes.get('layer')

    @layer.setter
    def layer(self, value):
        self.datastructure.attributes['layer'] = value

    @property
    def mesh(self):
        """compas.datastructures.Mesh: The mesh that should be painted."""
        return self.datastructure

    @mesh.setter
    def mesh(self, mesh):
        self.datastructure = mesh

    def clear(self):
        self.clear_vertices()
        self.clear_faces()
        self.clear_edges()

    def redraw(self, timeout=None):
        """Redraw the Grasshopper geometry.

        Parameters
        ----------
        timeout : float, optional
            The amount of time the artist waits before updating the Grasshopper view.
            The time should be specified in seconds.
            Default is ``None``.

        """
        if timeout:
            time.sleep(timeout)

        points = compas_ghpython.xdraw_points(self.objects['vertices'].values())
        faces = compas_ghpython.xdraw_faces(self.objects['faces'].values())
        edges = compas_ghpython.xdraw_lines(self.objects['edges'].values())

        return points + faces + edges
