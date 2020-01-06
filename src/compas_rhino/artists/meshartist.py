from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.artists import Artist

from compas.utilities import color_to_colordict
from compas.utilities import pairwise
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_polygon


__all__ = ['MeshArtist']


class MeshArtist(Artist):
    """A mesh artist defines functionality for visualising COMPAS meshes in Rhino.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
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

    __module__ = "compas_rhino.artists"

    def __init__(self, mesh, layer=None):
        super(MeshArtist, self).__init__(layer=layer)
        self.datastructure = mesh
        self.settings.update({
            'color.vertex': (255, 255, 255),
            'color.edge': (0, 0, 0),
            'color.face': (210, 210, 210),
            'color.normal:vertex': (0, 255, 0),
            'color.normal:face': (0, 255, 0),
            'scale.normal:vertex': 0.1,
            'scale.normal:face': 0.1,
            'on.vertices': True,
            'on.edges': True,
            'on.faces': True
        })

    @property
    def mesh(self):
        """Mesh: The mesh that should be painted."""
        return self.datastructure

    @mesh.setter
    def mesh(self, mesh):
        self.datastructure = mesh

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear(self):
        """Clear the vertices, faces and edges of the mesh, without clearing the
        other elements in the layer.

        """
        self.clear_mesh()
        self.clear_vertices()
        self.clear_faces()
        self.clear_edges()
        self.clear_vertexnormals()
        self.clear_facenormals()
        self.clear_vertexlabels()
        self.clear_facelabels()
        self.clear_edgelabels()

    def clear_mesh(self):
        name = "{}.mesh".format(self.datastructure.name)
        guids = compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_vertices(self, keys=None):
        """Clear all previously drawn vertices.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of vertices that should be cleared.
            Default is to clear all vertices.

        """
        if not keys:
            name = '{}.vertex.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.vertex.{}'.format(self.datastructure.name, key)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_faces(self, keys=None):
        """Clear all previously drawn faces.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of faces that should be cleared.
            Default is to clear all faces.

        """
        if not keys:
            name = '{}.face.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.face.{}'.format(self.datastructure.name, key)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_edges(self, keys=None):
        """Clear all previously drawn edges.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of edges that should be cleared.
            Default is to clear all edges.

        """
        if not keys:
            name = '{}.edge.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for u, v in keys:
                name = '{}.edge.{}-{}'.format(self.datastructure.name, u, v)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_vertexlabels(self, keys=None):
        """Clear all previously drawn vertex labels.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of vertex labels that should be cleared.
            Default is to clear all vertex labels.

        """
        if not keys:
            name = '{}.vertex.label.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.vertex.label.{}'.format(self.datastructure.name, key)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_facelabels(self, keys=None):
        """Clear all previously drawn face labels.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of face labels that should be cleared.
            Default is to clear all face labels.

        """
        if not keys:
            name = '{}.face.label.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.face.label.{}'.format(self.datastructure.name, key)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_edgelabels(self, keys=None):
        """Clear all previously drawn edge labels.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of edges of which the labels should be cleared.
            Default is to clear all edge labels.

        """
        if not keys:
            name = '{}.edge.label.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for u, v in keys:
                name = '{}.edge.label.{}-{}'.format(self.datastructure.name, u, v)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_vertexnormals(self, keys=None):
        """Clear all previously drawn vertex normals.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of vertices of which the normals should be cleared.
            Default is to clear the normals of all vertices.

        """
        if not keys:
            name = '{}.vertex.normal.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.vertex.normal.{}'.format(self.datastructure.name, key)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    def clear_facenormals(self, keys=None):
        """Clear the all previously drawn face normals.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of faces of which the normals should be cleared.
            Default is to clear the normals of all faces.

        """
        if not keys:
            name = '{}.face.normal.*'.format(self.datastructure.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.face.normal.{}'.format(self.datastructure.name, key)
                guids += compas_rhino.get_objects(name=name)
        compas_rhino.delete_objects(guids)

    # ==========================================================================
    # components
    # ==========================================================================

    def draw_mesh(self, color=None, disjoint=False):
        """Draw the mesh as a consolidated RhinoMesh.

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have
        only triangular or quadrilateral faces.

        """
        key_index = self.datastructure.key_index()
        vertices = self.datastructure.get_vertices_attributes('xyz')
        faces = [[key_index[key] for key in self.datastructure.face_vertices(fkey)] for fkey in self.datastructure.faces()]
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
        name = "{}.mesh".format(self.datastructure.name)
        return compas_rhino.draw_mesh(vertices, new_faces, layer=layer, name=name, color=color, disjoint=disjoint)

    def draw_vertices(self, keys=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        keys : list
            A list of vertex keys identifying which vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : str, tuple, dict
            The color specififcation for the vertices.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all vertices, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default vertex
            color (``self.settings['color.vertex']``).
            The default is ``None``, in which case all vertices are assigned the
            default vertex color.

        Notes
        -----
        The vertices are named using the following template:
        ``"{}.vertex.{}".format(self.datastructure.name, key)``.
        This name is used afterwards to identify vertices in the Rhino model.

        """
        keys = keys or list(self.datastructure.vertices())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings.get('color.vertex'),
                                       colorformat='rgb',
                                       normalize=False)
        points = []
        for key in keys:
            points.append({
                'pos': self.datastructure.vertex_coordinates(key),
                'name': "{}.vertex.{}".format(self.datastructure.name, key),
                'color': colordict[key],
                'layer': self.datastructure.get_vertex_attribute(key, 'layer', None)
            })
        return compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)

    def draw_faces(self, keys=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        fkeys : list
            A list of face keys identifying which faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : str, tuple, dict
            The color specififcation for the faces.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all faces, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.settings['face.color']``).
            The default is ``None``, in which case all faces are assigned the
            default face color.

        Notes
        -----
        The faces are named using the following template:
        ``"{}.face.{}".format(self.datastructure.name, key)``.
        This name is used afterwards to identify faces in the Rhino model.

        """
        keys = keys or list(self.datastructure.faces())

        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings.get('color.face'),
                                       colorformat='rgb',
                                       normalize=False)
        faces = []
        for fkey in keys:
            faces.append({
                'points': self.datastructure.face_coordinates(fkey),
                'name': "{}.face.{}".format(self.datastructure.name, fkey),
                'color': colordict[fkey],
                'layer': self.datastructure.get_face_attribute(fkey, 'layer', None)
            })

        guids = compas_rhino.draw_faces(faces, layer=self.layer, clear=False, redraw=False)
        if not join_faces:
            return guids
        guid = compas_rhino.rs.JoinMeshes(guids, delete_input=True)
        compas_rhino.rs.ObjectLayer(guid, self.layer)
        compas_rhino.rs.ObjectName(guid, '{}.mesh'.format(self.datastructure.name))
        if color:
            compas_rhino.rs.ObjectColor(guid, color)
        return guid

    def draw_edges(self, keys=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        keys : list
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : str, tuple, dict
            The color specififcation for the edges.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all edges, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.settings['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        Notes
        -----
        All edges are named using the following template:
        ``"{}.edge.{}-{}".fromat(self.datastructure.name, u, v)``.
        This name is used afterwards to identify edges in the Rhino model.

        """
        keys = keys or list(self.datastructure.edges())
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.settings.get('color.edge'),
                                       colorformat='rgb',
                                       normalize=False)
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.datastructure.vertex_coordinates(u),
                'end': self.datastructure.vertex_coordinates(v),
                'color': colordict[(u, v)],
                'name': "{}.edge.{}-{}".format(self.datastructure.name, u, v),
                'layer': self.datastructure.get_edge_attribute((u, v), 'layer', None)
            })

        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    # ==========================================================================
    # normals
    # ==========================================================================

    def draw_vertexnormals(self, keys=None, color=None, scale=None):
        keys = keys or list(self.datastructure.vertices())
        scale = scale or self.settings.get('scale.normal:vertex')
        color = color or self.settings.get('color.normal:vertex')
        lines = []
        for key in keys:
            a = self.datastructure.vertex_coordinates(key)
            n = self.datastructure.vertex_normal(key)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'color': color,
                'name': "{}.vertex.normal.{}".format(self.datastructure.name, key),
                'arrow': 'end'})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_facenormals(self, keys=None, color=None, scale=1.0):
        """Draw the normals of the faces.

        Parameters
        ----------
        color : str (HEX) or tuple (RGB), optional
            The color specification of the normal vectors.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            The default value is ``None``, in which case the labels are assigned
            the default normal vector color (``self.settings['color.normal']``).

        Notes
        -----
        The face normals are named using the following template:
        ``"{}.face.normal.{}".format(self.datastructure.name, key)``.
        This name is used afterwards to identify the normals in the Rhino model.

        """
        keys = keys or list(self.datastructure.faces())
        scale = scale or self.settings.get('scale.normal:face')
        color = color or self.settings.get('color.normal:face')
        lines = []
        for key in self.datastructure.faces():
            a = self.datastructure.face_centroid(key)
            n = self.datastructure.face_normal(key)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'name': "{}.face.normal.{}".format(self.datastructure.name, key),
                'color': color,
                'arrow': 'end'})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

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
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            If a dictionary of specififcations is provided, the keys of the
            should refer to vertex keys and the values should be color
            specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned
            the default vertex color (``self.settings['color.vertex']``).

        Notes
        -----
        All labels are assigned a name using the folling template:
        ``"{}.vertex.label.{}".format(self.datastructure.name, key)``.

        """
        if text is None:
            textdict = {key: str(key) for key in self.datastructure.vertices()}
        elif isinstance(text, dict):
            textdict = text
        elif text == 'key':
            textdict = {key: str(key) for key in self.datastructure.vertices()}
        elif text == 'index':
            textdict = {key: str(index) for index, key in enumerate(self.datastructure.vertices())}
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings.get('color.vertex'),
                                       colorformat='rgb',
                                       normalize=False)
        labels = []

        for key, text in iter(textdict.items()):
            labels.append({
                'pos': self.datastructure.vertex_coordinates(key),
                'name': "{}.vertex.label.{}".format(self.datastructure.name, key),
                'color': colordict[key],
                'text': textdict[key],
                'layer': self.datastructure.get_vertex_attribute(key, 'layer', None)
            })

        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_facelabels(self, text=None, color=None):
        """Draw labels for a selection of faces.

        Parameters
        ----------
        text : dict
            A dictionary of face labels as key-text pairs.
            The default value is ``None``, in which case every face will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            If a dictionary of specififcations is provided, the keys of the
            should refer to face keys and the values should be color
            specifications in the form of strings or tuples.
            The default value is ``None``, in which case the labels are assigned
            the default face color (``self.settings['color.face']``).

        Notes
        -----
        The face labels are named using the following template:
        ``"{}.face.label.{}".format(self.datastructure.name, key)``.
        This name is used afterwards to identify faces and face labels in the Rhino model.

        """
        if text is None:
            textdict = {key: str(key) for key in self.datastructure.faces()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings.get('color.face'),
                                       colorformat='rgb',
                                       normalize=False)

        labels = []
        for key, text in iter(textdict.items()):
            labels.append({
                'pos': self.datastructure.face_center(key),
                'name': "{}.face.label.{}".format(self.datastructure.name, key),
                'color': colordict[key],
                'text': textdict[key],
                'layer': self.datastructure.get_face_attribute(key, 'layer', None)
            })
        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)

    def draw_edgelabels(self, text=None, color=None):
        """Draw labels for a selection of edges.

        Parameters
        ----------
        text : dict
            A dictionary of edge labels as key-text pairs.
            The default value is ``None``, in which case every edge will be labelled with its key.
        color : str, tuple, dict
            The color sepcification of the labels.
            String values are interpreted as hex colors (e.g. ``'#ff0000'`` for red).
            Tuples are interpreted as RGB component specifications (e.g. ``(255, 0, 0) for red``.
            Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default face
            color (``self.settings['edge.color']``).
            The default is ``None``, in which case all edges are assigned the
            default edge color.

        Notes
        -----
        All labels are assigned a name using the folling template:
        ``"{}.edge.{}".format(self.datastructure.name, key)``.

        """
        if text is None:
            textdict = {(u, v): "{}-{}".format(u, v) for u, v in self.datastructure.edges()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError

        colordict = color_to_colordict(color,
                                       textdict.keys(),
                                       default=self.settings.get('color.edge'),
                                       colorformat='rgb',
                                       normalize=False)
        labels = []

        for (u, v), text in iter(textdict.items()):
            labels.append({
                'pos': self.datastructure.edge_midpoint(u, v),
                'name': "{}.edge.label.{}-{}".format(self.datastructure.name, u, v),
                'color': colordict[(u, v)],
                'text': textdict[(u, v)],
                'layer': self.datastructure.get_edge_attribute((u, v), 'layer', None)
            })

        return compas_rhino.draw_labels(labels, layer=self.layer, clear=False, redraw=False)


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
