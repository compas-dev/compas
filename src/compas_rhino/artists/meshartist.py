from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial
import compas_rhino

from compas_rhino.artists._artist import BaseArtist

from compas.utilities import color_to_colordict
from compas.utilities import pairwise
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_polygon
from compas.geometry import centroid_points


colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


__all__ = ['MeshArtist']


class MeshArtist(BaseArtist):
    """A mesh artist defines functionality for visualising COMPAS meshes in Rhino.

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
    color_vertices : 3-tuple
        Default color of the vertices.
    color_edges : 3-tuple
        Default color of the edges.
    color_faces : 3-tuple
        Default color of the faces.

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

    def __init__(self, mesh, layer=None):
        super(MeshArtist, self).__init__()
        self._guids = []
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_vertexnormal = {}
        self._guid_facenormal = {}
        self._guid_vertexlabel = {}
        self._guid_edgelabel = {}
        self._guid_facelabel = {}
        self._vertex_xyz = None
        self.mesh = mesh
        self.layer = layer
        self.color_vertices = (255, 255, 255)
        self.color_edges = (0, 0, 0)
        self.color_faces = (0, 0, 0)

    @property
    def vertex_xyz(self):
        """dict:
        The view coordinates of the mesh vertices.
        The view coordinates default to the actual mesh coordinates.
        """
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.mesh.vertex_attributes(vertex, 'xyz') for vertex in self.mesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    @property
    def guids(self):
        """list: The GUIDs of all Rhino objects created by this artist."""
        guids = self._guids
        guids += list(self.guid_vertex.keys())
        guids += list(self.guid_edge.keys())
        guids += list(self.guid_face.keys())
        guids += list(self.guid_vertexnormal.keys())
        guids += list(self.guid_facenormal.keys())
        guids += list(self.guid_vertexlabel.keys())
        guids += list(self.guid_edgelabel.keys())
        guids += list(self.guid_facelabel.keys())
        return guids

    @property
    def guid_vertex(self):
        """dict: Map between Rhino object GUIDs and mesh vertex identifiers."""
        return self._guid_vertex

    @guid_vertex.setter
    def guid_vertex(self, values):
        self._guid_vertex = dict(values)

    @property
    def guid_edge(self):
        """dict: Map between Rhino object GUIDs and mesh edge identifiers."""
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    @property
    def guid_face(self):
        """dict: Map between Rhino object GUIDs and mesh face identifiers."""
        return self._guid_face

    @guid_face.setter
    def guid_face(self, values):
        self._guid_face = dict(values)

    @property
    def guid_vertexnormal(self):
        """dict: Map between Rhino object GUIDs and mesh vertexnormal identifiers."""
        return self._guid_vertexnormal

    @guid_vertexnormal.setter
    def guid_vertexnormal(self, values):
        self._guid_vertexnormal = dict(values)

    @property
    def guid_facenormal(self):
        """dict: Map between Rhino object GUIDs and mesh facenormal identifiers."""
        return self._guid_facenormal

    @guid_facenormal.setter
    def guid_facenormal(self, values):
        self._guid_facenormal = dict(values)

    @property
    def guid_vertexlabel(self):
        """dict: Map between Rhino object GUIDs and mesh vertexlabel identifiers."""
        return self._guid_vertexlabel

    @guid_vertexlabel.setter
    def guid_vertexlabel(self, values):
        self._guid_vertexlabel = dict(values)

    @property
    def guid_facelabel(self):
        """dict: Map between Rhino object GUIDs and mesh facelabel identifiers."""
        return self._guid_facelabel

    @guid_facelabel.setter
    def guid_facelabel(self, values):
        self._guid_facelabel = dict(values)

    @property
    def guid_edgelabel(self):
        """dict: Map between Rhino object GUIDs and mesh edgelabel identifiers."""
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
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []
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

    # ==========================================================================
    # components
    # ==========================================================================

    def draw(self, color=(0, 0, 0), disjoint=False):
        """Draw the mesh as a consolidated RhinoMesh.

        Parameters
        ----------
        color : tuple, optional
            The color of the mesh.
            Default is black, ``(0, 0, 0)``.
        disjoint : bool, optional
            Draw the faces of the mesh with disjoint vertices.
            Default is ``False``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have only triangular or quadrilateral faces.
        Faces with more than 4 vertices will be triangulated on-the-fly.
        """
        self.clear()
        key_index = self.mesh.key_index()
        vertices = self.vertex_xyz.values()
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
        self._guids += [guid]
        return [guid]

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list
            A selection of vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : tuple or dict of tuple, optional
            The color specififcation for the vertices.
            The default is white, ``(255, 255, 255)``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        vertices = vertices or list(self.mesh.vertices())
        vertex_xyz = self.vertex_xyz
        vertex_color = colordict(color, vertices, default=self.color_vertices)
        points = []
        for vertex in vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.mesh.name, vertex),
                'color': vertex_color[vertex]})
        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        self.guid_vertex = zip(guids, vertices)
        return guids

    def draw_faces(self, faces=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list, optional
            A selection of faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : tuple or dict of tuple, optional
            The color specififcation for the faces.
            The default color is black ``(0, 0, 0)``.
        join_faces : bool, optional
            Join the faces into 1 mesh.
            Default is ``False``, in which case the faces are drawn as individual meshes.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        faces = faces or list(self.mesh.faces())
        vertex_xyz = self.vertex_xyz
        face_color = colordict(color, faces, default=self.color_faces)
        facets = []
        for face in faces:
            facets.append({
                'points': [vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)],
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

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list, optional
            A selection of edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : tuple or dict of tuple, optional
            The color specififcation for the edges.
            The default color is black, ``(0, 0, 0)``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        edges = edges or list(self.mesh.edges())
        vertex_xyz = self.vertex_xyz
        edge_color = colordict(color, edges, default=self.color_edges)
        lines = []
        for edge in edges:
            lines.append({
                'start': vertex_xyz[edge[0]],
                'end': vertex_xyz[edge[1]],
                'color': edge_color[edge],
                'name': "{}.edge.{}-{}".format(self.mesh.name, *edge)})
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guid_edge = zip(guids, edges)
        return guids

    # ==========================================================================
    # normals
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
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guid_vertexnormal = zip(guids, vertices)
        return guids

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
        text : dict, optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is ``None``, in which case every vertex will be labelled with its key.
        color : tuple or dict of tuple, optional
            The color sepcification of the labels.
            The default color is the same as the default vertex color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if not text or text == 'key':
            vertex_text = {vertex: str(vertex) for vertex in self.mesh.vertices()}
        elif text == 'index':
            vertex_text = {vertex: str(index) for index, vertex in enumerate(self.mesh.vertices())}
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
                'name': "{}.vertexlabel.{}".format(self.mesh.name, vertex),
                'color': vertex_color[vertex],
                'text': vertex_text[vertex]})
        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guid_vertexlabel = zip(guids, vertex_text)
        return guids

    def draw_facelabels(self, text=None, color=None):
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict, optional
            A dictionary of face labels as face-text pairs.
            The default value is ``None``, in which case every face will be labelled with its key.
        color : tuple or dict of tuple, optional
            The color sepcification of the labels.
            The default color is the same as the default face color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        if not text or text == 'key':
            face_text = {face: str(face) for face in self.mesh.faces()}
        elif text == 'index':
            face_text = {face: str(index) for index, face in enumerate(self.mesh.faces())}
        elif isinstance(text, dict):
            face_text = text
        else:
            raise NotImplementedError
        vertex_xyz = self.vertex_xyz
        face_color = colordict(color, face_text.keys(), default=self.color_faces)
        labels = []
        for face in face_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]),
                'name': "{}.facelabel.{}".format(self.mesh.name, face),
                'color': face_color[face],
                'text': face_text[face]})
        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guid_facelabel = zip(guids, face_text)
        return guids

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict, optional
            A dictionary of edge labels as edge-text pairs.
            The default value is ``None``, in which case every edge will be labelled with its key.
        color : tuple or dict of tuple, optional
            The color sepcification of the labels.
            The default color is the same as the default color for edges.

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
        vertex_xyz = self.vertex_xyz
        edge_color = colordict(color, edge_text.keys(), default=self.color_edges)
        labels = []
        for edge in edge_text:
            labels.append({
                'pos': centroid_points([vertex_xyz[edge[0]], vertex_xyz[edge[1]]]),
                'name': "{}.edgelabel.{}-{}".format(self.mesh.name, *edge),
                'color': edge_color[edge],
                'text': edge_text[edge]})
        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guid_edgelabel = zip(guids, edge_text)
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
