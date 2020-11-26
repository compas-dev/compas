from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial
import compas_rhino

from compas_rhino.artists._artist import BaseArtist

from compas.utilities import color_to_colordict
from compas.geometry import centroid_points


colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


__all__ = ['VolMeshArtist']


class VolMeshArtist(BaseArtist):
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
    color_vertices : 3-tuple
        Default color of the vertices.
    color_edges : 3-tuple
        Default color of the edges.
    color_faces : 3-tuple
        Default color of the faces.

    """

    def __init__(self, volmesh, layer=None):
        super(VolMeshArtist, self).__init__()
        self._volmesh = None
        self._vertex_xyz = None
        self.volmesh = volmesh
        self.layer = layer
        self.color_vertices = (255, 255, 255)
        self.color_edges = (0, 0, 0)
        self.color_faces = (210, 210, 210)
        self.color_cells = (255, 0, 0)

    @property
    def volmesh(self):
        return self._volmesh

    @volmesh.setter
    def volmesh(self, volmesh):
        self._volmesh = volmesh
        self._vertex_xyz = None

    @property
    def vertex_xyz(self):
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.volmesh.vertex_attributes(vertex, 'xyz') for vertex in self.volmesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_by_name(self):
        """Clear all objects in the "namespace" of the associated volmesh."""
        guids = compas_rhino.get_objects(name="{}.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self, settings=None):
        """Draw the volmesh using the chosen visualisation settings.

        Parameters
        ----------
        settings : dict, optional
            Dictionary of visualisation settings that will be merged with the settings of the artist.

        """
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
            The default color of the vertices is ``(255, 255, 255)``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        vertices = vertices or list(self.volmesh.vertices())
        vertex_xyz = self.vertex_xyz
        vertex_color = colordict(color, vertices, default=self.color_vertices)
        points = []
        for vertex in vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.volmesh.name, vertex),
                'color': vertex_color[vertex]})
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list
            A list of edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            The default color is ``(0, 0, 0)``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        edges = edges or list(self.volmesh.edges())
        vertex_xyz = self.vertex_xyz
        edge_color = colordict(color, edges, default=self.color_edges)
        lines = []
        for edge in edges:
            lines.append({
                'start': vertex_xyz[edge[0]],
                'end': vertex_xyz[edge[1]],
                'color': edge_color[edge],
                'name': "{}.edge.{}-{}".format(self.volmesh.name, *edge)})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_faces(self, faces=None, color=None):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list
            A list of faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : str, tuple, dict
            The color specififcation for the faces.
            The default color is ``(210, 210, 210)``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        faces = faces or list(self.volmesh.faces())
        vertex_xyz = self.vertex_xyz
        face_color = colordict(color, faces, default=self.color_faces)
        facets = []
        for face in faces:
            facets.append({
                'points': [vertex_xyz[vertex] for vertex in self.volmesh.halfface_vertices(face)],
                'name': "{}.face.{}".format(self.volmesh.name, face),
                'color': face_color[face]})
        return compas_rhino.draw_faces(facets, layer=self.layer, clear=False, redraw=False)

    def draw_cells(self, cells=None, color=None):
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list
            A list of cells to draw.
            The default is ``None``, in which case all cells are drawn.
        color : str, tuple, dict
            The color specififcation for the cells.
            The default color is ``(255, 0, 0)``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.
            Every cell is drawn as an individual mesh.

        """
        cells = cells or list(self.volmesh.cells())
        vertex_xyz = self.vertex_xyz
        cell_color = colordict(color, cells, default=self.color_cells)
        meshes = []
        for cell in cells:
            cell_faces = []
            for fkey in self.volmesh.cell_faces(cell):
                cell_faces.append({
                    'points': [vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(fkey)],
                    'name': "{}.cell.{}.face.{}".format(self.volmesh.name, cell, fkey),
                    'color': cell_color[cell]})
            guids = compas_rhino.draw_faces(cell_faces, layer=self.layer, clear=False, redraw=False)
            guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
            compas_rhino.rs.ObjectLayer(guid, self.layer)
            compas_rhino.rs.ObjectName(guid, '{}.cell.{}'.format(self.volmesh.name, cell))
            compas_rhino.rs.ObjectColor(guid, cell_color[cell])
            meshes.append(guid)
        return meshes

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_vertexlabels(self, text=None, color=None):
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict
            A dictionary of vertex labels as vertex-text pairs.
            The default value is ``None``, in which case every vertex will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            The default color is the same as the color of the vertices.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if not text or text == 'key':
            vertex_text = {vertex: str(vertex) for vertex in self.volmesh.vertices()}
        elif text == 'index':
            vertex_text = {vertex: str(index) for index, vertex in enumerate(self.volmesh.vertices())}
        elif isinstance(text, dict):
            vertex_text = text
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        vertex_color = colordict(color, vertex_text.keys(), default=self.color_vertices)
        labels = []
        for vertex in vertex_text:
            labels.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertexlabel.{}".format(self.volmesh.name, vertex),
                'color': vertex_color[vertex],
                'text': vertex_text[vertex]})
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict
            A dictionary of edge labels as edge-text pairs.
            The default value is ``None``, in which case every edge will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            The default color is tha same as the color of the edges.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if text is None:
            edge_text = {edge: "{}-{}".format(*edge) for edge in self.volmesh.edges()}
        elif isinstance(text, dict):
            edge_text = text
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        edge_color = colordict(color, edge_text.keys(), default=self.color_edges)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[edge[0]], vertex_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.volmesh.name, *edge),
                'color': edge_color[edge],
                'text': edge_text[edge]})
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_facelabels(self, text=None, color=None):
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict
            A dictionary of face labels as face-text pairs.
            The default value is ``None``, in which case every face will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            The default color is the same as the color of the faces.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if not text or text == 'key':
            face_text = {face: str(face) for face in self.volmesh.faces()}
        elif text == 'index':
            face_text = {face: str(index) for index, face in enumerate(self.volmesh.faces())}
        elif isinstance(text, dict):
            face_text = text
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        face_color = colordict(color, face_text.keys(), default=self.color_faces)
        labels = []
        for face in face_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(face)]),
                'name': "{}.facelabel.{}".format(self.volmesh.name, face),
                'color': face_color[face],
                'text': face_text[face]})
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_celllabels(self, text=None, color=None):
        """Draw labels for cells.

        Parameters
        ----------
        text : dict
            A dictionary of cell labels as cell-text pairs.
            The default value is ``None``, in which case every cell will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            The default color is the same as the color of the cells.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if not text or text == 'key':
            cell_text = {cell: str(cell) for cell in self.volmesh.cells()}
        elif text == 'index':
            cell_text = {cell: str(index) for index, cell in enumerate(self.volmesh.cells())}
        elif isinstance(text, dict):
            cell_text = text
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        cell_color = colordict(color, cell_text.keys(), default=self.color_cells)
        labels = []
        for cell in cell_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[vertex] for vertex in self.volmesh.cell_vertices(cell)]),
                'name': "{}.facelabel.{}".format(self.volmesh.name, cell),
                'color': cell_color[cell],
                'text': cell_text[cell]})
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
