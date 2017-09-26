""""""

# create abstract/agnostic versions of operations and algorithms
# the outside face of networks only has a special meaning in traditional TNA form diagrams

# make general plotters and viewers

# what happens with faces during operations and algorithms on networks?
# what happens with edges during operations and algorithms on meshes?

# note: leaves are currently identified using the halfedge dict
# => after breaking the outside face of a network, leaves no longer exist


from __future__ import print_function

import json

from ast import literal_eval
from copy import deepcopy
from random import sample

from compas.utilities import pairwise
from compas.utilities import window

from compas.geometry import distance_point_point
from compas.geometry import midpoint_line
from compas.geometry import normalize_vector
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import subtract_vectors
from compas.geometry import normal_polygon
from compas.geometry import area_polygon

# from compas.datastructures.network.algorithms import network_bfs
# from compas.datastructures.network.algorithms import network_bfs2


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


# this can only be used for objects that are not serializable
class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dict):
            return {repr(key): value for key, value in iter(obj.items())}
        return json.JSONEncoder.default(self, obj)


class Graph(object):

    def __init__(self):
        self._key_to_str = False
        self._max_int_key = -1
        self._max_int_fkey = -1
        self._plotter = None
        self._viewer = None
        self.attributes = {}
        self.vertex = {}
        self.edge = {}
        self.halfedge = {}
        self.face = {}
        self.facedata = {}
        self.default_vertex_attributes = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.default_edge_attributes = {}
        self.default_face_attributes = {}

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

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

    def __str__(self):
        raise NotImplementedError

    # use other customisation methods to make working with Graph-derived
    # objects a lot easier

    # see: https://docs.python.org/3/reference/datamodel.html

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    @property
    def name(self):
        """:obj:`str` : The name of the data structure.

        Any value assigned to this property will be stored in the attribute dict
        of the data structure instance.
        """
        return self.attributes.get('name', None)

    @name.setter
    def name(self, value):
        self.attributes['name'] = value

    # the current data implementations
    # allow for the recreation of corrupt data
    # should this be the case?
    # or should the builder functions be used instead

    @property
    def data(self):
        """Return a data dict of this data structure for serialisation.
        """
        data = {'attributes'  : self.attributes,
                'dva'         : self.default_vertex_attributes,
                'dea'         : self.default_edge_attributes,
                'dfa'         : self.default_face_attributes,
                'vertex'      : {},
                'edge'        : {},
                'halfedge'    : {},
                'face'        : {},
                'facedata'    : {},
                'max_int_key' : self._max_int_key,
                'max_int_fkey': self._max_int_fkey, }

        for key in self.vertex:
            rkey = repr(key)
            data['vertex'][rkey] = self.vertex[key]

        for u in self.edge:
            ru = repr(u)
            data['edge'][ru] = {}

            for v in self.edge[u]:
                rv = repr(v)
                data['edge'][ru][rv] = self.edge[u][v]

        for u in self.halfedge:
            ru = repr(u)
            data['halfedge'][ru] = {}

            for v in self.halfedge[u]:
                rv = repr(v)
                data['halfedge'][ru][rv] = repr(self.halfedge[u][v])

        for fkey in self.face:
            rfkey = repr(fkey)
            data['face'][rfkey] = [repr(key) for key in self.face[fkey]]

        for fkey in self.facedata:
            rfkey = repr(fkey)
            data['facedata'][rfkey] = self.facedata[fkey]

        return data

    @data.setter
    def data(self, data):
        attributes   = data.get('attributes') or {}
        dva          = data.get('dva') or {}
        dfa          = data.get('dfa') or {}
        dea          = data.get('dea') or {}
        vertex       = data.get('vertex') or {}
        halfedge     = data.get('halfedge') or {}
        face         = data.get('face') or {}
        facedata     = data.get('facedata') or {}
        edge         = data.get('edge') or {}
        max_int_key  = data.get('max_int_key', -1)
        max_int_fkey = data.get('max_int_fkey', -1)

        self.attributes.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_face_attributes.update(dfa)
        self.default_edge_attributes.update(dea)

        # add the vertices

        self.vertex = {literal_eval(key): attr for key, attr in iter(vertex.items())}

        # add the edges

        self.edge = {}

        for u, nbrs in iter(edge.items()):
            nbrs = nbrs or {}

            u = literal_eval(u)

            self.edge[u] = {}

            for v, attr in iter(nbrs.items()):
                attr = attr or {}

                v = literal_eval(v)

                self.edge[u][v] = attr

        # add the halfedges

        self.halfedge = {}

        for u, nbrs in iter(halfedge.items()):
            nbrs = nbrs or {}

            u = literal_eval(u)

            self.halfedge[u] = {}

            for v, fkey in iter(nbrs.items()):
                v = literal_eval(v)
                fkey = literal_eval(fkey)

                self.halfedge[u][v] = fkey

        # add the faces

        self.face = {}
        self.facedata = {}

        for fkey, vertices in iter(face.items()):
            attr = facedata.get(fkey) or {}
            fkey = literal_eval(fkey)
            vertices = [literal_eval(key) for key in vertices]

            self.face[fkey] = vertices
            self.facedata[fkey] = attr

        # set the counts

        self._max_int_key = max_int_key
        self._max_int_fkey = max_int_fkey

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

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

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

    @classmethod
    def from_obj(cls, filepath):
        """Create a data structure from the data in an obj file."""
        raise NotImplementedError

    @classmethod
    def from_dxf(cls, filepath, **kwargs):
        raise NotImplementedError

    @classmethod
    def from_stl(cls, filepath, **kwargs):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

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

    def to_obj(self):
        raise NotImplementedError

    def to_points(self, axes='xyz'):
        return [self.vertex_coordinates(key, axes) for key in self.vertices()]

    def to_lines(self, axes='xyz'):
        return [self.edge_coordinates(u, v, axes=axes) for u, v in self.edges()]

    def to_faces(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def _get_vertexkey(self, key):
        if key is None:
            key = self._max_int_key = self._max_int_key + 1
        else:
            try:
                i = int(key)
            except (ValueError, TypeError):
                pass
            else:
                if i > self._max_int_key:
                    self._max_int_key = i
        if self._key_to_str:
            return str(key)
        return key

    def _get_facekey(self, fkey):
        if fkey is None:
            fkey = self._max_int_fkey = self._max_int_fkey + 1
        else:
            try:
                i = int(fkey)
            except (ValueError, TypeError):
                pass
            else:
                if i > self._max_int_fkey:
                    self._max_int_fkey = i
        return fkey

    def copy(self):
        cls = type(self)
        return cls.from_data(deepcopy(self.data))

    def clear(self):
        del self.vertex
        del self.edge
        del self.halfedge
        del self.face
        del self.facedata
        self.vertex   = {}
        self.edge     = {}
        self.halfedge = {}
        self.face     = {}
        self.facedata = {}
        self._max_int_key = -1
        self._max_int_fkey = -1

    def clear_vertexdict(self):
        del self.vertex
        self.vertex = {}
        self._max_int_key = -1

    def clear_facedict(self):
        del self.face
        del self.facedata
        self.face = {}
        self.facedata = {}
        self._max_int_fkey = -1

    def clear_edgedict(self):
        del self.edge
        self.edge = {}

    def clear_halfedgedict(self):
        del self.halfedge
        self.halfedge = {}

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

    def uv_index(self):
        return {(u, v): index for index, (u, v) in enumerate(self.edges())}

    def index_uv(self):
        return dict(enumerate(self.edges()))

    def get_any_vertex(self):
        return self.get_any_vertices(1)[0]

    def get_any_vertices(self, n, exclude_leaves=False):
        if exclude_leaves:
            vertices = set(self.vertices()) - set(self.leaves())
        else:
            vertices = self.vertices()
        return sample(list(vertices), n)

    def get_any_edge(self):
        pass

    def get_any_face(self):
        return next(self.faces())

    def get_any_face_vertex(self, fkey):
        return self.face_vertices(fkey)[0]

    def min_vertex_attribute_value(self, name):
        pass

    def max_vertex_attribute_value(self, name):
        pass

    def vertex_name(self, key):
        return '{0}.vertex.{1}'.format(self.name, key)

    def edge_name(self, u, v):
        return '{0}.edge.{1}-{2}'.format(self.name, u, v)

    def face_name(self, fkey):
        return '{0}.face.{1}'.format(self.name, fkey)

    def vertex_label_name(self, key):
        return '{0}.vertex.label.{1}'.format(self.name, key)

    def edge_label_name(self, u, v):
        return '{0}.edge.label.{1}-{2}'.format(self.name, u, v)

    def face_label_name(self, fkey):
        return '{0}.face.label.{1}'.format(self.name, fkey)

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        raise NotImplementedError

    def add_vertices(self):
        raise NotImplementedError

    def add_edge(self):
        raise NotImplementedError

    def add_edges(self):
        raise NotImplementedError

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        raise NotImplementedError

    def add_faces(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------

    def number_of_vertices(self):
        return len(list(self.vertices()))

    def number_of_edges(self):
        return len(list(self.edges()))

    def number_of_faces(self):
        return len(list(self.faces()))

    def number_of_halfedges(self):
        return len(list(self.halfedges()))

    def is_valid(self):
        raise NotImplementedError

    def is_regular(self):
        raise NotImplementedError

    def is_connected(self):
        """Return True if for every two vertices a path exists connecting them."""
        if not self.vertex:
            return False

        root = self.get_any_vertex()
        nodes = network_bfs2(self.halfedge, root)

        return len(nodes) == self.number_of_vertices()

    def is_manifold(self):
        raise NotImplementedError

    def is_orientable(self):
        raise NotImplementedError

    def is_closed(self):
        raise NotImplementedError

    def is_trimesh(self):
        raise NotImplementedError

    def is_quadmesh(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        """Return an iterator for the vertices and their attributes (optional).

        Parameters:
            data (bool): Return key, data pairs, defaults to False.

        Returns:
            iter: An iterator of vertex keys, if data is False.
            iter: An iterator of key, data pairs, if data is True.
        """
        if data:
            return iter(self.vertex.items())
        return iter(self.vertex)

    def edges(self, data=False):
        """Return an iterator for the edges and their attributes (optional)."""
        for u, nbrs in iter(self.edge.items()):
            for v, attr in iter(nbrs.items()):
                if data:
                    yield u, v, attr
                else:
                    yield u, v

    def faces(self, data=False):
        """Return an iterator for the faces and their attributes (optional)."""
        for fkey in self.face:
            if data:
                yield fkey, self.facedata.setdefault(fkey, self.default_face_attributes.copy())
            else:
                yield fkey

    def halfedges(self):
        edges = set()
        for fkey in self.faces():
            for u, v in self.face_halfedges(fkey):
                if (u, v) in edges or (v, u) in edges:
                    continue
                edges.add((u, v))
        return list(edges)

    def wireframe(self):
        return self.halfedges()

    # --------------------------------------------------------------------------
    # additional accessors
    # --------------------------------------------------------------------------

    def indexed_edges(self):
        k_i = self.key_index()
        return [(k_i[u], k_i[v]) for u, v in self.edges()]

    def indexed_face_vertices(self):
        k_i = self.key_index()
        return [[k_i[key] for key in self.face_vertices(fkey)] for fkey in self.faces()]

    # --------------------------------------------------------------------------
    # default attributes
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
    # vertex attributes
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
    # edge attributes
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
    # face attributes
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
    # vertex topology
    # --------------------------------------------------------------------------

    def has_vertex(self, key):
        return key in self.vertex

    def is_vertex_leaf(self, key):
        return self.vertex_degree(key) == 1

    def leaves(self):
        return [key for key in self.vertices() if self.is_vertex_leaf(key)]

    def is_vertex_orphan(self, key):
        return not self.vertex_degree(key) > 0

    def is_vertex_connected(self, key):
        return self.vertex_degree(key) > 0

    def is_vertex_on_boundary(self, key):
        raise NotImplementedError

    def is_vertex_extraordinary(self, key, mtype=None):
        raise NotImplementedError

    def vertex_neighbours(self, key, ordered=False):
        """Return the neighbours of a vertex."""

        temp = list(self.halfedge[key])

        # temp = [nbr for nbr in self.halfedge[key] if self.has_edge(key, nbr, directed=False)]

        if not ordered:
            return temp

        if len(temp) == 1:
            return temp

        start = temp[0]
        for nbr in temp:
            if self.halfedge[key][nbr] is None:
                start = nbr
                break

        fkey = self.halfedge[start][key]
        nbrs = [start]
        count = 1000

        while count:
            count -= 1
            nbr = self.face_vertex_descendant(fkey, key)
            fkey = self.halfedge[nbr][key]

            if nbr == start:
                break

            nbrs.append(nbr)

            if fkey is None:
                break

        return nbrs

    def vertex_neighbourhood(self, key, ring=1):
        """Return the vertices in the neighbourhood of a vertex."""
        nbrs = set(self.vertex_neighbours(key))

        i = 1
        while True:
            if i == ring:
                break

            temp = []
            for key in nbrs:
                temp += self.vertex_neighbours(key)

            nbrs.update(temp)

            i += 1

        return nbrs

    def vertex_neighbours_out(self, key):
        """Return the outgoing neighbours of a vertex."""
        return list(self.edge[key])

    def vertex_neighbours_in(self, key):
        """Return the incoming neighbours of a vertex."""
        return list(set(self.halfedge[key]) - set(self.edge[key]))

    def vertex_degree(self, key):
        """Return the number of neighbours of a vertex."""
        return len(self.vertex_neighbours(key))

    def vertex_degree_out(self, key):
        """Return the number of outgoing neighbours of a vertex."""
        return len(self.vertex_neighbours_out(key))

    def vertex_degree_in(self, key):
        """Return the numer of incoming neighbours of a vertex."""
        return len(self.vertex_neighbours_in(key))

    def vertex_connected_edges(self, key):
        """Return the edges connected to a vertex."""
        edges = []
        for nbr in self.vertex_neighbours(key):
            if nbr in self.edge[key]:
                edges.append((key, nbr))
            else:
                edges.append((nbr, key))
        return edges

    def vertex_faces(self, key, ordered=False, include_None=False):
        """Return the faces connected to a vertex."""
        if not ordered:
            faces = list(self.halfedge[key].values())

        else:
            nbrs = self.vertex_neighbours(key, ordered=True)

            # if len(nbrs) == 1:
            #     nbr = nbrs[0]
            #     faces = [self.halfedge[key][nbr], self.halfedge[nbr][key]]

            # else:
            faces = [self.halfedge[key][n] for n in nbrs]

        if include_None:
            return faces

        return [fkey for fkey in faces if fkey is not None]

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    def has_edge(self, u, v, directed=True):
        if directed:
            return u in self.edge and v in self.edge[u]
        else:
            return (u in self.edge and v in self.edge[u]) or (v in self.edge and u in self.edge[v])

    def edge_faces(self, u, v):
        return [self.halfedge[u][v], self.halfedge[v][u]]

    def edge_connected_edges(self, u, v):
        edges = []
        for nbr in self.vertex_neighbours(u):
            if nbr in self.edge[u]:
                edges.append((u, nbr))
            else:
                edges.append((nbr, u))
        for nbr in self.vertex_neighbours(v):
            if nbr in self.edge[v]:
                edges.append((v, nbr))
            else:
                edges.append((nbr, v))
        return edges

    def is_edge_naked(self, u, v):
        return self.halfedge[u][v] is None or self.halfedge[v][u] is None

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    def face_vertices(self, fkey, ordered=True):
        """Return the vertices of the face."""
        return list(self.face[fkey])

    def face_halfedges(self, fkey):
        """Return the halfedges of a face."""
        vertices = self.face_vertices(fkey)
        return pairwise(vertices + vertices[0:1])

    def face_edges(self, fkey):
        """Return the edges corresponding to the halfedges of a face."""
        edges = []
        for u, v in self.face_halfedges(fkey):
            if v in self.edge[u]:
                edges.append((u, v))
            else:
                edges.append((v, u))
        return edges

    def face_corners(self, fkey):
        vertices = self.face_vertices(fkey)
        return window(vertices + vertices[0:2], 3)

    def face_neighbours(self, fkey):
        """Return the neighbours of a face across its edges."""
        nbrs = []
        for u, v in self.face_halfedges(fkey):
            nbr = self.halfedge[v][u]
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def face_vertex_neighbours(self, fkey):
        """Return the neighbours of a face across its corners."""
        nbrs = []
        for u, v in self.face_halfedges(fkey):
            nbr = self.halfedge[v][u]
            if nbr is not None:
                w = self.face_vertex_descendant(fkey, u)
                nbrs.append(self.halfedge[w][u])
        return nbrs

    def face_neighbourhood(self, fkey):
        """Return the neighbours of a face across both edges and corners."""
        nbrs = []
        for u, v in self.face_halfedges(fkey):
            nbr = self.halfedge[v][u]
            if nbr is not None:
                nbrs.append(nbr)
                w = self.face_vertex_descendant(fkey, u)
                nbrs.append(self.halfedge[w][u])
        return nbrs

    def face_vertex_ancestor(self, fkey, key):
        """Return the vertex before the specified vertex in a specific face."""
        i = self.face[fkey].index(key)
        return self.face[fkey][i - 1]

    def face_vertex_descendant(self, fkey, key):
        """Return the vertex after the specified vertex in a specific face."""
        if self.face[fkey][-1] == key:
            return self.face[fkey][0]
        i = self.face[fkey].index(key)
        return self.face[fkey][i + 1]

    def face_adjacency(self):
        # this function does not actually use any of the topological information
        # provided by the halfedges
        # it is used for unifying face cycles
        # so the premise is that halfedge data is not valid/reliable
        from scipy.spatial import cKDTree

        fkey_index = {fkey: index for index, fkey in self.faces_enum()}
        index_fkey = dict(self.faces_enum())
        points = [self.face_centroid(fkey) for fkey in self.faces()]

        tree = cKDTree(points)

        _, closest = tree.query(points, k=10, n_jobs=-1)

        adjacency = {}
        for fkey in self.face:
            nbrs  = []
            index = fkey_index[fkey]
            nnbrs = closest[index]
            found = set()
            for u, v in iter(self.face[fkey].items()):
                for index in nnbrs:
                    nbr = index_fkey[index]
                    if nbr == fkey:
                        continue
                    if nbr in found:
                        continue
                    if v in self.face[nbr] and u == self.face[nbr][v]:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break
                    if u in self.face[nbr] and v == self.face[nbr][u]:
                        nbrs.append(nbr)
                        found.add(nbr)
                        break
            adjacency[fkey] = nbrs
        return adjacency

    # def face_tree(self, root, algo=network_bfs):
    #     return algo(self.face_adjacency(), root)

    def face_adjacency_edge(self, f1, f2):
        for u, v in self.face_halfedges(f1):
            if self.halfedge[v][u] == f2:
                if v in self.edge[u]:
                    return u, v
                return v, u

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, key, axes='xyz'):
        """Return the coordinates of a vertex."""
        return [self.vertex[key][axis] for axis in axes]

    def vertex_area(self, key):
        """Return the tributary area of a vertex."""
        area = 0

        p0 = self.vertex_coordinates(key)

        for nbr in self.halfedge[key]:
            p1 = self.vertex_coordinates(nbr)
            v1 = subtract_vectors(p1, p0)

            fkey = self.halfedge[key][nbr]
            if fkey is not None:
                p2 = self.face_centroid(fkey)
                v2 = subtract_vectors(p2, p0)
                area += length_vector(cross_vectors(v1, v2))

            fkey = self.halfedge[nbr][key]
            if fkey is not None:
                p3 = self.face_centroid(fkey)
                v3 = subtract_vectors(p3, p0)
                area += length_vector(cross_vectors(v1, v3))

        return 0.25 * area

    def vertex_laplacian(self, key):
        """Return the vector from the vertex to the centroid of its 1-ring neighbourhood."""
        c = centroid_points([self.vertex_coordinates(nbr) for nbr in self.neighbours(key)])
        p = self.vertex_coordinates(key)
        return subtract_vectors(c, p)

    def vertex_neighbourhood_centroid(self, key):
        return centroid_points([self.vertex_coordinates(nbr) for nbr in self.neighbours(key)])

    # centroid_points is in fact an averaging of vectors
    # name it as such
    def vertex_normal(self, key):
        """Return the normal vector at the vertex as the weighted average of the
        normals of the neighbouring faces."""
        vectors = [self.face_normal(fkey) for fkey in self.vertex_faces(key) if fkey is not None]
        return normalize_vector(centroid_points(vectors))

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

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

    # --------------------------------------------------------------------------
    # face geometry
    # --------------------------------------------------------------------------

    def face_coordinates(self, fkey, axes='xyz'):
        """Return the coordinates of the vertices of a face."""
        return [self.vertex_coordinates(key, axes=axes) for key in self.face_vertices(fkey)]

    def face_normal(self, fkey, normalised=True):
        """Return the normal of a face."""
        return normal_polygon(self.face_coordinates(fkey), normalised=normalised)

    def face_centroid(self, fkey):
        """Return the location of the centroid of a face."""
        return centroid_points(self.face_coordinates(fkey))

    def face_center(self, fkey):
        """Return the location of the center of mass of a face."""
        return center_of_mass_polygon(self.face_coordinates(fkey))

    def face_area(self, fkey):
        """Return the area of a face."""
        return area_polygon(self.face_coordinates(fkey))

    # --------------------------------------------------------------------------
    # boundary
    # --------------------------------------------------------------------------

    def vertices_on_boundary(self):
        raise NotImplementedError

    def edges_on_boundary(self):
        raise NotImplementedError

    def faces_on_boundary(self):
        raise NotImplementedError

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

    def faces_where(self, conditions):
        raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
