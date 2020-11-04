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
    """Artists for drawing mesh data structures.

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
        self._mesh = None
        self._vertex_xyz = None
        self.mesh = mesh
        self.layer = layer
        self.color_vertices = (255, 255, 255)
        self.color_edges = (0, 0, 0)
        self.color_faces = (0, 0, 0)

    @property
    def mesh(self):
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh
        self._vertex_xyz = None

    @property
    def vertex_xyz(self):
        """dict:
        The view coordinates of the mesh vertices.
        The view coordinates default to the actual mesh coordinates.
        """
        if not self._vertex_xyz:
            return {vertex: self.mesh.vertex_attributes(vertex, 'xyz') for vertex in self.mesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_by_name(self):
        """Clear all objects in the "namespace" of the associated mesh."""
        guids = compas_rhino.get_objects(name="{}.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    def clear_layer(self):
        """Clear the main layer of the artist."""
        if self.layer:
            compas_rhino.clear_layer(self.layer)

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

    def draw_mesh(self, color=(0, 0, 0), disjoint=False):
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
        vertex_index = self.mesh.key_index()
        vertex_xyz = self.vertex_xyz
        vertices = [vertex_xyz[vertex] for vertex in self.mesh.vertices()]
        faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]
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
        name = "{}".format(self.mesh.name)
        guid = compas_rhino.draw_mesh(vertices, new_faces, layer=layer, name=name, color=color, disjoint=disjoint)
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
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

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
            return guids
        guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
        compas_rhino.rs.ObjectLayer(guid, self.layer)
        compas_rhino.rs.ObjectName(guid, '{}'.format(self.mesh.name))
        if color:
            compas_rhino.rs.ObjectColor(guid, color)
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
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

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

    # ==========================================================================
    # draw labels
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
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

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
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

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
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
