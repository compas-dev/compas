from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from copy import deepcopy
from ast import literal_eval

import compas

from compas.files import OBJ

from compas.utilities import geometric_key

from compas.geometry import centroid_points
from compas.geometry import subtract_vectors

from compas.datastructures import Datastructure

from compas.datastructures._mixins import VertexAttributesManagement
from compas.datastructures._mixins import VertexHelpers
from compas.datastructures._mixins import VertexCoordinatesDescriptors
from compas.datastructures._mixins import VertexMappings
from compas.datastructures._mixins import VertexFilter

from compas.datastructures._mixins import EdgeAttributesManagement
from compas.datastructures._mixins import EdgeHelpers
from compas.datastructures._mixins import EdgeGeometry
from compas.datastructures._mixins import EdgeMappings
from compas.datastructures._mixins import EdgeFilter

from compas.datastructures._mixins import FromToData
from compas.datastructures._mixins import FromToJson

from compas.datastructures.network.operations import network_split_edge


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


__all__ = ['Network', ]


class Network(FromToJson,
              FromToData,
              EdgeGeometry,
              EdgeHelpers,
              VertexHelpers,
              VertexMappings,
              EdgeMappings,
              VertexFilter,
              EdgeFilter,
              VertexCoordinatesDescriptors,
              EdgeAttributesManagement,
              VertexAttributesManagement,
              Datastructure):
    """Definition of a network.

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
        undirected adjacencies.
    attributes : dict
        A dictionary of miscellaneous information about the network.

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Network
        from compas.plotters import NetworkPlotter

        network = Network.from_obj(compas.get('lines.obj'))

        plotter = NetworkPlotter(network)

        plotter.draw_vertices(text={key: key for key in network.vertices()}, radius=0.2)
        plotter.draw_edges()

        plotter.show()

    """

    split_edge = network_split_edge

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
{0}
{7}

- default vertex attributes

{5}

- default edge attributes

{6}

- number of vertices: {1}
- number of edges: {2}

- vertex degree min: {3}
- vertex degree max: {4}

""".format(self.name, v, e, dmin, dmax, dva, dea, "=" * len(self.name))

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

    @classmethod
    def from_grid(cls, xlim, ylim):
        pass

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

    def to_points_and_lines(self):
        points = [self.vertex_coordinates(key) for key in self.vertices()]
        lines = [self.edge_coordinates(u, v) for u, v in self.edges()]
        return points, lines

    # --------------------------------------------------------------------------
    # helpers
    # move to mixin
    # --------------------------------------------------------------------------

    def _get_vertex_key(self, key):
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

        Notes:
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

        key = self._get_vertex_key(key)

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

    def delete_vertex(self, key):
        for nbr in self.vertex_neighbors(key):
            del self.halfedge[key][nbr]
            del self.halfedge[nbr][key]
            if key in self.edge and nbr in self.edge[key]:
                del self.edge[key][nbr]
            else:
                del self.edge[nbr][key]
        del self.vertex[key]
        del self.halfedge[key]
        del self.edge[key]

    def delete_edge(self, u, v):
        del self.halfedge[u][v]
        del self.halfedge[v][u]
        if u in self.edge and v in self.edge[u]:
            del self.edge[u][v]
        else:
            del self.edge[v][u]

    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------

    def number_of_vertices(self):
        return len(list(self.vertices()))

    def number_of_edges(self):
        return len(list(self.edges()))

    def number_of_halfedges(self):
        return len(list(self.halfedges()))

    # def is_connected(self):
    #     """Return True if for every two vertices a path exists connecting them."""
    #     if not self.vertex:
    #         return False

    #     root = self.get_any_vertex()
    #     nodes = breadth_first_traverse(self.halfedge, root)

    #     return len(nodes) == self.number_of_vertices()

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

    def vertex_neighbors(self, key):
        """Return the neighbors of a vertex."""
        return list(self.halfedge[key])

    def vertex_neighborhood(self, key, ring=1):
        """Return the vertices in the neighborhood of a vertex."""
        nbrs = set(self.vertex_neighbors(key))

        i = 1
        while True:
            if i == ring:
                break

            temp = []
            for key in nbrs:
                temp += self.vertex_neighbors(key)

            nbrs.update(temp)

            i += 1

        return nbrs

    def vertex_neighbors_out(self, key):
        """Return the outgoing neighbors of a vertex."""
        return list(self.edge[key])

    def vertex_neighbors_in(self, key):
        """Return the incoming neighbors of a vertex."""
        return list(set(self.halfedge[key]) - set(self.edge[key]))

    def vertex_degree(self, key):
        """Return the number of neighbors of a vertex."""
        return len(self.vertex_neighbors(key))

    def vertex_degree_out(self, key):
        """Return the number of outgoing neighbors of a vertex."""
        return len(self.vertex_neighbors_out(key))

    def vertex_degree_in(self, key):
        """Return the numer of incoming neighbors of a vertex."""
        return len(self.vertex_neighbors_in(key))

    def vertex_connected_edges(self, key):
        """Return the edges connected to a vertex."""
        edges = []
        for nbr in self.vertex_neighbors(key):
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
        return (u in self.edge and v in self.edge[u]) or (v in self.edge and u in self.edge[v])

    def edge_connected_edges(self, u, v):
        edges = []
        for nbr in self.vertex_neighbors(u):
            if nbr in self.edge[u]:
                edges.append((u, nbr))
            else:
                edges.append((nbr, u))
        for nbr in self.vertex_neighbors(v):
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
        """Return the vector from the vertex to the centroid of its 1-ring neighborhood."""
        c = centroid_points([self.vertex_coordinates(nbr) for nbr in self.neighbors(key)])
        p = self.vertex_coordinates(key)
        return subtract_vectors(c, p)

    def vertex_neighborhood_centroid(self, key):
        return centroid_points([self.vertex_coordinates(nbr) for nbr in self.neighbors(key)])

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    # inherited from EdgeGeometryMixin

    # --------------------------------------------------------------------------
    # boundary
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # selections
    # --------------------------------------------------------------------------

    # inherited from VertexAttributesMixin

    # inherited from EdgeAttributesMixin


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.plotters import NetworkPlotter

    network = Network.from_obj(compas.get('lines.obj'))

    plotter = NetworkPlotter(network, figsize=(10, 7))

    plotter.defaults['vertex.fontsize'] = 8

    network.delete_vertex(17)

    plotter.draw_vertices(text='key', radius=0.2)
    plotter.draw_edges()

    plotter.show()
