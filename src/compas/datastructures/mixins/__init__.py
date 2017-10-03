
# try:
#     import cjson as json
# except ImportError:
import json

from copy import deepcopy
from random import sample

from compas.geometry import distance_point_point
from compas.geometry import midpoint_line
from compas.geometry import normalize_vector
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'VertexAttributesMixin',
    'VertexHelpersMixin',
    'VertexCoordinatesDescriptorsMixin',
    'EdgeAttributesMixin',
    'EdgeHelpersMixin',
    'EdgeGeometryMixin'
    'FaceAttributesMixin',
    'FaceHelpersMixin',
    'FactoryMixin',
    'ConversionMixin',
    'MagicMixin',
]


# ==============================================================================
# Vertex Mixins
# ==============================================================================
# ==============================================================================
# ==============================================================================


class VertexAttributesMixin(object):

    # --------------------------------------------------------------------------
    # defaults
    # --------------------------------------------------------------------------

    def update_default_vertex_attributes(self, attr_dict=None, **kwattr):
        """"""
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_vertex_attributes.update(attr_dict)
        for key in self.vertices():
            attr = deepcopy(attr_dict)
            attr.update(self.vertex[key])
            self.vertex[key] = attr

    # --------------------------------------------------------------------------
    # get/set
    # --------------------------------------------------------------------------

    def set_vertex_attribute(self, key, name, value):
        self.vertex[key][name] = value

    def set_vertex_attributes(self, key, attr_dict=None, **kwattr):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.vertex[key].update(attr_dict)

    def set_vertices_attribute(self, name, value, keys=None):
        if not keys:
            for key, attr in self.vertices(True):
                attr[name] = value
        else:
            for key in keys:
                self.vertex[key][name] = value

    def set_vertices_attributes(self, keys=None, attr_dict=None, **kwattr):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        if not keys:
            for key, attr in self.vertices(True):
                attr.update(attr_dict)
        else:
            for key in keys:
                self.vertex[key].update(attr_dict)

    def get_vertex_attribute(self, key, name, value=None):
        return self.vertex[key].get(name, value)

    def get_vertex_attributes(self, key, names, values=None):
        if not values:
            values = [None] * len(names)
        return [self.vertex[key].get(name, value) for name, value in zip(names, values)]

    def get_vertices_attribute(self, name, value=None, keys=None):
        if not keys:
            return [attr.get(name, value) for key, attr in self.vertices(True)]
        return [self.vertex[key].get(name, value) for key in keys]

    def get_vertices_attributes(self, names, values=None, keys=None):
        if not values:
            values = [None] * len(names)
        temp = list(zip(names, values))
        if not keys:
            return [[attr.get(name, value) for name, value in temp] for key, attr in self.vertices(True)]
        return [[self.vertex[key].get(name, value) for name, value in temp] for key in keys]

    # --------------------------------------------------------------------------
    # selections
    # --------------------------------------------------------------------------

    def vertices_where(self, conditions):
        """Get vertices for which a certain condition or set of conditions is ``True``.

        Parameters:
            where (dict): A set of conditions in the form of key-value pairs.
                The keys should be attribute names. The values can be attribute
                values or ranges of attribute values in the form of min/max pairs.

        Returns:
            list: A list of vertex keys that satisfy the condition(s).

        """
        keys = []
        for key, attr in self.vertices(True):
            is_match = True
            for name, value in conditions.items():
                if name not in attr:
                    is_match = False
                    break
                if isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if attr[name] < minval or attr[name] > maxval:
                        is_match = False
                        break
                else:
                    if value != attr[name]:
                        is_match = False
                        break
            if is_match:
                keys.append(key)
        return keys

    # --------------------------------------------------------------------------
    # computed
    # --------------------------------------------------------------------------

    def min_vertex_attribute_value(self, name):
        pass

    def max_vertex_attribute_value(self, name):
        pass


