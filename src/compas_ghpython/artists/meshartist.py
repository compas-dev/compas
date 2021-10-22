from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
from functools import partial

from compas.geometry import centroid_polygon
from compas.utilities import color_to_colordict
from compas.utilities import pairwise

import compas_ghpython
from compas.artists import MeshArtist
from .artist import GHArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


class MeshArtist(GHArtist, MeshArtist):
    """Artist for drawing mesh data structures.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    """

    def __init__(self, mesh, **kwargs):
        super(MeshArtist, self).__init__(mesh=mesh, **kwargs)

    def draw(self, color=None):
        """Draw the mesh as a RhinoMesh.

        Parameters
        ----------
        color : tuple, optional
            The color of the mesh.
            Default is the value of ``~MeshArtist.default_color``.

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have only triangular or quadrilateral faces.
        Faces with more than 4 vertices will be triangulated on-the-fly.
        """
        color = color or self.default_color
        vertex_index = self.mesh.vertex_index()
        vertex_xyz = self.vertex_xyz
        vertices = [vertex_xyz[vertex] for vertex in self.mesh.vertices()]
        faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]
        new_faces = []
        for face in faces:
            f = len(face)
            if f == 3:
                new_faces.append(face + [face[-1]])
            elif f == 4:
                new_faces.append(face)
            elif f > 4:
                centroid = len(vertices)
                vertices.append(centroid_polygon(
                    [vertices[index] for index in face]))
                for a, b in pairwise(face + face[0:1]):
                    new_faces.append([centroid, a, b, b])
        return compas_ghpython.draw_mesh(vertices, new_faces, color)

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list, optional
            A selection of vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : tuple or dict of tuple, optional
            The color specififcation for the vertices.
            The default is the value of ``~MeshArtist.default_vertexcolor``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        self.vertex_color = color
        vertices = vertices or list(self.mesh.vertices())
        vertex_xyz = self.vertex_xyz
        points = []
        for vertex in vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.mesh.name, vertex),
                'color': self.vertex_color.get(vertex, self.default_vertexcolor)
            })
        return compas_ghpython.draw_points(points)

    def draw_faces(self, faces=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list, optional
            A selection of faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : tuple or dict of tuple, optional
            The color specififcation for the faces.
            The default color is the value of ``~MeshArtist.default_facecolor``.
        join_faces : bool, optional
            Join the faces into 1 mesh.
            Default is ``False``, in which case the faces are drawn as individual meshes.

        Returns
        -------
        list of :class:`Rhino.Geometry.Mesh`

        """
        self.face_color = color
        faces = faces or list(self.mesh.faces())
        vertex_xyz = self.vertex_xyz
        facets = []
        for face in faces:
            facets.append({
                'points': [vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)],
                'name': "{}.face.{}".format(self.mesh.name, face),
                'color': self.face_color.get(face, self.default_facecolor)
            })
        meshes = compas_ghpython.draw_faces(facets)
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
        color : tuple or dict of tuple, optional
            The color specififcation for the edges.
            The default color is the value of ``~MeshArtist.default_edgecolor``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`

        """
        self.edge_color = color
        edges = edges or list(self.mesh.edges())
        vertex_xyz = self.vertex_xyz
        lines = []
        for edge in edges:
            lines.append({
                'start': vertex_xyz[edge[0]],
                'end': vertex_xyz[edge[1]],
                'color': self.edge_color.get(edge, self.default_edgecolor),
                'name': "{}.edge.{}-{}".format(self.mesh.name, *edge)
            })
        return compas_ghpython.draw_lines(lines)

    def clear_edges(self):
        """GH Artists are state-less. Clear does not have any effect."""
        pass

    def clear_vertices(self):
        """GH Artists are state-less. Clear does not have any effect."""
        pass

    def clear_faces(self):
        """GH Artists are state-less. Clear does not have any effect."""
        pass
