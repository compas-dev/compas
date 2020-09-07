from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.artists._artist import BaseArtist

from compas.utilities import color_to_colordict as colordict
from compas.geometry import centroid_points


__all__ = ['VolMeshArtist']


class VolMeshArtist(BaseArtist):
    """A volmesh artist defines functionality for visualising COMPAS volmeshes in Rhino.

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
    color_vertices : 3-tuple
        Default color of the vertices.
    color_edges : 3-tuple
        Default color of the edges.
    color_faces : 3-tuple
        Default color of the faces.

    Examples
    --------
    .. code-block:: python

    """

    def __init__(self, volmesh, layer=None, settings=None):
        super(VolMeshArtist, self).__init__()
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_cell = {}
        self._guid_vertexlabel = {}
        self._guid_edgelabel = {}
        self._guid_facelabel = {}
        self._guid_celllabel = {}
        self._vertex_xyz = None
        self.volmesh = volmesh
        self.layer = layer
        self.settings = {
            'color.vertices': (255, 255, 255),
            'color.edges': (0, 0, 0),
            'color.faces': (210, 210, 210),
            'color.cells': (255, 0, 0),
            'show.vertices': True,
            'show.edges': True,
            'show.faces': False,
            'show.cells': False,
            'show.vertexlabels': False,
            'show.edgelabels': False,
            'show.facelabels': False,
            'show.celllabels': True,
        }
        if settings:
            self.settings.update(settings)

    @property
    def vertex_xyz(self):
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.volmesh.vertex_attributes(vertex, 'xyz') for vertex in self.volmesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    @property
    def guid_vertex(self):
        """Map between Rhino object GUIDs and volmesh vertex identifiers."""
        return self._guid_vertex

    @guid_vertex.setter
    def guid_vertex(self, values):
        self._guid_vertex = dict(values)

    @property
    def guid_edge(self):
        """Map between Rhino object GUIDs and volmsh edge identifiers."""
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    @property
    def guid_face(self):
        """Map between Rhino object GUIDs and volmesh face identifiers."""
        return self._guid_face

    @guid_face.setter
    def guid_face(self, values):
        self._guid_face = dict(values)

    @property
    def guid_cell(self):
        """Map between Rhino object GUIDs and volmesh face identifiers."""
        return self._guid_cell

    @guid_cell.setter
    def guid_cell(self, values):
        self._guid_cell = dict(values)

    @property
    def guid_vertexlabel(self):
        """Map between Rhino object GUIDs and volmshvertex label identifiers."""
        return self._guid_vertexlabel

    @guid_vertexlabel.setter
    def guid_vertexlabel(self, values):
        self._guid_vertexlabel = dict(values)

    @property
    def guid_edgelabel(self):
        """Map between Rhino object GUIDs and mesh edge label identifiers."""
        return self._guid_edgelabel

    @guid_edgelabel.setter
    def guid_edgelabel(self, values):
        self._guid_edgelabel = dict(values)

    @property
    def guid_facelabel(self):
        """Map between Rhino object GUIDs and volmsh face label identifiers."""
        return self._guid_facelabel

    @guid_facelabel.setter
    def guid_facelabel(self, values):
        self._guid_facelabel = dict(values)

    @property
    def guid_celllabel(self):
        """Map between Rhino object GUIDs and volmsh cell label identifiers."""
        return self._guid_celllabel

    @guid_celllabel.setter
    def guid_celllabel(self, values):
        self._guid_celllabel = dict(values)

    # ==========================================================================
    # clear
    # ==========================================================================
    def clear(self):
        """Clear all objects previously drawn by this artist.
        """
        guids = []
        guids_vertices = list(self.guid_vertex.keys())
        guids_edges = list(self.guid_edge.keys())
        guid_faces = list(self.guid_face.keys())
        guid_cells = list(self.guid_cell.keys())
        guids_vertexlabels = list(self.guid_vertexlabel.keys())
        guids_edgelabels = list(self.guid_edgelabel.keys())
        guids_facelabels = list(self.guid_facelabel.keys())
        guids_celllabels = list(self.guid_celllabel.keys())
        guids += guids_vertices + guids_edges + guid_faces + guid_cells
        guids += guids_vertexlabels + guids_edgelabels + guids_facelabels + guids_celllabels
        compas_rhino.delete_objects(self.guids + guids, purge=True)
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_cell = {}
        self._guid_vertexlabel = {}
        self._guid_edgelabel = {}
        self._guid_facelabel = {}
        self._guid_celllabel = {}

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)

    # ==========================================================================
    # components
    # ==========================================================================

    def draw(self, settings=None):
        """Draw the volmesh using the chosen visualisation settings.

        Parameters
        ----------
        settings : dict, optional
            Dictionary of visualisation settings that will be merged with the settings of the artist.

        """
        self.clear()
        if not settings:
            settings = {}
        self.settings.update(settings)
        if self.settings['show.vertices']:
            self.draw_vertices()
            if self.settings['show.vertexlabels']:
                self.draw_vertexlabels()
        if self.settings['show.edges']:
            self.draw_edges()
            if self.settings['show.edgelabels']:
                self.draw_edgelabels()
        if self.settings['show.faces']:
            self.draw_faces()
            if self.settings['show.facelabels']:
                self.draw_facelabels()
        if self.settings['show.cells']:
            self.draw_cells()
            if self.settings['show.celllabels']:
                self.draw_celllabels()

    def draw_vertices(self, keys=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        keys : list
            A list of vertex keys identifying which vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : str, tuple, dict
            The color specififcation for the vertices.
            Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
            To apply the same color to all vertices, provide a single color specification.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default vertex color (``self.settings['color.vertices']``).
            The default is ``None``, in which case all vertices are assigned the default vertex color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        vertices = keys or list(self.volmesh.vertices())
        vertex_xyz = self.vertex_xyz
        vertex_color = colordict(color, vertices, default=self.settings['color.vertices'], colorformat='rgb', normalize=False)
        points = []
        for vertex in vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.volmesh.name, vertex),
                'color': vertex_color[vertex]})

        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        self.guid_vertex = zip(guids, vertices)
        return guids

    def draw_edges(self, keys=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        keys : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
            To apply the same color to all edges, provide a single color specification.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default edge color (``self.settings['color.edges']``).
            The default is ``None``, in which case all edges are assigned the default edge color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        edges = keys or list(self.volmesh.edges())
        vertex_xyz = self.vertex_xyz
        edge_color = colordict(color, edges, default=self.settings['color.edges'], colorformat='rgb', normalize=False)
        lines = []
        for edge in edges:
            lines.append({
                'start': vertex_xyz[edge[0]],
                'end': vertex_xyz[edge[1]],
                'color': edge_color[edge],
                'name': "{}.edge.{}-{}".format(self.volmesh.name, *edge)})
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guid_edge = zip(guids, edges)
        return guids

    def draw_faces(self, keys=None, color=None):
        """Draw a selection of faces.

        Parameters
        ----------
        keys : list
            A list of face keys identifying which faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : str, tuple, dict
            The color specififcation for the faces.
            Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
            To apply the same color to all faces, provide a single color specification.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default face color (``self.settings['color.faces']``).
            The default is ``None``, in which case all faces are assigned the default face color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        faces = keys or list(self.volmesh.faces())
        vertex_xyz = self.vertex_xyz
        face_color = colordict(color, faces, default=self.settings['color.faces'], colorformat='rgb', normalize=False)
        facets = []
        for face in faces:
            facets.append({
                'points': [vertex_xyz[vertex] for vertex in self.volmesh.halfface_vertices(face)],
                'name': "{}.face.{}".format(self.volmesh.name, face),
                'color': face_color[face]})
        guids = compas_rhino.draw_faces(facets, layer=self.layer, clear=False, redraw=False)
        self.guid_face = zip(guids, faces)
        return guids

    def draw_cells(self, keys=None, color=None):
        """Draw a selection of cells.

        Parameters
        ----------
        keys : list
            A list of cell keys identifying which cells to draw.
            The default is ``None``, in which case all cells are drawn.
        color : str, tuple, dict
            The color specififcation for the cells.
            Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
            To apply the same color to all faces, provide a single color specification.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default face color (``self.settings['color.cells']``).
            The default is ``None``, in which case all cells are assigned the default cell color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects. Every cell is drawn as an individual mesh.

        """
        cells = keys or list(self.volmesh.cells())
        vertex_xyz = self.vertex_xyz
        cell_color = colordict(color, cells, default=self.settings['color.cells'], colorformat='rgb', normalize=False)
        meshes = []
        for cell in cells:
            cell_faces = []
            for fkey in self.volmesh.cell_halffaces(cell):
                cell_faces.append({
                    'points': [vertex_xyz[vertex] for vertex in self.volmesh.halfface_vertices(fkey)],
                    'name': "{}.cell.{}.face.{}".format(self.volmesh.name, cell, fkey),
                    'color': cell_color[cell]})
            guids = compas_rhino.draw_faces(cell_faces, layer=self.layer, clear=False, redraw=False)
            guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
            compas_rhino.rs.ObjectLayer(guid, self.layer)
            compas_rhino.rs.ObjectName(guid, '{}.cell.{}'.format(self.volmesh.name, cell))
            compas_rhino.rs.ObjectColor(guid, cell_color[cell])
            meshes.append(guid)
        self.guid_cell = zip(meshes, cells)
        return meshes

    # ==========================================================================
    # labels
    # ==========================================================================

    def draw_vertexlabels(self, text=None, color=None):
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict
            A dictionary of vertex labels as key-text pairs.
            The default value is ``None``, in which case every vertex will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors.
            Tuples are interpreted as RGB component specifications.
            If a dictionary of specififcations is provided,
            the keys should refer to vertex keys and the values should be color specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned the default vertex color (``self.settings['color.vertices']``).

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if text is None:
            vertex_text = {key: str(key) for key in self.volmesh.vertices()}
        elif isinstance(text, dict):
            vertex_text = text
        elif text == 'key':
            vertex_text = {key: str(key) for key in self.volmesh.vertices()}
        elif text == 'index':
            vertex_text = {key: str(index) for index, key in enumerate(self.volmesh.vertices())}
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        vertex_color = colordict(color, vertex_text.keys(), default=self.settings['color.vertices'], colorformat='rgb', normalize=False)
        labels = []
        for vertex in vertex_text:
            labels.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertexlabel.{}".format(self.volmesh.name, vertex),
                'color': vertex_color[vertex],
                'text': vertex_text[vertex]})
        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guid_vertexlabel = zip(guids, vertex_text.keys())
        return guids

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict
            A dictionary of edge labels as key-text pairs.
            The default value is ``None``, in which case every edge will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors.
            Tuples are interpreted as RGB component specifications.
            Individual colors can be assigned using a dictionary of edge-color pairs.
            Missing keys will be assigned the default edge color (``self.settings['color.edges']``).
            The default is ``None``, in which case all edges are assigned the default edge color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if text is None:
            edge_text = {(u, v): "{}-{}".format(u, v) for u, v in self.volmesh.edges()}
        elif isinstance(text, dict):
            edge_text = text
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        edge_color = colordict(color, edge_text.keys(), default=self.settings['color.edges'], colorformat='rgb', normalize=False)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[edge[0]], vertex_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.volmesh.name, *edge),
                'color': edge_color[edge],
                'text': edge_text[edge]})
        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guid_edgelabel = zip(guids, edge_text.keys())
        return guids

    def draw_facelabels(self, text=None, color=None):
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict
            A dictionary of face labels as key-text pairs.
            The default value is ``None``, in which case every face will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors.
            Tuples are interpreted as RGB component specifications.
            If a dictionary of specififcations is provided,
            the keys should refer to face keys and the values should be color specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned the default face color (``self.settings['color.faces']``).

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if text is None:
            face_text = {key: str(key) for key in self.volmesh.faces()}
        elif isinstance(text, dict):
            face_text = text
        elif text == 'key':
            face_text = {key: str(key) for key in self.volmesh.faces()}
        elif text == 'index':
            face_text = {key: str(index) for index, key in enumerate(self.volmesh.faces())}
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        face_color = colordict(color, face_text.keys(), default=self.settings['color.faces'], colorformat='rgb', normalize=False)
        labels = []
        for face in face_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[vertex] for vertex in self.volmesh.halfface_vertices(face)]),
                'name': "{}.facelabel.{}".format(self.volmesh.name, face),
                'color': face_color[face],
                'text': face_text[face]})
        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guid_facelabel = zip(guids, face_text.keys())
        return guids

    def draw_celllabels(self, text=None, color=None):
        """Draw labels for cells.

        Parameters
        ----------
        text : dict
            A dictionary of cell labels as key-text pairs.
            The default value is ``None``, in which case every cell will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors.
            Tuples are interpreted as RGB component specifications.
            If a dictionary of specififcations is provided,
            the keys should refer to face keys and the values should be color specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned the default face color (``self.settings['color.cells']``).

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if text is None:
            cell_text = {cell: str(cell) for cell in self.volmesh.cells()}
        elif isinstance(text, dict):
            cell_text = text
        elif text == 'key':
            cell_text = {cell: str(cell) for cell in self.volmesh.cells()}
        elif text == 'index':
            cell_text = {cell: str(index) for index, cell in enumerate(self.volmesh.cells())}
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        cell_color = colordict(color, cell_text.keys(), default=self.settings['color.cells'], colorformat='rgb', normalize=False)
        labels = []
        for cell in cell_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[vertex] for vertex in self.volmesh.cell_vertices(cell)]),
                'name': "{}.facelabel.{}".format(self.volmesh.name, cell),
                'color': cell_color[cell],
                'text': cell_text[cell]})
        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guid_celllabel = zip(guids, cell_text.keys())
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