class VertexHelpersMixin(object):

    def key_index(self):
        """Returns a *key-to-index* map.

        This function is primarily intended for working with arrays.
        For example::

            >>> import compas
            >>> import numpy as np
            >>> mesh = Mesh.from_obj(compas.get_data('faces.obj'))
            >>> xyz = np.array(mesh.vertex_coordinates(xyz='xyz'), dtype=float)
            >>> k2i = mesh.key_index()

            # do stuff to the coordinates
            # for example, apply smoothing
            # then update the vertex coordinates in the data structure

            >>> for key in mesh:
            ...     index = k2i[key]
            ...     mesh.vertex[key]['x'] = xyz[index, 0]
            ...     mesh.vertex[key]['y'] = xyz[index, 1]
            ...     mesh.vertex[key]['z'] = xyz[index, 2]

        >>> mesh = Mesh()
        >>> mesh.add_vertex()
        '0'
        >>> k_i = mesh.key_index()
        >>> k_i['0']
        0
        """
        return {key: index for index, key in enumerate(self.vertices())}

    def index_key(self):
        """Returns an *index-to-key* map.

        This function is primarily intended for working with arrays.
        For example::

            >>>

        >>> mesh = Mesh()
        >>> mesh.add_vertex()
        '0'
        >>> i_k = mesh.index_key()
        >>> i_k[0]
        '0'
        """
        return dict(enumerate(self.vertices()))

    def get_any_vertex(self):
        return self.get_any_vertices(1)[0]

    def get_any_vertices(self, n, exclude_leaves=False):
        if exclude_leaves:
            vertices = set(self.vertices()) - set(self.leaves())
        else:
            vertices = self.vertices()
        return sample(list(vertices), n)

    def vertex_name(self, key):
        return '{0}.vertex.{1}'.format(self.name, key)

    def vertex_label_name(self, key):
        return '{0}.vertex.label.{1}'.format(self.name, key)


class VertexCoordinatesDescriptorsMixin(object):

    @property
    def xyz(self):
        """:obj:`list` : The `xyz` coordinates of the vertices."""
        return [(a['x'], a['y'], a['z']) for k, a in self.vertices(True)]

    @property
    def xy(self):
        """:obj:`list` : The `xy` coordinates of the vertices."""
        return [(a['x'], a['y']) for k, a in self.vertices(True)]

    @property
    def x(self):
        """:obj:`list` : The `x` coordinates of the vertices."""
        return [a['x'] for k, a in self.vertices(True)]

    @property
    def y(self):
        """:obj:`list` : The `y` coordinates of the vertices."""
        return [a['y'] for k, a in self.vertices(True)]

    @property
    def z(self):
        """:obj:`list` : The `z` coordinates of the vertices."""
        return [a['z'] for k, a in self.vertices(True)]


# ==============================================================================
# Edge Mixins
# ==============================================================================
# ==============================================================================
# ==============================================================================


class EdgeAttributesMixin(object):

    # --------------------------------------------------------------------------
    # default
    # --------------------------------------------------------------------------

    def update_default_edge_attributes(self, attr_dict=None, **kwattr):
        """"""
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_edge_attributes.update(attr_dict)
        for u, v in self.edges():
            attr = deepcopy(attr_dict)
            attr.update(self.edge[u][v])
            self.edge[u][v] = attr

    # --------------------------------------------------------------------------
    # get/set
    # --------------------------------------------------------------------------

    def set_edge_attribute(self, u, v, name, value):
        self.edge[u][v][name] = value

    def set_edge_attributes(self, u, v, attr_dict=None, **kwattr):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.edge[u][v].update(attr_dict)

    def set_edges_attribute(self, name, value, keys=None):
        if not keys:
            for u, v, attr in self.edges(True):
                attr[name] = value
        else:
            for u, v in keys:
                self.edge[u][v][name] = value

    def set_edges_attributes(self, keys=None, attr_dict=None, **kwattr):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        if not keys:
            for u, v, attr in self.edges(True):
                attr.update(attr_dict)
        else:
            for u, v in keys:
                self.edge[u][v].update(attr_dict)

    def get_edge_attribute(self, u, v, name, value=None):
        if u in self.edge[v]:
            return self.edge[v][u].get(name, value)
        return self.edge[u][v].get(name, value)

    def get_edge_attributes(self, u, v, names, values=None):
        if not names:
            values = [None] * len(names)
        if v in self.edge[u]:
            return [self.edge[u][v].get(name, value) for name, value in zip(names, values)]
        return [self.edge[v][u].get(name, value) for name, value in zip(names, values)]

    def get_edges_attribute(self, name, value=None, keys=None):
        if not keys:
            return [attr.get(name, value) for u, v, attr in self.edges(True)]
        return [self.edge[u][v].get(name, value) for u, v in keys]

    def get_edges_attributes(self, names, values=None, keys=None):
        if not values:
            values = [None] * len(names)
        temp = list(zip(names, values))
        if not keys:
            return [[attr.get(name, value) for name, value in temp] for u, v, attr in self.edges(True)]
        return [[self.edge[u][v].get(name, value) for name, value in temp] for u, v in keys]

    # --------------------------------------------------------------------------
    # selections
    # --------------------------------------------------------------------------

    def edges_where(self, conditions):
        """Get edges for which a certain condition or set of conditions is ``True``.

        Parameters:
            where (dict) : A set of conditions in the form of key-value pairs.
                The keys should be attribute names. The values can be attribute
                values or ranges of attribute values in the form of min/max pairs.

        Returns:
            list: A list of edge keys that satisfy the condition(s).

        """
        keys = []
        for u, v, attr in self.edges(True):
            is_match = True
            for name, value in conditions.items():
                if name not in attr:
                    is_match = False
                    break
                if isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if attr[name] < minval or attr[name] > maxval:
                        is_match = False
                        break
                else:
                    if value != attr[name]:
                        is_match = False
                        break
            if is_match:
                keys.append((u, v))
        return keys

    # --------------------------------------------------------------------------
    # computed
    # --------------------------------------------------------------------------


