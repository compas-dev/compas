from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.utilities import is_color_rgb
from compas.geometry import centroid_points

from ._artist import Artist


__all__ = ['VolMeshArtist']


class VolMeshArtist(Artist):
    """Artist for drawing volmesh data structures.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A COMPAS volmesh.
    layer : str, optional
        The name of the layer that will contain the volmesh.

    Attributes
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        The COMPAS volmesh associated with the artist.
    layer : str
        The layer in which the volmesh should be contained.
    vertices : list
        The list of vertices to draw.
        Default is a list of all vertices of the volmesh.
    edges : list
        The list of edges to draw.
        Default is a list of all edges of the volmesh.
    faces : list
        The list of faces to draw.
        Default is a list of all faces of the volmesh.
    cells : list
        The list of cells to draw.
        Default is a list of all cells of the volmesh.
    vertex_xyz : dict[int, tuple(float, float, float)]
        Mapping between vertices and their view coordinates.
        The default view coordinates are the actual coordinates of the vertices of the volmesh.
    vertex_color : dict[int, tuple(int, int, int)]
        Mapping between vertices and RGB color values.
        The colors have to be integer tuples with values in the range ``0-255``.
        Missing vertices get the default vertex color (``MeshArtist.default_vertexcolor``).
    vertex_text : dict[int, str]
        Mapping between vertices and text labels.
        Missing vertices are labelled with the corresponding vertex identifiers.
    edge_color : dict[tuple(int, int), tuple(int, int, int)]
        Mapping between edges and RGB color values.
        The colors have to be integer tuples with values in the range ``0-255``.
        Missing edges get the default edge color (``MeshArtist.default_edgecolor``).
    edge_text : dict[tuple(int, int), str]
        Mapping between edges and text labels.
        Missing edges are labelled with the corresponding edge identifiers.
    face_color : dict[tuple, tuple(int, int, int)]
        Mapping between faces and RGB color values.
        The colors have to be integer tuples with values in the range ``0-255``.
        Missing faces get the default face color (``MeshArtist.default_facecolor``).
    face_text : dict[tuple, str]
        Mapping between faces and text labels.
        Missing faces are labelled with the corresponding face identifiers.
    cell_color : dict[int, tuple(int, int, int)]
        Mapping between cells and RGB color values.
        The colors have to be integer tuples with values in the range ``0-255``.
        Missing cells get the default cell color (``MeshArtist.default_cellcolor``).
    cell_text : dict[int, str]
        Mapping between cells and text labels.
        Missing cells are labelled with the corresponding cell identifiers.

    """

    default_vertexcolor = (255, 255, 255)
    default_edgecolor = (0, 0, 0)
    default_facecolor = (210, 210, 210)
    default_cellcolor = (255, 0, 0)

    def __init__(self, volmesh, layer=None):
        super(VolMeshArtist, self).__init__(volmesh, layer=layer)
        self._vertices = None
        self._edges = None
        self._faces = None
        self._cells = None
        self._vertex_xyz = None
        self._vertex_color = None
        self._edge_color = None
        self._face_color = None
        self._cell_color = None
        self._vertex_text = None
        self._edge_text = None
        self._face_text = None
        self._cell_text = None

    @property
    def volmesh(self):
        return self.item

    @volmesh.setter
    def volmesh(self, volmesh):
        self.item = volmesh
        self._vertex_xyz = None

    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = list(self.volmesh.vertices())
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    def edges(self):
        if self._edges is None:
            self._edges = list(self.volmesh.edges())
        return self._edges

    @edges.setter
    def edges(self, edges):
        self._edges = edges

    @property
    def faces(self):
        if self._faces is None:
            self._faces = list(self.volmesh.faces())
        return self._faces

    @faces.setter
    def faces(self, faces):
        self._faces = faces

    @property
    def cells(self):
        if self._cells is None:
            self._cells = list(self.volmesh.cells())
        return self._cells

    @cells.setter
    def cells(self, cells):
        self._cells = cells

    @property
    def vertex_xyz(self):
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.volmesh.vertex_attributes(vertex, 'xyz') for vertex in self.volmesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    @property
    def vertex_color(self):
        if not self._vertex_color:
            self._vertex_color = {vertex: self.artist.default_vertexcolor for vertex in self.volmesh.vertices()}
        return self._vertex_color

    @vertex_color.setter
    def vertex_color(self, vertex_color):
        if isinstance(vertex_color, dict):
            self._vertex_color = vertex_color
        elif is_color_rgb(vertex_color):
            self._vertex_color = {vertex: vertex_color for vertex in self.volmesh.vertices()}

    @property
    def edge_color(self):
        if not self._edge_color:
            self._edge_color = {edge: self.artist.default_edgecolor for edge in self.volmesh.edges()}
        return self._edge_color

    @edge_color.setter
    def edge_color(self, edge_color):
        if isinstance(edge_color, dict):
            self._edge_color = edge_color
        elif is_color_rgb(edge_color):
            self._edge_color = {edge: edge_color for edge in self.volmesh.edges()}

    @property
    def face_color(self):
        if not self._face_color:
            self._face_color = {face: self.artist.default_facecolor for face in self.volmesh.faces()}
        return self._face_color

    @face_color.setter
    def face_color(self, face_color):
        if isinstance(face_color, dict):
            self._face_color = face_color
        elif is_color_rgb(face_color):
            self._face_color = {face: face_color for face in self.volmesh.faces()}

    @property
    def cell_color(self):
        if not self._cell_color:
            self._cell_color = {cell: self.artist.default_cellcolor for cell in self.volmesh.cells()}
        return self._cell_color

    @cell_color.setter
    def cell_color(self, cell_color):
        if isinstance(cell_color, dict):
            self._cell_color = cell_color
        elif is_color_rgb(cell_color):
            self._cell_color = {cell: cell_color for cell in self.volmesh.cells()}

    @property
    def vertex_text(self):
        if not self._vertex_text:
            self._vertex_text = {vertex: str(vertex) for vertex in self.volmesh.vertices()}
        return self._vertex_text

    @vertex_text.setter
    def vertex_text(self, text):
        if text == 'key':
            self._vertex_text = {vertex: str(vertex) for vertex in self.volmesh.vertices()}
        elif text == 'index':
            self._vertex_text = {vertex: str(index) for index, vertex in enumerate(self.volmesh.vertices())}
        elif isinstance(text, dict):
            self._vertex_text = text

    @property
    def edge_text(self):
        if not self._edge_text:
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.volmesh.edges()}
        return self._edge_text

    @edge_text.setter
    def edge_text(self, text):
        if text == 'key':
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.volmesh.edges()}
        elif text == 'index':
            self._edge_text = {edge: str(index) for index, edge in enumerate(self.volmesh.edges())}
        elif isinstance(text, dict):
            self._edge_text = text

    @property
    def face_text(self):
        if not self._face_text:
            self._face_text = {face: str(face) for face in self.volmesh.faces()}
        return self._face_text

    @face_text.setter
    def face_text(self, text):
        if text == 'key':
            self._face_text = {face: str(face) for face in self.volmesh.faces()}
        elif text == 'index':
            self._face_text = {face: str(index) for index, face in enumerate(self.volmesh.faces())}
        elif isinstance(text, dict):
            self._face_text = text

    @property
    def cell_text(self):
        if not self._cell_text:
            self._cell_text = {cell: str(cell) for cell in self.volmesh.cells()}
        return self._cell_text

    @cell_text.setter
    def cell_text(self, text):
        if text == 'key':
            self._cell_text = {cell: str(cell) for cell in self.volmesh.cells()}
        elif text == 'index':
            self._cell_text = {cell: str(index) for index, cell in enumerate(self.volmesh.cells())}
        elif isinstance(text, dict):
            self._cell_text = text

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_by_name(self):
        """Clear all objects in the "namespace" of the associated volmesh."""
        guids = compas_rhino.get_objects(name="{}.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self):
        """Draw the volmesh using the chosen visualisation settings.

        """
        raise NotImplementedError

    def draw_vertices(self):
        """Draw a selection of vertices.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        vertex_xyz = self.vertex_xyz
        vertex_color = self.vertex_color
        points = []
        for vertex in self.vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.volmesh.name, vertex),
                'color': vertex_color.get(vertex, self.default_vertexcolor)
            })
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self):
        """Draw a selection of edges.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        vertex_xyz = self.vertex_xyz
        edge_color = self.edge_color
        lines = []
        for edge in self.edges:
            lines.append({
                'start': vertex_xyz[edge[0]],
                'end': vertex_xyz[edge[1]],
                'color': edge_color.get(edge, self.default_edgecolor),
                'name': "{}.edge.{}-{}".format(self.volmesh.name, *edge)
            })
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_faces(self):
        """Draw a selection of faces.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        vertex_xyz = self.vertex_xyz
        face_color = self.face_color
        facets = []
        for face in self.faces:
            facets.append({
                'points': [vertex_xyz[vertex] for vertex in self.volmesh.halfface_vertices(face)],
                'name': "{}.face.{}".format(self.volmesh.name, face),
                'color': face_color.get(face, self.default_facecolor)
            })
        return compas_rhino.draw_faces(facets, layer=self.layer, clear=False, redraw=False)

    def draw_cells(self):
        """Draw a selection of cells.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
            Every cell is drawn as an individual mesh.
        """
        vertex_xyz = self.vertex_xyz
        cell_color = self.cell_color
        volmeshes = []
        for cell in self.cells:
            cell_faces = []
            for fkey in self.volmesh.cell_faces(cell):
                cell_faces.append({
                    'points': [vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(fkey)],
                    'name': "{}.cell.{}.face.{}".format(self.volmesh.name, cell, fkey),
                    'color': cell_color.get(cell, self.default_cellcolor)
                })
            guids = compas_rhino.draw_faces(cell_faces, layer=self.layer, clear=False, redraw=False)
            guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
            compas_rhino.rs.ObjectLayer(guid, self.layer)
            compas_rhino.rs.ObjectName(guid, '{}.cell.{}'.format(self.volmesh.name, cell))
            compas_rhino.rs.ObjectColor(guid, cell_color[cell])
            volmeshes.append(guid)
        return volmeshes

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_vertexlabels(self):
        """Draw labels for a selection vertices.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        vertex_xyz = self.vertex_xyz
        vertex_color = self.vertex_color
        vertex_text = self.vertex_text
        labels = []
        for vertex in vertex_text:
            labels.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertexlabel.{}".format(self.volmesh.name, vertex),
                'color': vertex_color.get(vertex, self.default_vertexcolor),
                'text': vertex_text[vertex]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self):
        """Draw labels for a selection of edges.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        vertex_xyz = self.vertex_xyz
        edge_color = self.edge_color
        edge_text = self.edge_text
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[edge[0]], vertex_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.volmesh.name, *edge),
                'color': edge_color.get(edge, self.default_edgecolor),
                'text': edge_text[edge]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_facelabels(self):
        """Draw labels for a selection of faces.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        vertex_xyz = self.vertex_xyz
        face_color = self.face_color
        face_text = self.face_text
        labels = []
        for face in face_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(face)]),
                'name': "{}.facelabel.{}".format(self.volmesh.name, face),
                'color': face_color.get(face, self.default_facecolor),
                'text': face_text[face]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_celllabels(self):
        """Draw labels for cells.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
        """
        vertex_xyz = self.vertex_xyz
        cell_color = self.cell_color
        cell_text = self.cell_text
        labels = []
        for cell in cell_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[vertex] for vertex in self.volmesh.cell_vertices(cell)]),
                'name': "{}.facelabel.{}".format(self.volmesh.name, cell),
                'color': cell_color.get(cell, self.default_cellcolor),
                'text': cell_text[cell]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
