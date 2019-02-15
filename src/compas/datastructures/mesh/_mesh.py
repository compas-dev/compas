from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import pickle
import json
import collections

from copy import deepcopy
from ast import literal_eval

from math import pi

from compas.utilities import average

from compas.files import OBJ
from compas.files import PLY
from compas.files import STL
from compas.files import OFF

from compas.utilities import pairwise
from compas.utilities import window
from compas.utilities import geometric_key

from compas.geometry import normalize_vector
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import cross_vectors
from compas.geometry import length_vector
from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import sum_vectors
from compas.geometry import subtract_vectors
from compas.geometry import normal_polygon
from compas.geometry import area_polygon
from compas.geometry import flatness
from compas.geometry import Polyhedron
from compas.geometry import angle_points
from compas.geometry import bestfit_plane
from compas.geometry import distance_point_plane
from compas.geometry import distance_point_point

from compas.datastructures import Datastructure

from compas.datastructures._mixins import VertexAttributesManagement
from compas.datastructures._mixins import VertexHelpers
from compas.datastructures._mixins import VertexFilter

from compas.datastructures._mixins import EdgeHelpers
from compas.datastructures._mixins import EdgeGeometry
from compas.datastructures._mixins import EdgeFilter

from compas.datastructures._mixins import FaceAttributesManagement
from compas.datastructures._mixins import FaceHelpers
from compas.datastructures._mixins import FaceFilter

from compas.datastructures._mixins import FromToData
from compas.datastructures._mixins import FromToJson
from compas.datastructures._mixins import FromToPickle

from compas.datastructures._mixins import VertexMappings
from compas.datastructures._mixins import EdgeMappings
from compas.datastructures._mixins import FaceMappings


__all__ = ['Mesh']


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

