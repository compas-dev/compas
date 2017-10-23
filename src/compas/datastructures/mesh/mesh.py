from __future__ import print_function

from copy import deepcopy
from ast import literal_eval

from compas.files.obj import OBJ
from compas.files.ply import PLYreader

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

from compas.datastructures.mixins import VertexAttributesManagement
from compas.datastructures.mixins import VertexHelpers
from compas.datastructures.mixins import VertexFilter
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

from compas.topology import bfs_traverse


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


TPL = """
================================================================================
Mesh summary
================================================================================

- name: {}
- vertices: {}
- edges: {}
- faces: {}
- vertex degree: {}/{}
- face degree: {}/{}

================================================================================
"""


class Mesh(FromToJson,
           FromToData,
           EdgeGeometry,
           FaceHelpers,
           EdgeHelpers,
           VertexHelpers,
           VertexFilter,
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

    Attributes
    ----------
    vertex : dict
        The vertex dictionary.
        With every key in the dictionary corresponds a dictionary of attributes.
    face : dict
        The face dictionary.
        With every key in the dictionary corresponds a dictionary of half-edges.
    facedata : dict
        A dictionary with face attributes.
        For every face, there is a corresponding entry in this dict.
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
        """Compile a summary of the mesh."""
        numv = self.number_of_vertices()
        nume = self.number_of_edges()
        numf = self.number_of_faces()

        vmin = self.vertex_min_degree()
        vmax = self.vertex_max_degree()
        fmin = self.face_min_degree()
        fmax = self.face_max_degree()

        return TPL.format(self.name, numv, nume, numf, vmin, vmax, fmin, fmax)

    def summary(self):
        """Print a summary of the mesh."""
        print(self)

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    @property
    def name(self):
        """str : The name of the data structure.

        Any value assigned to this property will be stored in the attribute dict
        of the data structure instance.
        """
        return self.attributes.get('name') or self.__class__.__name__

    @name.setter
    def name(self, value):
        self.attributes['name'] = value

    @property
    def data(self):
        """dict: A data dict representing the mesh data structure for serialisation.

        The dict has the following structure:

        * 'attributes'   => dict
        * 'dva'          => dict
        * 'dea'          => dict
        * 'dfa'          => dict
        * 'vertex'       => dict
        * 'edge'         => dict
        * 'face'         => dict
        * 'facedata'     => dict
        * 'max_int_key'  => int
        * 'max_int_fkey' => int

        Note
        ----
        All dictionary keys are converted to their representation value (``repr(key)``)
        to ensure compatibility of all allowed key types with the JSON serialisation
        format, which only allows for dict keys that are strings.

        See Also
        --------
        * :meth:`to_data`
        * :meth:`to_json`
        * :meth:`from_data`
        * :meth:`from_json`

        """
        data = {'attributes'  : self.attributes,
                'dva'         : self.default_vertex_attributes,
                'dea'         : self.default_edge_attributes,
                'dfa'         : self.default_face_attributes,
                'vertex'      : {},
                'edge'        : {},
                'face'        : {},
                'facedata'    : {},
                'max_int_key' : self._max_int_key,
                'max_int_fkey': self._max_int_fkey, }

        for key in self.vertex:
            rkey = repr(key)
            data['vertex'][rkey] = self.vertex[key]

        for fkey in self.face:
            rfkey = repr(fkey)
            data['face'][rfkey] = [repr(key) for key in self.face[fkey]]

        for fkey in self.facedata:
            rfkey = repr(fkey)
            data['facedata'][rfkey] = self.facedata[fkey]

        for u in self.edge:
            ru = repr(u)
            data['edge'][ru] = {}

            for v in self.edge[u]:
                rv = repr(v)
                data['edge'][ru][rv] = self.edge[u][v]

        return data

    @data.setter
    def data(self, data):
        """"""
        attributes   = data.get('attributes') or {}
        dva          = data.get('dva') or {}
        dfa          = data.get('dfa') or {}
        dea          = data.get('dea') or {}
        vertex       = data.get('vertex') or {}
        face         = data.get('face') or {}
        facedata     = data.get('facedata') or {}
        edge         = data.get('edge') or {}
        max_int_key  = data.get('max_int_key', -1)
        max_int_fkey = data.get('max_int_fkey', -1)

        self.attributes.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_face_attributes.update(dfa)
        self.default_edge_attributes.update(dea)

        self.clear()

        # add the vertices
        for key, attr in iter(vertex.items()):
            key = literal_eval(key)
            self.add_vertex(key, attr_dict=attr)

        # add the faces
        for fkey, vertices in iter(face.items()):
            attr = facedata.get(fkey) or {}
            vertices = map(literal_eval, vertices)
            fkey = literal_eval(fkey)
            self.add_face(vertices, fkey=fkey, attr_dict=attr)

        # add the edges
        # todo: replace by method call
        for u, nbrs in iter(edge.items()):
            nbrs = nbrs or {}
            u = literal_eval(u)
            self.edge[u] = {}

            for v, attr in iter(nbrs.items()):
                attr = attr or {}
                v = literal_eval(v)

                self.add_edge(u, v, attr_dict=attr)

        # set the counts
        self._max_int_key = max_int_key
        self._max_int_fkey = max_int_fkey

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath):
        """Construct a mesh object from the data described in an OBJ file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        Mesh :
            A mesh object.

        Note
        ----
        There are a few sample files available for testing and debugging:

        * faces.obj
        * faces_big.obj
        * faces_reversed.obj
        * hypar.obj
        * mesh.obj
        * quadmesh.obj

        Examples
        --------
        >>> import compas
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_obj(compas.get('faces.obj'))

        """
        mesh = cls()
        obj = OBJ(filepath)
        vertices = obj.parser.vertices
        faces = obj.parser.faces
        for x, y, z in vertices:
            mesh.add_vertex(x=x, y=y, z=z)
        for face in faces:
            mesh.add_face(face)
        return mesh

    @classmethod
    def from_ply(cls, filepath):
        """Construct a mesh object from the data described in a PLY file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        Mesh :
            A mesh object.

        Note
        ----
        There are a few sample files available for testing and debugging:

        * bunny.ply

        Examples
        --------
        >>> import compas
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_obj(compas.get('bunny.ply'))

        """
        reader = PLYreader(filepath)
        reader.read()
        vertices = [(vertex['x'], vertex['y'], vertex['z']) for vertex in reader.vertices]
        faces = [face['vertex_indices'] for face in reader.faces]
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    @classmethod
    def from_lines(cls, lines, delete_boundary_face=True, precision='3f'):
        """Construct a mesh object from a list of lines described by start and end point coordinates.

        Parameters
        ----------
        lines : list
            A list of pairs of point coordinates.
        delete_boundary_face : bool, optional
            The algorithm that finds the faces formed by the connected lines
            first finds the face *on the outside*. In most cases this face is not expected
            to be there. Therefore, there is the option to have it automatically deleted.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Mesh :
            A mesh object.

        See Also
        --------
        * :func:`compas.datastructures.network_find_faces`
        * :func:`compas.datastructures.FaceNetwork`
        * :meth:`from_vertices_and_faces`

        Examples
        --------
        >>> import compas
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_obj(compas.get('bunny.ply'))

        """
        from compas.datastructures import network_find_faces
        from compas.datastructures import FaceNetwork

        network = FaceNetwork.from_lines(lines, precision=precision)

        network_find_faces(network, breakpoints=network.leaves())

        key_index = network.key_index()
        vertices = [network.vertex_coordinates(key) for key in network.vertices()]
        faces = [[key_index[key] for key in network.face_vertices(fkey)] for fkey in network.faces()]
        mesh = cls.from_vertices_and_faces(vertices, faces)

        if delete_boundary_face:
            mesh.delete_face(0)

        return mesh

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces):
        """Construct a mesh object from a list of vertices and faces.

        Parameters
        ----------
        vertices : list
            A list of vertices, represented by their XYZ coordinates.
        faces : list
            A list of faces.
            Each face is a list of indices referencing the list of vertex coordinates.

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        >>> import compas
        >>> from compas.datastructures import Mesh
        >>> vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]]
        >>> faces = [[0, 1, 2]]
        >>> mesh = Mesh.from_vertices_and_faces(vertices, faces)

        """
        mesh = cls()
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

        Parameters
        ----------
        filepath : str
            Full path of the file.

        Warning
        -------
        Currently this function only writes geometric data about the vertices and
        the faces to the file.

        Examples
        --------
        >>>

        """
        key_index = self.key_index()

        with open(filepath, 'w+') as fh:
            for key, attr in self.vertices(True):
                fh.write('v {0[x]:.3f} {0[y]:.3f} {0[z]:.3f}\n'.format(attr))
            for fkey in self.faces():
                vertices = self.face_vertices(fkey)
                vertices = [key_index[key] + 1 for key in vertices]
                fh.write(' '.join(['f'] + [str(index) for index in vertices]) + '\n')

    def to_vertices_and_faces(self):
        """Return the vertices and faces of a mesh.

        Returns
        -------
        tuple
            A 2-tuple containing

            * a list of vertices, represented by their XYZ coordinates, and
            * a list of faces.

            Each face is a list of indices referencing the list of vertex coordinates.

        Example
        -------
        >>>

        """
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [self.face_vertices(fkey, ordered=True) for fkey in self.faces()]
        return vertices, faces

    # --------------------------------------------------------------------------
    # helpers
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

    def _get_face_key(self, fkey):
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

    def _compile_vattr(self, attr_dict, kwattr):
        attr = self.default_vertex_attributes.copy()
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        attr.update(attr_dict)
        return attr

    def _compile_eattr(self, attr_dict, kwattr):
        attr = self.default_edge_attributes.copy()
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        attr.update(attr_dict)
        return attr

    def _compile_fattr(self, attr_dict, kwattr):
        attr = self.default_face_attributes.copy()
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        attr.update(attr_dict)
        return attr

    def _clean_vertices(self, vertices):
        if vertices[0] == vertices[-1]:
            del vertices[-1]
        if vertices[-2] == vertices[-1]:
            del vertices[-1]

    def _cycle_keys(self, keys):
        return pairwise(keys + keys[0:1])

    def copy(self):
        """Make an independent copy of the mesh object.

        Returns
        -------
        Mesh
            A separate, but identical mesh object.

        """
        cls = type(self)
        return cls.from_data(deepcopy(self.data))

    def clear(self):
        """Clear all the mesh data."""
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
        """Clear only the vertices."""
        del self.vertex
        self.vertex = {}
        self._max_int_key = -1

    def clear_facedict(self):
        """Clear only the faces."""
        del self.face
        del self.facedata
        self.face = {}
        self.facedata = {}
        self._max_int_fkey = -1

    def clear_edgedict(self):
        """Clear only the edges."""
        del self.edge
        self.edge = {}

    def clear_halfedgedict(self):
        """Clear only the half edges."""
        del self.halfedge
        self.halfedge = {}

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex to the mesh object.

        Parameters
        ----------
        key : int
            An identifier for the vertex.
            Defaults to None.
            The key is converted to a string before it is used.
        attr_dict : dict, optional
            Vertex attributes.
        kwattr : dict, optional
            Additional named vertex attributes.
            Named vertex attributes overwrite corresponding attributes in the
            attribute dict (``attr_dict``).

        Returns
        -------
        int
            The key of the vertex.
            If no key was provided, this is always an integer.
        hashable
            The key of the vertex.
            Any hashable object may be provided as identifier for the vertex.
            Provided keys are returned unchanged.

        Raises
        ------
        TypeError
            If the provided vertex key is of an unhashable type.

        Notes
        -----
        If no key is provided for the vertex, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        See Also
        --------
        * :meth:`add_face`
        * :meth:`add_edge`

        Examples
        --------
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
        attr = self._compile_vattr(attr_dict, kwattr)
        key = self._get_vertex_key(key)

        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
            self.edge[key] = {}

        self.vertex[key].update(attr)

        return key

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face to the mesh object.

        Parameters
        ----------
        vertices : list
            A list of vertex keys.
            For every vertex that does not yet exist, a new vertex is created.
        attr_dict : dict, optional
            Face attributes.
        kwattr : dict, optional
            Additional named face attributes.
            Named face attributes overwrite corresponding attributes in the
            attribute dict (``attr_dict``).

        Returns
        -------
        int
            The key of the face.
            The key is an integer, if no key was provided.
        hashable
            The key of the face.
            Any hashable object may be provided as identifier for the face.
            Provided keys are returned unchanged.

        Raises
        ------
        TypeError
            If the provided face key is of an unhashable type.

        Notes
        -----
        If no key is provided for the face, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        See Also
        --------
        * :meth:`add_vertex`
        * :meth:`add_edge`

        Examples
        --------
        >>>

        """
        attr = self._compile_fattr(attr_dict, kwattr)

        self._clean_vertices(vertices)

        if len(vertices) < 3:
            return

        keys = []
        for key in vertices:
            if key not in self.vertex:
                key = self.add_vertex(key)
            keys.append(key)

        fkey = self._get_face_key(fkey)

        self.face[fkey] = keys
        self.facedata[fkey] = attr

        for u, v in self._cycle_keys(keys):
            self.halfedge[u][v] = fkey
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None

        return fkey

    def add_edge(self, u, v, attr_dict=None, **kwattr):
        """Add an edge to the mesh object.

        Parameters
        ----------
        u : hashable
            The identifier of the starting vertex.
        v : hashable
            The identifier of the end vertex.
        attr_dict : dict, optional
            Edge attributes.
        kwattr : dict, optional
            Additional named edge attributes.
            Named face attributes overwrite corresponding attributes in the
            attribute dict (``attr_dict``).

        Returns
        -------
        None
            If adding the edge was unsuccessful.
            This is the case when

            * there is no corresponding half-edge present in the mesh, or
            * the opposite edge already exists.

        tuple
            The identifiers of start and end vertex.

        Notes
        -----
        Adding an edge to a mesh has no effect on the topology.
        In fact, the addition of an edge is only allowed if the edge matches one
        of the existing half-edges. In other words, an edge can only be added if
        it corresponds to the sides of one of the faces.
        The purpose of adding edges is to store information about the edges explicitly.
        For example, for form-finding algorithms.

        Examples
        --------
        >>>

        """
        # check if a corresponding halfedge exists
        if u in self.halfedge and v in self.halfedge[u]:
            pass
        elif v in self.halfedge and u in self.halfedge[v]:
            pass
        else:
            return

        # check if the opposite edge already exists
        if v in self.edge and u in self.edge[v]:
            return

        # add or update edge
        if u not in self.edge:
            self.edge[u] = {}
        if v not in self.edge[u]:
            self.edge[u][v] = {}
        attr = self._compile_eattr(attr_dict, kwattr)
        self.edge[u][v].update(attr)

        return u, v

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    def delete_vertex(self, key):
        """Delete a vertex from the mesh and everything that is attached to it.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Examples
        --------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            mesh.delete_vertex(17)

            color = {key: '#ff0000' for key in mesh.vertices() if mesh.vertex_degree(key) == 2}

            plotter = MeshPlotter(mesh)
            plotter.draw_vertices(facecolor=color)
            plotter.draw_faces()
            plotter.show()

        In some cases, disconnected vertices can remain after application of this
        method. To remove these vertices as well, combine this method with vertex
        culling (:meth:`cull_vertices`).

        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            mesh.delete_vertex(17)
            mesh.delete_vertex(18)
            mesh.delete_vertex(0)
            mesh.cull_vertices()

            color = {key: '#ff0000' for key in mesh.vertices() if mesh.vertex_degree(key) == 2}

            plotter = MeshPlotter(mesh)
            plotter.draw_vertices(facecolor=color)
            plotter.draw_faces()
            plotter.show()

        """
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

    def insert_vertex(self, fkey, key=None, xyz=None, return_fkeys=False):
        """Insert a vertex in the specified face.

        Parameters
        ----------
        fkey : hashable
            The key of the face in which the vertex should be inserted.
        key : hashable, optional
            The key to be used to identify the inserted vertex.
        xyz : list, optional
            Specific XYZ coordinates for the inserted vertex.
        return_fkeys : bool, optional
            By default, this method returns only the key of the inserted vertex.
            This flag can be used to indicate that the keys of the newly created
            faces should be returned as well.

        Returns
        -------
        hashable
            The key of the inserted vertex, if ``return_fkeys`` is false.
        tuple
            The key of the newly created vertex
            and a list with the newly created faces, if ``return_fkeys`` is true.

        Examples
        --------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            key, fkeys = mesh.insert_vertex(12, return_fkeys=True)

            plotter = MeshPlotter(mesh)
            plotter.draw_vertices(radius=0.15, text={key: str(key)})
            plotter.draw_faces(text={fkey: fkey for fkey in fkeys})
            plotter.show()

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

        if return_fkeys:
            return w, fkeys
        return w

    def delete_face(self, fkey):
        """Delete a face from the mesh object.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Examples
        --------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            mesh.delete_face(12)

            plotter = MeshPlotter(mesh)
            plotter.draw_vertices()
            plotter.draw_faces()
            plotter.show()

        """
        for u, v in self.face_halfedges(fkey):
            self.halfedge[u][v] = None
            if self.halfedge[v][u] is None:
                del self.halfedge[u][v]
                del self.halfedge[v][u]
        del self.face[fkey]

    def cull_vertices(self):
        """Remove all unused vertices from the mesh object.
        """
        for u in list(self.vertices()):
            if u not in self.halfedge:
                del self.vertex[u]
            else:
                if not self.halfedge[u]:
                    del self.vertex[u]
                    del self.halfedge[u]

    def cull_edges(self):
        """Remove all unused edges from the mesh object."""
        for u, v in list(self.edges()):
            if u not in self.halfedge:
                del self.edge[u][v]
            if v not in self.halfedge[u]:
                del self.edge[u][v]
            if len(self.edge[u]) == 0:
                del self.edge[u]

    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------

    def number_of_vertices(self):
        """Count the number of vertices in the mesh."""
        return len(list(self.vertices()))

    def number_of_edges(self):
        """Count the number of edges in the mesh."""
        return len(list(self.edges()))

    def number_of_faces(self):
        """Count the number of faces in the mesh."""
        return len(list(self.faces()))

    def number_of_halfedges(self):
        """Count the number of halfedges in the mesh."""
        return len(list(self.halfedges()))

    def is_valid(self):
        """Verify that the mesh is valid.

        A mesh is valid if the following conditions are fulfilled:

        * halfedges don't point at non-existing faces
        * all vertices are in the halfedge dict
        * there are no None-None halfedges
        * all faces have corresponding halfedge entries

        Returns
        -------
        bool
            True, if the mesh is valid.
            False, otherwise.

        """
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
        """Verify that the mesh is regular.

        A mesh is regular if the following conditions are fulfilled:

        * All faces have the same number of edges.
        * All vertices have the same degree, i.e. they are incident to the same number of edges.

        Returns
        -------
        bool
            True, if the mesh is regular.
            False, otherwise.

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
        """Verify that the mesh is connected.

        A mesh is connected if the following conditions are fulfilled:

        * For every two vertices a path exists connecting them.

        Returns
        -------
        bool
            True, if the mesh is connected.
            False, otherwise.

        """
        if not self.vertex:
            return False

        root = self.get_any_vertex()
        nodes = bfs_traverse(self.halfedge, root)

        return len(nodes) == self.number_of_vertices()

    def is_manifold(self):
        """Verify that the mesh is manifold.

        A mesh is manifold if the fllowing conditions are fulfilled:

        * Each edge is incident to only one or two faces.
        * The faces incident to a vertex form a closed or an open fan.

        Returns
        -------
        bool
            True, if the mesh is manifold.
            False, otherwise.

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
        """Verify that the mesh is orientable.

        A manifold mesh is orientable if the following conditions are fulfilled:

        * Any two adjacent faces have compatible orientation, i.e. the faces have a unified cycle direction.

        Returns
        -------
        bool
            True, if the mesh is orientable.
            False, otherwise.

        """
        raise NotImplementedError

    def is_trimesh(self):
        """Verify that the mesh consists of only triangles.

        Returns
        -------
        bool
            True, if the mesh is a triangle mesh.
            False, otherwise.

        """
        if not self.face:
            return False
        return not any(3 != len(self.face_vertices(fkey)) for fkey in self.faces())

    def is_quadmesh(self):
        """Verify that the mesh consists of only quads.

        Returns
        -------
        bool
            True, if the mesh is a quad mesh.
            False, otherwise.

        """
        if not self.face:
            return False
        return not any(4 != len(self.face_vertices(fkey)) for fkey in self.faces())

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        """Iterate over the vertices of the mesh.

        Parameters
        ----------
        data : bool, optional
            Return the vertex data as well as the vertex keys.

        Yields
        ------
        hashable
            The next vertex identifier (*key*), if ``data`` is false.
        2-tuple
            The next vertex as a (key, attr) tuple, if ``data`` is true.

        """
        if data:
            return iter(self.vertex.items())
        return iter(self.vertex)

    def faces(self, data=False):
        """Iterate over the faces of the mesh.

        Parameters
        ----------
        data : bool, optional
            Return the face data as well as the face keys.

        Yields
        ------
        hashable
            The next face identifier (*key*), if ``data`` is false.
        2-tuple
            The next face as a (fkey, attr) tuple, if ``data`` is true.

        """
        for fkey in self.face:
            if data:
                yield fkey, self.facedata.setdefault(fkey, self.default_face_attributes.copy())
            else:
                yield fkey

    def halfedges(self):
        """Iterate ove the halfedges of the mesh.

        Yields
        ------
        tuple
            The next halfedge as a (u, v) tuple.

        Note
        ----
        Duplicates (opposite halfedges) are automatically excluded.
        This method thus yields the undirected edges of the mesh.

        """
        edges = set()
        for fkey in self.faces():
            for u, v in self.face_halfedges(fkey):
                if (u, v) in edges or (v, u) in edges:
                    continue

                edges.add((u, v))
                edges.add((v, u))

                yield u, v

    def edges(self, data=False):
        """Iterate over the edges of the mesh.

        Parameters
        ----------
        data : bool, optional
            Return the edge data as well as the edge vertex keys.

        Yields
        ------
        2-tuple
            The next edge as a (u, v) tuple, if ``data`` is false.
        3-tuple
            The next edge as a (u, v, data) tuple, if ``data`` is true.

        Note
        ----
        Mesh edges have no topological meaning. They are only used to store data.
        Edges are not automatically created when vertices and faces are added to
        the mesh. Instead, they are created when data is stored on them, or when
        they are accessed using this method.

        This method yields the directed edges of the mesh.
        Unless edges were added explicitly using :meth:`add_edge` the order of
        edges is *as they come out*. However, as long as the toplogy remains
        unchanged, the order is consistent.

        Example
        -------
        .. code-block:: python

            import compas
            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            for index, (u, v, attr) in enumerate(mesh.edges(True)):
                attr['index1'] = index

            for index, (u, v, attr) in enumerate(mesh.edges(True)):
                attr['index2'] = index

            plotter = MeshPlotter(mesh)

            text = {(u, v): '{}-{}'.format(a['index1'], a['index2']) for u, v, a in mesh.edges(True)}

            plotter.draw_vertices()
            plotter.draw_faces()
            plotter.draw_edges(text=text)
            plotter.show()

        """
        edges = set()
        for fkey in self.faces():
            for u, v in self.face_halfedges(fkey):
                if (u, v) in edges or (v, u) in edges:
                    continue

                edges.add((u, v))
                edges.add((v, u))

                if u in self.edge and v in self.edge[u]:
                    # the edge (u, v) already exists in the edge dict
                    if data:
                        yield u, v, self.edge[u][v]
                    else:
                        yield u, v

                elif v in self.edge and u in self.edge[v]:
                    # the edge (v, u) already exists in the edge dict
                    if data:
                        yield v, u, self.edge[v][u]
                    else:
                        yield v, u

                else:
                    # the edge does not exist yet.
                    # therefore create the edge and yield the result.
                    if u not in self.edge:
                        self.edge[u] = {}

                    self.edge[u][v] = self.default_edge_attributes.copy()

                    if data:
                        yield u, v, self.edge[u][v]
                    else:
                        yield u, v

    def wireframe(self):
        """Iterate over the halfedges of the mesh.

        Yields
        ------
        tuple
            The next halfedge as a (u, v) tuple.

        """
        return self.halfedges()

    # --------------------------------------------------------------------------
    # special accessors
    # --------------------------------------------------------------------------

    def indexed_edges(self):
        key_index = self.key_index()
        return [(key_index[u], key_index[v]) for u, v in self.edges()]

    def indexed_face_vertices(self):
        key_index = self.key_index()
        return [[key_index[key] for key in self.face_vertices(fkey)] for fkey in self.faces()]

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    def has_vertex(self, key):
        """Verify that a vertex is in the mesh.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is in the mesh.
            False otherwise.

        """
        return key in self.vertex

    def is_vertex_connected(self, key):
        """Verify that a vertex is connected.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is connected to at least one other vertex.
            False otherwise.

        """
        return self.vertex_degree(key) > 0

    def is_vertex_on_boundary(self, key):
        """Verify that a vertex is on a boundary.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is on the boundary.
            False otherwise.

        """
        for nbr in self.halfedge[key]:
            if self.halfedge[key][nbr] is None:
                return True
        return False

    def vertex_neighbours(self, key, ordered=False):
        """Return the neighbours of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        ordered : bool, optional
            Return the neighbours in the cycling order of the faces.
            Default is false.

        Returns
        -------
        list
            The list of neighbouring vertices.
            If the vertex lies on the boundary of the mesh,
            an ordered list always starts and ends with with boundary vertices.

        Note
        ----
        Due to the nature of the ordering algorithm, the neighbours cycle around
        the node in the opposite direction as the cycling direction of the faces.
        For some algorithms this produces the expected results. For others it doesn't.
        For example, a dual mesh constructed relying on these conventions will have
        oposite face cycle directions compared to the original.

        Example
        -------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            key = 17
            nbrs = mesh.vertex_neighbours(key, ordered=True)

            plotter = MeshPlotter(mesh)

            color = {nbr: '#cccccc' for nbr in nbrs}
            color[key] = '#ff0000'

            text = {nbr: str(index) for index, nbr in enumerate(nbrs)}
            text[key] = str(key)

            plotter.draw_vertices(text=text, facecolor=color)
            plotter.draw_faces()
            plotter.draw_edges()

            plotter.show()

        """

        temp = list(self.halfedge[key])

        if not ordered:
            return temp

        if len(temp) == 1:
            return temp

        # if one of the neighbours points to the *outside* face
        # start there
        # otherwise the starting point can be random
        start = temp[0]
        for nbr in temp:
            if self.halfedge[key][nbr] is None:
                start = nbr
                break

        # start in the opposite direction
        # to avoid pointing at an *outside* face again
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
        """Return the vertices in the neighbourhood of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        ring : int, optional
            The number of neighbourhood rings to include. Default is ``1``.

        Returns
        -------
        list
            The vertices in the neighbourhood.

        Note
        ----
        The vertices in the neighbourhood are unordered.

        Example
        -------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            key = 17
            nbrs = mesh.vertex_neighbourhood(key, ring=2)

            plotter = MeshPlotter(mesh)

            color = {nbr: '#cccccc' for nbr in nbrs}
            color[key] = '#ff0000'

            text = {nbr: str(index) for index, nbr in enumerate(nbrs)}
            text[key] = str(key)

            plotter.draw_vertices(text=text, facecolor=color)
            plotter.draw_faces()
            plotter.draw_edges()

            plotter.show()

        """
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

    def vertex_degree(self, key):
        """Count the neighbours of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        int
            The degree of the vertex.

        """
        return len(self.vertex_neighbours(key))

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

    # def vertex_connected_edges(self, key):
    #     """Return the edges connected to a vertex."""
    #     edges = []
    #     for nbr in self.vertex_neighbours(key):
    #         if nbr in self.edge[key]:
    #             edges.append((key, nbr))
    #         else:
    #             edges.append((nbr, key))
    #     return edges

    def vertex_faces(self, key, ordered=False, include_none=False):
        """The faces connected to a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        ordered : bool, optional
            Return the faces in cycling order.
            Default is ``False``.
        include_none : bool, optional
            Include *outside* faces in the list.
            Default is ``False``.

        Returns
        -------
        list
            The faces connected to a vertex.

        Example
        -------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            key = 17
            nbrs = mesh.vertex_faces(key, ordered=True)

            plotter = MeshPlotter(mesh)

            plotter.draw_vertices(
                text={17: '17'},
                facecolor={17: '#ff0000'},
                radius=0.2
            )
            plotter.draw_faces(
                text={nbr: str(index) for index, nbr in enumerate(nbrs)},
                facecolor={nbr: '#cccccc' for nbr in nbrs}
            )
            plotter.draw_edges()
            plotter.show()

        """
        if not ordered:
            faces = list(self.halfedge[key].values())

        else:
            nbrs = self.vertex_neighbours(key, ordered=True)
            faces = [self.halfedge[key][n] for n in nbrs]

        if include_none:
            return faces

        return [fkey for fkey in faces if fkey is not None]

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    def has_edge(self, u, v, directed=True):
        """Verify that the mesh contains a specific edge.

        Warning
        -------
        This method may produce unexpected results.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex.
        v : hashable
            The identifier of the second vertex.
        directed : bool, optional
            Only consider directed edges.
            Default is ``True``.

        Returns
        -------
        bool
            True if the edge exists.
            False otherwise.

        """
        if directed:
            return u in self.edge and v in self.edge[u]
        else:
            return u in self.halfedge and v in self.halfedge[u]

    def edge_faces(self, u, v):
        """Find the two faces adjacent to an edge.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex.
        v : hashable
            The identifier of the second vertex.

        Returns
        -------
        tuple
            The identifiers of the adjacent faces.
            If the edge is on the bboundary, one of the identifiers is ``None``.

        """
        return self.halfedge[u][v], self.halfedge[v][u]

    # def edge_connected_edges(self, u, v):
    #     edges = []
    #     for nbr in self.vertex_neighbours(u):
    #         if nbr in self.edge[u]:
    #             edges.append((u, nbr))
    #         else:
    #             edges.append((nbr, u))
    #     for nbr in self.vertex_neighbours(v):
    #         if nbr in self.edge[v]:
    #             edges.append((v, nbr))
    #         else:
    #             edges.append((nbr, v))
    #     return edges

    def is_edge_on_boundary(self, u, v):
        """Verify that an edge is on the boundary.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex.
        v : hashable
            The identifier of the second vertex.

        Returns
        -------
        bool
            True if the edge is on the boundary.
            False otherwise.

        """
        return self.halfedge[u][v] is None or self.halfedge[v][u] is None

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    def face_vertices(self, fkey):
        """The vertices of a face.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.

        Returns
        -------
        list
            Ordered vertex identifiers.

        """
        return self.face[fkey]

    def face_halfedges(self, fkey):
        """The halfedges of a face.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.

        Returns
        -------
        list
            The halfedges of a face.

        """
        vertices = self.face_vertices(fkey)
        return list(pairwise(vertices + vertices[0:1]))

    # def face_edges(self, fkey):
    #     """Return the edges corresponding to the halfedges of a face."""
    #     edges = []
    #     for u, v in self.face_halfedges(fkey):
    #         if v in self.edge[u]:
    #             edges.append((u, v))
    #         else:
    #             edges.append((v, u))
    #     return edges

    def face_corners(self, fkey):
        """Return triplets of face vertices forming the corners of the face.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.

        Returns
        -------
        list
            The corners of the face in the form of a list of vertex triplets.

        """
        vertices = self.face_vertices(fkey)
        return list(window(vertices + vertices[0:2], 3))

    def face_neighbours(self, fkey):
        """Return the neighbours of a face across its edges.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.

        Returns
        -------
        list
            The identifiers of the neighbouring faces.

        Example
        -------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            key = 12
            nbrs = mesh.face_neighbours(key)

            text = {nbr: str(nbr) for nbr in nbrs}
            text[key] = str(key)

            color = {nbr: '#cccccc' for nbr in nbrs}
            color[key] = '#ff0000'

            plotter = MeshPlotter(mesh)
            plotter.draw_vertices()
            plotter.draw_faces(text=text, facecolor=color)
            plotter.draw_edges()
            plotter.show()

        """
        nbrs = []
        for u, v in self.face_halfedges(fkey):
            nbr = self.halfedge[v][u]
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def face_degree(self, fkey):
        """Count the neighbours of a face.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.

        Returns
        -------
        int
            The count.

        """
        return len(self.face_neighbours(fkey))

    def face_min_degree(self):
        """Compute the minimum degree of all faces.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.

        Returns
        -------
        int
            The lowest degree.

        """
        if not self.face:
            return 0
        return min(self.face_degree(fkey) for fkey in self.faces())

    def face_max_degree(self):
        """Compute the maximum degree of all faces.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.

        Returns
        -------
        int
            The highest degree.

        """
        if not self.face:
            return 0
        return max(self.face_degree(fkey) for fkey in self.faces())

    # def face_vertex_neighbours(self, fkey):
    #     """Return the neighbours of a face across its vertices.

    #     Parameters
    #     ----------
    #     fkey : hashable
    #         Identifier of the face.

    #     Returns
    #     -------
    #     list
    #         The identifiers of the neighbouring faces.

    #     Example
    #     -------
    #     .. plot::
    #         :include-source:

    #         import compas
    #         from compas.datastructures import Mesh
    #         from compas.visualization import MeshPlotter

    #         mesh = Mesh.from_obj(compas.get('faces.obj'))

    #         key = 12
    #         nbrs = mesh.face_vertex_neighbours(key)

    #         text = {nbr: str(nbr) for nbr in nbrs}
    #         text[key] = str(key)

    #         color = {nbr: '#cccccc' for nbr in nbrs}
    #         color[key] = '#ff0000'

    #         plotter = MeshPlotter(mesh)
    #         plotter.draw_vertices()
    #         plotter.draw_faces(text=text, facecolor=color)
    #         plotter.draw_edges()
    #         plotter.show()

    #     """
    #     nbrs = []
    #     for u, v in self.face_halfedges(fkey):
    #         nbr = self.halfedge[v][u]
    #         if nbr is not None:
    #             w = self.face_vertex_descendant(fkey, u)
    #             nbrs.append(self.halfedge[w][u])
    #     return nbrs

    # def face_neighbourhood(self, fkey):
    #     """Return the neighbours of a face across both edges and corners."""
    #     nbrs = []
    #     for u, v in self.face_halfedges(fkey):
    #         nbr = self.halfedge[v][u]
    #         if nbr is not None:
    #             nbrs.append(nbr)
    #             w = self.face_vertex_descendant(fkey, u)
    #             nbrs.append(self.halfedge[w][u])
    #     return nbrs

    def face_vertex_ancestor(self, fkey, key):
        """Return the vertex before the specified vertex in a specific face.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        hashable
            The identifier of the vertex before the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.

        """
        i = self.face[fkey].index(key)
        return self.face[fkey][i - 1]

    def face_vertex_descendant(self, fkey, key):
        """Return the vertex after the specified vertex in a specific face.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        hashable
            The identifier of the vertex after the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.

        """
        if self.face[fkey][-1] == key:
            return self.face[fkey][0]
        i = self.face[fkey].index(key)
        return self.face[fkey][i + 1]

    # move to algorithms
    def face_adjacency(self):
        # this function does not actually use any of the topological information
        # provided by the halfedges
        # it is used for unifying face cycles
        # so the premise is that halfedge data is not valid/reliable
        from scipy.spatial import cKDTree

        fkey_index = {fkey: index for index, fkey in enumerate(self.faces())}
        index_fkey = {index: fkey for index, fkey in enumerate(self.faces())}
        points = [self.face_centroid(fkey) for fkey in self.faces()]

        tree = cKDTree(points)

        _, closest = tree.query(points, k=10, n_jobs=-1)

        adjacency = {}

        for fkey in self.faces():
            nbrs  = []
            index = fkey_index[fkey]
            nnbrs = closest[index]
            found = set()

            for u, v in self.face_halfedges(fkey):
                for index in nnbrs:
                    nbr = index_fkey[index]

                    if nbr == fkey:
                        continue
                    if nbr in found:
                        continue

                    # if v in self.face[nbr] and u == self.face[nbr][v]:
                    # if u == self.face_vertex_descendant(nbr, v):
                    for a, b in self.face_halfedges(nbr):
                        if v == a and u == b:
                            nbrs.append(nbr)
                            found.add(nbr)
                            break

                    # if u in self.face[nbr] and v == self.face[nbr][u]:
                    # if v == self.face_vertex_descendant(nbr, u):
                    for a, b in self.face_halfedges(nbr):
                        if u == a and v == b:
                            nbrs.append(nbr)
                            found.add(nbr)
                            break

            adjacency[fkey] = nbrs

        return adjacency

    def face_adjacency_halfedge(self, f1, f2):
        """Find the half-edge over which tow faces are adjacent.

        Parameters
        ----------
        f1 : hashable
            The identifier of the first face.
        f2 : hashable
            The identifier of the second face.

        Returns
        -------
        tuple
            The half-edge separating face 1 from face 2.
        None
            If the faces are not adjacent.

        Note
        ----
        For use in form-finding algorithms, that rely on form-force duality information,
        further checks relating to the orientation of the corresponding are required.

        """
        for u, v in self.face_halfedges(f1):
            if self.halfedge[v][u] == f2:
                # if v in self.edge[u]:
                #     return u, v
                return u, v

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
            The axes alon which to take the coordinates.
            Should be a combination of ``'x'``, ``'y'``, ``'z'``.
            Default is ``'xyz'``.

        Returns
        -------
        list
            Coordinates of the vertex.

        """
        return [self.vertex[key][axis] for axis in axes]

    def vertex_area(self, key):
        """Compute the tributary area of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        float
            The tributary are.

        Example
        -------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            k_a = {key: mesh.vertex_area(key) for key in mesh.vertices()}

            plotter = MeshPlotter(mesh)
            plotter.draw_vertices(
                radius=0.2,
                text={key: '{:.1f}'.format(k_a[key]) for key in mesh.vertices()}
            )
            plotter.draw_faces()
            plotter.draw_edges()
            plotter.show()

        """
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
        """Compute the vector from a vertex to the centroid of its neighbours.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The components of the vector.

        """
        c = self.vertex_neighbourhood_centroid(key)
        p = self.vertex_coordinates(key)
        return subtract_vectors(c, p)

    def vertex_neighbourhood_centroid(self, key):
        """Compute the centroid of the neighbours of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The coordinates of the centroid.

        """
        return centroid_points([self.vertex_coordinates(nbr) for nbr in self.neighbours(key)])

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
        """Compute the coordinates of the vertices of a face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of ``'x'``, ``'y'``, ``'z'``.
            Default is ``'xyz'``.

        Returns
        -------
        list of list
            The coordinates of the vertices of the face.

        """
        return [self.vertex_coordinates(key, axes=axes) for key in self.face_vertices(fkey)]

    def face_normal(self, fkey, unitized=True):
        """Compute the normal of a face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.
        unitized : bool, optional
            Unitize the normal vector.
            Default is ``True``.

        Returns
        -------
        list
            The components of the normal vector.

        """
        return normal_polygon(self.face_coordinates(fkey), unitized=unitized)

    def face_centroid(self, fkey):
        """Compute the location of the centroid of a face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Returns
        -------
        list
            The coordinates of the centroid.

        """
        return centroid_points(self.face_coordinates(fkey))

    def face_center(self, fkey):
        """Compute the location of the center of mass of a face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Returns
        -------
        list
            The coordinates of the center of mass.

        """
        return center_of_mass_polygon(self.face_coordinates(fkey))

    def face_area(self, fkey):
        """Compute the area of a face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Returns
        -------
        float
            The area of the face.

        """
        return area_polygon(self.face_coordinates(fkey))

    # --------------------------------------------------------------------------
    # boundary
    # --------------------------------------------------------------------------

    def vertices_on_boundary(self, ordered=False):
        """Find the vertices on the boundary.

        Parameters
        ----------
        ordered : bool, optional
            If ``True``, Return the vertices in the same order as they are found on the boundary.
            Default is ``False``.

        Returns
        -------
        list
            The vertices of the boundary.

        Warning
        -------
        If the vertices are requested in order, and the mesh has multiple borders,
        currently only the vertices of one of the borders will be returned.

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
        """Find the faces on the boundary.

        Returns
        -------
        list
            The faces on the boundary.

        """
        faces = {}
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, fkey in iter(nbrs.items()):
                if fkey is None:
                    faces[self.halfedge[nbr][key]] = 1
        return faces.keys()

    def edges_on_boundary(self):
        """Find the edges on the boundary.

        Returns
        -------
        list
            The edges on the boundary.

        """
        return [(u, v) for u, v in self.edges() if self.is_edge_on_boundary(u, v)]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.visualization import MeshPlotter

    mesh = Mesh.from_obj(compas.get_data('faces.obj'))

    # data = mesh.to_data()
    # mesh = Mesh.from_data(data)

    # mesh.summary()

    # print(mesh.is_valid())
    # print(mesh.is_connected())

    # mesh.delete_vertex(17)
    # mesh.delete_vertex(18)
    # mesh.delete_vertex(0)

    # mesh.cull_vertices()

    # key, fkeys = mesh.insert_vertex(12, return_fkeys=True)

    # mesh.delete_face(12)

    # for w, e in zip(list(mesh.wireframe()), list(mesh.edges())):
    #     print(w, e, w == e)

    # plotter = MeshPlotter(mesh, figsize=(10, 7))

    # plotter.defaults['face.facecolor'] = '#eeeeee'
    # plotter.defaults['face.edgewidth'] = 0.0

    # plotter.draw_vertices(
    #     radius=0.2,
    #     facecolor={key: '#ff0000' for key in mesh.vertices() if mesh.vertex_degree(key) == 2}
    # )

    # plotter.draw_faces()
    # plotter.draw_edges()

    # plotter.show()

    # key = 17
    # nbrs = mesh.vertex_faces(key, ordered=True)

    # plotter = MeshPlotter(mesh)

    # plotter.draw_vertices(text={17: '17'}, facecolor={17: '#ff0000'}, radius=0.2)
    # plotter.draw_faces(text={nbr: str(index) for index, nbr in enumerate(nbrs)}, facecolor={nbr: '#cccccc' for nbr in nbrs})
    # plotter.draw_edges()
    # plotter.show()

    # for index, (u, v, attr) in enumerate(mesh.edges(True)):
    #     attr['index1'] = index

    # for index, (u, v, attr) in enumerate(mesh.edges(True)):
    #     attr['index2'] = index

    # plotter = MeshPlotter(mesh)

    # text = {(u, v): '{}-{}'.format(a['index1'], a['index2']) for u, v, a in mesh.edges(True)}

    # plotter.draw_vertices()
    # plotter.draw_faces()
    # plotter.draw_edges(text=text)
    # plotter.show()

    # key = 12
    # nbrs = mesh.face_neighbours(key)

    # text = {nbr: str(nbr) for nbr in nbrs}
    # text[key] = str(key)

    # color = {nbr: '#cccccc' for nbr in nbrs}
    # color[key] = '#ff0000'

    # plotter = MeshPlotter(mesh)
    # plotter.draw_vertices()
    # plotter.draw_faces(text=text, facecolor=color)
    # plotter.draw_edges()
    # plotter.show()

    k_a = {key: mesh.vertex_area(key) for key in mesh.vertices()}

    plotter = MeshPlotter(mesh)
    plotter.draw_vertices(radius=0.2, text={key: '{:.1f}'.format(k_a[key]) for key in mesh.vertices()})
    plotter.draw_faces()
    plotter.draw_edges()
    plotter.show()
