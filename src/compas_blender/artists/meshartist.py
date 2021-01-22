# from __future__ import annotations

from functools import partial

import compas_blender

from compas_blender.artists._artist import BaseArtist
from compas.utilities import color_to_colordict

colordict = partial(color_to_colordict, colorformat='rgb', normalize=True)


__all__ = ['MeshArtist']


class MeshArtist(BaseArtist):
    """A mesh artist defines functionality for visualising COMPAS meshes in Blender.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    settings : dict, optional
        A dict with custom visualisation settings.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The COMPAS mesh associated with the artist.
    settings : dict
        Default settings for color, scale, tolerance, ...

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas_blender.artists import MeshArtist

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        MeshArtist(mesh).draw()

    """

    def __init__(self, mesh):
        super().__init__()
        self._collection = None
        self._vertexcollection = None
        self._edgecollection = None
        self._facecollection = None
        self._object_vertex = {}
        self._object_edge = {}
        self._object_face = {}
        self.color_vertices = (1.0, 1.0, 1.0)
        self.color_edges = (0.0, 0.0, 0.0)
        self.color_faces = (0.7, 0.7, 0.7)
        self.show_vertices = True
        self.show_edges = True
        self.show_faces = True
        self.mesh = mesh

    @property
    def collection(self):
        if not self._collection:
            self._collection = compas_blender.create_collection(self.mesh.name)
        return self._collection

    @property
    def vertexcollection(self):
        path = f"{self.mesh.name}::Vertices"
        if not self._vertexcollection:
            self._vertexcollection = compas_blender.create_collections_from_path(path)[1]
        return self._vertexcollection

    @property
    def edgecollection(self):
        path = f"{self.mesh.name}::Edges"
        if not self._edgecollection:
            self._edgecollection = compas_blender.create_collections_from_path(path)[1]
        return self._edgecollection

    @property
    def facecollection(self):
        path = f"{self.mesh.name}::Faces"
        if not self._facecollection:
            self._facecollection = compas_blender.create_collections_from_path(path)[1]
        return self._facecollection

    @property
    def object_vertex(self):
        """Map between Blender object objects and mesh vertex identifiers."""
        return self._object_vertex

    @object_vertex.setter
    def object_vertex(self, values):
        self._object_vertex = dict(values)

    @property
    def object_edge(self):
        """Map between Blender object objects and mesh edge identifiers."""
        return self._object_edge

    @object_edge.setter
    def object_edge(self, values):
        self._object_edge = dict(values)

    @property
    def object_face(self):
        """Map between Blender object objects and mesh face identifiers."""
        return self._object_face

    @object_face.setter
    def object_face(self, values):
        self._object_face = dict(values)

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Clear all objects previously drawn by this artist.
        """
        objects = []
        objects += list(self.object_vertex)
        objects += list(self.object_edge)
        objects += list(self.object_face)
        compas_blender.delete_objects(objects, purge_data=True)
        self._object_vertex = {}
        self._object_edge = {}
        self._object_face = {}

    # ==========================================================================
    # components
    # ==========================================================================

    def draw(self):
        """Draw the mesh using the chosen visualisation settings.

        Parameters
        ----------
        settings : dict, optional
            Dictionary of visualisation settings that will be merged with the settings of the artist.

        """
        self.clear()
        if self.show_vertices:
            self.draw_vertices()
        if self.show_faces:
            self.draw_faces()
        if self.show_edges:
            self.draw_edges()

    def draw_mesh(self):
        """Draw the mesh."""
        vertices, faces = self.mesh.to_vertices_and_faces()
        obj = compas_blender.draw_mesh(vertices, faces, name=self.mesh.name, collection=self.collection)
        return [obj]

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list
            A list of vertex keys identifying which vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : rgb-tuple or dict of rgb-tuple
            The color specififcation for the vertices.

        Returns
        -------
        list of :class:`bpy.types.Object`

        """
        vertices = vertices or list(self.mesh.vertices())
        vertex_color = colordict(color, vertices, default=self.color_vertices)
        points = []
        for vertex in vertices:
            points.append({
                'pos': self.mesh.vertex_coordinates(vertex),
                'name': f"{self.mesh.name}.vertex.{vertex}",
                'color': vertex_color[vertex],
                'radius': 0.01
            })
        objects = compas_blender.draw_points(points, self.vertexcollection)
        self.object_vertex = zip(objects, vertices)
        return objects

    def draw_faces(self, faces=None, color=None):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list
            A list of face keys identifying which faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : rgb-tuple or dict of rgb-tuple
            The color specififcation for the faces.

        Returns
        -------
        list of :class:`bpy.types.Object`

        """
        faces = faces or list(self.mesh.faces())
        face_color = colordict(color, faces, default=self.color_faces)
        facets = []
        for face in faces:
            facets.append({
                'points': self.mesh.face_coordinates(face),
                'name': f"{self.mesh.name}.face.{face}",
                'color': face_color[face]
            })
        objects = compas_blender.draw_faces(facets, self.facecollection)
        self.object_face = zip(objects, faces)
        return objects

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : rgb-tuple or dict of rgb-tuple
            The color specififcation for the edges.

        Returns
        -------
        list of :class:`bpy.types.Object`

        """
        edges = edges or list(self.mesh.edges())
        edge_color = colordict(color, edges, default=self.color_edges)
        lines = []
        for edge in edges:
            lines.append({
                'start': self.mesh.vertex_coordinates(edge[0]),
                'end': self.mesh.vertex_coordinates(edge[1]),
                'color': edge_color[edge],
                'name': f"{self.mesh.name}.edge.{edge[0]}-{edge[1]}"
            })
        objects = compas_blender.draw_lines(lines, self.edgecollection)
        self.object_edge = zip(objects, edges)
        return objects


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
