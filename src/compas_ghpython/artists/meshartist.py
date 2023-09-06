from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.artists import MeshArtist as BaseArtist
from compas.colors import Color
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino
from compas_rhino.artists._helpers import ngon
from .artist import GHArtist


class MeshArtist(GHArtist, BaseArtist):
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

    def draw(self, color=None, vertexcolors=None, facecolors=None, disjoint=False):
        """Draw the mesh.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The color of the mesh.

        Returns
        -------
        :rhino:`Rhino.Geometry.Mesh`

        """
        # the rhino artist can set an overal color and component colors simultaneously
        # because it can set an overall color on the mesh object attributes
        # this is not possible in GH (since there is no such object)
        # either we set an overall color or we set component colors
        if not vertexcolors and not facecolors:
            color = Color.coerce(color) or self.color

        vertex_index = self.mesh.vertex_index()  # type: ignore
        vertex_xyz = self.vertex_xyz

        vertices = [vertex_xyz[vertex] for vertex in self.mesh.vertices()]  # type: ignore
        faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]  # type: ignore

        return vertices_and_faces_to_rhino(
            vertices,
            faces,
            color=color,
            vertexcolors=vertexcolors,
            facecolors=facecolors,
            disjoint=disjoint,
        )

    def draw_mesh(self, color=None, vertexcolors=None, facecolors=None, disjoint=False):
        """Draw the mesh as a RhinoMesh.

        This method is an alias for :attr:`MeshArtist.draw`.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The color of the mesh.

        Returns
        -------
        :rhino:`Rhino.Geometry.Mesh`

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have only triangular or quadrilateral faces.
        Faces with more than 4 vertices will be triangulated on-the-fly.

        """
        return self.draw(color=color, vertexcolors=vertexcolors, facecolors=facecolors, disjoint=disjoint)

    def draw_vertices(self, vertices=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertices to draw.
            Default is None, in which case all vertices are drawn.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        vertices = vertices or self.mesh.vertices()  # type: ignore
        vertex_xyz = self.vertex_xyz

        points = []

        for vertex in vertices:
            points.append(point_to_rhino(vertex_xyz[vertex]))

        return points

    def draw_faces(self, faces=None, color=None):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color specification for the faces.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        faces = faces or self.mesh.faces()  # type: ignore

        self.face_color = color
        vertex_xyz = self.vertex_xyz
        face_color = self.face_color

        meshes = []

        for face in faces:
            color = face_color[face]  # type: ignore
            vertices = [vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]  # type: ignore
            facet = ngon(len(vertices))
            if facet:
                meshes.append(vertices_and_faces_to_rhino(vertices, [facet]))

        return meshes

    def draw_edges(self, edges=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A selection of edges to draw.
            The default is None, in which case all edges are drawn.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        edges = edges or self.mesh.edges()  # type: ignore

        vertex_xyz = self.vertex_xyz

        lines = []

        for edge in edges:
            lines.append(line_to_rhino((vertex_xyz[edge[0]], vertex_xyz[edge[1]])))

        return lines
