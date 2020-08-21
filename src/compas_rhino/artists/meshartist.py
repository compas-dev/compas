from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.artists._artist import BaseArtist

from compas.utilities import color_to_colordict
from compas.utilities import pairwise
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_polygon


__all__ = ['MeshArtist']


class MeshArtist(BaseArtist):
    """A mesh artist defines functionality for visualising COMPAS meshes in Rhino.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    layer : str, optional
        The name of the layer that will contain the mesh.
    settings : dict, optional
        A dict with custom visualisation settings.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The COMPAS mesh associated with the artist.
    layer : str
        The layer in which the mesh should be contained.
    settings : dict
        Default settings for color, scale, tolerance, ...

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas_rhino.artists import MeshArtist

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        artist = MeshArtist(mesh, layer='COMPAS::MeshArtist')
        artist.clear_layer()
        artist.draw_faces(join_faces=True)
        artist.draw_vertices(color={key: '#ff0000' for key in mesh.vertices_on_boundary()})
        artist.draw_edges()
        artist.redraw()

    """

    def __init__(self, mesh, layer=None, settings=None):
        super(MeshArtist, self).__init__()
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_vertexnormal = {}
        self._guid_facenormal = {}
        self._guid_vertexlabel = {}
        self._guid_edgelabel = {}
        self._guid_facelabel = {}
        self.mesh = mesh
        self.layer = layer
        self.settings = {
            'color.vertices': (255, 255, 255),
            'color.edges': (0, 0, 0),
            'color.faces': (210, 210, 210),
            'color.vertexnormals': (0, 255, 0),
            'color.facenormals': (0, 255, 0),
            'scale.vertexnormals': 0.1,
            'scale.facenormals': 0.1,
            'show.vertices': True,
            'show.edges': True,
            'show.faces': True,
            'show.vertexnormals': False,
            'show.facenormals': False,
            'show.vertexlabels': False,
            'show.facelabels': False,
            'show.edgelabels': False,
            'join_faces': True}
        if settings:
            self.settings.update(settings)

    @property
    def guid_vertex(self):
        """Map between Rhino object GUIDs and mesh vertex identifiers."""
        return self._guid_vertex

    @guid_vertex.setter
    def guid_vertex(self, values):
        self._guid_vertex = dict(values)

    @property
    def guid_edge(self):
        """Map between Rhino object GUIDs and mesh edge identifiers."""
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    @property
    def guid_face(self):
        """Map between Rhino object GUIDs and mesh face identifiers."""
        return self._guid_face

    @guid_face.setter
    def guid_face(self, values):
        self._guid_face = dict(values)

    @property
    def guid_vertexnormal(self):
        """Map between Rhino object GUIDs and force diagram vertex normal identifiers."""
        return self._guid_vertexnormal

    @guid_vertexnormal.setter
    def guid_vertexnormal(self, values):
        self._guid_vertexnormal = dict(values)

    @property
    def guid_facenormal(self):
        """Map between Rhino object GUIDs and force diagram face normal identifiers."""
        return self._guid_facenormal

    @guid_facenormal.setter
    def guid_facenormal(self, values):
        self._guid_facenormal = dict(values)

    @property
    def guid_vertexlabel(self):
        """Map between Rhino object GUIDs and force diagram vertex label identifiers."""
        return self._guid_vertexlabel

    @guid_vertexlabel.setter
    def guid_vertexlabel(self, values):
        self._guid_vertexlabel = dict(values)

    @property
    def guid_facelabel(self):
        """Map between Rhino object GUIDs and mesh face label identifiers."""
        return self._guid_facelabel

    @guid_facelabel.setter
    def guid_facelabel(self, values):
        self._guid_facelabel = dict(values)

    @property
    def guid_edgelabel(self):
        """Map between Rhino object GUIDs and mesh edge label identifiers."""
        return self._guid_edgelabel

    @guid_edgelabel.setter
    def guid_edgelabel(self, values):
        self._guid_edgelabel = dict(values)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Clear all objects previously drawn by this artist.
        """
        guids = []
        guids_vertices = list(self.guid_vertex.keys())
        guids_edges = list(self.guid_edge.keys())
        guids_faces = list(self.guid_face.keys())
        guids_vertexnormals = list(self.guid_vertexnormal.keys())
        guids_facenormals = list(self.guid_facenormal.keys())
        guids_vertexlabels = list(self.guid_vertexlabel.keys())
        guids_edgelabels = list(self.guid_edgelabel.keys())
        guids_facelabels = list(self.guid_facelabel.keys())
        guids += guids_vertices + guids_edges + guids_faces
        guids += guids_vertexnormals + guids_facenormals
        guids += guids_vertexlabels + guids_edgelabels + guids_facelabels
        compas_rhino.delete_objects(self.guids + guids, purge=True)
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_vertexnormal = {}
        self._guid_facenormal = {}
        self._guid_vertexlabel = {}
        self._guid_edgelabel = {}
        self._guid_facelabel = {}

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)
        else:
            compas_rhino.clear_current_layer()

    # ==========================================================================
    # components
    # ==========================================================================

    def draw(self, settings=None):
        """Draw the mesh using the chosen visualisation settings.

        Parameters
        ----------
        settings : dict, optional
            Dictionary of visualisation settings that will be merged with the settings of the artist.

        Notes
        -----
        This method will attempt to clear all previously drawn elements by this artist.
        However, clearing the artist layer has to be done explicitly with a call to ``MeshArtist.clear_layer``.

        """
        self.clear()
        if not settings:
            settings = {}
        self.settings.update(settings)
        if self.settings['show.vertices']:
            self.draw_vertices()
            if self.settings['show.vertexlabels']:
                self.draw_vertexlabels()
            if self.settings['show.vertexnormals']:
                self.draw_vertexnormals()
        if self.settings['show.faces']:
            self.draw_faces(join_faces=self.settings['join_faces'])
            if self.settings['show.facelabels']:
                self.draw_facelabels()
            if self.settings['show.facenormals']:
                self.draw_facenormals()
        if self.settings['show.edges']:
            self.draw_edges()
            if self.settings['show.edgelabels']:
                self.draw_edgelabels()

    def draw_mesh(self, color=None, disjoint=False):
        """Draw the mesh as a consolidated RhinoMesh.

        Parameters
        ----------
        color : 3-tuple, optional
            RGB color components in integer format (0-255).
        disjoint : bool, optional
            Draw the faces of the mesh with disjoint vertices.
            Default is ``False``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have
        only triangular or quadrilateral faces.
        Faces with more than 4 vertices will be triangulated on-the-fly.
        """
        key_index = self.mesh.key_index()
        vertices = self.mesh.vertices_attributes('xyz')
        faces = [[key_index[key] for key in self.mesh.face_vertices(fkey)] for fkey in self.mesh.faces()]
        new_faces = []
        for face in faces:
            f = len(face)
            if f == 3:
                new_faces.append(face + face[-1:])
            elif f == 4:
                new_faces.append(face)
            elif f > 4:
                centroid = len(vertices)
                vertices.append(centroid_polygon([vertices[index] for index in face]))
                for a, b in pairwise(face + face[0:1]):
                    new_faces.append([centroid, a, b, b])
            else:
                continue
        layer = self.layer
        name = "{}.mesh".format(self.mesh.name)
        guid = compas_rhino.draw_mesh(vertices, new_faces, layer=layer, name=name, color=color, disjoint=disjoint)
        self.guids += [guid]
        return [guid]

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
        vertices = keys or list(self.mesh.vertices())
        vertex_color = color_to_colordict(color,
                                          vertices,
                                          default=self.settings['color.vertices'],
                                          colorformat='rgb',
                                          normalize=False)
        points = []
        for vertex in vertices:
            points.append({
                'pos': self.mesh.vertex_coordinates(vertex),
                'name': "{}.vertex.{}".format(self.mesh.name, vertex),
                'color': vertex_color[vertex]})

        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        self.guid_vertex = zip(guids, vertices)
        return guids

    def draw_faces(self, keys=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        fkeys : list
            A list of face keys identifying which faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : str, tuple, dict
            The color specififcation for the faces.
            Colors should be specified in the form of a string (hex colors) or as a tuple of RGB components.
            To apply the same color to all faces, provide a single color specification.
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default face color (``self.settings['color.faces']``).
            The default is ``None``, in which case all faces are assigned the default face color.
        join_faces : bool, optional
            Join the faces into 1 mesh.
            Default is ``False``, in which case the faces are drawn as individual meshes.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        faces = keys or list(self.mesh.faces())
        face_color = color_to_colordict(color,
                                        faces,
                                        default=self.settings['color.faces'],
                                        colorformat='rgb',
                                        normalize=False)
        facets = []
        for face in faces:
            facets.append({
                'points': self.mesh.face_coordinates(face),
                'name': "{}.face.{}".format(self.mesh.name, face),
                'color': face_color[face]})

        guids = compas_rhino.draw_faces(facets, layer=self.layer, clear=False, redraw=False)
        if not join_faces:
            self.guid_face = zip(guids, faces)
            return guids

        guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
        compas_rhino.rs.ObjectLayer(guid, self.layer)
        compas_rhino.rs.ObjectName(guid, '{}.mesh'.format(self.mesh.name))
        if color:
            compas_rhino.rs.ObjectColor(guid, color)

        self.guids += [guid]
        return [guid]

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
        edges = keys or list(self.mesh.edges())
        edge_color = color_to_colordict(color,
                                        edges,
                                        default=self.settings['color.edges'],
                                        colorformat='rgb',
                                        normalize=False)
        lines = []
        for edge in edges:
            lines.append({
                'start': self.mesh.vertex_coordinates(edge[0]),
                'end': self.mesh.vertex_coordinates(edge[1]),
                'color': edge_color[edge],
                'name': "{}.edge.{}-{}".format(self.mesh.name, *edge)})

        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guid_edge = zip(guids, edges)
        return guids

    # ==========================================================================
    # normals
    # ==========================================================================

    def draw_vertexnormals(self, keys=None, color=None, scale=None):
        """Draw the normals at the vertices of the mesh.

        Parameters
        ----------
        keys : list, optional
            A (sub)set of vertices for which the normals should be drawn.
            Default is to draw all vertex normals.
        color : str (HEX) or tuple (RGB), optional
            The color specification of the normal vectors.
            String values are interpreted as hex colors.
            Tuples are interpreted as RGB components.
            The default vector color is in the settings: ``self.settings['color.vertexnormals']``.
        scale : float, optional
            Scale factor for the vertex normals.
            Default is ``1.0``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        vertices = keys or list(self.mesh.vertices())
        scale = scale or self.settings['scale.vertexnormals']
        color = color or self.settings['color.vertexnormals']

        lines = []
        for vertex in vertices:
            a = self.mesh.vertex_coordinates(vertex)
            n = self.mesh.vertex_normal(vertex)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'color': color,
                'name': "{}.vertexnormal.{}".format(self.mesh.name, vertex),
                'arrow': 'end'})

        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guid_vertexnormal = zip(guids, vertices)
        return guids

    def draw_facenormals(self, keys=None, color=None, scale=None):
        """Draw the normals of the faces.

        Parameters
        ----------
        keys : list, optional
            A (sub)set of faces for which the normals should be drawn.
            Default is to draw all face normals.
        color : str (HEX) or tuple (RGB), optional
            The color specification of the normal vectors.
            String values are interpreted as hex colors.
            Tuples are interpreted as RGB components.
            The default vector color is in the settings: ``self.settings['color.facenormals']``.
        scale : float, optional
            Scale factor for the face normals.
            Default is ``1.0``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        faces = keys or list(self.mesh.faces())
        scale = scale or self.settings['scale.facenormals']
        color = color or self.settings['color.facenormals']

        lines = []
        for face in faces:
            a = self.mesh.face_centroid(face)
            n = self.mesh.face_normal(face)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'name': "{}.facenormal.{}".format(self.mesh.name, face),
                'color': color,
                'arrow': 'end'})

        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guid_facenormal = zip(guids, faces)
        return guids

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
            vertex_text = {key: str(key) for key in self.mesh.vertices()}
        elif isinstance(text, dict):
            vertex_text = text
        elif text == 'key':
            vertex_text = {key: str(key) for key in self.mesh.vertices()}
        elif text == 'index':
            vertex_text = {key: str(index) for index, key in enumerate(self.mesh.vertices())}
        else:
            raise NotImplementedError

        vertex_color = color_to_colordict(color,
                                          vertex_text.keys(),
                                          default=self.settings['color.vertices'],
                                          colorformat='rgb',
                                          normalize=False)
        labels = []
        for vertex in vertex_text:
            labels.append({
                'pos': self.mesh.vertex_coordinates(vertex),
                'name': "{}.vertexlabel.{}".format(self.mesh.name, vertex),
                'color': vertex_color[vertex],
                'text': vertex_text[vertex]})

        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guid_vertexlabel = zip(guids, vertex_text.keys())
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
            face_text = {key: str(key) for key in self.mesh.faces()}
        elif isinstance(text, dict):
            face_text = text
        elif text == 'key':
            face_text = {key: str(key) for key in self.mesh.faces()}
        elif text == 'index':
            face_text = {key: str(index) for index, key in enumerate(self.mesh.faces())}
        else:
            raise NotImplementedError

        face_color = color_to_colordict(color,
                                        face_text.keys(),
                                        default=self.settings['color.faces'],
                                        colorformat='rgb',
                                        normalize=False)

        labels = []
        for face in face_text:
            labels.append({
                'pos': self.mesh.face_center(face),
                'name': "{}.facelabel.{}".format(self.mesh.name, face),
                'color': face_color[face],
                'text': face_text[face]})

        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guid_facelabel = zip(guids, face_text.keys())
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
            edge_text = {(u, v): "{}-{}".format(u, v) for u, v in self.mesh.edges()}
        elif isinstance(text, dict):
            edge_text = text
        else:
            raise NotImplementedError

        edge_color = color_to_colordict(color,
                                        edge_text.keys(),
                                        default=self.settings['color.edges'],
                                        colorformat='rgb',
                                        normalize=False)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': self.mesh.edge_midpoint(*edge),
                'name': "{}.edgelabel.{}-{}".format(self.mesh.name, *edge),
                'color': edge_color[edge],
                'text': edge_text[edge]})

        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guid_edgelabel = zip(guids, edge_text.keys())
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures import Mesh

    mesh = Mesh.from_polyhedron(20)

    artist = MeshArtist(mesh)
    artist.clear()
    artist.draw_faces()
    artist.draw_vertices()
    artist.draw_edges()
