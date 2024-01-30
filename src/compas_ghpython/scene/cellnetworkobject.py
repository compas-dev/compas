from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions
from compas_rhino.scene._helpers import ngon

from compas.scene import CellNetworkObject as BaseCellNetworkObject
from .sceneobject import GHSceneObject


class CellNetworkObject(GHSceneObject, BaseCellNetworkObject):
    """Scene object for drawing cellnetwork data structures.

    Parameters
    ----------
    cellnetwork : :class:`compas.datastructures.CellNetwork`
        A COMPAS cellnetwork.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, cellnetwork, **kwargs):
        super(CellNetworkObject, self).__init__(cellnetwork=cellnetwork, **kwargs)

    def draw(self, cells=None, color=None):
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the cells.
            The default color is :attr:`CellNetworkObject.default_cellcolor`.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]
            List of created Rhino meshes.

        """
        self._guids = self.draw_cells(cells=cells, color=color)
        return self.guids

    def draw_vertices(self, vertices=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list
            A list of vertices to draw.
            Default is None, in which case all vertices are drawn.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        points = []

        for vertex in vertices or self.cellnetwork.vertices():  # type: ignore
            points.append(conversions.point_to_rhino(self.vertex_xyz[vertex]))

        return points

    def draw_edges(self, edges=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        lines = []

        for edge in edges or self.cellnetwork.edges():  # type: ignore
            lines.append(conversions.line_to_rhino((self.vertex_xyz[edge[0]], self.vertex_xyz[edge[1]])))

        return lines

    def draw_faces(self, faces=None, color=None):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[list[int]], optional
            A list of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color specification for the faces.
            The default color is :attr:`CellNetworkObject.default_facecolor`.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        faces = faces or self.cellnetwork.faces()  # type: ignore

        self.facecolor = color

        meshes = []

        for face in faces:
            color = self.facecolor[face]  # type: ignore
            vertices = [self.vertex_xyz[vertex] for vertex in self.cellnetwork.face_vertices(face)]  # type: ignore
            facet = ngon(len(vertices))
            if facet:
                meshes.append(conversions.vertices_and_faces_to_rhino(vertices, [facet]))

        return meshes

    def draw_cells(self, cells=None, color=None):
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color of the cells.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        self.cellcolor = color

        meshes = []

        for cell in cells or self.cellnetwork.cells():  # type: ignore
            color = self.cellcolor[cell]  # type: ignore

            vertices = self.cellnetwork.cell_vertices(cell)  # type: ignore
            faces = self.cellnetwork.cell_faces(cell)  # type: ignore
            vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))
            vertices = [self.vertex_xyz[vertex] for vertex in vertices]
            faces = [[vertex_index[vertex] for vertex in self.cellnetwork.face_vertices(face)] for face in faces]  # type: ignore

            mesh = conversions.vertices_and_faces_to_rhino(vertices, faces, disjoint=True)
            meshes.append(mesh)

        return meshes
