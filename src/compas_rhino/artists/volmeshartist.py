from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import TextDot  # type: ignore
import scriptcontext as sc  # type: ignore

import compas_rhino
from compas.geometry import centroid_points
from compas.geometry import Line
from compas.artists import VolMeshArtist as BaseArtist
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from compas_rhino.conversions import vertices_and_faces_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes
from ._helpers import ngon


class VolMeshArtist(RhinoArtist, BaseArtist):
    """Artist for drawing volmesh data structures.

    Parameters
    ----------
    volmesh : :class:`~compas.datastructures.VolMesh`
        A COMPAS volmesh.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`VolMeshArtist`.

    """

    def __init__(self, volmesh, **kwargs):
        super(VolMeshArtist, self).__init__(volmesh=volmesh, **kwargs)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Delete all objects drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.*".format(self.volmesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertices(self):
        """Delete all vertices drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*".format(self.volmesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edges(self):
        """Delete all edges drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edge.*".format(self.volmesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_faces(self):
        """Delete all faces drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.face.*".format(self.volmesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_cells(self):
        """Delete all cells drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.cell.*".format(self.volmesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertexlabels(self):
        """Delete all vertex labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*.label".format(self.volmesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edgelabels(self):
        """Delete all edge labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edge.*.label".format(self.volmesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_facelabels(self):
        """Delete all face labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.face.*.label".format(self.volmesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

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
        list[System.Guid]
            The GUIDs of the created Rhino objects.
            Every cell is drawn as an individual mesh.

        """
        return self.draw_cells(cells=cells, color=color)

    def draw_vertices(self, vertices=None, color=None, text=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A list of vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the vertices.
        text : dict[int, str], optional
            A dictionary of vertex labels as vertex-text pairs.
        fontheight : int, optional
            Font height of the vertex labels.
        fontface : str, optional
            Font face of the vertex labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        vertices = vertices or self.volmesh.vertices()  # type: ignore
        self.vertex_color = color
        self.vertex_text = text
        vertex_xyz = self.vertex_xyz
        vertex_color = self.vertex_color
        vertex_text = self.vertex_text

        guids = []

        for vertex in vertices:
            point = vertex_xyz[vertex]
            color = vertex_color[vertex]  # type: ignore
            name = "{}.vertex.{}".format(self.volmesh.name, vertex)  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)
            guid = sc.doc.Objects.AddPoint(point_to_rhino(point), attr)
            guids.append(guid)

            if text:
                if vertex in vertex_text:
                    attr = attributes(name="{}.label".format(name), color=color, layer=self.layer)
                    dot = TextDot(str(vertex_text[vertex]), point)  # type: ignore
                    dot.FontHeight = fontheight
                    dot.FontFace = fontface
                    sc.doc.Objects.AddTextDot(dot, attr)

        return guids

    def draw_edges(self, edges=None, color=None, text=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[int, int], :class:`~compas.colors.Color`], optional
            The color of the edges.
        text : dict[tuple[int, int], str], optional
            A dictionary of edge labels as edge-text pairs.
        fontheight : int, optional
            Font height of the edge labels.
        fontface : str, optional
            Font face of the edge labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino line objects.

        """
        edges = edges or self.volmesh.edges()  # type: ignore

        self.edge_color = color
        self.edge_text = text
        vertex_xyz = self.vertex_xyz
        edge_color = self.edge_color
        edge_text = self.edge_text

        guids = []

        for edge in edges:
            color = edge_color[edge]  # type: ignore
            name = "{}.edge.{}-{}".format(self.volmesh.name, *edge)  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)
            line = Line(vertex_xyz[edge[0]], vertex_xyz[edge[1]])
            guid = sc.doc.Objects.AddLine(line_to_rhino(line), attr)
            guids.append(guid)

            if text:
                if edge in edge_text:
                    point = point_to_rhino(line.midpoint)
                    attr = attributes(name="{}.label".format(name), color=color, layer=self.layer)
                    dot = TextDot(str(edge_text[edge]), point)  # type: ignore
                    dot.FontHeight = fontheight
                    dot.FontFace = fontface
                    sc.doc.Objects.AddTextDot(dot, attr)

        return guids

    def draw_faces(self, faces=None, color=None, text=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A list of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the faces.
        text : dict[int, str], optional
            A dictionary of face labels as face-text pairs.
        fontheight : int, optional
            Font height of the face labels.
        fontface : str, optional
            Font face of the face labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        faces = faces or self.volmesh.faces()  # type: ignore
        self.face_color = color
        self.face_text = text
        vertex_xyz = self.vertex_xyz
        face_color = self.face_color
        face_text = self.face_text

        guids = []

        for face in faces:
            color = face_color[face]  # type: ignore
            name = "{}.face.{}".format(self.volmesh.name, face)  # type: ignore
            vertices = [vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(face)]  # type: ignore
            facet = ngon(vertices)
            if facet:
                attr = attributes(name=name, color=color, layer=self.layer)
                guid = sc.doc.Objects.AddMesh(vertices_and_faces_to_rhino(vertices, [facet]), attr)
                guids.append(guid)

            if text:
                if face in face_text:
                    point = point_to_rhino(centroid_points(vertices))  # type: ignore
                    attr = attributes(name="{}.label".format(name), color=color, layer=self.layer)
                    dot = TextDot(str(face_text[face]), point)  # type: ignore
                    dot.FontHeight = fontheight
                    dot.FontFace = fontface
                    sc.doc.Objects.AddTextDot(dot, attr)

        return guids

    def draw_cells(self, cells=None, color=None, text=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the cells.
        text : dict[int, str], optional
            A dictionary of face labels as cell-text pairs.
        fontheight : int, optional
            Font height of the cell labels.
        fontface : str, optional
            Font face of the cell labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.
            Every cell is drawn as an individual mesh.

        """
        cells = cells or self.volmesh.cells()  # type: ignore
        self.cell_color = color
        self.cell_text = text
        vertex_xyz = self.vertex_xyz
        cell_color = self.cell_color
        cell_text = self.cell_text

        guids = []

        for cell in cells:
            vertices = self.volmesh.cell_vertices(cell)  # type: ignore
            faces = self.volmesh.cell_faces(cell)  # type: ignore
            vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))
            vertices = [vertex_xyz[vertex] for vertex in vertices]
            faces = [[vertex_index[vertex] for vertex in self.volmesh.halfface_vertices(face)] for face in faces]  # type: ignore
            name = "{}.cell.{}".format(self.volmesh.name, cell)  # type: ignore
            color = cell_color[cell]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)
            guid = sc.doc.Objects.AddMesh(vertices_and_faces_to_rhino(vertices, faces, disjoint=True), attr)
            guids.append(guid)

            if text:
                if cell in cell_text:
                    point = point_to_rhino(centroid_points(vertices))  # type: ignore
                    attr = attributes(name="{}.label".format(name), color=color, layer=self.layer)
                    dot = TextDot(str(cell_text[cell]), point)  # type: ignore
                    dot.FontHeight = fontheight
                    dot.FontFace = fontface
                    sc.doc.Objects.AddTextDot(dot, attr)

        return guids
