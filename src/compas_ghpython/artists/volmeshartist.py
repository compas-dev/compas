from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython
from compas.artists import VolMeshArtist
from .artist import GHArtist


class VolMeshArtist(GHArtist, VolMeshArtist):
    """Artist for drawing volmesh data structures.

    Parameters
    ----------
    volmesh : :class:`~compas.datastructures.VolMesh`
        A COMPAS volmesh.
    **kwargs : dict, optional
        Additional keyword arguments.
        See :class:`~compas_ghpython.artists.GHArtist` and :class:`~compas.artists.VolMeshArtist` for more info.

    """

    def __init__(self, volmesh, **kwargs):
        super(VolMeshArtist, self).__init__(volmesh=volmesh, **kwargs)

    def draw(self, cells=None, color=None):
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the cells.
            The default color is :attr:`VolMeshArtist.default_cellcolor`.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]
            The GUIDs of the created Rhino objects.
            Every cell is drawn as an individual mesh.

        """
        return self.draw_cells(cells=cells, color=color)

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list
            A list of vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`]
            The color specification for the vertices.
            The default color of the vertices is :attr:`VolMeshArtist.default_vertexcolor`.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        self.vertex_color = color
        vertices = vertices or self.vertices
        vertex_xyz = self.vertex_xyz
        points = []
        for vertex in vertices:
            points.append(
                {
                    "pos": vertex_xyz[vertex],
                    "name": "{}.vertex.{}".format(self.volmesh.name, vertex),
                    "color": self.vertex_color[vertex].rgb255,
                }
            )
        return compas_ghpython.draw_points(points)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[int, int], :class:`~compas.colors.Color`], optional
            The color specification for the edges.
            The default color is :attr:`VolMeshArtist.default_edgecolor`.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        self.edge_color = color
        edges = edges or self.edges
        vertex_xyz = self.vertex_xyz
        lines = []
        for edge in edges:
            u, v = edge
            lines.append(
                {
                    "start": vertex_xyz[u],
                    "end": vertex_xyz[v],
                    "color": self.edge_color[edge].rgb255,
                    "name": "{}.edge.{}-{}".format(self.volmesh.name, u, v),
                }
            )
        return compas_ghpython.draw_lines(lines)

    def draw_faces(self, faces=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[list[int]], optional
            A list of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color specification for the faces.
            The default color is :attr:`VolMeshArtist.default_facecolor`.
        join_faces : bool, optional
            If True, join the faces into one mesh.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        self.face_color = color
        faces = faces or self.faces
        vertex_xyz = self.vertex_xyz
        facets = []
        for face in faces:
            facets.append(
                {
                    "points": [vertex_xyz[vertex] for vertex in self.volmesh.halfface_vertices(face)],
                    "name": "{}.face.{}".format(self.volmesh.name, face),
                    "color": self.face_color[face].rgb255,
                }
            )
        return compas_ghpython.draw_faces(facets)

    def draw_cells(self, cells=None, color=None):
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the cells.
            The default color is :attr:`VolMeshArtist.default_cellcolor`.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        self.cell_color = color
        cells = cells or self.cells
        vertex_xyz = self.vertex_xyz
        meshes = []
        for cell in cells:
            vertices = self.volmesh.cell_vertices(cell)
            faces = self.volmesh.cell_faces(cell)
            vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))
            vertices = [vertex_xyz[vertex] for vertex in vertices]
            faces = [[vertex_index[vertex] for vertex in self.volmesh.halfface_vertices(face)] for face in faces]
            mesh = compas_ghpython.draw_mesh(vertices, faces, color=self.cell_color[cell].rgb255)
            meshes.append(mesh)
        return meshes

    def clear_vertices(self):
        """GH Artists are state-less. Therefore, clear does not have any effect.

        Returns
        -------
        None

        """
        pass

    def clear_edges(self):
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

    def clear_cells(self):
        """GH Artists are state-less. Therefore, clear does not have any effect.

        Returns
        -------
        None

        """
        pass

    def clear_vertexlabels(self):
        """GH Artists are state-less. Therefore, clear does not have any effect.

        Returns
        -------
        None

        """
        pass

    def clear_edgelabels(self):
        """GH Artists are state-less. Therefore, clear does not have any effect.

        Returns
        -------
        None

        """
        pass

    def clear_facelabels(self):
        """GH Artists are state-less. Therefore, clear does not have any effect.

        Returns
        -------
        None

        """
        pass

    def clear_celllabels(self):
        """GH Artists are state-less. Therefore, clear does not have any effect.

        Returns
        -------
        None

        """
        pass
