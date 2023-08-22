from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from Rhino.Geometry import TextDot  # type: ignore
import scriptcontext as sc  # type: ignore

from compas.geometry import centroid_points
from compas.geometry import Point
from compas.geometry import Line

import compas_rhino
from compas.artists import MeshArtist as BaseArtist
from compas.colors import Color
from compas_rhino.conversions import vertices_and_faces_to_rhino
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import line_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes
from ._helpers import ngon


class MeshArtist(RhinoArtist, BaseArtist):
    """Artists for drawing mesh data structures.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        A COMPAS mesh.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`MeshArtist`.

    """

    def __init__(self, mesh, **kwargs):
        super(MeshArtist, self).__init__(mesh=mesh, **kwargs)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Delete all objects drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.*".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertices(self):
        """Delete all vertices drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edges(self):
        """Delete all edges drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edge.*".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_faces(self):
        """Delete all faces drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.face.*".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertexnormals(self):
        """Delete all vertex normals drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*.normal".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_facenormals(self):
        """Delete all face normals drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.face.*.normal".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_vertexlabels(self):
        """Delete all vertex labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.vertex.*.label".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_edgelabels(self):
        """Delete all edge labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.edge.*.label".format(self.mesh.name))  # type: ignore
        compas_rhino.delete_objects(guids, purge=True)

    def clear_facelabels(self):
        """Delete all face labels drawn by this artist.

        Returns
        -------
        None

        """
        guids = compas_rhino.get_objects(name="{}.face.*.label".format(self.mesh.name))  # type: ignore
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
        color = Color.coerce(color) or self.color
        vertex_index = self.mesh.vertex_index()  # type: ignore
        vertex_xyz = self.vertex_xyz
        vertices = [vertex_xyz[vertex] for vertex in self.mesh.vertices()]  # type: ignore
        faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]  # type: ignore
        layer = self.layer
        name = "{}.mesh".format(self.mesh.name)  # type: ignore
        attr = attributes(name=name, color=color, layer=layer)
        guid = sc.doc.Objects.AddMesh(vertices_and_faces_to_rhino(vertices, faces, disjoint=disjoint), attr)
        return [guid]

    def draw_vertices(self, vertices=None, color=None, text=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertices to draw.
            Default is None, in which case all vertices are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the vertices.
            The default is the value of :attr:`MeshArtist.default_vertexcolor`.
        text : dict[int, str], optional
            A dictionary of vertex labels as vertex-text pairs.
        fontheight : int, optional
            Font height of the vertex labels.
        fontface : str, optional
            Font face of the vertex labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino point objects.

        """
        vertices = vertices or self.mesh.vertices()  # type: ignore

        self.vertex_color = color
        self.vertex_text = text
        vertex_xyz = self.vertex_xyz
        vertex_color = self.vertex_color
        vertex_text = self.vertex_text

        guids = []

        for vertex in vertices:
            point = point_to_rhino(vertex_xyz[vertex])
            name = "{}.vertex.{}".format(self.mesh.name, vertex)  # type: ignore
            color = vertex_color[vertex]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)
            guid = sc.doc.Objects.AddPoint(point, attr)
            guids.append(guid)

            if text:
                if vertex in vertex_text:
                    attr = attributes(name="{}.label".format(name), color=color, layer=self.layer)
                    dot = TextDot(str(vertex_text[vertex]), point)  # type: ignore
                    dot.FontHeight = fontheight
                    dot.FontFace = fontface
                    sc.doc.Objects.AddTextDot(dot, attr)

        return guids

    def draw_edges(self, edges=None, color=None, text=None, fontheight=10, fontface="Arial Regular"):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A selection of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[int, int], :class:`~compas.colors.Color`], optional
            The color of the edges.
            The default color is the value of :attr:`MeshArtist.default_edgecolor`.
        text : dict[tuple[int, int], str], optional
            A dictionary of edge labels as edge-text pairs.
        fontheight : int, optional
            Font height of the edge labels.
        fontface : str, optional
            Font face of the edge labels.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino line objects.

        """
        edges = edges or self.mesh.edges()  # type: ignore

        self.edge_color = color
        self._edge_text = text
        vertex_xyz = self.vertex_xyz
        edge_color = self.edge_color
        edge_text = self.edge_text

        guids = []

        for edge in edges:
            name = "{}.edge.{}-{}".format(self.mesh.name, *edge)  # type: ignore
            color = edge_color[edge]  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)
            line = Line(vertex_xyz[edge[0]], vertex_xyz[edge[1]])
            guid = sc.doc.Objects.AddLine(line_to_rhino(line), attr)
            guids.append(guid)

            if text:
                if edge in edge_text:
                    point = point_to_rhino(line.midpoint)
                    attr = attributes(name="{}.label".format(name), color=color, layer=self.layer)
                    dot = TextDot(str(edge_text[edge]), point)  # type: ignore
                    dot.FontHeight = fontheight
                    dot.FontFace = fontface
                    sc.doc.Objects.AddTextDot(dot, attr)

        return guids

    def draw_faces(self, faces=None, color=None, text=None, fontheight=10, fontface="Arial Regular", join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`~compas.colors.Color` | dict[int, :class:`~compas.colors.Color`], optional
            The color of the faces.
            The default color is the value of :attr:`MeshArtist.default_facecolor`.
        text : dict[int, str], optional
            A dictionary of face labels as face-text pairs.
        fontheight : int, optional
            Font height of the face labels.
        fontface : str, optional
            Font face of the face labels.
        join_faces : bool, optional
            If True, join the faces into a single mesh.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino mesh objects.

        """
        if join_faces:
            return self.draw(color=color, disjoint=True)

        faces = faces or self.mesh.faces()  # type: ignore

        self.face_color = color
        self.face_text = text
        vertex_xyz = self.vertex_xyz
        face_color = self.face_color
        face_text = self.face_text

        guids = []

        for face in faces:
            name = "{}.face.{}".format(self.mesh.name, face)  # type: ignore
            color = face_color[face]  # type: ignore
            vertices = [vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]  # type: ignore
            facet = ngon(len(vertices))
            if facet:
                attr = attributes(name=name, color=color, layer=self.layer)
                guid = sc.doc.Objects.AddMesh(vertices_and_faces_to_rhino(vertices, [facet]), attr)
                guids.append(guid)

            if text:
                if face in face_text:
                    point = point_to_rhino(centroid_points(vertices))  # type: ignore
                    attr = attributes(name="{}.label".format(name), color=color, layer=self.layer)
                    dot = TextDot(str(face_text[face]), point)  # type: ignore
                    dot.FontHeight = fontheight
                    dot.FontFace = fontface
                    sc.doc.Objects.AddTextDot(dot, attr)

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
        color = Color.coerce(color)
        vertex_xyz = self.vertex_xyz
        vertices = vertices or self.mesh.vertices()  # type: ignore
        guids = []
        for vertex in vertices:
            normal = self.mesh.vertex_normal(vertex)  # type: ignore
            start = Point(*vertex_xyz[vertex])
            end = start + normal * scale
            name = "{}.vertex.{}.normal".format(self.mesh.name, vertex)  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)
            guid = sc.doc.Objects.AddLine(point_to_rhino(start), point_to_rhino(end), attr)
            guids.append(guid)
        return guids

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
        color = Color.coerce(color)
        vertex_xyz = self.vertex_xyz
        faces = faces or self.mesh.faces()  # type: ignore
        guids = []
        for face in faces:
            point = Point(*centroid_points([vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]))  # type: ignore
            normal = self.mesh.face_normal(face)  # type: ignore
            start = point
            end = start + normal * scale
            name = "{}.face.{}.normal".format(self.mesh.name, face)  # type: ignore
            attr = attributes(name=name, color=color, layer=self.layer)
            guid = sc.doc.Objects.AddLine(point_to_rhino(start), point_to_rhino(end), attr)
            guids.append(guid)
        return guids
