from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

from compas.utilities import color_to_colordict
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_points

import compas_rhino
from compas.artists import MeshArtist
from .artist import RhinoArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


class MeshArtist(RhinoArtist, MeshArtist):
    """Artists for drawing mesh data structures.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    layer : str, optional
        The name of the layer that will contain the mesh.
    vertices : list[int], optional
        Selection of vertices to draw.
    edges : list[tuple[int, int]], optional
        Selection of edges to draw.
    faces : list[int], optional
        Selection of faces to draw.
    vertexcolor : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
        Color of the vertices.
        Default color is :attr:`MeshArtists.default_vertexcolor`.
    edgecolor : tuple[int, int, int] or dict[tuple[int, int], tuple[int, int, int]], optional
        Color of the edges.
        Default color is :attr:`MeshArtists.default_edgecolor`.
    facecolor : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
        Color of the faces.
        Default color is :attr:`MeshArtists.default_facecolor`.
    show_vertices : bool, optional
        If True, draw the vertices.
    show_edges : bool, optional
        If True, draw the edges.
    show_faces : bool, optional
        If True, draw the faces.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`MeshArtist`.

    Class Attributes
    ----------------
    default_color : tuple[int, int, int]
        Default base color of the mesh.
    default_vertexcolor : tuple[int, int, int]
        Default color for vertices.
    default_edgecolor : tuple[int, int, int]
        Default color for edges.
    default_facecolor : tuple[int, int, int]
        Default color for faces.

    """

    # default_color = (0, 0, 0)
    # default_vertexcolor = (255, 255, 255)
    # default_edgecolor = (0, 0, 0)
    # default_facecolor = (200, 200, 200)

    def __init__(self,
                 mesh,
                 layer=None,
                 vertices=None,
                 edges=None,
                 faces=None,
                 vertexcolor=None,
                 edgecolor=None,
                 facecolor=None,
                 show_mesh=False,
                 show_vertices=True,
                 show_edges=True,
                 show_faces=True,
                 **kwargs):

        super(MeshArtist, self).__init__(mesh=mesh, layer=layer, **kwargs)

        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        self.vertex_color = vertexcolor
        self.edge_color = edgecolor
        self.face_color = facecolor
        self.show_mesh = show_mesh
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Delete all objects drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_mesh(self):
        """Delete the mesh drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.mesh".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertices(self):
        """Delete all vertices drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edges(self):
        """Delete all edges drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edge.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_faces(self):
        """Delete all faces drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.face.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertexnormals(self):
        """Delete all vertex normals drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertexnormal.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_facenormals(self):
        """Delete all face normals drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.facenormal.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertexlabels(self):
        """Delete all vertex labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertexlabel.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edgelabels(self):
        """Delete all edge labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edgelabel.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_facelabels(self):
        """Delete all face labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.facelabel.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self, vertices=None, edges=None, faces=None, vertexcolor=None, edgecolor=None, facecolor=None, join_faces=False):
        """Draw the mesh using the chosen visualization settings.

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
        vertexcolor : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color of the vertices.
            The default color is the value of :attr:`MeshArtist.default_vertexcolor`.
        edgecolor : tuple[int, int, int] or dict[tuple[int, int], tuple[int, int, int]], optional
            The color of the edges.
            The default color is the value of :attr:`MeshArtist.default_edgecolor`.
        facecolor : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color of the faces.
            The default color is the value of :attr:`MeshArtist.default_facecolor`.
        join_faces : bool, optional
            If True, join the faces into a single mesh.

        Returns
        -------
        None

        """
        self.clear()
        if self.show_mesh:
            self.draw_mesh()
        if self.show_vertices:
            self.draw_vertices(vertices=vertices, color=vertexcolor)
        if self.show_edges:
            self.draw_edges(edges=edges, color=edgecolor)
        if self.show_faces:
            self.draw_faces(faces=faces, color=facecolor, join_faces=join_faces)

    def draw_mesh(self, color=None, disjoint=False):
        """Draw the mesh as a consolidated RhinoMesh.

        Parameters
        ----------
        color : tuple[int, int, int], optional
            The color of the mesh.
            Default is the value of :attr:`MeshArtist.default_color`.
        disjoint : bool, optional
            If True, draw the faces of the mesh with disjoint vertices.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have only triangular or quadrilateral faces.
        Faces with more than 4 vertices will be triangulated on-the-fly.

        """
        color = color or self.default_color
        vertex_index = self.mesh.vertex_index()
        vertex_xyz = self.vertex_xyz
        vertices = [vertex_xyz[vertex] for vertex in self.mesh.vertices()]
        faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]
        layer = self.layer
        name = "{}.mesh".format(self.mesh.name)
        guid = compas_rhino.draw_mesh(vertices, faces, layer=layer, name=name, color=color, disjoint=disjoint)
        return [guid]

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color of the vertices.
            The default is the value of :attr:`MeshArtist.default_vertexcolor`.

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
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.mesh.name, vertex),
                'color': self.vertex_color.get(vertex, self.default_vertexcolor).rgb255
            })
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        return guids

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A selection of edges to draw.
            The default is None, in which case all edges are drawn.
        color : tuple[int, int, int] or dict[tuple[int, int], tuple[int, int, int]], optional
            The color of the edges.
            The default color is the value of :attr:`MeshArtist.default_edgecolor`.

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
            lines.append({
                'start': vertex_xyz[edge[0]],
                'end': vertex_xyz[edge[1]],
                'color': self.edge_color.get(edge, self.default_edgecolor).rgb255,
                'name': "{}.edge.{}-{}".format(self.mesh.name, *edge)
            })
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids

    def draw_faces(self, faces=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of faces to draw.
            The default is None, in which case all faces are drawn.
        color : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color of the faces.
            The default color is the value of :attr:`MeshArtist.default_facecolor`.
        join_faces : bool, optional
            If True, join the faces into a single mesh.

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
            facets.append({
                'points': [vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)],
                'name': "{}.face.{}".format(self.mesh.name, face),
                'color': self.face_color.get(face, self.default_facecolor).rgb255
            })
        guids = compas_rhino.draw_faces(facets, layer=self.layer, clear=False, redraw=False)
        if join_faces:
            guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
            compas_rhino.rs.ObjectLayer(guid, self.layer)
            compas_rhino.rs.ObjectName(guid, '{}.mesh'.format(self.mesh.name))
            compas_rhino.rs.ObjectColor(guid, color)
            guids = [guid]
        return guids

    # ==========================================================================
    # draw normals
    # ==========================================================================

    def draw_vertexnormals(self, vertices=None, color=(0, 255, 0), scale=1.0):
        """Draw the normals at the vertices of the mesh.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertex normals to draw.
            Default is to draw all vertex normals.
        color : tuple[int, int, int], optional
            The color specification of the normal vectors.
        scale : float, optional
            Scale factor for the vertex normals.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        vertex_xyz = self.vertex_xyz
        vertices = vertices or self.vertices
        lines = []
        for vertex in vertices:
            a = vertex_xyz[vertex]
            n = self.mesh.vertex_normal(vertex)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'color': color,
                'name': "{}.vertexnormal.{}".format(self.mesh.name, vertex),
                'arrow': 'end'
            })
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_facenormals(self, faces=None, color=(0, 255, 255), scale=1.0):
        """Draw the normals of the faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of face normals to draw.
            Default is to draw all face normals.
        color : tuple[int, int, int], optional
            The color specification of the normal vectors.
        scale : float, optional
            Scale factor for the face normals.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        vertex_xyz = self.vertex_xyz
        faces = faces or self.faces
        lines = []
        for face in faces:
            a = centroid_points([vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)])
            n = self.mesh.face_normal(face)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'name': "{}.facenormal.{}".format(self.mesh.name, face),
                'color': color,
                'arrow': 'end'
            })
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_vertexlabels(self, text=None, color=None):
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is None, in which case every vertex will be labelled with its identifier.
        color : tuple[int, int, int] or dict[int, tuple[int, int, int]], optional
            The color specification of the labels.
            The default color is the same as the default vertex color.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        if not text or text == 'key':
            vertex_text = {vertex: str(vertex) for vertex in self.vertices}
        elif text == 'index':
            vertex_text = {vertex: str(index) for index, vertex in enumerate(self.vertices)}
        elif isinstance(text, dict):
            vertex_text = text
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        vertex_color = colordict(color, vertex_text.keys(), default=self.default_vertexcolor)
        labels = []
        for vertex in vertex_text:
            labels.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertexlabel.{}".format(self.mesh.name, vertex),
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
            The default value is None, in which case every edge will be labelled with its identifier.
        color : tuple[int, int, int] or dict[tuple[int, int], tuple[int, int, int]], optional
            The color specification of the labels.
            The default color is the same as the default edge color.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        if text is None:
            edge_text = {(u, v): "{}-{}".format(u, v) for u, v in self.edges}
        elif isinstance(text, dict):
            edge_text = text
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        edge_color = colordict(color, edge_text.keys(), default=self.default_edgecolor)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[edge[0]], vertex_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.mesh.name, *edge),
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
            The color specification of the labels.
            The default color is the same as the default face color.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        if not text or text == 'key':
            face_text = {face: str(face) for face in self.faces}
        elif text == 'index':
            face_text = {face: str(index) for index, face in enumerate(self.faces)}
        elif isinstance(text, dict):
            face_text = text
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        face_color = colordict(color, face_text.keys(), default=self.default_facecolor)
        labels = []
        for face in face_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]),
                'name': "{}.facelabel.{}".format(self.mesh.name, face),
                'color': face_color[face],
                'text': face_text[face]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
