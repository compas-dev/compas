from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_points
from compas.utilities import is_color_rgb

from ._artist import Artist


__all__ = ['MeshArtist']


class MeshArtist(Artist):
    """Artist for drawing mesh data structures.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    layer : str, optional
        The name of the layer that will contain the mesh.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The COMPAS mesh associated with the artist.
    layer : str
        The layer in which the mesh should be contained.
    vertices : list
        The list of vertices to draw.
        Default is a list of all vertices of the mesh.
    edges : list
        The list of edges to draw.
        Default is a list of all edges of the mesh.
    faces : list
        The list of faces to draw.
        Default is a list of all faces of the mesh.
    vertex_xyz : dict[int, tuple(float, float, float)]
        Mapping between vertices and their view coordinates.
        The default view coordinates are the actual coordinates of the vertices of the mesh.
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
    face_color : dict[int, tuple(int, int, int)]
        Mapping between faces and RGB color values.
        The colors have to be integer tuples with values in the range ``0-255``.
        Missing faces get the default face color (``MeshArtist.default_facecolor``).
    face_text : dict[int, str]
        Mapping between faces and text labels.
        Missing faces are labelled with the corresponding face identifiers.
    meshcolor : tuple(int, int, int)
        RGB color of the mesh.

    Examples
    --------
    .. code-block:: python

        import random
        import compas_rhino
        from compas.datastructures import Mesh
        from compas.utilities import i_to_rgb

        from compas_rhino.artists import MeshArtist

        compas_rhino.clear()

        mesh = Mesh.from_polyhedron(12)

        artist = MeshArtist(mesh)
        artist.vertex_color = (255, 255, 255)
        artist.face_color = {face: i_to_rgb(random.random()) for face in mesh.faces()}
        artist.draw()
        artist.draw_facelabels()

        compas_rhino.update()

    """

    default_vertexcolor = (255, 255, 255)
    default_edgecolor = (0, 0, 0)
    default_facecolor = (0, 0, 0)
    default_meshcolor = (0, 0, 0)

    def __init__(self, mesh, layer=None):
        super(MeshArtist, self).__init__(mesh, layer=layer)
        self._vertices = None
        self._edges = None
        self._faces = None
        self._vertex_xyz = None
        self._vertex_color = None
        self._edge_color = None
        self._face_color = None
        self._meshcolor = None
        self._vertex_text = None
        self._edge_text = None
        self._face_text = None
        self.join_faces = False

    @property
    def mesh(self):
        return self.item

    @mesh.setter
    def mesh(self, mesh):
        self.item = mesh
        self._vertex_xyz = None

    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = list(self.mesh.vertices())
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    def edges(self):
        if self._edges is None:
            self._edges = list(self.mesh.edges())
        return self._edges

    @edges.setter
    def edges(self, edges):
        self._edges = edges

    @property
    def faces(self):
        if self._faces is None:
            self._faces = list(self.mesh.faces())
        return self._faces

    @faces.setter
    def faces(self, faces):
        self._faces = faces

    @property
    def vertex_xyz(self):
        if not self._vertex_xyz:
            return {vertex: self.mesh.vertex_attributes(vertex, 'xyz') for vertex in self.mesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    @property
    def vertex_color(self):
        if not self._vertex_color:
            self._vertex_color = {vertex: self.default_vertexcolor for vertex in self.mesh.vertices()}
        return self._vertex_color

    @vertex_color.setter
    def vertex_color(self, vertex_color):
        if isinstance(vertex_color, dict):
            self._vertex_color = vertex_color
        elif is_color_rgb(vertex_color):
            self._vertex_color = {vertex: vertex_color for vertex in self.mesh.vertices()}

    @property
    def edge_color(self):
        if not self._edge_color:
            self._edge_color = {edge: self.default_edgecolor for edge in self.mesh.edges()}
        return self._edge_color

    @edge_color.setter
    def edge_color(self, edge_color):
        if isinstance(edge_color, dict):
            self._edge_color = edge_color
        elif is_color_rgb(edge_color):
            self._edge_color = {edge: edge_color for edge in self.mesh.edges()}

    @property
    def face_color(self):
        if not self._face_color:
            self._face_color = {face: self.default_facecolor for face in self.mesh.faces()}
        return self._face_color

    @face_color.setter
    def face_color(self, face_color):
        if isinstance(face_color, dict):
            self._face_color = face_color
        elif is_color_rgb(face_color):
            self._face_color = {face: face_color for face in self.mesh.faces()}

    @property
    def meshcolor(self):
        if not self._meshcolor:
            self._meshcolor = self.default_meshcolor
        return self._meshcolor

    @meshcolor.setter
    def meshcolor(self, meshcolor):
        if is_color_rgb(meshcolor):
            self._meshcolor = meshcolor

    @property
    def vertex_text(self):
        if not self._vertex_text:
            self._vertex_text = {vertex: str(vertex) for vertex in self.mesh.vertices()}
        return self._vertex_text

    @vertex_text.setter
    def vertex_text(self, text):
        if text == 'key':
            self._vertex_text = {vertex: str(vertex) for vertex in self.mesh.vertices()}
        elif text == 'index':
            self._vertex_text = {vertex: str(index) for index, vertex in enumerate(self.mesh.vertices())}
        elif isinstance(text, dict):
            self._vertex_text = text

    @property
    def edge_text(self):
        if not self._edge_text:
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.mesh.edges()}
        return self._edge_text

    @edge_text.setter
    def edge_text(self, text):
        if text == 'key':
            self._edge_text = {edge: "{}-{}".format(*edge) for edge in self.mesh.edges()}
        elif text == 'index':
            self._edge_text = {edge: str(index) for index, edge in enumerate(self.mesh.edges())}
        elif isinstance(text, dict):
            self._edge_text = text

    @property
    def face_text(self):
        if not self._face_text:
            self._face_text = {face: str(face) for face in self.mesh.faces()}
        return self._face_text

    @face_text.setter
    def face_text(self, text):
        if text == 'key':
            self._face_text = {face: str(face) for face in self.mesh.faces()}
        elif text == 'index':
            self._face_text = {face: str(index) for index, face in enumerate(self.mesh.faces())}
        elif isinstance(text, dict):
            self._face_text = text

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_by_name(self):
        """Clear all objects in the "namespace" of the associated mesh."""
        guids = compas_rhino.get_objects(name="{}.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self):
        """Draw the mesh using the chosen visualisation settings.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        guids = self.draw_vertices()
        guids += self.draw_faces()
        guids += self.draw_edges()
        return guids

    def draw_mesh(self):
        """Draw the mesh as a consolidated RhinoMesh.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have only triangular or quadrilateral faces.
        Faces with more than 4 vertices will be triangulated on-the-fly.
        """
        vertex_index = self.mesh.key_index()
        vertex_xyz = self.vertex_xyz
        vertices = [vertex_xyz[vertex] for vertex in self.mesh.vertices()]
        faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]
        guid = compas_rhino.draw_mesh(vertices, faces, layer=self.layer, name=self.mesh.name, color=self.meshcolor, disjoint=self.join_faces, clear=False, redraw=False)
        return [guid]

    def draw_vertices(self):
        """Draw a selection of vertices.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        vertices = self.vertices
        vertex_xyz = self.vertex_xyz
        vertex_color = self.vertex_color
        points = []
        for vertex in vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.mesh.name, vertex),
                'color': vertex_color.get(vertex, self.default_vertexcolor)
            })
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_faces(self):
        """Draw a selection of faces.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        vertex_xyz = self.vertex_xyz
        face_color = self.face_color
        faces = []
        for face in self.faces:
            faces.append({
                'points': [vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)],
                'name': "{}.face.{}".format(self.mesh.name, face),
                'color': face_color.get(face, self.default_facecolor)
            })
        guids = compas_rhino.draw_faces(faces, layer=self.layer, clear=False, redraw=False)
        if not self.join_faces:
            return guids
        guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
        compas_rhino.rs.ObjectLayer(guid, self.layer)
        compas_rhino.rs.ObjectName(guid, '{}'.format(self.mesh.name))
        compas_rhino.rs.ObjectColor(guid, self.meshcolor)
        return [guid]

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
                'name': "{}.edge.{}-{}".format(self.mesh.name, *edge)
            })
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

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
        vertex_text = self.vertex_text
        vertex_xyz = self.vertex_xyz
        vertex_color = self.vertex_color
        labels = []
        for vertex in vertex_text:
            labels.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertexlabel.{}".format(self.mesh.name, vertex),
                'color': vertex_color.get(vertex, self.default_vertexcolor),
                'text': vertex_text[vertex]})
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_facelabels(self):
        """Draw labels for a selection of faces.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        vertex_xyz = self.vertex_xyz
        face_text = self.face_text
        face_color = self.face_color
        labels = []
        for face in face_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]),
                'name': "{}.facelabel.{}".format(self.mesh.name, face),
                'color': face_color.get(face, self.default_facecolor),
                'text': face_text[face]
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
        edge_text = self.edge_text
        edge_color = self.edge_color
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[edge[0]], vertex_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.mesh.name, *edge),
                'color': edge_color.get(edge, self.default_edgecolor),
                'text': edge_text[edge]
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    # ==========================================================================
    # draw normals
    # ==========================================================================

    def draw_vertexnormals(self, vertices=None, color=(0, 255, 0), scale=1.0):
        """Draw the normals at the vertices of the mesh.

        Parameters
        ----------
        vertices : list, optional
            A selection of vertex normals to draw.
            Default is to draw all vertex normals.
        color : tuple, optional
            The color specification of the normal vectors.
            The default color is green, ``(0, 255, 0)``.
        scale : float, optional
            Scale factor for the vertex normals.
            Default is ``1.0``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        vertex_xyz = self.vertex_xyz
        vertices = vertices or list(self.mesh.vertices())
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
                'arrow': 'end'})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_facenormals(self, faces=None, color=(0, 255, 255), scale=1.0):
        """Draw the normals of the faces.

        Parameters
        ----------
        faces : list, optional
            A selection of face normals to draw.
            Default is to draw all face normals.
        color : tuple, optional
            The color specification of the normal vectors.
            The default color is cyan, ``(0, 255, 255)``.
        scale : float, optional
            Scale factor for the face normals.
            Default is ``1.0``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        vertex_xyz = self.vertex_xyz
        faces = faces or list(self.mesh.faces())
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
                'arrow': 'end'})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