class EdgeHelpersMixin(object):

    def uv_index(self):
        return {(u, v): index for index, (u, v) in enumerate(self.edges())}

    def index_uv(self):
        return dict(enumerate(self.edges()))

    def get_any_edge(self):
        pass

    def edge_name(self, u, v):
        return '{0}.edge.{1}-{2}'.format(self.name, u, v)

    def edge_label_name(self, u, v):
        return '{0}.edge.label.{1}-{2}'.format(self.name, u, v)


class EdgeGeometryMixin(object):

    def edge_coordinates(self, u, v, axes='xyz'):
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    def edge_length(self, u, v):
        """Return the length of an edge."""
        a, b = self.edge_coordinates(u, v)
        return distance_point_point(a, b)

    def edge_vector(self, u, v):
        """Return the vector of an edge."""
        a, b = self.edge_coordinates(u, v)
        ab = subtract_vectors(b, a)
        return ab

    def edge_point(self, u, v, t=0.5):
        """Return the location of a point along an edge."""
        a, b = self.edge_coordinates(u, v)
        ab = subtract_vectors(b, a)
        return add_vectors(a, scale_vector(ab, t))

    def edge_midpoint(self, u, v):
        """Return the location of the midpoint of an edge."""
        a, b = self.edge_coordinates(u, v)
        return midpoint_line((a, b))

    def edge_direction(self, u, v):
        """Return the direction vector of an edge."""
        return normalize_vector(self.edge_vector(u, v))


# ==============================================================================
# Face Mixins
# ==============================================================================
# ==============================================================================
# ==============================================================================


class FaceAttributesMixin(object):

    # --------------------------------------------------------------------------
    # default
    # --------------------------------------------------------------------------

    def update_default_face_attributes(self, attr_dict=None, **kwattr):
        """"""
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_face_attributes.update(attr_dict)
        for fkey in self.faces():
            attr = deepcopy(attr_dict)
            attr.update(self.facedata[fkey])
            self.facedata[fkey] = attr

    # --------------------------------------------------------------------------
    # get/set
    # --------------------------------------------------------------------------

    def set_face_attribute(self, fkey, name, value):
        if fkey not in self.facedata:
            self.facedata[fkey] = self.default_face_attributes.copy()
        self.facedata[fkey][name] = value

    def set_face_attributes(self, fkey, attr_dict=None, **kwattr):
        attr_dict = attr_dict or {}
        attr_dict.update(kwattr)
        if fkey not in self.facedata:
            self.facedata[fkey] = self.default_face_attributes.copy()
        self.facedata[fkey].update(attr_dict)

    def set_faces_attribute(self, name, value, fkeys=None):
        if not fkeys:
            for fkey, attr in self.faces_iter(True):
                attr[name] = value
        else:
            for fkey in fkeys:
                if fkey not in self.facedata:
                    self.facedata[fkey] = self.default_face_attributes.copy()
                self.facedata[fkey][name] = value

    def set_faces_attributes(self, fkeys=None, attr_dict=None, **kwattr):
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        if not fkeys:
            for fkey, attr in self.faces(True):
                attr.update(attr_dict)
        else:
            for fkey in fkeys:
                if fkey not in self.facedata:
                    self.facedata[fkey] = self.default_face_attributes.copy()
                self.facedata[fkey].update(attr_dict)

    def get_face_attribute(self, fkey, name, value=None):
        if not self.facedata:
            return value
        if fkey not in self.facedata:
            return value
        return self.facedata[fkey].get(name, value)

    def get_face_attributes(self, fkey, names, values=None):
        if not values:
            values = [None] * len(names)
        if not self.facedata:
            return values
        if fkey not in self.facedata:
            return values
        return [self.facedata[fkey].get(name, value) for name, value in zip(names, values)]

    def get_faces_attribute(self, name, value=None, fkeys=None):
        if not fkeys:
            if not self.facedata:
                return [value for fkey in self.face]
            return [self.get_face_attribute(fkey, name, value) for fkey in self.face]
        if not self.facedata:
            return [value for fkey in fkeys]
        return [self.get_face_attribute(fkey, name, value) for fkey in fkeys]

    def get_faces_attributes(self, names, values=None, fkeys=None):
        if not values:
            values = [None] * len(names)
        temp = list(zip(names, values))
        if not fkeys:
            if not self.facedata:
                return [[value for name, value in temp] for fkey in self.face]
            return [[self.get_face_attribute(fkey, name, value) for name, value in temp] for fkey in self.face]
        if not self.facedata:
            return [[value for name, value in temp] for fkey in fkeys]
        return [[self.get_face_attribute(fkey, name, value) for name, value in temp] for fkey in fkeys]

    # --------------------------------------------------------------------------
    # selections
    # --------------------------------------------------------------------------

    def faces_where(self, conditions):
        raise NotImplementedError


