from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_points

import compas_rhino
from compas.artists import MeshArtist
from compas.colors import Color
from .artist import RhinoArtist


class MeshArtist(RhinoArtist, MeshArtist):
    """Artists for drawing mesh data structures.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A COMPAS mesh.
    layer : str, optional
        The name of the layer that will contain the mesh.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`MeshArtist`.

    """

    def __init__(self, mesh, layer=None, **kwargs):
        super(MeshArtist, self).__init__(mesh=mesh, layer=layer, **kwargs)

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

    def draw(self, color=None, disjoint=False):
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
        self.color = color
        vertex_index = self.mesh.vertex_index()
        vertex_xyz = self.vertex_xyz
        vertices = [vertex_xyz[vertex] for vertex in self.mesh.vertices()]
        faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]
        layer = self.layer
        name = "{}.mesh".format(self.mesh.name)
        guid = compas_rhino.draw_mesh(
            vertices,
            faces,
            layer=layer,
            name=name,
            color=self.color.rgb255,
            disjoint=disjoint,
        )
        return [guid]

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
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
            points.append(
                {
                    "pos": vertex_xyz[vertex],
                    "name": "{}.vertex.{}".format(self.mesh.name, vertex),
                    "color": self.vertex_color[vertex].rgb255,
                }
            )
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A selection of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[int, int], :class:`~compas.colors.Color`], optional
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
            lines.append(
                {
                    "start": vertex_xyz[edge[0]],
                    "end": vertex_xyz[edge[1]],
                    "color": self.edge_color[edge].rgb255,
                    "name": "{}.edge.{}-{}".format(self.mesh.name, *edge),
                }
            )
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        return guids

    def draw_faces(self, faces=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
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
            facets.append(
                {
                    "points": [vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)],
                    "name": "{}.face.{}".format(self.mesh.name, face),
                    "color": self.face_color[face].rgb255,
                }
            )
        guids = compas_rhino.draw_faces(facets, layer=self.layer, clear=False, redraw=False)
        if join_faces:
            guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
            compas_rhino.rs.ObjectLayer(guid, self.layer)
            compas_rhino.rs.ObjectName(guid, "{}.mesh".format(self.mesh.name))
            if color:
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
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The color specification of the normal vectors.
        scale : float, optional
            Scale factor for the vertex normals.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color).rgb255
        vertex_xyz = self.vertex_xyz
        vertices = vertices or self.vertices
        lines = []
        for vertex in vertices:
            a = vertex_xyz[vertex]
            n = self.mesh.vertex_normal(vertex)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append(
                {
                    "start": a,
                    "end": b,
                    "color": color,
                    "name": "{}.vertexnormal.{}".format(self.mesh.name, vertex),
                    "arrow": "end",
                }
            )
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_facenormals(self, faces=None, color=(0, 255, 255), scale=1.0):
        """Draw the normals of the faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of face normals to draw.
            Default is to draw all face normals.
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The color specification of the normal vectors.
        scale : float, optional
            Scale factor for the face normals.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        color = Color.coerce(color).rgb255
        vertex_xyz = self.vertex_xyz
        faces = faces or self.faces
        lines = []
        for face in faces:
            a = centroid_points([vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)])
            n = self.mesh.face_normal(face)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append(
                {
                    "start": a,
                    "end": b,
                    "name": "{}.facenormal.{}".format(self.mesh.name, face),
                    "color": color,
                    "arrow": "end",
                }
            )
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # ==========================================================================
    # draw labels
    # ==========================================================================

    def draw_vertexlabels(self, text=None):
        """Draw labels for a selection vertices.

        Parameters
        ----------
        text : dict[int, str], optional
            A dictionary of vertex labels as vertex-text pairs.
            The default value is None, in which case every vertex will be labelled with its identifier.

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
                    "name": "{}.vertexlabel.{}".format(self.mesh.name, vertex),
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
            The default value is None, in which case every edge will be labelled with its identifier.

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
                    "name": "{}.edgelabel.{}-{}".format(self.mesh.name, *edge),
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
                    "pos": centroid_points([vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]),
                    "name": "{}.facelabel.{}".format(self.mesh.name, face),
                    "color": self.face_color[face].rgb255,
                    "text": self.face_text[face],
                }
            )
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
