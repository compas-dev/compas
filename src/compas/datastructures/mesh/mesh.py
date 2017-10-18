from __future__ import print_function

from copy import deepcopy
from ast import literal_eval

from compas.files.obj import OBJ
from compas.files.ply import PLYreader

from compas.utilities import pairwise
from compas.utilities import window
from compas.utilities import geometric_key

from compas.geometry import normalize_vector
from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import subtract_vectors
from compas.geometry import normal_polygon
from compas.geometry import area_polygon

from compas.datastructures import Datastructure

from compas.datastructures.mixins import VertexAttributesManagement
from compas.datastructures.mixins import VertexHelpers
from compas.datastructures.mixins import VertexCoordinatesDescriptors

from compas.datastructures.mixins import EdgeAttributesManagement
from compas.datastructures.mixins import EdgeHelpers
from compas.datastructures.mixins import EdgeGeometry

from compas.datastructures.mixins import FaceAttributesManagement
from compas.datastructures.mixins import FaceHelpers

from compas.datastructures.mixins import FromToData
from compas.datastructures.mixins import FromToJson

from compas.datastructures.mixins import VertexMappings
from compas.datastructures.mixins import EdgeMappings
from compas.datastructures.mixins import FaceMappings

from compas.datastructures.network.algorithms import network_bfs2


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


# @todo: don't allow the addition of edges
#        for which two opposite halfedges do not already exist


