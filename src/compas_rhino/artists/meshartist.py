from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

from compas.utilities import color_to_colordict
from compas.utilities import pairwise
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_polygon
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
    """

    def __init__(self, mesh, layer=None, **kwargs):
        super(MeshArtist, self).__init__(mesh=mesh, layer=layer, **kwargs)

    def clear_by_name(self):
        """Clear all objects in the "namespace" of the associated mesh."""
        guids = compas_rhino.get_objects(name="{}.*".format(self.mesh.name))
        compas_rhino.delete_objects(guids, purge=True)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self, vertices=None, edges=None, faces=None, vertexcolor=None, edgecolor=None, facecolor=None, join_faces=False):
        """Draw the network using the chosen visualisation settings.

        Parameters
        ----------
        vertices : list, optional
            A list of vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        edges : list, optional
            A list of edges to draw.
            The default is ``None``, in which case all edges are drawn.
        faces : list, optional
            A selection of faces to draw.
            The default is ``None``, in which case all faces are drawn.
        vertexcolor : tuple or dict of tuple, optional
            The color specififcation for the vertices.
            The default color is the value of ``~MeshArtist.default_vertexcolor``.
        edgecolor : tuple or dict of tuple, optional
            The color specififcation for the edges.
            The default color is the value of ``~MeshArtist.default_edgecolor``.
        facecolor : tuple or dict of tuple, optional
            The color specififcation for the faces.
            The default color is the value of ``~MeshArtist.default_facecolor``.
        join_faces : bool, optional
            Join the faces into 1 mesh.
            Default is ``False``, in which case the faces are drawn as individual meshes.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        guids = self.draw_vertices(vertices=vertices, color=vertexcolor)
        guids += self.draw_edges(edges=edges, color=edgecolor)
        guids += self.draw_faces(faces=faces, color=facecolor, join_faces=join_faces)
        return guids

    def draw_mesh(self, color=None, disjoint=False):
        """Draw the mesh as a consolidated RhinoMesh.

        Parameters
        ----------
        color : tuple, optional
            The color of the mesh.
            Default is the value of ``~MeshArtist.default_color``.
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
        color = color or self.default_color
        vertex_index = self.mesh.vertex_index()
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
        layer = self.layer
        name = "{}".format(self.mesh.name)
        guid = compas_rhino.draw_mesh(vertices, new_faces, layer=layer, name=name, color=color, disjoint=disjoint)
        return [guid]

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list, optional
            A selection of vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : tuple or dict of tuple, optional
            The color specififcation for the vertices.
            The default is the value of ``~MeshArtist.default_vertexcolor``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        self.vertex_color = color
        vertices = vertices or list(self.mesh.vertices())
        vertex_xyz = self.vertex_xyz
        points = []
        for vertex in vertices:
            points.append({
                'pos': vertex_xyz[vertex],
                'name': "{}.vertex.{}".format(self.mesh.name, vertex),
                'color': self.vertex_color.get(vertex, self.default_vertexcolor)
            })
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
            The default color is the value of ``~MeshArtist.default_facecolor``.
        join_faces : bool, optional
            Join the faces into 1 mesh.
            Default is ``False``, in which case the faces are drawn as individual meshes.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        self.face_color = color
        faces = faces or list(self.mesh.faces())
        vertex_xyz = self.vertex_xyz
        facets = []
        for face in faces:
            facets.append({
                'points': [vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)],
                'name': "{}.face.{}".format(self.mesh.name, face),
                'color': self.face_color.get(face, self.default_facecolor)
            })
        guids = compas_rhino.draw_faces(facets, layer=self.layer, clear=False, redraw=False)
        if not join_faces:
            return guids
        guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
        compas_rhino.rs.ObjectLayer(guid, self.layer)
        compas_rhino.rs.ObjectName(guid, '{}'.format(self.mesh.name))
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
            The default color is the value of ``~MeshArtist.default_edgecolor``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        """
        self.edge_color = color
        edges = edges or list(self.mesh.edges())
        vertex_xyz = self.vertex_xyz
        lines = []
        for edge in edges:
            lines.append({
                'start': vertex_xyz[edge[0]],
                'end': vertex_xyz[edge[1]],
                'color': self.edge_color.get(edge, self.default_edgecolor),
                'name': "{}.edge.{}-{}".format(self.mesh.name, *edge)
            })
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
                'arrow': 'end'
            })
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
        text : dict, optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is ``None``, in which case every vertex will be labelled with its key.
        color : tuple or dict of tuple, optional
            The color specification of the labels.
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
            The color specification of the labels.
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
            The color specification of the labels.
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
