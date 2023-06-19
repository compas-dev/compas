from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import centroid_points
from compas.artists import VolMeshArtist
from .artist import RhinoArtist


class VolMeshArtist(RhinoArtist, VolMeshArtist):
    """Artist for drawing volmesh data structures.

    Parameters
    ----------
    volmesh : :class:`~compas.datastructures.VolMesh`
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
        """Delete all objects drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertices(self):
        """Delete all vertices drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edges(self):
        """Delete all edges drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edge.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_faces(self):
        """Delete all faces drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.face.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_cells(self):
        """Delete all cells drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.cell.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertexlabels(self):
        """Delete all vertex labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertexlabel.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edgelabels(self):
        """Delete all edge labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edgelabel.*".format(self.volmesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_facelabels(self):
        """Delete all face labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.facelabel.*".format(self.volmesh.name))
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

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A list of vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the vertices.
            The default color of the vertices is :attr:`VolMeshArtist.default_vertexcolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

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
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[int, int], :class:`~compas.colors.Color`], optional
            The color of the edges.
            The default color is :attr:`VolMeshArtist.default_edgecolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.edge_color = color
        edges = edges or self.edges
        vertex_xyz = self.vertex_xyz
        lines = []
        for edge in edges:
            lines.append(
                {
                    "start": vertex_xyz[edge[0]],
                    "end": vertex_xyz[edge[1]],
                    "color": self.edge_color[edge].rgb255,
                    "name": "{}.edge.{}-{}".format(self.volmesh.name, *edge),
                }
            )
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_faces(self, faces=None, color=None):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A list of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the faces.
            The default color is :attr:`VolMeshArtist.default_facecolor`.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

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
        return compas_rhino.draw_faces(facets, layer=self.layer, clear=False, redraw=False)

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
        list[System.Guid]
            The GUIDs of the created Rhino objects.
            Every cell is drawn as an individual mesh.

        """
        self.cell_color = color
        cells = cells or self.cells
        vertex_xyz = self.vertex_xyz
        guids = []
        for cell in cells:
            vertices = self.volmesh.cell_vertices(cell)
            faces = self.volmesh.cell_faces(cell)
            vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))
            vertices = [vertex_xyz[vertex] for vertex in vertices]
            faces = [[vertex_index[vertex] for vertex in self.volmesh.halfface_vertices(face)] for face in faces]
            guid = compas_rhino.draw_mesh(
                vertices,
                faces,
                layer=self.layer,
                name="{}.cell.{}".format(self.volmesh.name, cell),
                color=self.cell_color[cell].rgb255,
                disjoint=True,
            )
            guids.append(guid)
        return guids

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_vertexlabels(self, text=None):
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is None, in which case every vertex will be labelled with its key.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.vertex_text = text
        vertex_xyz = self.vertex_xyz
        labels = []
        for vertex in self.vertex_text:
            labels.append(
                {
                    "pos": vertex_xyz[vertex],
                    "name": "{}.vertexlabel.{}".format(self.volmesh.name, vertex),
                    "color": self.vertex_color[vertex].rgb255,
                    "text": self.vertex_text[vertex],
                }
            )
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self, text=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict[tuple[int, int], str], optional
            A dictionary of edge labels as edge-text pairs.
            The default value is None, in which case every edge will be labelled with its key.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.edge_text = text
        vertex_xyz = self.vertex_xyz
        labels = []
        for edge in self.edge_text:
            labels.append(
                {
                    "pos": centroid_points([vertex_xyz[edge[0]], vertex_xyz[edge[1]]]),
                    "name": "{}.edgelabel.{}-{}".format(self.volmesh.name, *edge),
                    "color": self.edge_color[edge].rgb255,
                    "text": self.edge_text[edge],
                }
            )
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_facelabels(self, text=None):
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of face labels as face-text pairs.
            The default value is None, in which case every face will be labelled with its key.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.face_text = text
        vertex_xyz = self.vertex_xyz
        labels = []
        for face in self.face_text:
            labels.append(
                {
                    "pos": centroid_points([vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(face)]),
                    "name": "{}.facelabel.{}".format(self.volmesh.name, face),
                    "color": self.face_color[face].rgb255,
                    "text": self.face_text[face],
                }
            )
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_celllabels(self, text=None):
        """Draw labels for cells.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of cell labels as cell-text pairs.
            The default value is None, in which case every cell will be labelled with its key.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        self.cell_text = text
        vertex_xyz = self.vertex_xyz
        labels = []
        for cell in self.cell_text:
            labels.append(
                {
                    "pos": centroid_points([vertex_xyz[vertex] for vertex in self.volmesh.cell_vertices(cell)]),
                    "name": "{}.facelabel.{}".format(self.volmesh.name, cell),
                    "color": self.cell_color[cell].rgb255,
                    "text": self.cell_text[cell],
                }
            )
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