class Mesh(FromToJson,
           FromToData,
           EdgeGeometry,
           FaceHelpers,
           EdgeHelpers,
           VertexHelpers,
           FaceMappings,
           EdgeMappings,
           VertexMappings,
           VertexCoordinatesDescriptors,
           FaceAttributesManagement,
           EdgeAttributesManagement,
           VertexAttributesManagement,
           Datastructure):
    """Definition of a mesh.

    The datastructure of the mesh is implemented as a half-edge.

    Parameters
    ----------
    vertices : :obj:`list` of :obj:`dict`
        Optional. A sequence of vertices to add to the mesh.
        Each vertex should be a dictionary of vertex attributes.
    faces : :obj:`list` of :obj:`list`
        Optional. A sequence of faces to add to the mesh.
        Each face should be a list of vertex keys.
    dva : dict
        Optional. A dictionary of default vertex attributes.
    dfa : dict
        Optional. A dictionary of default face attributes.
    dea : dict
        Optional. A dictionary of default edge attributes.
    kwargs : dict
        The remaining named parameters. These are added to the attributes
        dictionary of the instance.

    Attributes
    ----------
    vertex : dict
        The vertex dictionary.
        With every key in the dictionary corresponds a dictionary of attributes.
    face : dict
        The face dictionary.
        With every key in the dictionary corresponds a dictionary of half-edges.
    halfedge : dict
        The half-edge dictionary.
        Every key in the dictionary corresponds to a vertex of the mesh.
        With every key corresponds a dictionary of neighbours pointing to face keys.
    edge : dict
        The edge dictionary.
        Every key in the dictionary corresponds to a vertex.
        With every key corresponds a dictionary of neighbours pointing to attribute dictionaries.
    attributes : dict
        General mesh attributes.
    facedata : Mesh, optional
        A ``Mesh`` object for keeping track of face attributes
        by storing them on dual vertices.

    Examples
    --------

    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.visualization.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get_data('faces.obj'))

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(radius=0.2)
        plotter.draw_faces()
        plotter.show()


    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.visualization.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get_data('faces.obj'))

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2)
        plotter.draw_faces()
        plotter.show()


    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh
        from compas.visualization.plotters import MeshPlotter

        mesh = Mesh.from_obj(compas.get_data('faces.obj'))

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(radius=0.2)
        plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})
        plotter.show()


    >>> for key in mesh.vertices():
    ...     print(key)
    ...

    >>> for key, attr in mesh.vertices(True):
    ...     print(key, attr)
    ...

    """

    def __init__(self):
        super(Mesh, self).__init__()
        self._key_to_str = False
        self._max_int_key = -1
        self._max_int_fkey = -1
        self.attributes = {
            'name'         : None,
            'color.vertex' : None,
            'color.edge'   : None,
            'color.face'   : None,
        }
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

    def __str__(self):
        """"""
        v = self.number_of_vertices()
        e = self.number_of_edges()
        f = self.number_of_faces()

        if not self.vertex:
            dmin = 0
        else:
            dmin = min(self.vertex_degree(key) for key in self.vertices())

        if not self.vertex:
            dmax = 0
        else:
            dmax = max(self.vertex_degree(key) for key in self.vertices())

        if not self.default_vertex_attributes:
            dva = None
        else:
            dva = '\n'.join(['{0} => {1}'.format(key, value) for key, value in self.default_vertex_attributes.items()])

        if not self.default_edge_attributes:
            dea = None
        else:
            dea = '\n'.join(['{0} => {1}'.format(key, value) for key, value in self.default_edge_attributes.items()])

        if not self.default_face_attributes:
            dfa = None
        else:
            dfa = '\n'.join(['{0} => {1}'.format(key, value) for key, value in self.default_face_attributes.items()])

        return """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
mesh: {}
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- default vertex attributes

{}

- default edge attributes

{}

- default face attributes

{}

- number of vertices: {}
- number of edges: {}
- number of faces: {}

- vertex degree min: {}
- vertex degree max: {}

- face degree min: {}
- face degree max: {}

""".format(self.attributes['name'], dva, dea, dfa, v, e, f, dmin, dmax, None, None)

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    @property
    def name(self):
        """:obj:`str` : The name of the data structure.

        Any value assigned to this property will be stored in the attribute dict
        of the data structure instance.
        """
        return self.attributes.get('name') or self.__class__.__name__

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

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath, **kwargs):
        """Initialise a mesh from the data described in an obj file.

        Parameters:
            filepath (str): The path to the obj file.
            kwargs (dict) : Remaining named parameters. Default is an empty :obj:`dict`.

        Returns:
            Mesh: A ``Mesh`` of class ``cls``.

        >>> mesh = Mesh.from_obj('path/to/file.obj')

        """
        mesh = cls()
        mesh.attributes.update(kwargs)
        obj = OBJ(filepath)
        vertices = obj.parser.vertices
        faces = obj.parser.faces
        for x, y, z in vertices:
            mesh.add_vertex(x=x, y=y, z=z)
        for face in faces:
            mesh.add_face(face)
        return mesh

    @classmethod
    def from_ply(cls, filepath, **kwargs):
        reader = PLYreader(filepath)
        reader.read()
        vertices = [(vertex['x'], vertex['y'], vertex['z']) for vertex in reader.vertices]
        faces = [face['vertex_indices'] for face in reader.faces]
        mesh = cls.from_vertices_and_faces(vertices, faces, **kwargs)
        return mesh

    # @classmethod
    # def from_lines(cls, lines, boundary_face=False, precision='3f'):
    #     """"""
    #     from compas.datastructures.network.algorithms.duality import _sort_neighbours
    #     from compas.datastructures.network.algorithms.duality import _find_first_neighbour
    #     from compas.datastructures.network.algorithms.duality import _find_edge_face

    #     mesh = cls()
    #     edges   = []
    #     vertex  = {}
    #     for line in lines:
    #         sp = line[0]
    #         ep = line[1]
    #         a  = geometric_key(sp, precision)
    #         b  = geometric_key(ep, precision)
    #         vertex[a] = sp
    #         vertex[b] = ep
    #         edges.append((a, b))
    #     key_index = dict((k, i) for i, k in enumerate(iter(vertex)))
    #     for key, xyz in iter(vertex.items()):
    #         i = key_index[key]
    #         mesh.add_vertex(i, x=xyz[0], y=xyz[1], z=xyz[2])
    #     edges_uv = []
    #     for u, v in edges:
    #         i = key_index[u]
    #         j = key_index[v]
    #         edges_uv.append((i, j))
    #     # the clear commands below are from the network equivalent. Needed?
    #     # network.clear_facedict()
    #     # network.clear_halfedgedict()
    #     mesh.halfedge = dict((key, {}) for key in mesh.vertex)
    #     for u, v in edges_uv:
    #         mesh.halfedge[u][v] = None
    #         mesh.halfedge[v][u] = None
    #     _sort_neighbours(mesh)

    #     u = sorted(mesh.vertices(True), key=lambda x: (x[1]['y'], x[1]['x']))[0][0]
    #     v = _find_first_neighbour(u, mesh)
    #     key_boundary_face = _find_edge_face(u, v, mesh)
    #     print(key_boundary_face)
    #     for u, v in mesh.edges():
    #         if mesh.halfedge[u][v] is None:
    #             _find_edge_face(u, v, mesh)
    #         if mesh.halfedge[v][u] is None:
    #             _find_edge_face(v, u, mesh)

    #     if not boundary_face:
    #         mesh.delete_face(key_boundary_face)
    #     return mesh

    @classmethod
    def from_lines(cls, lines, boundary_face=False, precision='3f'):
        """"""
        from compas.datastructures import network_find_faces
        from compas.datastructures import FaceNetwork

        network = FaceNetwork.from_lines(lines)

        network_find_faces(network, breakpoints=network.leaves())

        key_index = network.key_index()
        vertices = [network.vertex_coordinates(key) for key in network.vertices()]
        faces = [[key_index[key] for key in network.face_vertices(fkey)] for fkey in network.faces()]
        mesh = cls.from_vertices_and_faces(vertices, faces)

        if not boundary_face:
            mesh.delete_face(0)

        return mesh

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces, **kwargs):
        """Initialise a mesh from a list of vertices and faces.

        Parameters:
            vertices (list) : A list of vertices, represented by their XYZ coordinates.
            faces (list) : A list of faces. Each face is a list of indices referencing
                the list of vertex coordinates.
            kwargs (dict) : Remaining named parameters. Default is an empty :obj:`dict`.

        Returns:
            Mesh: A ``Mesh`` of class ``cls``.

        >>> vertices = []
        >>> faces = []
        >>> mesh = Mesh.from_vertices_and_faces(vertices, faces)

        """
        mesh = cls()
        mesh.attributes.update(kwargs)
        for x, y, z in iter(vertices):
            mesh.add_vertex(x=x, y=y, z=z)
        for face in iter(faces):
            mesh.add_face(face)
        return mesh

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_obj(self, filepath):
        """Write the mesh to an OBJ file.

        Parameters:
            filepath (str): Full path of the file to write.

        Notes:
            Use the framework ``OBJ`` functionality for this. How to write vertices
            and faces to an ``OBJ`` is not necessarily something a mesh knows how
            to do.
        """
        key_index = self.key_index()
        with open(filepath, 'wb+') as fh:
            for key, attr in self.vertices(True):
                fh.write('v {0[x]:.3f} {0[y]:.3f} {0[z]:.3f}\n'.format(attr))
            for fkey in self.face:
                vertices = self.face_vertices(fkey, ordered=True)
                vertices = [key_index[key] + 1 for key in vertices]
                ixs = ['f']
                for vkey in vertices:
                    ixs.append('{0}'.format(vkey))
                fh.write(' '.join(ixs) + '\n')

    def to_vertices_and_faces(self):
        """Return the vertices and faces of a mesh.

        Returns:
            (list, list): A tuple with a list of vertices, represented by their
                XYZ coordinates, and a list of faces. Each face is a list of
                indices referencing the list of vertex coordinates.
        """
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [self.face_vertices(fkey, ordered=True) for fkey in self.faces()]
        return vertices, faces

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
        attr = self.default_vertex_attributes.copy()
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
            self.halfedge[u][v] = fkey
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None
            if v not in self.edge[u]:
                if u not in self.edge[v]:
                    self.edge[u][v] = self.default_edge_attributes.copy()

        return fkey

    def add_faces(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    # this should be delete_vertex
    def remove_vertex(self, key):
        nbrs = self.vertex_neighbours(key)
        for nbr in nbrs:
            fkey = self.halfedge[key][nbr]
            if fkey is None:
                continue
            for u, v in self.face_halfedges(fkey):
                self.halfedge[u][v] = None
            del self.face[fkey]
        for nbr in nbrs:
            del self.halfedge[nbr][key]
        for nbr in nbrs:
            for n in self.vertex_neighbours(nbr):
                if self.halfedge[nbr][n] is None and self.halfedge[n][nbr] is None:
                    del self.halfedge[nbr][n]
                    del self.halfedge[n][nbr]
        del self.halfedge[key]
        del self.vertex[key]

    def delete_vertex(self, key):
        raise NotImplementedError

    def insert_vertex(self, fkey, key=None, xyz=None, return_key=False):
        """Insert a vertex in the specified face.

        Parameters:
            fkey (str): The key of the face in which the vertex should be inserted.

        Returns:
            str: The keys of the newly created faces.

        Raises:
            ValueError: If the face does not exist.
        """
        fkeys = []
        if not xyz:
            x, y, z = self.face_center(fkey)
        else:
            x, y, z = xyz
        w = self.add_vertex(key=key, x=x, y=y, z=z)
        for u, v in self.face_halfedges(fkey):
            fkeys.append(self.add_face([u, v, w]))
        del self.face[fkey]
        if return_key:
            return w
        return fkeys

    def delete_face(self, fkey):
        for u, v in self.face_halfedges(fkey):
            self.halfedge[u][v] = None
            if self.halfedge[v][u] is None:
                del self.halfedge[u][v]
                del self.halfedge[v][u]
        del self.face[fkey]

    def cull_unused_vertices(self):
        for u in self.vertices():
            if u not in self.halfedge:
                del self.vertex[u]
            else:
                if not self.halfedge[u]:
                    del self.vertex[u]
                    del self.halfedge[u]

    def cull_unused_edges(self):
        for u, v in self.edges():
            if u not in self.halfedge:
                del self.edge[u][v]
            if v not in self.halfedge[u]:
                del self.edge[u][v]
            if len(self.edge[u]) == 0:
                del self.edge[u]

    # def add_edges_from_faces(self):
    #     for fkey in self.faces():
    #         for u, v in self.face_halfedges(fkey):
    #             if u in self.edge and v in self.edge[u]:
    #                 continue
    #             if v in self.edge and u in self.edge[v]:
    #                 continue
    #             self.add_edge(u, v)

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
        # a mesh is valid if the following conditions are true
        # - halfedges don't point at non-existing faces
        # - all vertices are in the halfedge dict
        # - there are no None-None halfedges
        # - all faces have corresponding halfedge entries
        for key in self.vertices():
            if key not in self.halfedge:
                return False
        for u in self.halfedge:
            if u not in self.vertex:
                return False
            for v in self.halfedge[u]:
                if v not in self.vertex:
                    return False
                if self.halfedge[u][v] is None and self.halfedge[v][u] is None:
                    return False
                fkey = self.halfedge[u][v]
                if fkey:
                    if fkey not in self.face:
                        return False
        for fkey in self.faces():
            for u, v in self.face_halfedges(fkey):
                if u not in self.vertex:
                    return False
                if v not in self.vertex:
                    return False
                if u not in self.halfedge:
                    return False
                if v not in self.halfedge[u]:
                    return False
                if fkey != self.halfedge[u][v]:
                    return False
        return True

    def is_regular(self):
        """Return True if all faces have the same number of edges, and all vertices
        have the same degree (i.e. have the same valence: are incident to the same
        number of edges).

        Note:
            Not sure if the second condition makes sense.
            Example of a regular mesh?
        """
        if not self.vertex or not self.face:
            return False

        vkey = self.get_any_vertex()
        degree = self.vertex_degree(vkey)

        for vkey in self.vertices():
            if self.vertex_degree(vkey) != degree:
                return False

        fkey = self.get_any_face()
        vcount = len(self.face_vertices(fkey))

        for fkey in self.faces():
            vertices = self.face_vertices(fkey)

            if len(vertices) != vcount:
                return False

        return True

    def is_connected(self):
        """Return True if for every two vertices a path exists connecting them."""
        if not self.vertex:
            return False

        root = self.get_any_vertex()
        nodes = network_bfs2(self.halfedge, root)

        return len(nodes) == self.number_of_vertices()

    def is_manifold(self):
        """Return True if each edge is incident to only one or two faces, and the
        faces incident to a vertex form a closed or an open fan.

        Note:
            The first condition seems to be fullfilled by construction?!
        """
        if not self.vertex:
            return False

        for key in self.vertices():
            nbrs = self.vertex_neighbours(key, ordered=True)

            if not nbrs:
                return False

            if self.halfedge[nbrs[0]][key] is None:
                for nbr in nbrs[1:-1]:
                    if self.halfedge[key][nbr] is None:
                        return False

                if self.halfedge[key][nbrs[-1]] is not None:
                    return False
            else:
                for nbr in nbrs[1:]:
                    if self.halfedge[key][nbr] is None:
                        return False

        return True

    def is_orientable(self):
        """A manifold mesh is orientable if any two adjacent faces have compatible
        orientation (i.e. if the faces have a unified cycle direction)."""
        raise NotImplementedError

    # as in "does the mesh have a boundary?"
    # and no holes?
    def is_closed(self):
        raise NotImplementedError

    def is_trimesh(self):
        if not self.face:
            return False
        return not any(3 != len(self.face_vertices(fkey)) for fkey in self.faces())

    def is_quadmesh(self):
        if not self.face:
            return False
        return not any(4 != len(self.face_vertices(fkey)) for fkey in self.faces())

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
        for u, v in self.halfedges():
            if u in self.edge and v in self.edge[u]:
                if data:
                    yield u, v, self.edge[u][v]
                else:
                    yield u, v
            elif v in self.edge and u in self.edge[v]:
                if data:
                    yield v, u, self.edge[v][u]
                else:
                    yield v, u
            else:
                if u not in self.edge:
                    self.edge[u] = {}
                self.edge[u][v] = {}
                if data:
                    yield u, v, self.edge[u][v]
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

    # def vertex_cycle(self, key):
    #     nbrs = self.vertex_neighbours(key, ordered=True)
    #     return dict((nbrs[i], nbrs[i + 1]) for i in range(-1, len(nbrs) - 1))

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
        for nbr in self.halfedge[key]:
            if self.halfedge[key][nbr] is None:
                return True
        return False

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
        """Return triplets of face vertices forming the corners of the face."""
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

    # inherited from EdgeGeometryMixin

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

    # --------------------------------------------------------------------------
    # selections
    # --------------------------------------------------------------------------


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.visualization.plotters.meshplotter import MeshPlotter

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    mesh.to_json('./test.json')
    mesh = Mesh.from_json('./test.json')

    mesh.update_default_vertex_attributes({'px': 0.0, 'py': 0.0, 'pz': 0.0})
    mesh.update_default_vertex_attributes({'is_fixed': False})

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    print(mesh.number_of_vertices())
    print(mesh.number_of_edges())
    print(mesh.number_of_faces())

    plotter.defaults['face.facecolor'] = '#eeeeee'
    plotter.defaults['face.edgewidth'] = 0.0

    plotter.draw_vertices(
        facecolor={key: '#ff0000' for key in mesh.vertices() if mesh.vertex_degree(key) == 2}
    )

    plotter.draw_faces(text={key: str(key) for key in mesh.faces()})
    plotter.draw_edges()

    plotter.show()
