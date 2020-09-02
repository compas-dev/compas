from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_ghpython

from compas_ghpython.artists._artist import BaseArtist
from compas.utilities import color_to_colordict as colordict


__all__ = ['VolMeshArtist']


class VolMeshArtist(BaseArtist):
    """A volmesh artist defines functionality for visualising COMPAS volmeshes in GhPython.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A COMPAS volmesh.
    settings : dict, optional
        A dict with custom visualisation settings.

    Attributes
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        The COMPAS volmesh associated with the artist.
    settings : dict
        Default settings for color, scale, tolerance, ...

    Examples
    --------
    .. code-block:: python

        pass

    """

    def __init__(self, volmesh):
        self._volmesh = None
        self.volmesh = volmesh
        self.settings = {
            'color.vertices': (255, 255, 255),
            'color.edges': (0, 0, 0),
            'color.faces': (210, 210, 210),
            'show.vertices': True,
            'show.edges': True,
            'show.faces': True,
            'show.vertexlabels': False,
            'show.facelabels': False,
            'show.edgelabels': False,
        }

    @property
    def volmesh(self):
        """compas.datastructures.VolMesh: The volmesh that should be painted."""
        return self._volmesh

    @volmesh.setter
    def volmesh(self, volmesh):
        self._volmesh = volmesh

    def draw(self):
        """For meshes (and data structures in general), a main draw function does not exist.
        Instead, you should use the drawing functions for the various components of the mesh:

        * ``draw_vertices``
        * ``draw_faces``
        * ``draw_edges``
        """
        raise NotImplementedError

    # ==============================================================================
    # components
    # ==============================================================================

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list, optional
            A selection of vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : rgb-tuple or dict of rgb-tuple, optional
            The color specififcation for the vertices.
            The default color is defined in the class settings.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        vertices = vertices or list(self.volmesh.vertices())
        vertex_color = colordict(color, vertices, default=self.settings['color.vertices'], colorformat='rgb', normalize=False)
        points = []
        for vertex in vertices:
            points.append({
                'pos': self.volmesh.vertex_coordinates(vertex),
                'name': "{}.vertex.{}".format(self.volmesh.name, vertex),
                'color': vertex_color[vertex]})
        return compas_ghpython.draw_points(points)

    def draw_faces(self, faces=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list
            A selection of faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : rgb-tuple or dict of rgb-tuple, optional
            The color specififcation for the faces.
            The default color is in the class settings.

        Returns
        -------
        list of :class:`Rhino.Geometry.Mesh`

        """
        faces = faces or list(self.volmesh.faces())
        face_color = colordict(color, faces, default=self.settings['color.faces'], colorformat='rgb', normalize=False)
        faces_ = []
        for face in faces:
            faces_.append({
                'points': self.volmesh.face_coordinates(face),
                'name': "{}.face.{}".format(self.volmesh.name, face),
                'color': face_color[face]})
        meshes = compas_ghpython.draw_faces(faces_)
        if not join_faces:
            return meshes
        joined_mesh = Rhino.Geometry.Mesh()
        for mesh in meshes:
            joined_mesh.Append(mesh)
        return [joined_mesh]

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list, optional
            A selection of edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : rgb-tuple or dict of rgb-tuple, optional
            The color specififcation for the edges.
            The default color is in the class settings.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`

        """
        edges = edges or list(self.volmesh.edges())
        edge_color = colordict(color, edges, default=self.settings['color.edges'], colorformat='rgb', normalize=False)
        lines = []
        for edge in edges:
            start, end = self.volmesh.edge_coordinates(*edge)
            lines.append({
                'start': start,
                'end': end,
                'color': edge_color[edge],
                'name': "{}.edge.{}-{}".format(self.volmesh.name, *edge)})
        return compas_ghpython.draw_lines(lines)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
