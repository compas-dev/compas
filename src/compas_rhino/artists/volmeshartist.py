from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial
import compas_rhino

from compas.utilities import color_to_colordict
from compas.geometry import centroid_points

from compas.artists import VolMeshArtist
from .artist import RhinoArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


class VolMeshArtist(RhinoArtist, VolMeshArtist):
    """Artist for drawing volmesh data structures.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A COMPAS volmesh.
    layer : str, optional
        The name of the layer that will contain the volmesh.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`VolMeshArtist`.

    """

    def __init__(self, volmesh, layer=None, **kwargs):
        super(VolMeshArtist, self).__init__(volmesh=volmesh, layer=layer, **kwargs)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        guids = compas_rhino.get_objects(name="{}.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertices(self):
        guids = compas_rhino.get_objects(name="{}.vertex.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edges(self):
        guids = compas_rhino.get_objects(name="{}.edge.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_faces(self):
        guids = compas_rhino.get_objects(name="{}.face.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_cells(self):
        guids = compas_rhino.get_objects(name="{}.cell.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertexlabels(self):
        guids = compas_rhino.get_objects(name="{}.vertexlabel.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edgelabels(self):
        guids = compas_rhino.get_objects(name="{}.edgelabel.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_facelabels(self):
        guids = compas_rhino.get_objects(name="{}.facelabel.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self, vertices=None, edges=None, faces=None, cells=None, vertexcolor=None, edgecolor=None, facecolor=None, cellcolor=None):
        """Draw the network using the chosen visualisation settings.

        Parameters
        ----------
        vertices : list[int], optional
            A list of vertices to draw.
            Default is None, in which case all vertices are drawn.
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        faces : list[int], optional
            A selection of faces to draw.
            The default is None, in which case all faces are drawn.
        cells : list[int], optional
            A selection of cells to draw.
            The default is None, in which case all cells are drawn.
        vertexcolor : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color of the vertices.
            The default color is the value of :attr:`VolMeshArtist.default_vertexcolor`.
        edgecolor : tuple[int, int, int] or dict[tuple[int, int], tuple[int, int, int]], optional
            The color of the edges.
            The default color is the value of :attr:`VolMeshArtist.default_edgecolor`.
        facecolor : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color of the faces.
            The default color is the value of :attr:`VolMeshArtist.default_facecolor`.
        cellcolor : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color of the cells.
            The default color is the value of :attr:`VolMeshArtist.default_cellcolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        guids = self.draw_vertices(vertices=vertices, color=vertexcolor)
        guids += self.draw_edges(edges=edges, color=edgecolor)
        guids += self.draw_faces(faces=faces, color=facecolor)
        guids += self.draw_cells(cells=cells, color=cellcolor)
        return guids

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A list of vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color of the vertices.
            The default color of the vertices is :attr:`VolMeshArtist.default_vertexcolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

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
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : tuple[int, int, int] or dict[tuple[int, int], tuple[int, int, int]], optional
            The color of the edges.
            The default color is :attr:`VolMeshArtist.default_edgecolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

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
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_faces(self, faces=None, color=None):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A list of faces to draw.
            The default is None, in which case all faces are drawn.
        color : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color of the faces.
            The default color is :attr:`VolMeshArtist.default_facecolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

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
        return compas_rhino.draw_faces(facets, layer=self.layer, clear=False, redraw=False)

    def draw_cells(self, cells=None, color=None):
        """Draw a selection of cells.

        Parameters
        ----------
        cells : list[int], optional
            A list of cells to draw.
            The default is None, in which case all cells are drawn.
        color : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color of the cells.
            The default color is :attr:`VolMeshArtist.default_cellcolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.
            Every cell is drawn as an individual mesh.

        """
        self.cell_color = color
        cells = cells or list(self.volmesh.cells())
        vertex_xyz = self.vertex_xyz
        meshes = []
        for cell in cells:
            cell_faces = []
            for fkey in self.volmesh.cell_faces(cell):
                cell_faces.append({
                    'points': [vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(fkey)],
                    'name': "{}.cell.{}.face.{}".format(self.volmesh.name, cell, fkey),
                    'color': self.cell_color.get(cell, self.default_cellcolor)
                })
            guids = compas_rhino.draw_faces(cell_faces, layer=self.layer, clear=False, redraw=False)
            guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
            compas_rhino.rs.ObjectLayer(guid, self.layer)
            compas_rhino.rs.ObjectName(guid, '{}.cell.{}'.format(self.volmesh.name, cell))
            compas_rhino.rs.ObjectColor(guid, self.cell_color.get(cell, self.default_cellcolor))
            meshes.append(guid)
        return meshes

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_vertexlabels(self, text=None, color=None):
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is None, in which case every vertex will be labelled with its key.
        color : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            Color of the labels.
            The default color is the same as the color of the vertices.

        Returns
        -------
        list[System.Guid]
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
                'text': vertex_text[vertex]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict[tuple[int, int], str], optional
            A dictionary of edge labels as edge-text pairs.
            The default value is None, in which case every edge will be labelled with its key.
        color : tuple[int, int, int] or dict[tuple[int, int], tuple[int, int, int]], optional
            Color of the labels.
            The default color is tha same as the color of the edges.

        Returns
        -------
        list[System.Guid]
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
                'text': edge_text[edge]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_facelabels(self, text=None, color=None):
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of face labels as face-text pairs.
            The default value is None, in which case every face will be labelled with its key.
        color : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            Color of the labels.
            The default color is the same as the color of the faces.

        Returns
        -------
        list[System.Guid]
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
                'text': face_text[face]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_celllabels(self, text=None, color=None):
        """Draw labels for cells.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of cell labels as cell-text pairs.
            The default value is None, in which case every cell will be labelled with its key.
        color : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            Color of the labels.
            The default color is the same as the color of the cells.

        Returns
        -------
        list[System.Guid]
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
                'text': cell_text[cell]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
