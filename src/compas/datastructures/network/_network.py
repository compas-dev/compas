from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import pickle
import pprint
import json
import collections

from copy import deepcopy
from ast import literal_eval

from compas.files import OBJ

from compas.utilities import geometric_key

from compas.geometry import centroid_points
from compas.geometry import subtract_vectors

from compas.datastructures import Datastructure

from compas.datastructures._mixins import VertexAttributesManagement
from compas.datastructures._mixins import VertexHelpers
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


__all__ = ['Network']


TPL = """
================================================================================
Network summary
================================================================================

- name: {}
- vertices: {}
- edges: {}
- vertex degree: {}/{}

"""

class Network(FromToJson,
              FromToData,
              EdgeGeometry,
              EdgeHelpers,
              VertexHelpers,
              VertexMappings,
              EdgeMappings,
              VertexFilter,
              EdgeFilter,
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

        network = Network.from_obj(compas.get('lines.obj'))

        network.plot(
            vertextext={key: key for key in network.vertices()},
            vertexsize=0.2
        )

    """

    __module__ = "compas.datastructures"

    split_edge = network_split_edge

    def __init__(self):
        super(Network, self).__init__()
        self._key_to_str = False
        self._max_int_key = -1

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
        """Generate a readable representation of the data of the mesh."""
        return json.dumps(self.data, sort_keys=True, indent=4)

    def summary(self):
        """Print a summary of the mesh."""
        numv = self.number_of_vertices()
        nume = self.number_of_edges()

        vmin = self.vertex_min_degree()
        vmax = self.vertex_max_degree()

        s = TPL.format(self.name, numv, nume, vmin, vmax)

        print(s)

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    @property
    def name(self):
        """str : The name of the data structure.

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
            data['vertex'][repr(key)] = self.vertex[key]

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
    # serialisation
    # --------------------------------------------------------------------------

    def dump(self, filepath):
        """Dump the data representing the network to a file using Python's built-in
        object serialisation.

        Parameters
        ----------
        filepath : str
            Path to the dump file.

        """
        data = {
            'attributes'  : self.attributes,
            'dva'         : self.default_vertex_attributes,
            'dea'         : self.default_edge_attributes,
            'vertex'      : self.vertex,
            'edge'        : self.edge,
            'halfedge'    : self.halfedge,
            'max_int_key' : self._max_int_key,
        }
        with open(filepath, 'wb+') as fo:
            pickle.dump(data, fo, protocol=pickle.HIGHEST_PROTOCOL)

    def dumps(self):
        """Dump the data representing the network to a string using Python's built-in
        object serialisation.

        Returns
        -------
        str
            The pickled string representation of the data.

        """
        data = {
            'attributes'  : self.attributes,
            'dva'         : self.default_vertex_attributes,
            'dea'         : self.default_edge_attributes,
            'vertex'      : self.vertex,
            'edge'        : self.edge,
            'halfedge'    : self.halfedge,
            'max_int_key' : self._max_int_key,
        }
        return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, filepath):
        """Load serialised network data from a pickle file.

        Parameters
        ----------
        filepath : str
            The path to the pickle file.

        """
        with open(filepath, 'rb') as fo:
            data = pickle.load(fo)

        self.attributes = data['attributes']
        self.default_vertex_attributes = data['dva']
        self.default_edge_attributes = data['dea']
        self.vertex = data['vertex']
        self.edge = data['edge']
        self.halfedge = data['halfedge']
        self._max_int_key = data['max_int_key']

    def loads(self, s):
        """Load serialised network data from a pickle string.

        Parameters
        ----------
        s : str
            The pickled string.

        """
        data = pickle.loads(s)

        self.attributes = data['attributes']
        self.default_vertex_attributes = data['dva']
        self.default_edge_attributes = data['dea']
        self.vertex = data['vertex']
        self.edge = data['edge']
        self.halfedge = data['halfedge']
        self._max_int_key = data['max_int_key']

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath, precision=None):
        """Construct a network from the data contained in an OBJ file.

        Parameters
        ----------
        filepath : str
            Path to the OBJ file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Network
            A network object.

        Note
        ----
        There are a few sample files available for testing and debugging:

        * lines.obj

        Examples
        --------
        .. code-block:: python

            import compas
            from compas.datastructures import Network

            network = Network.from_obj(compas.get('lines.obj'))

        """
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
    def from_lines(cls, lines, precision=None):
        """Construct a network from a set of lines represented by their start and end point coordinates.

        Parameters
        ----------
        lines : list
            A list of pairs of point coordinates.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Network
            A network object.

        Examples
        --------
        .. code-block:: python

            import json

            import compas
            from compas.datastructures import Network

            with open(compas.get('lines.json'), 'r') as fo:
                lines = json.load(fo)

            network = Network.from_lines(lines)

        """
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
        """Construct a network from vertices and edges.

        Parameters
        ----------
        vertices : list , dict
            A list of vertex coordinates or a dictionary of keys pointing to vertex coordinates to specify keys.
        edges : list of tuple of int

        Returns
        -------
        Network
            A network object.

        Examples
        --------
        .. code-block:: python

            pass

        """
        network = cls()

        if isinstance(vertices, collections.Sequence):
            for x, y, z in vertices:
                network.add_vertex(x=x, y=y, z=z)
        elif isinstance(vertices, collections.Mapping):
            for key, xyz in vertices.items():
                network.add_vertex(key = key, attr_dict = {i: j for i, j in zip(['x', 'y', 'z'], xyz)})
        
        for u, v in edges:
            network.add_edge(u, v)
        return network

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_obj(self):
        """Write the network to an OBJ file.

        Parameters
        ----------
        filepath : str
            Full path of the file.

        Examples
        --------
        .. code-block:: python

            pass

        """
        raise NotImplementedError

    def to_points(self, axes='xyz'):
        """Return the coordinates of the network.

        Parameters
        ----------
        axes : str, optional
            The components of the point coordinates to return.
            Default is to return XYZ components.

        Examples
        --------
        .. code-block:: python

            pass

        """
        return [self.vertex_coordinates(key, axes) for key in self.vertices()]

    def to_lines(self, axes='xyz'):
        """Return the lines of the network as pairs of start and end point coordinates.

        Parameters
        ----------
        axes : str, optional
            The components of the point coordinates to return.
            Default is to return XYZ components.

        Examples
        --------
        .. code-block:: python

            pass

        """
        return [self.edge_coordinates(u, v, axes=axes) for u, v in self.edges()]

    def to_vertices_and_edges(self):
        """Return the vertices and edges of a network.

        Returns
        -------
        tuple
            A 2-tuple containing

            * a list of vertices, represented by their XYZ coordinates, and
            * a list of edges.

            Each face is a list of indices referencing the list of vertex coordinates.

        Example
        -------
        .. code-block:: python

            pass

        """
        key_index = dict((key, index) for index, key in enumerate(self.vertices()))
        vertices  = [self.vertex_coordinates(key) for key in self.vertices()]
        edges     = [(key_index[u], key_index[v]) for u, v in self.edges()]
        return vertices, edges

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
        """Make an independent copy of the network object.

        Returns
        -------
        Network
            A separate, but identical network object.

        """
        cls = type(self)
        return cls.from_data(deepcopy(self.data))

    def clear(self):
        """Clear all the network data."""
        del self.vertex
        del self.edge
        del self.halfedge
        self.vertex   = {}
        self.edge     = {}
        self.halfedge = {}
        self._max_int_key = -1
        self._max_int_fkey = -1

    def clear_vertexdict(self):
        """Clear only the vertices."""
        del self.vertex
        self.vertex = {}
        self._max_int_key = -1

    def clear_edgedict(self):
        """Clear only the edges."""
        del self.edge
        self.edge = {}

    def clear_halfedgedict(self):
        """Clear only the half-edges."""
        del self.halfedge
        self.halfedge = {}

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex and specify its attributes (optional).

        Parameters
        ----------
        key : hashable, optional
            An identifier for the vertex.
            Defaults to ``None``, in which case an identifier of type ``int`` is automatically generated.
        attr_dict : dict, optional
            Vertex attributes, defaults to ``None``.
        kwattr
            Other named vertex attributes, defaults to an empty dict.

        Returns
        -------
        str
            The key of the vertex.

        Notes
        -----
        If no key is provided for the vertex, one is generated
        automatically. An automatically generated key increments the highest
        key in use by 1::

            key = int(sorted(self.vertex.keys())[-1]) + 1

        Examples
        --------
        >>> network.add_vertex()
        0
        >>> network.add_vertex(x=0, y=0, z=0)
        1
        >>> network.add_vertex(key=2)
        2
        >>> network.add_vertex(key=0, x=1)
        0

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
        """Add an edge and specify its attributes.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex of the edge.
        v : hashable
            The identifier of the second vertex of the edge.
        attr_dict : dict, optional
            A dictionary of edge attributes.
        kwattr
            Other edge attributes as additional keyword arguments.

        Returns
        -------
        tuple
            The identifiers of the edge vertices.

        Examples
        --------
        .. code-block:: python

            pass

        """
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
        """Delete a vertex from the network.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Examples
        --------
        .. code-block:: python

            pass

        """
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
        """Delete an edge from the network.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex.
        v : hashable
            The identifier of the second vertex.

        Examples
        --------
        .. code-block:: python

            pass

        """
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
        """Compute the number of vertices of the network.

        Returns
        -------
        int
            the number of vertices.

        """
        return len(list(self.vertices()))

    def number_of_edges(self):
        """Compute the number of edges of the network.

        Returns
        -------
        int
            the number of edges.

        """
        return len(list(self.edges()))

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        """Iterate over the vertices of the network.

        Parameters
        ----------
        data : bool, optional
            If ``True``, yield both the identifier and the attributes.

        Yields
        ------
        hashable
            The next vertex identifier (*key*), if ``data`` is ``False``.
        2-tuple
            The next vertex as a (key, attr) tuple, if ``data`` is ``True``.

        """
        if data:
            return iter(self.vertex.items())
        return iter(self.vertex)

    def edges(self, data=False):
        """Iterate over the edges of the network.

        Parameters
        ----------
        data : bool, optional
            If ``True``, yield both the identifier and the attributes.

        Yields
        ------
        2-tuple
            The next edge identifier (u, v), if ``data`` is ``False``.
        3-tuple
            The next vertex as a (u, v, attr) tuple, if ``data`` is ``True``.

        """
        for u, nbrs in iter(self.edge.items()):
            for v, attr in iter(nbrs.items()):
                if data:
                    yield u, v, attr
                else:
                    yield u, v

    # --------------------------------------------------------------------------
    # additional accessors
    # --------------------------------------------------------------------------

    # def indexed_edges(self):
    #     k_i = self.key_index()
    #     return [(k_i[u], k_i[v]) for u, v in self.edges()]

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
        """Verify if a specific vertex is present in the network.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        bool
            True or False.

        """
        return key in self.vertex

    def is_vertex_leaf(self, key):
        """Verify if a vertex is a leaf.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        bool
            True or False.

        Notes
        -----
        A vertex is a *leaf* if it has only one neighbor.

        """
        return self.vertex_degree(key) == 1

    def leaves(self):
        """Return all leaves of the network.

        Returns
        -------
        list
            A list of vertex identifiers.

        """
        return [key for key in self.vertices() if self.is_vertex_leaf(key)]

    def is_vertex_connected(self, key):
        """Verify if a specific vertex is connected.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        bool
            True or False.

        """
        return self.vertex_degree(key) > 0

    def vertex_neighbors(self, key):
        """Return the neighbors of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            A list of vertex identifiers.

        """
        return list(self.halfedge[key])

    def vertex_neighborhood(self, key, ring=1):
        """Return the vertices in the neighborhood of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        ring : int, optional
            The size of the neighborhood.
            Default is ``1``.

        Returns
        -------
        list
            A list of vertex identifiers.

        """
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

        if key in nbrs:
            nbrs.remove(key)

        return list(nbrs)

    def vertex_neighbors_out(self, key):
        """Return the outgoing neighbors of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            A list of vertex identifiers.

        """
        return list(self.edge[key])

    def vertex_neighbors_in(self, key):
        """Return the incoming neighbors of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            A list of vertex identifiers.

        """
        return list(set(self.halfedge[key]) - set(self.edge[key]))

    def vertex_degree(self, key):
        """Return the number of neighbors of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        int
            The number of neighbors of the vertex.

        """
        return len(self.vertex_neighbors(key))

    def vertex_min_degree(self):
        """Compute the minimum degree of all vertices.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        int
            The lowest degree of all vertices.

        """
        if not self.vertex:
            return 0
        return min(self.vertex_degree(key) for key in self.vertices())

    def vertex_max_degree(self):
        """Compute the maximum degree of all vertices.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        int
            The highest degree of all vertices.

        """
        if not self.vertex:
            return 0
        return max(self.vertex_degree(key) for key in self.vertices())

    def vertex_degree_out(self, key):
        """Return the number of outgoing neighbors of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        int
            The number of outgoing neighbors of the vertex.

        """
        return len(self.vertex_neighbors_out(key))

    def vertex_degree_in(self, key):
        """Return the numer of incoming neighbors of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        int
            The number of incoming neighbors of the vertex.

        """
        return len(self.vertex_neighbors_in(key))

    def vertex_connected_edges(self, key):
        """Return the edges connected to a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The edges connected to the vertex.

        """
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
        """Verify if the network contains a specific edge.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex of the edge.
        v : hashable
            The identifier of the secondt vertex of the edge.
        directed : bool, optional
            Take into accoun the direction of the edge.
            Default is ``True``.

        Returns
        -------
        bool
            True if the edge is present, False otherwise.

        """
        if directed:
            return u in self.edge and v in self.edge[u]
        return (u in self.edge and v in self.edge[u]) or (v in self.edge and u in self.edge[v])

    def edge_connected_edges(self, u, v):
        """Return the edges connected to an edge.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex of the edge.
        v : hashable
            The identifier of the secondt vertex of the edge.

        Returns
        -------
        list
            A list of connected edges.

        """
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
        """Return the coordinates of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        axes : str, optional
            The components of the vertex coordinates to return.
            Default is ``'xyz'``.

        Returns
        -------
        list
            The coordniates of the vertex.

        """
        return [self.vertex[key][axis] for axis in axes]

    def vertex_laplacian(self, key):
        """Return the vector from the vertex to the centroid of its 1-ring neighborhood.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The laplacian vector.

        """
        c = centroid_points([self.vertex_coordinates(nbr) for nbr in self.neighbors(key)])
        p = self.vertex_coordinates(key)
        return subtract_vectors(c, p)

    def vertex_neighborhood_centroid(self, key):
        """Compute the centroid of the neighboring vertices.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The coordinates of the centroid.

        """
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

    # --------------------------------------------------------------------------
    # visualisation
    # --------------------------------------------------------------------------

    def plot(self,
             vertexcolor=None,
             edgecolor=None,
             vertexsize=None,
             edgewidth=None,
             vertextext=None,
             edgetext=None):
        """Plot a 2D representation of the network.

        Parameters
        ----------
        vertexcolor : dict, optional
            A dictionary mapping vertex identifiers to colors.
        edgecolor : dict, optional
            A dictionary mapping edge identifiers to colors.
        vertexsize : dict, optional
            A dictionary mapping vertex identifiers to sizes.
        edgewidth : dict, optional
            A dictionary mapping edge identifiers to widths.
        vertextext : dict, optional
            A dictionary mappping vertex identifiers to labels.
        edgetext : dict, optional
            A dictionary mappping edge identifiers to labels.

        Examples
        --------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Network

            network = Network.from_obj(compas.get('lines.obj'))

            network.plot()

        """
        from compas.plotters import NetworkPlotter

        plotter = NetworkPlotter(self)
        plotter.draw_vertices(
            facecolor=vertexcolor,
            radius=vertexsize,
            text=vertextext
        )
        plotter.draw_edges(
            color=edgecolor,
            width=edgewidth,
            text=edgetext
        )
        plotter.show()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.plotters import NetworkPlotter

    network = Network.from_obj(compas.get('lines.obj'))

    plotter = NetworkPlotter(network, figsize=(10, 7))

    plotter.defaults['vertex.fontsize'] = 8

    network.delete_vertex(17)

    plotter.draw_vertices(text='key', radius=0.2)
    plotter.draw_edges()

    plotter.show()

    vertices = {44: [0.0, 0.0, 0.0], 38: [1.0, 0.0, 0.0], 2: [2.0, 0.0, 0.0]}
    edges = [(44, 38), (38, 2)]

    network = Network.from_vertices_and_edges(vertices, edges)
    print(network)

    plotter = NetworkPlotter(network, figsize=(10, 7))
    plotter.defaults['vertex.fontsize'] = 8
    plotter.draw_vertices(text='key', radius=0.2)
    plotter.draw_edges()
    plotter.show()

    vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]]
    edges = [(0, 1), (1, 2)]

    network = Network.from_vertices_and_edges(vertices, edges)
    print(network)

    plotter = NetworkPlotter(network, figsize=(10, 7))
    plotter.defaults['vertex.fontsize'] = 8
    plotter.draw_vertices(text='key', radius=0.2)
    plotter.draw_edges()
    plotter.show()

