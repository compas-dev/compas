from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

import Rhino

from compas.utilities import color_to_colordict

import compas_ghpython
from compas.artists import VolMeshArtist
from .artist import GHArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


class VolMeshArtist(GHArtist, VolMeshArtist):
    """Artist for drawing volmesh data structures.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A COMPAS volmesh.
    """

    def __init__(self, volmesh, **kwargs):
        super(VolMeshArtist, self).__init__(volmesh=volmesh, **kwargs)

    def draw(self):
        """"""
        raise NotImplementedError

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list
            A list of vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : str, tuple, dict
            The color specififcation for the vertices.
            The default color of the vertices is ``~VolMeshArtist.default_vertexcolor``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`
        """
        self.vertex_color = color
        vertices = vertices or list(self.volmesh.vertices())
        vertex_xyz = self.vertex_xyz
        points = []
        for vertex in vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.volmesh.name, vertex),
                'color': self.vertex_color.get(vertex, self.default_vertexcolor)
            })
        return compas_ghpython.draw_points(points)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list, optional
            A list of edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            The default color is ``~VolMeshArtist.default_edgecolor``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`
        """
        self.edge_color = color
        edges = edges or list(self.volmesh.edges())
        vertex_xyz = self.vertex_xyz
        lines = []
        for edge in edges:
            lines.append({
                'start': vertex_xyz[edge[0]],
                'end': vertex_xyz[edge[1]],
                'color': self.edge_color.get(edge, self.default_edgecolor),
                'name': "{}.edge.{}-{}".format(self.volmesh.name, *edge)
            })
        return compas_ghpython.draw_lines(lines)

    def draw_faces(self, faces=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list, optional
            A list of faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : str, tuple, dict
            The color specififcation for the faces.
            The default color is ``~VolMeshArtist.default_facecolor``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Mesh`
        """
        self.face_color = color
        faces = faces or list(self.volmesh.faces())
        vertex_xyz = self.vertex_xyz
        facets = []
        for face in faces:
            facets.append({
                'points': [vertex_xyz[vertex] for vertex in self.volmesh.halfface_vertices(face)],
                'name': "{}.face.{}".format(self.volmesh.name, face),
                'color': self.face_color.get(face, self.default_facecolor)
            })
        meshes = compas_ghpython.draw_faces(facets)
        if not join_faces:
            return meshes
        joined_mesh = Rhino.Geometry.Mesh()
        for mesh in meshes:
            joined_mesh.Append(mesh)
        return [joined_mesh]
