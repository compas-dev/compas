from __future__ import print_function

from copy import deepcopy

import compas

from compas.files.obj import OBJ

from compas.utilities import geometric_key
from compas.utilities.itertools_ import pairwise

from compas.datastructures._graph import Graph


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


# @todo: do not allow the addition of faces,
#        faces have to be "found"


class Network(Graph):
    """Definition of a network object.

    The ``Network`` class is implemented as a directed edge graph, with optional support
    for face topology and face data if the network is planar.

    Attributes:
        vertex (dict): The vertex dictionary. Each key in the vertex dictionary
            represents a vertex of the network and maps to a dictionary of
            vertex attributes.
        edge (dict of dict): The edge dictionary. Each key in the edge dictionary
            corresponds to a key in the vertex dictionary, and maps to a dictionary
            with connected vertices. In the latter, the keys are again references
            to items in the vertex dictionary, and the values are dictionaries
            of edge attributes.
        halfedge (dict of dict): A half-edge dictionary, which keeps track of
            undirected adjacencies. If the network is planar, the halfedges point
            at entries in the face dictionary.
        face (dict): The face dictionary. If the network is planar, this dictionary
            is populated by a face finding algorithm. Each key represents a face
            and points to its corresponding vertex cycle.
        facedata (dict): Face attributes.
        attributes (dict): A dictionary of miscellaneous information about the network.

    Examples:

        .. plot::
            :include-source:

            import compas
            from compas.datastructures.network import Network
            from compas.visualization.plotters import NetworkPlotter

            network = Network.from_obj(compas.get_data('lines.obj'))

            plotter = NetworkPlotter(network)

            plotter.draw_vertices(text={key: key for key in network.vertices()}, radius=0.2)
            plotter.draw_edges()

            plotter.show()


        .. code-block:: python

            import compas
            from compas.datastructures.network import Network

            network = Network.from_obj(compas.get_data('lines.obj'))

            # structure of the vertex dict

            for key in network.vertex:
                print(key, network.vertex[key])

            # structure of the edge dict

            for u in network.edge:
                for v in network.edge[u]:
                    print(u, v, network.edge[u][v])

            # structure of the halfedge dict

            for u in network.halfedge:
                for v in network.halfedge[u]:
                    if network.halfedge[u][v] is not None:
                        print(network.face[network.halfedge[u][v]])
                    if network.halfedge[v][u] is not None:
                        print(network.face[network.halfedge[v][u]])

            # structure of the face dict

            for fkey in network.face:
                print(fkey, network.face[fkey], network.facedata[fkey])

    """

    def __init__(self):
        super(Network, self).__init__()
        self.attributes.update({
            'name'         : 'Network',
            'color.vertex' : None,
            'color.edge'   : None,
            'color.face'   : None,
        })

    # --------------------------------------------------------------------------
    # customisation
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
    def adjacency(self):
        """Alias for the halfedge attribute."""
        return self.halfedge

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

    def to_vertices_and_edges(self):
        key_index = dict((key, index) for index, key in enumerate(self.vertices()))
        vertices  = [self.vertex_coordinates(key) for key in self.vertices()]
        edges     = [(key_index[u], key_index[v]) for u, v in self.edges()]
        return vertices, edges

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

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
            >>> mesh = Mesh()
            >>> mesh.add_vertex()
            '0'
            >>> mesh.add_vertex(x=0, y=0, z=0)
            '1'
            >>> mesh.add_vertex(key=2)
            '2'
            >>> mesh.add_vertex(key=0, x=1)
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

    # def _add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
    #     """Add a face and specify its attributes (optional).

    #     Note:
    #         * A dictionary key for the face will be generated automatically, based on
    #           the keys of its vertices.
    #         * All faces are closed. The closing link is implied and, therefore,
    #           the last vertex in the list should be different from the first.
    #         * Building a face_adjacency list is slow, if we can't rely on the fact
    #           that all faces have the same cycle directions. Therefore, it is
    #           worth considering to ensure unified cycle directions upon addition
    #           of a new face.

    #     Parameters:
    #         vertices (list): A list of vertex keys.

    #     Returns:
    #         str: The key of the face.
    #     """
    #     attr = self.default_face_attributes.copy()
    #     if attr_dict is None:
    #         attr_dict = {}
    #     attr_dict.update(kwattr)
    #     attr.update(attr_dict)

    #     if vertices[0] == vertices[-1]:
    #         del vertices[-1]
    #     if vertices[-2] == vertices[-1]:
    #         del vertices[-1]
    #     if len(vertices) < 3:
    #         return

    #     keys = []
    #     for key in vertices:
    #         if key not in self.vertex:
    #             key = self.add_vertex(key)
    #         keys.append(key)

    #     fkey = self._get_facekey(fkey)

    #     self.face[fkey] = keys
    #     self.facedata[fkey] = attr

    #     halfedges = keys + keys[0:1]

    #     for u, v in pairwise(halfedges):
    #         self.halfedge[u][v] = fkey
    #         if u not in self.halfedge[v]:
    #             self.halfedge[v][u] = None

    #     return fkey

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
    # accessors
    # --------------------------------------------------------------------------

    # def vertices_iter(self, data=False):
    #     return self.vertices(data=data)

    # def vertices_enum(self, data=False):
    #     for index, (key, attr) in enumerate(self.vertices(True)):
    #         if data:
    #             yield index, key, attr
    #         else:
    #             yield index, key

    # def edges_iter(self, data=False):
    #     return self.edges(data=data)

    # def edges_enum(self, data=False):
    #     index = 0
    #     for u, nbrs in iter(self.edge.items()):
    #         for v, attr in iter(nbrs.items()):
    #             if data:
    #                 yield index, u, v, attr
    #             else:
    #                 yield index, u, v
    #             index += 1

    # def faces_iter(self, data=False):
    #     return self.faces(data=data)

    # def faces_enum(self, data=False):
    #     for index, fkey in enumerate(self.faces()):
    #         if data:
    #             yield index, fkey, self.facedata.setdefault(fkey, self.default_face_attributes.copy())
    #         else:
    #             yield index, fkey

    # --------------------------------------------------------------------------
    # default attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # vertex attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # edge attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # face attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    # def neighbours(self, key, ordered=None):
    #     return self.vertex_neighbours(key, ordered=ordered)

    # def neighbourhood(self, key, ring=1):
    #     return self.vertex_neighbourhood(key, ring=ring)

    # def neighbours_out(self, key):
    #     return self.vertex_neighbours_out(key)

    # def neighbours_in(self, key):
    #     return self.vertex_neighbours_in(key)

    # def degree(self, key):
    #     return len(self.vertex_neighbours(key))

    # def degree_out(self, key):
    #     return len(self.vertex_neighbours_out(key))

    # def degree_in(self, key):
    #     return len(self.vertex_neighbours_in(key))

    # def connected_edges(self, key):
    #     return self.vertex_connected_edges(key)

    # def is_vertex_leaf(self, key):
    #     return self.degree(key) == 1

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    # def face_descendant(self, fkey, key):
    #     return self.face_vertex_descendant(fkey, key)

    # def face_ancestor(self, fkey, key):
    #     return self.face_vertex_ancestor(fkey, key)

    # def face_tree(self, root, algo=network_bfs):
    #     adj = self.face_adjacency()
    #     tree = algo(root, adj)
    #     return tree

    # def face_adjacency_edge(self, f1, f2):
    #     for u, v in self.face_halfedges(f1):
    #         if self.halfedge[v][u] == f2:
    #             if v in self.edge[u]:
    #                 return u, v
    #             return v, u

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # face geometry
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # boundary
    # --------------------------------------------------------------------------

    def vertices_on_boundary(self):
        vertices = []
        seen = set()
        for fkey in self.boundary_faces():
            for key in self.face[fkey]:
                if key not in seen:
                    seen.add(key)
                    vertices.append(key)
        return vertices

    def edges_on_boundary(self):
        edges = []
        for fkey in self.boundary_faces():
            vertices = self.face[fkey]
            for i in range(len(vertices) - 1):
                u = vertices[i]
                v = vertices[i + 1]
                if v in self.edge[u]:
                    edges.append((u, v))
                else:
                    edges.append((v, u))
        return edges

    def faces_on_boundary(self):
        faces = []
        for fkey, vertices in iter(self.face.items()):
            if vertices[0] != vertices[-1]:
                if len(vertices) > 4:
                    faces.append(fkey)
        return faces

    # --------------------------------------------------------------------------
    # selections
    # --------------------------------------------------------------------------


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    from compas.visualization.plotters.networkplotter import NetworkPlotter

    network = Network.from_obj(compas.get_data('open_edges.obj'))

    print(network)

    plotter = NetworkPlotter(network)

    plotter.defaults['vertex.fontsize'] = 10.0

    plotter.draw_vertices(
        facecolor={key: '#ff0000' for key in network.leaves()},
        radius=0.2,
        text={key: key for key in network.vertices()}
    )

    plotter.draw_edges()

    plotter.show()
