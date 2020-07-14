from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.artists.base import BaseArtist

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

    Attributes
    ----------
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

    def __init__(self, mesh, layer=None, name=None):
        super(MeshArtist, self).__init__()
        self.layer = layer
        self.name = name
        self.mesh = mesh
        # update this to plurals
        # make settings an optional parameter
        self.settings = {
            'color.vertices': (255, 255, 255),
            'color.edges': (0, 0, 0),
            'color.faces': (210, 210, 210),
            'color.vertex_normals': (0, 255, 0),
            'color.face_normals': (0, 255, 0),
            'scale.vertex_normals': 0.1,
            'scale.face_normals': 0.1,
            'show.vertices': True,
            'show.edges': True,
            'show.faces': True,
            'show.vertex_labels': False,
            'show.face_labels': False,
            'show.edge_labels': False,
            'join_faces': True}

    # ==========================================================================
    # clear
    # ==========================================================================

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

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

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
            if self.settings['show.vertex_labels']:
                self.draw_vertexlabels()
        if self.settings['show.faces']:
            self.draw_faces(join_faces=self.settings['join_faces'])
            if self.settings['show.face_labels']:
                self.draw_facelabels()
        if self.settings['show.edges']:
            self.draw_edges()
            if self.settings['show.edge_labels']:
                self.draw_edgelabels()
        return self.guids

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
        guids = compas_rhino.draw_mesh(vertices, new_faces, layer=layer, name=name, color=color, disjoint=disjoint)
        self.guids += guids
        return guids

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

        Notes
        -----
        The vertices are named using the following template: ``"{mesh.name}.vertex.{id}"``.
        This name can be used afterwards to identify vertices in the Rhino model.
        """
        keys = keys or list(self.mesh.vertices())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings.get('color.vertices'),
                                       colorformat='rgb',
                                       normalize=False)
        points = []
        for key in keys:
            points.append({
                'pos': self.mesh.vertex_coordinates(key),
                'name': "{}.vertex.{}".format(self.mesh.name, key),
                'color': colordict[key]})

        guids = compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        self.guids += guids
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
            Missing keys will be assigned the default face color (``self.settings['face.color']``).
            The default is ``None``, in which case all faces are assigned the default face color.
        join_faces : bool, optional
            Join the faces into 1 mesh.
            Default is ``False``, in which case the faces are drawn as individual meshes.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        Notes
        -----
        The faces are named using the following template: ``"{mesh.name}.face.{id}"``.
        This name can be used afterwards to identify faces in the Rhino model.
        """
        keys = keys or list(self.mesh.faces())

        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings.get('color.faces'),
                                       colorformat='rgb',
                                       normalize=False)
        faces = []
        for fkey in keys:
            faces.append({
                'points': self.mesh.face_coordinates(fkey),
                'name': "{}.face.{}".format(self.mesh.name, fkey),
                'color': colordict[fkey]})

        guids = compas_rhino.draw_faces(faces, layer=self.layer, clear=False, redraw=False)
        if not join_faces:
            self.guids += guids
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
            Missing keys will be assigned the default edge color (``self.settings['edge.color']``).
            The default is ``None``, in which case all edges are assigned the default edge color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        Notes
        -----
        All edges are named using the following template: ``"{mesh.name}.edge.{u}-{v}"``.
        This name can be used afterwards to identify edges in the Rhino model.

        """
        keys = keys or list(self.mesh.edges())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings.get('color.edges'),
                                       colorformat='rgb',
                                       normalize=False)
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.mesh.vertex_coordinates(u),
                'end': self.mesh.vertex_coordinates(v),
                'color': colordict[(u, v)],
                'name': "{}.edge.{}-{}".format(self.mesh.name, u, v)})

        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guids += guids
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
            The default vector color is in the settings: ``self.settings['color.normal']``.
        scale : float, optional
            Scale factor for the vertex normals.
            Default is ``1.0``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        Notes
        -----
        All vertex normals are named using the following template: ``"{mesh.name}.vertex_normal.{id}"``.
        This name can be used afterwards to identify vertex normals in the Rhino model.

        """
        keys = keys or list(self.mesh.vertices())
        scale = scale or self.settings.get('scale.vertex_normals')
        color = color or self.settings.get('color.vertex_normals')
        lines = []
        for key in keys:
            a = self.mesh.vertex_coordinates(key)
            n = self.mesh.vertex_normal(key)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'color': color,
                'name': "{}.vertex_normal.{}".format(self.mesh.name, key),
                'arrow': 'end'})

        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guids += guids
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
            The default vector color is in the settings: ``self.settings['color.normal']``.
        scale : float, optional
            Scale factor for the face normals.
            Default is ``1.0``.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        Notes
        -----
        All face normals are named using the following template: ``"{mesh.name}.face_normal.{id}"``.
        This name can be used afterwards to identify face normals in the Rhino model.

        """
        keys = keys or list(self.mesh.faces())
        scale = scale or self.settings.get('scale.face_normals')
        color = color or self.settings.get('color.face_normals')
        lines = []
        for key in self.mesh.faces():
            a = self.mesh.face_centroid(key)
            n = self.mesh.face_normal(key)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'name': "{}.face_normal.{}".format(self.mesh.name, key),
                'color': color,
                'arrow': 'end'})
        guids = compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        self.guids += guids
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

        Notes
        -----
        All vertex labels are named using the following template: ``"{mesh.name}.vertex_label.{id}"``.
        This name can be used afterwards to identify vertices in the Rhino model.

        """
        if text is None:
            textdict = {key: str(key) for key in self.mesh.vertices()}
        elif isinstance(text, dict):
            textdict = text
        elif text == 'key':
            textdict = {key: str(key) for key in self.mesh.vertices()}
        elif text == 'index':
            textdict = {key: str(index) for index, key in enumerate(self.mesh.vertices())}
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings.get('color.vertices'),
                                       colorformat='rgb',
                                       normalize=False)
        labels = []
        for key, text in iter(textdict.items()):
            labels.append({
                'pos': self.mesh.vertex_coordinates(key),
                'name': "{}.vertex_label.{}".format(self.mesh.name, key),
                'color': colordict[key],
                'text': textdict[key]})

        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guids += guids
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

        Notes
        -----
        The face labels are named using the following template: ``"{mesh.name}.face_label.{id}"``.
        This name is used afterwards to identify faces and face labels in the Rhino model.

        """
        if text is None:
            textdict = {key: str(key) for key in self.mesh.faces()}
        elif isinstance(text, dict):
            textdict = text
        elif text == 'key':
            textdict = {key: str(key) for key in self.mesh.faces()}
        elif text == 'index':
            textdict = {key: str(index) for index, key in enumerate(self.mesh.faces())}
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings.get('color.faces'),
                                       colorformat='rgb',
                                       normalize=False)

        labels = []
        for key, text in iter(textdict.items()):
            labels.append({
                'pos': self.mesh.face_center(key),
                'name': "{}.face_label.{}".format(self.mesh.name, key),
                'color': colordict[key],
                'text': textdict[key]})

        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guids += guids
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
            Individual colors can be assigned using a dictionary of key-color pairs.
            Missing keys will be assigned the default face color (``self.settings['edge.color']``).
            The default is ``None``, in which case all edges are assigned the default edge color.

        Returns
        -------
        list
            The GUIDs of the created Rhino objects.

        Notes
        -----
        The edge labels are named using the following template: ``"{mesh.name}.edge_label.{u}-{v}"``.
        This name can be used afterwards to identify edges in the Rhino model.

        """
        if text is None:
            textdict = {(u, v): "{}-{}".format(u, v) for u, v in self.mesh.edges()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings.get('color.edges'),
                                       colorformat='rgb',
                                       normalize=False)
        labels = []
        for (u, v), text in iter(textdict.items()):
            labels.append({
                'pos': self.mesh.edge_midpoint(u, v),
                'name': "{}.edge_label.{}-{}".format(self.mesh.name, u, v),
                'color': colordict[(u, v)],
                'text': textdict[(u, v)]})

        guids = compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)
        self.guids += guids
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