class Mesh(FromToPickle,
           FromToJson,
           FromToData,
           EdgeGeometry,
           FaceHelpers,
           FaceFilter,
           EdgeHelpers,
           VertexHelpers,
           VertexFilter,
           EdgeFilter,
           FaceMappings,
           EdgeMappings,
           VertexMappings,
           FaceAttributesManagement,
           VertexAttributesManagement,
           Datastructure):
    """Definition of a mesh.

    Attributes
    ----------
    attributes : dict
        A dictionary of general mesh attributes.
        The following items are built in:

        * ``'name'`` : ``'Mesh'``

    default_vertex_attributes : dict
        The default data attributes assigned to every new vertex.
        The following items are built in:

        * ``'x'`` : ``0.0``,
        * ``'y'`` : ``0.0``,
        * ``'z'`` : ``0.0``,

    default_edge_attributes : dict
        The default data attributes assigned to every new edge.
    default_face_attributes : dict
        The default data attributes assigned to every new face.
    name : str
        The name of the mesh.
        Shorthand for ``mesh.attributes['name'] = 'Mesh'``
    adjacency : dict, **read-only**
        The vertex adjacency dictionary.
    data : dict
        The data representing the mesh.
        The dict has the following structure:

        * 'attributes'   => dict
        * 'dva'          => dict
        * 'dea'          => dict
        * 'dfa'          => dict
        * 'vertex'       => dict
        * 'face'         => dict
        * 'facedata'     => dict
        * 'edgedata'     => dict
        * 'max_int_key'  => int
        * 'max_int_fkey' => int

    Examples
    --------
    .. plot::
        :include-source:

        import compas
        from compas.datastructures import Mesh

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        mesh.plot(
            vertextext={key: key for key in mesh.vertices()},
            vertexcolor={key: '#ff0000' for key in mesh.vertices_where({'vertex_degree': 2})},
            vertexsize=0.2
        )

    """

    __module__ = 'compas.datastructures'

    def __init__(self):
        super(Mesh, self).__init__()
        self._key_to_str = False
        self._max_int_key = -1
        self._max_int_fkey = -1
        self.vertex = {}
        self.halfedge = {}
        self.face = {}
        self.facedata = {}
        self.edgedata = {}
        self.attributes = {'name' : 'Mesh'}
        self.default_vertex_attributes = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.default_edge_attributes = {}
        self.default_face_attributes = {}

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

    def __str__(self):
        """Generate a readable representation of the data of the mesh."""
        return json.dumps(self.data, sort_keys=True, indent=4)

    def summary(self):
        """Print a summary of the mesh."""
        numv = self.number_of_vertices()
        nume = self.number_of_edges()
        numf = self.number_of_faces()
        vmin = self.vertex_min_degree()
        vmax = self.vertex_max_degree()
        fmin = self.face_min_degree()
        fmax = self.face_max_degree()
        s = TPL.format(self.name, numv, nume, numf, vmin, vmax, fmin, fmax)
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
        return self.attributes.get('name') or self.__class__.__name__

    @name.setter
    def name(self, value):
        self.attributes['name'] = value

    @property
    def adjacency(self):
        return self.halfedge

    @property
    def data(self):
        """dict : A data dict representing the mesh data structure for serialisation.

        The dict has the following structure:

        * 'attributes'   => dict
        * 'dva'          => dict
        * 'dea'          => dict
        * 'dfa'          => dict
        * 'vertex'       => dict
        * 'face'         => dict
        * 'facedata'     => dict
        * 'edgedata'     => dict
        * 'max_int_key'  => int
        * 'max_int_fkey' => int

        Note
        ----
        All dictionary keys are converted to their representation value (``repr(key)``)
        to ensure compatibility of all allowed key types with the JSON serialisation
        format, which only allows for dict keys that are strings.

        """
        data = {'attributes'  : self.attributes,
                'dva'         : self.default_vertex_attributes,
                'dea'         : self.default_edge_attributes,
                'dfa'         : self.default_face_attributes,
                'vertex'      : {},
                'face'        : {},
                'facedata'    : {},
                'edgedata'    : {},
                'max_int_key' : self._max_int_key,
                'max_int_fkey': self._max_int_fkey, }

        for key in self.vertex:
            data['vertex'][repr(key)] = self.vertex[key]

        for fkey in self.face:
            data['face'][repr(fkey)] = [repr(key) for key in self.face[fkey]]

        for fkey in self.facedata:
            data['facedata'][repr(fkey)] = self.facedata[fkey]

        for uv in self.edgedata:
            data['edgedata'][repr(uv)] = self.edgedata[uv]

        return data

    @data.setter
    def data(self, data):
        attributes   = data.get('attributes') or {}
        dva          = data.get('dva') or {}
        dfa          = data.get('dfa') or {}
        dea          = data.get('dea') or {}
        vertex       = data.get('vertex') or {}
        face         = data.get('face') or {}
        facedata     = data.get('facedata') or {}
        edgedata     = data.get('edgedata') or {}
        max_int_key  = data.get('max_int_key', -1)
        max_int_fkey = data.get('max_int_fkey', -1)

        self.attributes.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_face_attributes.update(dfa)
        self.default_edge_attributes.update(dea)

        self.clear()

        for key, attr in iter(vertex.items()):
            self.add_vertex(literal_eval(key), attr_dict=attr)

        for fkey, vertices in iter(face.items()):
            attr = facedata.get(fkey) or {}
            vertices = [literal_eval(k) for k in vertices]
            self.add_face(vertices, fkey=literal_eval(fkey), attr_dict=attr)

        for uv, attr in iter(edgedata.items()):
            self.edgedata[literal_eval(uv)] = attr or {}

        self._max_int_key = max_int_key
        self._max_int_fkey = max_int_fkey

    # --------------------------------------------------------------------------
    # serialisation
    # --------------------------------------------------------------------------

    def dump(self, filepath):
        """Dump the data representing the mesh to a file using Python's built-in
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
            'dfa'         : self.default_face_attributes,
            'vertex'      : self.vertex,
            'face'        : self.face,
            'facedata'    : self.facedata,
            'edgedata'    : self.edgedata,
            'max_int_key' : self._max_int_key,
            'max_int_fkey': self._max_int_fkey,
        }
        with open(filepath, 'wb+') as fo:
            pickle.dump(data, fo, protocol=pickle.HIGHEST_PROTOCOL)

    def dumps(self):
        """Dump the data representing the mesh to a string using Python's built-in
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
            'dfa'         : self.default_face_attributes,
            'vertex'      : self.vertex,
            'face'        : self.face,
            'facedata'    : self.facedata,
            'edgedata'    : self.edgedata,
            'max_int_key' : self._max_int_key,
            'max_int_fkey': self._max_int_fkey,
        }
        return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, filepath):
        """Load serialised mesh data from a pickle file.

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
        self.default_face_attributes = data['dfa']
        self.vertex = data['vertex']
        self.face = data['face']
        self.edgedata = data['edgedata']
        self.facedata = data['facedata']
        self._max_int_key = data['max_int_key']
        self._max_int_fkey = data['max_int_fkey']

    def loads(self, s):
        """Load serialised mesh data from a pickle string.

        Parameters
        ----------
        s : str
            The pickled string.

        """
        data = pickle.loads(s)

        self.attributes = data['attributes']
        self.default_vertex_attributes = data['dva']
        self.default_edge_attributes = data['dea']
        self.default_face_attributes = data['dfa']
        self.vertex = data['vertex']
        self.face = data['face']
        self.edgedata = data['edgedata']
        self.facedata = data['facedata']
        self._max_int_key = data['max_int_key']
        self._max_int_fkey = data['max_int_fkey']

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath, precision=None):
        """Construct a mesh object from the data described in an OBJ file.

        Parameters
        ----------
        filepath : str
            The path to the file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Mesh
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
        .. code-block:: python

            import compas
            from compas.datastructures import Mesh

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            mesh.plot()

        """
        obj = OBJ(filepath, precision)
        vertices = obj.parser.vertices
        faces    = obj.parser.faces
        edges    = obj.parser.lines
        if faces:
            return cls.from_vertices_and_faces(vertices, faces)
        if edges:
            lines = [(vertices[u], vertices[v], 0) for u, v in edges]
            return cls.from_lines(lines)

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
        .. code-block:: python

            import compas
            from compas.datastructures import Mesh

            mesh = Mesh.from_obj(compas.get('bunny.ply'))

        """
        ply = PLY(filepath)
        vertices = ply.parser.vertices
        faces    = ply.parser.faces
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    @classmethod
    def from_stl(cls, filepath):
        """Construct a mesh object from the data described in a STL file.

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

        * cube_ascii.stl
        * cube_binary.stl

        Examples
        --------
        .. code-block:: python

            import compas
            from compas.datastructures import Mesh

            mesh = Mesh.from_stl(compas.get('cube_ascii.stl'))

        """
        stl = STL(filepath)
        vertices = stl.parser.vertices
        faces = stl.parser.faces
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    @classmethod
    def from_off(cls, filepath):
        """Construct a mesh object from the data described in a STL file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        Mesh :
            A mesh object.

        Examples
        --------
        .. code-block:: python

            import compas
            from compas.datastructures import Mesh

            mesh = Mesh.from_stl(compas.get('cube_ascii.stl'))

        """
        off = OFF(filepath)
        vertices = off.reader.vertices
        faces = off.reader.faces
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    def leaves(self):
        leaves = []
        for key in self.halfedge:
            nbrs = self.halfedge[key]
            if len(nbrs) == 1:
                leaves.append(key)
        return leaves

    @classmethod
    def from_lines(cls, lines, delete_boundary_face=False, precision=None):
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
        Mesh
            A mesh object.

        Examples
        --------
        .. code-block:: python

            import json

            import compas
            from compas.datastructures import Mesh

            with open(compas.get('lines.json'), 'r') as fo:
                lines = json.load(fo)

            mesh = Mesh.from_lines(lines)

        """
        from compas.datastructures import Network
        from compas.datastructures import network_find_faces

        network = Network.from_lines(lines, precision=precision)

        mesh = cls()

        for key, attr in network.vertices(True):
            mesh.add_vertex(key, x=attr['x'], y=attr['y'], z=attr['z'])

        mesh.halfedge = network.halfedge

        network_find_faces(mesh)

        if delete_boundary_face:
            mesh.delete_face(0)

        return mesh

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces):
        """Construct a mesh object from a list of vertices and faces.

        Parameters
        ----------
        vertices : list, dict
            A list of vertices, represented by their XYZ coordinates,
            or a dictionary of vertex keys pointing to their XYZ coordinates.
        faces : list, dict
            A list of faces, represented by a list of indices referencing the list of vertex coordinates,
            or a dictionary of face keys pointing to a list of indices referencing the list of vertex coordinates.

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        .. code-block:: python

            import compas
            from compas.datastructures import Mesh

            vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]]
            faces = [[0, 1, 2]]

            mesh = Mesh.from_vertices_and_faces(vertices, faces)

        """
        mesh = cls()

        if isinstance(vertices, collections.Mapping):
            for key, xyz in vertices.items():
                mesh.add_vertex(key = key, attr_dict = {i: j for i, j in zip(['x', 'y', 'z'], xyz)})
        else:
            for x, y, z in iter(vertices):
                mesh.add_vertex(x=x, y=y, z=z)

        if isinstance(faces, collections.Mapping):
            for fkey, vertices in faces.items():
                mesh.add_face(vertices, fkey)
        else:
            for face in iter(faces):
                mesh.add_face(face)

        return mesh

    @classmethod
    def from_polyhedron(cls, f):
        """Construct a mesh from a platonic solid.

        Parameters
        ----------
        f : int
            The number of faces.
            Should be one of ``4, 6, 8, 12, 20``.

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        .. code-block:: python

            import compas
            from compas.datastructures import Mesh

            mesh = Mesh.from_polyhedron(8)

        """
        p = Polyhedron.generate(f)
        return cls.from_vertices_and_faces(p.vertices, p.faces)

    @classmethod
    def from_points(cls, points, boundary=None, holes=None):
        """Construct a mesh from a delaunay triangulation of a set of points.

        Parameters
        ----------
        points : list
            XYZ coordinates of the points.
            Z coordinates should be zero.

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        .. code-block:: python

            pass

        """
        from compas.topology import delaunay_from_points
        faces = delaunay_from_points(points, boundary=boundary, holes=holes)
        return cls.from_vertices_and_faces(points, faces)

    @classmethod
    def from_polygons(cls, polygons, precision=None):
        """Construct a mesh from a series of polygons.

        Parameters
        ----------
        polygons : list
            A list of polygons, with each polygon defined as an ordered list of
            XYZ coordinates of its corners.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Mesh
            A mesh object.

        """
        faces = []
        gkey_xyz = {}

        for points in polygons:
            face = []
            for xyz in points:
                gkey = geometric_key(xyz, precision=precision)
                gkey_xyz[gkey] = xyz
                face.append(gkey)
            faces.append(face)

        gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz)}
        vertices = gkey_xyz.values()
        faces[:] = [[gkey_index[gkey] for gkey in face] for face in faces]

        return cls.from_vertices_and_faces(vertices, faces)

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
        .. code-block:: python

            pass

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
        .. code-block:: python

            pass

        """
        key_index = self.key_index()
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [[key_index[key] for key in self.face_vertices(fkey)] for fkey in self.faces()]
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
        del self.edgedata
        del self.halfedge
        del self.face
        del self.facedata
        self.vertex   = {}
        self.edgedata = {}
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

        Examples
        --------
        >>> mesh.add_vertex()
        0
        >>> mesh.add_vertex(x=0, y=0, z=0)
        1
        >>> mesh.add_vertex(key=2)
        2
        >>> mesh.add_vertex(key=0, x=1)
        0

        """
        attr = self._compile_vattr(attr_dict, kwattr)
        key = self._get_vertex_key(key)

        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}

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
            from compas.plotters import MeshPlotter

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
            from compas.plotters import MeshPlotter

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
        nbrs = self.vertex_neighbors(key)
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
            for n in self.vertex_neighbors(nbr):
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
            from compas.plotters import MeshPlotter

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
            from compas.plotters import MeshPlotter

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

    # to be updated
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

    def is_manifold(self):
        """Verify that the mesh is manifold.

        A mesh is manifold if the following conditions are fulfilled:

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

            if list(self.halfedge[key].values()).count(None) > 1:
                return False

            nbrs = self.vertex_neighbors(key, ordered=True)

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

    def is_empty(self):
        """Boolean whether the mesh is empty.

        Parameters
        ----------

        Returns
        -------
        bool
            True if no vertices. False otherwise.
        """

        if self.number_of_vertices() == 0:
            return True

        return False

    def euler(self):
        """Calculate the Euler characterisic.

        Parameters
        ----------

        Returns
        -------
        int
            The Euler chracteristic.
        """

        V = len([vkey for vkey in self.vertices() if len(self.vertex_neighbors(vkey)) != 0])
        E = self.number_of_edges()
        F = self.number_of_faces()

        return V - E + F

    def genus(self):
        """Calculate the genus.

        Parameters
        ----------

        Returns
        -------
        int
            The genus.

         References
        ----------
        .. [1] Wolfram MathWorld. *Genus*.
               Available at: http://mathworld.wolfram.com/Genus.html.

        """

        X = self.euler()

        # each boundary must be taken into account as if it was one face
        B = len(self.boundaries())

        if mesh.is_orientable:
            return (2 - (X + B)) / 2
        else:
            return 2 - (X + B)

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
        for key in self.vertex:
            if data:
                yield key, self.vertex[key]
            else:
                yield key

    def faces(self, data=False):
        """Iterate over the faces of the mesh.

        Parameters
        ----------
        data : bool, optional
            Return the face data as well as the face keys.

        Yields
        ------
        hashable
            The next face identifier (*key*), if ``data`` is ``False``.
        2-tuple
            The next face as a (fkey, attr) tuple, if ``data`` is ``True``.

        """
        for fkey in self.face:
            if data:
                yield fkey, self.facedata.setdefault(fkey, self.default_face_attributes.copy())
            else:
                yield fkey

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
            from compas.plotters import MeshPlotter

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

        for u in self.halfedge:
            for v in self.halfedge[u]:

                if (u, v) in edges or (v, u) in edges:
                    continue

                edges.add((u, v))
                edges.add((v, u))

                if (u, v) in self.edgedata:
                    attr = self.edgedata[v, u] = self.edgedata[u, v]
                elif (v, u) in self.edgedata:
                    attr = self.edgedata[u, v] = self.edgedata[v, u]
                else:
                    attr = self.edgedata[u, v] = self.edgedata[v, u] = self.default_edge_attributes.copy()

                if data:
                    yield u, v, attr
                else:
                    yield u, v

    # --------------------------------------------------------------------------
    # special accessors
    # --------------------------------------------------------------------------

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

    def vertex_neighbors(self, key, ordered=False):
        """Return the neighbors of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        ordered : bool, optional
            Return the neighbors in the cycling order of the faces.
            Default is false.

        Returns
        -------
        list
            The list of neighboring vertices.
            If the vertex lies on the boundary of the mesh,
            an ordered list always starts and ends with with boundary vertices.

        Note
        ----
        Due to the nature of the ordering algorithm, the neighbors cycle around
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
            from compas.plotters import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            key = 17
            nbrs = mesh.vertex_neighbors(key, ordered=True)

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

        if not temp:
            return temp

        if len(temp) == 1:
            return temp

        # if one of the neighbors points to the *outside* face
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

    def vertex_neighborhood(self, key, ring=1):
        """Return the vertices in the neighborhood of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        ring : int, optional
            The number of neighborhood rings to include. Default is ``1``.

        Returns
        -------
        list
            The vertices in the neighborhood.

        Note
        ----
        The vertices in the neighborhood are unordered.

        Example
        -------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.plotters import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            key = 17
            nbrs = mesh.vertex_neighborhood(key, ring=2)

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

    def vertex_degree(self, key):
        """Count the neighbors of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        int
            The degree of the vertex.

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
            from compas.plotters import MeshPlotter

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
            nbrs = self.vertex_neighbors(key, ordered=True)
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
            return (u, v) in self.edgedata
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
    # polyedge topology
    # --------------------------------------------------------------------------

    def boundaries(self):
        """Collect the mesh boundaries as lists of vertices.

        Parameters
        ----------
        mesh : Mesh
            Mesh.

        Returns
        -------
        boundaries : list
            List of boundaries as lists of vertex keys.

        """

        boundaries = []

        # get all boundary edges pointing outwards
        boundary_edges = {u: v for u, v in self.edges_on_boundary()}

        # start new boundary
        while len(boundary_edges) > 0:
            boundary = list(boundary_edges.popitem())

            # get consecuvite vertex until the boundary is closed
            while boundary[0] != boundary[-1]:
                boundary.append(boundary_edges[boundary[-1]])
                boundary_edges.pop(boundary[-2])

            boundaries.append(boundary[: -1])

        return boundaries

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

    def face_neighbors(self, fkey):
        """Return the neighbors of a face across its edges.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.

        Returns
        -------
        list
            The identifiers of the neighboring faces.

        Example
        -------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh
            from compas.plotters import MeshPlotter

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            key = 12
            nbrs = mesh.face_neighbors(key)

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
        """Count the neighbors of a face.

        Parameters
        ----------
        fkey : hashable
            Identifier of the face.

        Returns
        -------
        int
            The count.

        """
        return len(self.face_neighbors(fkey))

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

    def face_adjacency_halfedge(self, f1, f2):
        """Find one half-edge over which two faces are adjacent.

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
                return u, v

    def face_adjacency_vertices(self, f1, f2):
        """Find all vertices over which two faces are adjacent.

        Parameters
        ----------
        f1 : hashable
            The identifier of the first face.
        f2 : hashable
            The identifier of the second face.

        Returns
        -------
        list
            The vertices separating face 1 from face 2.
        None
            If the faces are not adjacent.

        """

        return [vkey for vkey in self.face_vertices(f1) if vkey in self.face_vertices(f2)]

    def is_face_on_boundary(self, key):
        """Verify that a face is on a boundary.

        Parameters
        ----------
        key : hashable
            The identifier of the face.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.

        """
        a = [self.halfedge[v][u] for u, v in self.face_halfedges(key)]
        if None in a:
            return True
        else:
            return False
    # --------------------------------------------------------------------------
    # mesh geometry
    # --------------------------------------------------------------------------

    def area(self):
        """Calculate the total mesh area.

        Parameters
        ----------

        Returns
        -------
        float
            The area.
        """

        return sum(self.face_area(fkey) for fkey in self.faces())

    def centroid(self):
        """Calculate the mesh centroid.

        Parameters
        ----------

        Returns
        -------
        list
            The coordinates of the mesh centroid.
        """

        return scale_vector(sum_vectors([scale_vector(self.face_centroid(fkey), self.face_area(fkey)) for fkey in self.faces()]), 1. / self.area())

    def normal(self):
        """Calculate the average mesh normal.

        Parameters
        ----------

        Returns
        -------
        list
            The coordinates of the mesh normal.
        """

        return scale_vector(sum_vectors([scale_vector(self.face_normal(fkey), self.face_area(fkey)) for fkey in self.faces()]), 1. / self.area())

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
            from compas.plotters import MeshPlotter

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
        area = 0.

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
        """Compute the vector from a vertex to the centroid of its neighbors.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The components of the vector.

        """
        c = self.vertex_neighborhood_centroid(key)
        p = self.vertex_coordinates(key)
        return subtract_vectors(c, p)

    def vertex_neighborhood_centroid(self, key):
        """Compute the centroid of the neighbors of a vertex.

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

    def vertex_normal(self, key):
        """Return the normal vector at the vertex as the weighted average of the
        normals of the neighboring faces.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The components of the normal vector.

        """
        vectors = [self.face_normal(fkey, False) for fkey in self.vertex_faces(key) if fkey is not None]
        return normalize_vector(centroid_points(vectors))

    def vertex_curvature(self, vkey):
        """Dimensionless vertex curvature.

        Parameters
        ----------
        fkey : Key
            The face key.

        Returns
        -------
        float
            The dimensionless curvature.

        References
        ----------
        .. [1] Botsch, Mario, et al. *Polygon mesh processing.* AK Peters/CRC Press, 2010.

        """

        return 2 * pi - sum([angle_points(mesh.vertex_coordinates(vkey), mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)) for u, v in pairwise(self.vertex_neighbors(vkey, ordered = True) + self.vertex_neighbors(vkey, ordered = True)[:1])])

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
        return centroid_polygon(self.face_coordinates(fkey))

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

    def face_flatness(self, fkey):
        """Compute the flatness of the mesh face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Returns
        -------
        float
            The flatness.

        Note
        ----
        Flatness is computed as the ratio of the distance between the diagonals
        of the face to the average edge length. A practical limit on this value
        realted to manufacturing is 0.02 (2%).

        Warning
        -------
        This method only makes sense for quadrilateral faces.

        """
        vertices = self.face_coordinates(fkey)
        face = range(len(self.face_vertices(fkey)))
        return flatness(vertices, [face])[0]

    def face_aspect_ratio(self, fkey):
        """Face aspect ratio as the ratio between the lengths of the maximum and minimum face edges.

        Parameters
        ----------
        fkey : Key
            The face key.

        Returns
        -------
        float
            The aspect ratio.

         References
        ----------
        .. [1] Wikipedia. *Types of mesh*.
               Available at: https://en.wikipedia.org/wiki/Types_of_mesh.

        """

        face_edge_lengths = [self.edge_length(u, v) for u, v in self.face_halfedges(fkey)]
        return max(face_edge_lengths) / min(face_edge_lengths)

    def face_skewness(self, fkey):
        """Face skewness as the maximum absolute angular deviation from the ideal polygon angle.

        Parameters
        ----------
        fkey : Key
            The face key.

        Returns
        -------
        float
            The skewness.

         References
        ----------
        .. [1] Wikipedia. *Types of mesh*.
               Available at: https://en.wikipedia.org/wiki/Types_of_mesh.

        """

        ideal_angle = 180 * (1 - 2 / float(len(self.face_vertices(fkey))))

        angles = [angle_points(self.vertex_coordinates(v), self.vertex_coordinates(u), self.vertex_coordinates(w), deg = True) for u, v, w in window(self.face_vertices(fkey) + self.face_vertices(fkey)[:2], n = 3)]

        return max((max(angles) - ideal_angle) / (180 - ideal_angle), (ideal_angle - min(angles)) / ideal_angle)

    def face_curvature(self, fkey):
        """Dimensionless face curvature as the maximum face vertex deviation from the best-fit plane of the face vertices divided by the average lengths of the face vertices to the face centroid.

        Parameters
        ----------
        fkey : Key
            The face key.

        Returns
        -------
        float
            The dimensionless curvature.

        """

        plane = bestfit_plane([self.vertex_coordinates(vkey) for vkey in self.vertices()])

        max_deviation = max([distance_point_plane(self.vertex_coordinates(vkey), plane) for vkey in self.vertices()])

        average_distances = average([distance_point_point(self.vertex_coordinates(vkey), self.face_centroid(fkey)) for vkey in self.vertices()])

        return max_deviation / average_distances

    # def face_circle(self, fkey):
    #     pass

    # def face_frame(self, fkey):
    #     pass

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

        key = sorted([(key, self.vertex_coordinates(key)) for key in vertices], key=lambda x: (x[1][1], x[1][0]))[0][0]

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

    def vertices_on_boundaries(self):
        """Find the vertices on all boundaries of the mesh.

        Returns
        -------
        list of list
            A list of vertex keys per boundary.

        Examples
        --------
        >>>

        """
        vertices_set = set()
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, face in iter(nbrs.items()):
                if face is None:
                    vertices_set.add(key)
                    vertices_set.add(nbr)

        vertices_all = list(vertices_set)
        boundaries = []

        key = sorted([(key, self.vertex_coordinates(key)) for key in vertices_all], key=lambda x: (x[1][1], x[1][0]))[0][0]

        while vertices_all:
            vertices = []
            start = key
            while 1:
                for nbr, fkey in iter(self.halfedge[key].items()):
                    if fkey is None:
                        vertices.append(nbr)
                        key = nbr
                        break
                if key == start:
                    boundaries.append(vertices)
                    vertices_all = [x for x in vertices_all if x not in vertices]
                    break
            if vertices_all:
                key = vertices_all[0]

        return boundaries

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

    def edges_on_boundary(self, oriented = True):
        """Find the edges on the boundary.

        Parameters
        ----------
        oriented : bool
            Boolean whether the boundary edges should point outwards.

        Returns
        -------
        boundary_edges : list
            The boundary edges.


        """

        boundary_edges =  [(u, v) for u, v in self.edges() if self.is_edge_on_boundary(u, v)]

        if not oriented:
            return boundary_edges

        else:
            return [(v, u) if self.halfedge[u][v] is not None else (u, v) for u, v in boundary_edges]


    # --------------------------------------------------------------------------
    # attributes
    # --------------------------------------------------------------------------

    def update_default_edge_attributes(self, attr_dict=None, **kwattr):
        """Update the default edge attributes (this also affects already existing edges).

        Parameters
        ----------
        attr_dict : dict (None)
            A dictionary of attributes with their default values.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Notes
        -----
        Named arguments overwrite correpsonding key-value pairs in the attribute dictionary,
        if they exist.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        for u, v, data in self.edges(True):
            attr = deepcopy(attr_dict)
            attr.update(data)
            self.edgedata[u, v] = self.edgedata[v, u] = attr
        self.default_edge_attributes.update(attr_dict)

    def set_edge_attribute(self, key, name, value):
        """Set one attribute of one edge.

        Parameters
        ----------
        key : tuple of hashable
            The identifier of the edge, in the form of a pair of vertex identifiers.
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.

        """
        u, v = key
        if (u, v) not in self.edgedata:
            self.edgedata[u, v] = self.default_edge_attributes.copy()
        if (v, u) in self.edgedata:
            self.edgedata[u, v].update(self.edgedata[v, u])
            del self.edgedata[v, u]
            self.edgedata[v, u] = self.edgedata[u, v]
        self.edgedata[u, v][name] = value

    def set_edge_attributes(self, key, names, values):
        """Set multiple attributes of one edge.

        Parameters
        ----------
        key : tuple of hashable
            The identifier of the edge, in the form of a pair of vertex identifiers.
        names : list of str
            The names of the attributes.
        values : list of object
            The values of the attributes.

        """
        for name, value in zip(names, values):
            self.set_edge_attribute(key, name, value)

    def set_edges_attribute(self, name, value, keys=None):
        """Set one attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.
        keys : list of hashable, optional
            A list of edge identifiers.
            Each edge identifier is a pair of vertex identifiers.
            Defaults to all edges.

        """
        if not keys:
            keys = self.edges()
        for key in keys:
            self.set_edge_attribute(key, name, value)

    def set_edges_attributes(self, names, values, keys=None):
        """Set multiple attributes of multiple edges.

        Parameters
        ----------
        names : list of str
            The names of the attributes.
        values : list of object
            The values of the attributes.
        keys : list of hashable, optional
            A list of edge identifiers.
            Each edge identifier is a pair of vertex identifiers.
            Defaults to all edges.

        """
        for name, value in zip(names, values):
            self.set_edges_attribute(name, value, keys=keys)

    def get_edge_attribute(self, key, name, value=None):
        """Get the value of a named attribute of one edge.

        Parameters
        ----------
        key : tuple of hashable
            The identifier of the edge, in the form of a pair of vertex identifiers.
        name : str
            The name of the attribute.
        value : object (None)
            The default value.

        Returns
        -------
        value
            The value of the attribute,
            or the default value if the attribute does not exist.

        """
        u, v = key
        if (u, v) in self.edgedata:
            return self.edgedata[u, v].get(name, value)
        if (v, u) in self.edgedata:
            return self.edgedata[v, u].get(name, value)
        self.edgedata[u, v] = self.edgedata[v, u] = self.default_edge_attributes.copy()
        return self.edgedata[u, v].get(name, value)

    def get_edge_attributes(self, key, names, values=None):
        """Get the value of a named attribute of one edge.

        Parameters
        ----------
        key : tuple of hashable
            The identifier of the edge, in the form of a pair of vertex identifiers.
        names : list
            A list of attribute names.
        values : list, optional
            A list of default values.
            Defaults to a list of ``None``.

        Returns
        -------
        values : list
            A list of values.
            Every attribute that does not exist is replaced by the corresponding
            default value.

        """
        if not values:
            values = [None] * len(names)

        return [self.get_edge_attribute(key, name, value) for name, value in zip(names, values)]

    def get_edges_attribute(self, name, value=None, keys=None):
        """Get the value of a named attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object (None)
            The default value.
        keys : iterable (None)
            A list of edge identifiers.
            Each edge identifier is a pair of vertex identifiers.
            Defaults to all edges.

        Returns
        -------
        values : list
            A list of values of the named attribute of the specified edges.

        """
        if not keys:
            keys = self.edges()

        return [self.get_edge_attribute(key, name, value) for key in keys]

    def get_edges_attributes(self, names, values=None, keys=None):
        """Get the values of multiple named attribute of multiple edges.

        Parameters
        ----------
        names : list
            The names of the attributes.
        values : list, optional
            A list of default values.
            Defaults to a list of ``None``.
        keys : list of hashable, optional
            A list of edge identifiers.
            Each edge identifier is a pair of vertex identifiers.
            Defaults to all edges.

        Returns
        -------
        values: list of list
            The values of the attributes of the specified edges.
            If an attribute does not exist for a specific edge, it is replaced
            by the default value.

        """
        if not keys:
            keys = self.edges()

        return [self.get_edge_attributes(key, names, values) for key in keys]

    # --------------------------------------------------------------------------
    # visualisation
    # --------------------------------------------------------------------------

    def plot(self,
             vertexcolor=None,
             edgecolor=None,
             facecolor=None,
             vertexsize=None,
             edgewidth=None,
             vertextext=None,
             edgetext=None,
             facetext=None):
        """Plot a 2D representation of the mesh.

        Parameters
        ----------
        vertexcolor : dict, optional
            A dictionary mapping vertex identifiers to colors.
        edgecolor : dict, optional
            A dictionary mapping edge identifiers to colors.
        facecolor : dict, optional
            A dictionary mapping face identifiers to colors.
        vertexsize : dict, optional
            A dictionary mapping vertex identifiers to sizes.
        edgewidth : dict, optional
            A dictionary mapping edge identifiers to widths.
        vertextext : dict, optional
            A dictionary mappping vertex identifiers to labels.
        edgetext : dict, optional
            A dictionary mappping edge identifiers to labels.
        facetext : dict, optional
            A dictionary mappping face identifiers to labels.

        Examples
        --------
        .. plot::
            :include-source:

            import compas
            from compas.datastructures import Mesh

            mesh = Mesh.from_obj(compas.get('faces.obj'))

            mesh.plot()

        """
        from compas.plotters import MeshPlotter

        plotter = MeshPlotter(self)
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
        plotter.draw_faces(
            facecolor=facecolor,
            text=facetext
        )
        plotter.show()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas
    from compas.plotters import MeshPlotter

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh.update_default_edge_attributes({'q': 1.0})

    # vertices = [
    #     [0, 0, 0],
    #     [1, 1, 0],
    #     [1, -1, 0],
    #     [-1, -1, 0],
    #     [-1, 1, 0]
    # ]
    # faces = [
    #     [0, 2, 1],
    #     [0, 4, 3]
    # ]

    # mesh = Mesh.from_vertices_and_faces(vertices, faces)

    # print(mesh.is_manifold())

    # # mesh = Mesh()

    # # a = mesh.add_vertex(x=0, y=0)
    # # b = mesh.add_vertex(x=0.5, y=0.1)
    # # c = mesh.add_vertex(x=1, y=0)
    # # d = mesh.add_vertex(x=0.9, y=0.5)
    # # e = mesh.add_vertex(x=0.9, y=1)
    # # f = mesh.add_vertex(x=0.5, y=1)
    # # g = mesh.add_vertex(x=0, y=1)
    # # h = mesh.add_vertex(x=0, y=0.5)

    # # mesh.add_face([a, b, c, d, e, f, g, h])

    # for k in mesh.faces():
    #     print(k, mesh.is_face_on_boundary(k))


    # print(list(mesh.edges(True)))


    # plotter = MeshPlotter(mesh)

    # plotter.draw_vertices()
    # plotter.draw_edges()
    # plotter.draw_faces(text='key')
    # plotter.show()

    # print(mesh.get_vertices_attribute('x'))
    # print(mesh.get_vertices_attributes('xy'))

    # print(mesh.get_edges_attribute('q', 1.0))
    # print(mesh.get_edges_attributes('qf', (1.0, 2.0)))

    vertices = {
        0: [0, 0, 0],
        1: [1, 1, 0],
        2: [1, -1, 0],
        3: [-1, -1, 0],
        18: [-1, 1, 0]
    }
    faces = {
        0: [0, 2, 1],
        45: [0, 18, 3]
    }

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    plotter = MeshPlotter(mesh)
    plotter.draw_vertices(text='key')
    plotter.draw_edges()
    plotter.draw_faces(text='key')
    plotter.show()

    vertices = [
        [0, 0, 0],
        [1, 1, 0],
        [1, -1, 0],
        [-1, -1, 0],
        [-1, 1, 0]
    ]
    faces = [
        [0, 2, 1],
        [0, 4, 3]
    ]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    plotter = MeshPlotter(mesh)
    plotter.draw_vertices(text='key')
    plotter.draw_edges()
    plotter.draw_faces(text='key')
    plotter.show()
