from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
import compas_ghpython
from compas.artists import MeshArtist
from .artist import GHArtist


class MeshArtist(GHArtist, MeshArtist):
    """Artist for drawing mesh data structures.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A COMPAS mesh.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.MeshArtist` for more info.

    """

    def __init__(self, mesh, **kwargs):
        super(MeshArtist, self).__init__(mesh=mesh, **kwargs)

    def draw(self, color=None):
        """Draw the mesh.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The color of the mesh.
            Default is the value of :attr:`MeshArtist.default_color`.

        Returns
        -------
        :rhino:`Rhino.Geometry.Mesh`

        """
        self.color = color
        vertices, faces = self.mesh.to_vertices_and_faces()
        return compas_ghpython.draw_mesh(vertices, faces, self.color.rgb255)

    def draw_mesh(self, color=None):
        """Draw the mesh as a RhinoMesh.

        This method is an alias for :attr:`MeshArtist.draw`.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The color of the mesh.
            Default is the value of :attr:`MeshArtist.default_color`.

        Returns
        -------
        :rhino:`Rhino.Geometry.Mesh`

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have only triangular or quadrilateral faces.
        Faces with more than 4 vertices will be triangulated on-the-fly.

        """
        return self.draw(color=color)

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color specification for the vertices.
            The default is the value of :attr:`MeshArtist.default_vertexcolor`.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        self.vertex_color = color
        vertices = vertices or list(self.mesh.vertices())
        vertex_xyz = self.vertex_xyz
        points = []
        for vertex in vertices:
            points.append(
                {
                    "pos": vertex_xyz[vertex],
                    "name": "{}.vertex.{}".format(self.mesh.name, vertex),
                    "color": self.vertex_color[vertex].rgb255,
                }
            )
        return compas_ghpython.draw_points(points)

    def draw_faces(self, faces=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color specification for the faces.
            The default color is the value of :attr:`MeshArtist.default_facecolor`.
        join_faces : bool, optional
            If True, join the individual faces into one mesh.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        self.face_color = color
        faces = faces or list(self.mesh.faces())
        vertex_xyz = self.vertex_xyz
        facets = []
        for face in faces:
            facets.append(
                {
                    "points": [vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)],
                    "name": "{}.face.{}".format(self.mesh.name, face),
                    "color": self.face_color[face].rgb255,
                }
            )
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
        edges : list[tuple[int, int]], optional
            A selection of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[int, int], :class:`~compas.colors.Color`], optional
            The color specification for the edges.
            The default color is the value of :attr:`MeshArtist.default_edgecolor`.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        self.edge_color = color
        edges = edges or list(self.mesh.edges())
        vertex_xyz = self.vertex_xyz
        lines = []
        for edge in edges:
            u, v = edge
            lines.append(
                {
                    "start": vertex_xyz[u],
                    "end": vertex_xyz[v],
                    "color": self.edge_color[edge].rgb255,
                    "name": "{}.edge.{}-{}".format(self.mesh.name, u, v),
                }
            )
        return compas_ghpython.draw_lines(lines)

    def clear_edges(self):
        """GH Artists are state-less. Therefore, clear does not have any effect.

        Returns
        -------
        None

        """
        pass

    def clear_vertices(self):
        """GH Artists are state-less. Therefore, clear does not have any effect.

        Returns
        -------
        None

        """
        pass

    def clear_faces(self):
        """GH Artists are state-less. Therefore, clear does not have any effect.

        Returns
        -------
        None

        """
        pass
