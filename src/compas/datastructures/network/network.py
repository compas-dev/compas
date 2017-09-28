from __future__ import print_function

from copy import deepcopy
from ast import literal_eval

import compas

from compas.files import OBJ

from compas.utilities import geometric_key
from compas.utilities import pairwise
from compas.utilities import window

from compas.geometry import normalize_vector
from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import subtract_vectors
from compas.geometry import normal_polygon
from compas.geometry import area_polygon

from compas.datastructures import Datastructure

from compas.datastructures.mixins import VertexAttributesMixin
from compas.datastructures.mixins import VertexHelpersMixin
from compas.datastructures.mixins import VertexCoordinatesDescriptorsMixin

from compas.datastructures.mixins import EdgeAttributesMixin
from compas.datastructures.mixins import EdgeHelpersMixin
from compas.datastructures.mixins import EdgeGeometryMixin

from compas.datastructures.mixins import FaceAttributesMixin
from compas.datastructures.mixins import FaceHelpersMixin

from compas.datastructures.mixins import FactoryMixin
from compas.datastructures.mixins import ConversionMixin
from compas.datastructures.mixins import MagicMixin

from compas.datastructures.network.algorithms import network_bfs2


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


__all__ = ['Network', 'FaceNetwork', ]


class Network(MagicMixin,
              ConversionMixin,
              FactoryMixin,
              EdgeGeometryMixin,
              EdgeHelpersMixin,
              EdgeAttributesMixin,
              VertexCoordinatesDescriptorsMixin,
              VertexHelpersMixin,
              VertexAttributesMixin,
              Datastructure):
    """Definition of a network object.

    The ``Network`` class is implemented as a directed edge graph.

    Attributes
    ----------
    vertex : dict
        The vertex dictionary. Each key in the vertex dictionary
        represents a vertex of the network and maps to a dictionary of
        vertex attributes.
    edge : dict of dict
        The edge dictionary. Each key in the edge dictionary
        corresponds to a key in the vertex dictionary, and maps to a dictionary
        with connected vertices. In the latter, the keys are again references
        to items in the vertex dictionary, and the values are dictionaries
        of edge attributes.
    halfedge : dict of dict
        A half-edge dictionary, which keeps track of
        undirected adjacencies. If the network is planar, the halfedges point
        at entries in the face dictionary.
    face : dict
        The face dictionary. If the network is planar, this dictionary
        is populated by a face finding algorithm. Each key represents a face
        and points to its corresponding vertex cycle.
    facedata : dict
        Face attributes.
    attributes : dict
        A dictionary of miscellaneous information about the network.

    Examples
    --------

    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Network
        from compas.visualization import NetworkPlotter

        network = Network.from_obj(compas.get_data('lines.obj'))

        plotter = NetworkPlotter(network)

        plotter.draw_vertices(text={key: key for key in network.vertices()}, radius=0.2)
        plotter.draw_edges()

        plotter.show()

    """

    def __init__(self):
        super(Network, self).__init__()
        self._key_to_str = False
        self._max_int_key = -1
        self._key_to_str = False
        self.attributes = {
            'name'         : 'Network',
            'color.vertex' : None,
            'color.edge'   : None,
            'color.face'   : None,
        }
        self.vertex = {}
        self.edge = {}
        self.halfedge = {}
        self.default_vertex_attributes = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.default_edge_attributes = {}

    # --------------------------------------------------------------------------
    # customisation
    # see: https://docs.python.org/3/reference/datamodel.html
    # move these to a mixin?
    # --------------------------------------------------------------------------

    def __str__(self):
        """"""
        v = self.number_of_vertices()
        e = self.number_of_edges()

        dmin = 0 if not self.vertex else min(self.vertex_degree(key) for key in self.vertices())
        dmax = 0 if not self.vertex else max(self.vertex_degree(key) for key in self.vertices())

        if not self.default_vertex_attributes:
            dva = None
        else:
            dva = '\n'.join(['{0} => {1}'.format(key, value) for key, value in self.default_vertex_attributes.items()])

        if not self.default_edge_attributes:
            dea = None
        else:
            dea = '\n'.join(['{0} => {1}'.format(key, value) for key, value in self.default_edge_attributes.items()])

        return """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
network: {0}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- default vertex attributes

{5}

- default edge attributes

{6}

- number of vertices: {1}
- number of edges: {2}

- vertex degree min: {3}
- vertex degree max: {4}

""".format(self.attributes['name'], v, e, dmin, dmax, dva, dea)

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

    @property
    def adjacency(self):
        """Alias for the halfedge attribute."""
        return self.halfedge

    @property
    def data(self):
        """Return a data dict of this data structure for serialisation.
        """
        data = {'attributes'  : self.attributes,
                'dva'         : self.default_vertex_attributes,
                'dea'         : self.default_edge_attributes,
                'vertex'      : {},
                'edge'        : {},
                'halfedge'    : {},
                'max_int_key' : self._max_int_key, }

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

        return data

    @data.setter
    def data(self, data):
        attributes   = data.get('attributes') or {}
        dva          = data.get('dva') or {}
        dea          = data.get('dea') or {}
        vertex       = data.get('vertex') or {}
        halfedge     = data.get('halfedge') or {}
        edge         = data.get('edge') or {}
        max_int_key  = data.get('max_int_key', -1)

        self.attributes.update(attributes)
        self.default_vertex_attributes.update(dva)
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

        # set the counts

        self._max_int_key = max_int_key

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath, precision='3f'):
        network  = cls()
        obj      = OBJ(filepath, precision=precision)
        vertices = obj.parser.vertices
        edges    = obj.parser.lines
        for i, (x, y, z) in enumerate(vertices):
            network.add_vertex(i, x=x, y=y, z=z)
        for u, v in edges:
            network.add_edge(u, v)
        return network

    @classmethod
    def from_lines(cls, lines, precision='3f'):
        network = cls()
        edges   = []
        vertex  = {}
        for line in lines:
            sp = line[0]
            ep = line[1]
            a  = geometric_key(sp, precision)
            b  = geometric_key(ep, precision)
            vertex[a] = sp
            vertex[b] = ep
            edges.append((a, b))
        key_index = dict((k, i) for i, k in enumerate(iter(vertex)))
        for key, xyz in iter(vertex.items()):
            i = key_index[key]
            network.add_vertex(i, x=xyz[0], y=xyz[1], z=xyz[2])
        for u, v in edges:
            i = key_index[u]
            j = key_index[v]
            network.add_edge(i, j)
        return network

    @classmethod
    def from_vertices_and_edges(cls, vertices, edges):
        network = cls()
        for x, y, z in vertices:
            network.add_vertex(x=x, y=y, z=z)
        for u, v in edges:
            network.add_edge(u, v)
        return network

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_obj(self):
        raise NotImplementedError

    def to_points(self, axes='xyz'):
        return [self.vertex_coordinates(key, axes) for key in self.vertices()]

    def to_lines(self, axes='xyz'):
        return [self.edge_coordinates(u, v, axes=axes) for u, v in self.edges()]

    def to_vertices_and_edges(self):
        key_index = dict((key, index) for index, key in enumerate(self.vertices()))
        vertices  = [self.vertex_coordinates(key) for key in self.vertices()]
        edges     = [(key_index[u], key_index[v]) for u, v in self.edges()]
        return vertices, edges

    # --------------------------------------------------------------------------
    # helpers
    # move to mixin
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
        self._max_int_key = -1
        self._max_int_fkey = -1

    def clear_vertexdict(self):
        del self.vertex
        self.vertex = {}
        self._max_int_key = -1

    def clear_edgedict(self):
        del self.edge
        self.edge = {}

    def clear_halfedgedict(self):
        del self.halfedge
        self.halfedge = {}

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex and specify its attributes (optional).

        Note:
            If no key is provided for the vertex, one is generated
            automatically. An automatically generated key increments the highest
            key in use by 1::

                key = int(sorted(self.vertex.keys())[-1]) + 1

        Parameters:
            key (int): An identifier for the vertex. Defaults to None. The key
                is converted to a string before it is used.
            attr_dict (dict): Vertex attributes, defaults to ``None``.
            **attr: Other named vertex attributes, defaults to an empty :obj:`dict`.

        Returns:
            str: The key of the vertex.

        Examples:
            >>> network = Network()
            >>> network.add_vertex()
            '0'
            >>> network.add_vertex(x=0, y=0, z=0)
            '1'
            >>> network.add_vertex(key=2)
            '2'
            >>> network.add_vertex(key=0, x=1)
            '0'
        """
        attr = deepcopy(self.default_vertex_attributes)
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        attr.update(attr_dict)

        key = self._get_vertexkey(key)

        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
            self.edge[key] = {}

        self.vertex[key].update(attr)

        return key

    def add_edge(self, u, v, attr_dict=None, **kwattr):
        """Add an edge and specify its attributes (optional)."""
        attr = deepcopy(self.default_edge_attributes)
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        attr.update(attr_dict)

        if u not in self.vertex:
            u = self.add_vertex(u)
        if v not in self.vertex:
            v = self.add_vertex(v)

        data = self.edge[u].get(v, {})
        data.update(attr)

        self.edge[u][v] = data
        if v not in self.halfedge[u]:
            self.halfedge[u][v] = None
        if u not in self.halfedge[v]:
            self.halfedge[v][u] = None

        return u, v

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    # def remove_vertex(self, key):
    #     pass

    # def remove_edge(self, u, v):
    #     raise NotImplementedError
    #     if self.face:
    #         # there are faces
    #         f1 = self.halfedge[u][v]
    #         f2 = self.halfedge[v][u]
    #         if f1 is not None and f2 is not None:
    #             vertices1 = self.face[f1]
    #             vertices2 = self.face[f2]
    #     else:
    #         # there are no faces
    #         del self.halfedge[u][v]
    #         del self.halfedge[v][u]
    #         del self.edge[u][v]

    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------

    def number_of_vertices(self):
        return len(list(self.vertices()))

    def number_of_edges(self):
        return len(list(self.edges()))

    def number_of_halfedges(self):
        return len(list(self.halfedges()))

    def is_connected(self):
        """Return True if for every two vertices a path exists connecting them."""
        if not self.vertex:
            return False

        root = self.get_any_vertex()
        nodes = network_bfs2(self.halfedge, root)

        return len(nodes) == self.number_of_vertices()

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

    # --------------------------------------------------------------------------
    # additional accessors
    # --------------------------------------------------------------------------

    def indexed_edges(self):
        k_i = self.key_index()
        return [(k_i[u], k_i[v]) for u, v in self.edges()]

    # --------------------------------------------------------------------------
    # default attributes
    # --------------------------------------------------------------------------

    # inherited from VertexAttributesMixin

    # inherited from EdgeAttributesMixin

    # --------------------------------------------------------------------------
    # vertex attributes
    # --------------------------------------------------------------------------

    # inherited from VertexAttributesMixin

    # --------------------------------------------------------------------------
    # edge attributes
    # --------------------------------------------------------------------------

    # inherited from EdgeAttributesMixin

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

    def vertex_neighbours(self, key):
        """Return the neighbours of a vertex."""
        return list(self.halfedge[key])

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

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    def has_edge(self, u, v, directed=True):
        if directed:
            return u in self.edge and v in self.edge[u]
        else:
            return (u in self.edge and v in self.edge[u]) or (v in self.edge and u in self.edge[v])

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

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, key, axes='xyz'):
        """Return the coordinates of a vertex."""
        return [self.vertex[key][axis] for axis in axes]

    def vertex_laplacian(self, key):
        """Return the vector from the vertex to the centroid of its 1-ring neighbourhood."""
        c = centroid_points([self.vertex_coordinates(nbr) for nbr in self.neighbours(key)])
        p = self.vertex_coordinates(key)
        return subtract_vectors(c, p)

    def vertex_neighbourhood_centroid(self, key):
        return centroid_points([self.vertex_coordinates(nbr) for nbr in self.neighbours(key)])

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    # inherited from EdgeGeometryMixin

    # --------------------------------------------------------------------------
    # boundary
    # --------------------------------------------------------------------------

    # def vertices_on_boundary(self):
    #     vertices = []
    #     seen = set()
    #     for fkey in self.boundary_faces():
    #         for key in self.face[fkey]:
    #             if key not in seen:
    #                 seen.add(key)
    #                 vertices.append(key)
    #     return vertices

    # def edges_on_boundary(self):
    #     edges = []
    #     for fkey in self.boundary_faces():
    #         vertices = self.face[fkey]
    #         for i in range(len(vertices) - 1):
    #             u = vertices[i]
    #             v = vertices[i + 1]
    #             if v in self.edge[u]:
    #                 edges.append((u, v))
    #             else:
    #                 edges.append((v, u))
    #     return edges

    # --------------------------------------------------------------------------
    # selections
    # --------------------------------------------------------------------------

    # inherited from VertexAttributesMixin

    # inherited from EdgeAttributesMixin


class FaceNetwork(FaceHelpersMixin,
                  FaceAttributesMixin,
                  Network):

    def __init__(self):
        super(FaceNetwork, self).__init__()
        self._max_int_fkey = -1
        self.face = {}
        self.facedata = {}
        self.default_face_attributes = {}

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

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

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    # add edge support
    @classmethod
    def from_obj(cls, filepath, **kwargs):
        """Initialise a network from the data described in an obj file.

        Parameters:
            filepath (str): The path to the obj file.
            kwargs (dict) : Remaining named parameters. Default is an empty :obj:`dict`.

        Returns:
            Network: A ``Network`` of class ``cls``.

        >>> network = Network.from_obj('path/to/file.obj')

        """
        network = cls()
        network.attributes.update(kwargs)
        obj = OBJ(filepath)
        vertices = obj.parser.vertices
        edges    = obj.parser.lines
        faces = obj.parser.faces
        for i, (x, y, z) in enumerate(vertices):
            network.add_vertex(i, x=x, y=y, z=z)
        for u, v in edges:
            network.add_edge(u, v)
        for face in faces:
            network.add_face(face)
        return network

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_obj(self, filepath):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

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

    def clear_facedict(self):
        del self.face
        del self.facedata
        self.face = {}
        self.facedata = {}
        self._max_int_fkey = -1

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face and specify its attributes (optional).

        Note:
            * A dictionary key for the face will be generated automatically, based on
              the keys of its vertices.
            * All faces are closed. The closing link is implied and, therefore,
              the last vertex in the list should be different from the first.
            * Building a face_adjacency list is slow, if we can't rely on the fact
              that all faces have the same cycle directions. Therefore, it is
              worth considering to ensure unified cycle directions upon addition
              of a new face.

        Parameters:
            vertices (list): A list of vertex keys.

        Returns:
            str: The key of the face.
        """
        attr = self.default_face_attributes.copy()
        if attr_dict is None:
            attr_dict = {}
        attr_dict.update(kwattr)
        attr.update(attr_dict)

        if vertices[0] == vertices[-1]:
            del vertices[-1]
        if vertices[-2] == vertices[-1]:
            del vertices[-1]
        if len(vertices) < 3:
            return

        keys = []
        for key in vertices:
            if key not in self.vertex:
                key = self.add_vertex(key)
            keys.append(key)

        fkey = self._get_facekey(fkey)

        self.face[fkey] = keys
        self.facedata[fkey] = attr

        halfedges = keys + keys[0:1]

        for u, v in pairwise(halfedges):
            if self.has_edge(u, v, directed=False):
                self.halfedge[u][v] = fkey
                if u not in self.halfedge[v]:
                    self.halfedge[v][u] = None

        return fkey

    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------

    def number_of_faces(self):
        return len(list(self.faces()))

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

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

    def indexed_face_vertices(self):
        k_i = self.key_index()
        return [[k_i[key] for key in self.face_vertices(fkey)] for fkey in self.faces()]

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

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

    def edge_faces(self, u, v):
        return [self.halfedge[u][v], self.halfedge[v][u]]

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

    # centroid_points is in fact an averaging of vectors
    # name it as such
    def vertex_normal(self, key):
        """Return the normal vector at the vertex as the weighted average of the
        normals of the neighbouring faces."""
        vectors = [self.face_normal(fkey) for fkey in self.vertex_faces(key) if fkey is not None]
        return normalize_vector(centroid_points(vectors))

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

    def vertices_on_boundary(self, ordered=False):
        """Return the vertices on the boundary.

        Warning
        -------
        If the vertices are requested in order, and the mesh has multiple borders,
        currently only the vertices of one of the borders will be returned.

        Parameters
        ----------
        ordered : bool, optional
            If ``True``, Return the vertices in the same order as they are found on the boundary.
            Default is ``False``.

        Returns
        -------
        list
            The vertices of the boundary.

        Examples
        --------
        >>>

        """
        vertices = set()
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, face in iter(nbrs.items()):
                if face is None:
                    vertices.add(key)
                    vertices.add(nbr)

        vertices = list(vertices)

        if not ordered:
            return vertices

        key = vertices[0]
        vertices = []
        start = key

        while 1:
            for nbr, fkey in iter(self.halfedge[key].items()):
                if fkey is None:
                    vertices.append(nbr)
                    key = nbr
                    break

            if key == start:
                break

        return vertices

    def faces_on_boundary(self):
        """Return the faces on the boundary."""
        faces = {}
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, fkey in iter(nbrs.items()):
                if fkey is None:
                    faces[self.halfedge[nbr][key]] = 1
        return faces.keys()

    def edges_on_boundary(self):
        return [(u, v) for u, v in self.edges() if self.is_edge_naked(u, v)]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from compas.visualization.plotters.networkplotter import NetworkPlotter

    network = Network.from_obj(compas.get_data('open_edges.obj'))

    print(network)

    plotter = NetworkPlotter(network, figsize=(10, 7))

    plotter.defaults['vertex.fontsize'] = 8.0

    plotter.draw_vertices(
        facecolor={key: '#ff0000' for key in network.leaves()},
        radius=0.2,
        text={key: key for key in network.vertices()}
    )

    plotter.draw_edges()

    plotter.show()