class FaceHelpersMixin(object):

    def get_any_face(self):
        return next(self.faces())

    def get_any_face_vertex(self, fkey):
        return self.face_vertices(fkey)[0]

    def face_name(self, fkey):
        return '{0}.face.{1}'.format(self.name, fkey)

    def face_label_name(self, fkey):
        return '{0}.face.label.{1}'.format(self.name, fkey)


# ==============================================================================
# Other Mixins
# ==============================================================================
# ==============================================================================
# ==============================================================================


class FactoryMixin(object):

    @classmethod
    def from_data(cls, data):
        """Construct a mesh from actual mesh data.

        This function should be used in combination with the data obtained from
        ``mesh.data``.

        Parameters:
            data (dict): The data dictionary.

        Returns:
            Mesh: A ``Mesh`` of class ``cls``.

        >>> data = m1.to_data()
        >>> m2 = Mesh.from_data(data)

        """
        graph = cls()
        graph.data = data
        return graph

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        graph = cls()
        graph.data = data
        return graph


class ConversionMixin(object):

    def to_data(self):
        """Return the data dict that represents the mesh, and from which it can
        be reconstructed."""
        return self.data

    def to_json(self, filepath=None):
        """Serialize the mesh data to a JSON file.

        Parameters:
            filepath (str): Path to the file to write.

        Returns:
            None
        """
        if filepath is None:
            return json.dumps(self.data)
        else:
            with open(filepath, 'w+') as fp:
                json.dump(self.data, fp)


class MagicMixin(object):

    def __contains__(self, key):
        """Verify if the mesh contains a specific vertex.

        Parameters:
            key (str) : The identifier ('key') of the vertex.

        >>> mesh = Mesh()
        >>> mesh.add_vertex()
        '0'
        >>> '0' in mesh
        True
        >>> '1' in mesh
        False
        """
        return key in self.vertex

    def __len__(self):
        """Defines the length of the mesh as the number of vertices in the mesh.

        >>> len(mesh) == len(mesh.vertex) == len(mesh.vertex.keys())
        True
        """
        return len(self.vertex)

    def __iter__(self):
        """Defines mesh iteration as iteration over the vertex keys.

        >>> mesh = Mesh()
        >>> mesh.add_vertex()
        >>> mesh.add_vertex()
        >>> for key in mesh: print(key)
        '0'
        '1'
        """
        return iter(self.vertex)

    def __getitem__(self, key):
        """Defines the behaviour of the mesh when it is treated as a container and
        one of its items is accessed directly. Because of this implementation,
        the mesh will respond by returning the vertex attributes corresponding to
        the requested vertex key.

        >>> mesh = Mesh()
        >>> mesh.add_vertex(x=0, y=0, z=0)
        '0'
        >>> mesh.vertex['0']
        {'x': 0, 'y': 0, 'z': 0}
        >>> mesh['0']
        {'x': 0, 'y': 0, 'z': 0}
        """
        return self.vertex[key]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
