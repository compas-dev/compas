from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

import Rhino

import compas_ghpython
from compas_ghpython.artists._artist import BaseArtist

# from compas.geometry import centroid_polygon
from compas.utilities import color_to_colordict
# from compas.utilities import pairwise


colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


__all__ = ['VolMeshArtist']


class VolMeshArtist(BaseArtist):
    """A volmesh artist defines functionality for visualising COMPAS volmeshes in GhPython.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A COMPAS volmesh.

    Attributes
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        The COMPAS volmesh associated with the artist.
    color_vertices : 3-tuple
        Default color of the vertices.
    color_edges : 3-tuple
        Default color of the edges.
    color_faces : 3-tuple
        Default color of the faces.

    """

    def __init__(self, volmesh):
        self._volmesh = None
        self.volmesh = volmesh
        self.color_vertices = (255, 255, 255)
        self.color_edges = (0, 0, 0)
        self.color_faces = (210, 210, 210)

    @property
    def volmesh(self):
        """compas.datastructures.VolMesh: The volmesh that should be painted."""
        return self._volmesh

    @volmesh.setter
    def volmesh(self, volmesh):
        self._volmesh = volmesh

    def draw(self):
        """"""
        raise NotImplementedError

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list, optional
            A selection of vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : 3-tuple or dict of 3-tuple, optional
            The color specififcation for the vertices.
            The default color is ``(255, 255, 255)``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        vertices = vertices or list(self.volmesh.vertices())
        vertex_color = colordict(color, vertices, default=self.color_vertices)
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
        color : 3-tuple or dict of 3-tuple, optional
            The color specififcation for the faces.
            The default color is ``(210, 210, 210)``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Mesh`

        """
        faces = faces or list(self.volmesh.faces())
        face_color = colordict(color, faces, default=self.color_faces)
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
        color : 3-tuple or dict of 3-tuple, optional
            The color specififcation for the edges.
            The default color is ``(0, 0, 0)``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`

        """
        edges = edges or list(self.volmesh.edges())
        edge_color = colordict(color, edges, default=self.color_edges)
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
