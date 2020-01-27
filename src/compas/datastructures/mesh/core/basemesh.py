from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import json
import pickle
import sys
from collections import OrderedDict
from copy import deepcopy
from math import pi
from ast import literal_eval

from compas.datastructures import Datastructure

from compas.datastructures._mixins import EdgeFilter
from compas.datastructures._mixins import EdgeGeometry
from compas.datastructures._mixins import EdgeHelpers
from compas.datastructures._mixins import EdgeMappings
from compas.datastructures._mixins import FaceFilter
from compas.datastructures._mixins import FaceHelpers
from compas.datastructures._mixins import FaceMappings
from compas.datastructures._mixins import VertexFilter
from compas.datastructures._mixins import VertexHelpers
from compas.datastructures._mixins import VertexMappings

from compas.files import OBJ
from compas.files import OFF
from compas.files import PLY
from compas.files import STL

from compas.geometry import Polyhedron
from compas.geometry import angle_points
from compas.geometry import area_polygon
from compas.geometry import bestfit_plane
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import cross_vectors
from compas.geometry import distance_point_plane
from compas.geometry import distance_point_point
from compas.geometry import flatness
from compas.geometry import length_vector
from compas.geometry import normal_polygon
from compas.geometry import normalize_vector
from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import sum_vectors
from compas.geometry import midpoint_line

from compas.utilities import average
from compas.utilities import geometric_key
from compas.utilities import pairwise
from compas.utilities import window


__all__ = ['BaseMesh']


class AttributeView(object):
    """Mixin for attribute dict views."""

    def __str__(self):
        s = []
        for k, v in self.items():
            s.append("{}: {}".format(repr(k), repr(v)))
        return "{" + ", ".join(s) + "}"

    def __len__(self):
        return len(self.defaults)


class VertexAttributeView(AttributeView, collections.MutableMapping):
    """Mutable Mapping that provides a read/write view of the custom attributes of a vertex
    combined with the default attributes of all vertices."""

    def __init__(self, defaults, attr):
        self.defaults = defaults
        self.attr = attr

    def __getitem__(self, key):
        try:
            return self.attr[key]
        except KeyError:
            return self.defaults[key]

    def __setitem__(self, key, value):
        self.attr[key] = value

    def __delitem__(self, key):
        if key in self.attr:
            del self.attr[key]
        else:
            raise KeyError

    def __iter__(self):
        for key in self.defaults:
            yield key


class FaceAttributeView(AttributeView, collections.MutableMapping):
    """Mutable Mapping that provides a read/write view of the custom attributes of a face
    combined with the default attributes of all faces."""

    def __init__(self, defaults, attr, key, custom_only=False):
        self.defaults = defaults
        self.attr = attr
        self.key = key
        self.custom_only = custom_only
        self.attr.setdefault(self.key, {})

    def __getitem__(self, name):
        return self.attr[self.key].get(name, self.defaults[name])

    def __setitem__(self, name, value):
        self.attr[self.key][name] = value

    def __delitem__(self, name):
        del self.attr[self.key][name]

    def __iter__(self):
        if self.custom_only:
            for name in self.attr[self.key]:
                yield name
        else:
            for name in self.defaults:
                yield name


class EdgeAttributeView(AttributeView, collections.MutableMapping):
    """Mutable Mapping that provides a read/write view of the custom attributes of an edge
    combined with the default attributes of all edges."""

    def __init__(self, defaults, attr, key, custom_only=False):
        self.defaults = defaults
        self.attr = attr
        self.key = key
        self.custom_only = custom_only
        self.attr.setdefault(self.key, {})

    def __getitem__(self, name):
        return self.attr[self.key].get(name, self.defaults[name])

    def __setitem__(self, name, value):
        self.attr[self.key][name] = value

    def __delitem__(self, name):
        del self.attr[self.key][name]

    def __iter__(self):
        if self.custom_only:
            for name in self.attr[self.key]:
                yield name
        else:
            for name in self.defaults:
                yield name


class BaseMesh(EdgeGeometry,
               FaceHelpers,
               FaceFilter,
               EdgeHelpers,
               VertexHelpers,
               VertexFilter,
               EdgeFilter,
               FaceMappings,
               EdgeMappings,
               VertexMappings,
               Datastructure):
    """Definition of a mesh.

    Attributes
    ----------
    attributes : dict
        A dictionary of general mesh attributes.

        * ``'name': "Mesh"``

    default_vertex_attributes : dict
        The names of pre-assigned vertex attributes and their default values.

        * ``'x': 0.0``
        * ``'y': 0.0``
        * ``'z': 0.0``

    default_edge_attributes : dict
        The default data attributes assigned to every new edge.
    default_face_attributes : dict
        The default data attributes assigned to every new face.
    name : str
        The name of the mesh.
        Shorthand for ``mesh.attributes['name']``
    adjacency : dict, read-only
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
    >>> mesh = BaseMesh.from_polyhedron(6)
    >>> V = mesh.number_of_vertices()
    >>> E = mesh.number_of_edges()
    >>> F = mesh.number_of_faces()
    >>> mesh.euler() == V - E + F
    True

    """

    __module__ = 'compas.datastructures'

    def __init__(self):
        super(BaseMesh, self).__init__()
        self._key_to_str = False
        self._max_int_key = -1
        self._max_int_fkey = -1
        self.vertex = {}
        self.halfedge = {}
        self.face = {}
        self.facedata = {}
        self.edgedata = {}
        self.attributes = {'name': 'Mesh'}
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
        tpl = "\n".join(
            ["Mesh summary",
             "============",
             "- name: {}",
             "- vertices: {}",
             "- edges: {}",
             "- faces: {}",
             "- vertex degree: {}/{}",
             "- face degree: {}/{}"])
        s = tpl.format(self.name,
                       self.number_of_vertices(),
                       self.number_of_edges(),
                       self.number_of_faces(),
                       self.vertex_min_degree(),
                       self.vertex_max_degree(),
                       self.face_min_degree(),
                       self.face_max_degree())
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
        vertex = {}
        face = {}
        facedata = {}
        edgedata = {}

        for key in self.vertex:
            vertex[repr(key)] = self.vertex[key]

        for key in self.face:
            face[repr(key)] = [repr(k) for k in self.face[key]]

        for key in self.facedata:
            facedata[repr(key)] = self.facedata[key]

        for key in self.edgedata:
            edgedata[repr(key)] = self.edgedata[key]

        data = {'attributes': self.attributes,
                'dva': self.default_vertex_attributes,
                'dea': self.default_edge_attributes,
                'dfa': self.default_face_attributes,
                'vertex': vertex,
                'face': face,
                'facedata': facedata,
                'edgedata': edgedata,
                'max_int_key': self._max_int_key,
                'max_int_fkey': self._max_int_fkey}

        return data

    @data.setter
    def data(self, data):
        attributes = data['attributes']
        dva = data.get('dva') or {}
        dfa = data.get('dfa') or {}
        dea = data.get('dea') or {}
        vertex = data.get('vertex') or {}
        face = data.get('face') or {}
        facedata = data.get('facedata') or {}
        edgedata = data.get('edgedata') or {}
        max_int_key = data.get('max_int_key', -1)
        max_int_fkey = data.get('max_int_fkey', -1)

        self.attributes.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_face_attributes.update(dfa)
        self.default_edge_attributes.update(dea)

        self.vertex = {}
        self.face = {}
        self.halfedge = {}
        self.facedata = {}
        self.edgedata = {}

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
    # from/to
    # --------------------------------------------------------------------------

    @classmethod
    def from_data(cls, data):
        """Construct a mesh from structured data.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_data* method.

        """
        mesh = cls()
        mesh.data = data
        return mesh

    def to_data(self):
        """Returns a dictionary of structured data representing the mesh.

        Returns
        -------
        dict
            The structured data.

        Note
        ----
        This method produces the data that can be used in conjuction with the
        corresponding *from_data* class method.
        """
        return self.data

    @classmethod
    def from_json(cls, filepath):
        """Construct a datastructure from structured data contained in a json file.

        Parameters
        ----------
        filepath : str
            The path to the json file.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_json* method.
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        mesh = cls()
        mesh.data = data
        return mesh

    def to_json(self, filepath, pretty=False):
        """Serialise the structured data representing the data structure to json.

        Parameters
        ----------
        filepath : str
            The path to the json file.
        """
        with open(filepath, 'w+') as f:
            if pretty:
                json.dump(self.data, f, sort_keys=True, indent=4)
            else:
                json.dump(self.data, f)

    @classmethod
    def from_pickle(cls, filepath):
        """Construct a mesh from serialised data contained in a pickle file.

        Parameters
        ----------
        filepath : str
            The path to the pickle file.

        Returns
        -------
        object
            An object of type ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_pickle* method.
        """
        with open(filepath, 'rb') as fo:
            data = pickle.load(fo)
        o = cls()
        o.data = data
        return o

    def to_pickle(self, filepath):
        """Serialise the structured data representing the mesh to a pickle file.

        Parameters
        ----------
        filepath : str
            The path to the pickle file.
        """
        with open(filepath, 'wb+') as f:
            pickle.dump(self.data, f, protocol=pickle.HIGHEST_PROTOCOL)

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
        >>>
        """
        obj = OBJ(filepath, precision)
        obj.read()
        vertices = obj.vertices
        faces = obj.faces
        edges = obj.lines
        if faces:
            return cls.from_vertices_and_faces(vertices, faces)
        if edges:
            lines = [(vertices[u], vertices[v], 0) for u, v in edges]
            return cls.from_lines(lines)

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
        with open(filepath, 'w+') as f:
            for key, attr in self.vertices(True):
                f.write('v {0[x]:.3f} {0[y]:.3f} {0[z]:.3f}\n'.format(attr))
            for fkey in self.faces():
                vertices = self.face_vertices(fkey)
                vertices = [key_index[key] + 1 for key in vertices]
                f.write(' '.join(['f'] + [str(index) for index in vertices]) + '\n')

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
        faces = ply.parser.faces
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    def to_ply(self, filepath):
        raise NotImplementedError

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
        >>>
        """
        stl = STL(filepath)
        vertices = stl.parser.vertices
        faces = stl.parser.faces
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    def to_stl(self, filepath):
        raise NotImplementedError

    @classmethod
    def from_off(cls, filepath):
        """Construct a mesh object from the data described in a OFF file.

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
        >>>
        """
        off = OFF(filepath)
        vertices = off.reader.vertices
        faces = off.reader.faces
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    def to_off(self, filepath):
        raise NotImplementedError

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
        >>>
        """
        from compas.datastructures import Network
        from compas.datastructures import network_find_faces
        mesh = cls()
        network = Network.from_lines(lines, precision=precision)
        for key, attr in network.vertices(True):
            mesh.add_vertex(key, x=attr['x'], y=attr['y'], z=attr['z'])
        mesh.halfedge = network.halfedge
        network_find_faces(mesh)
        if delete_boundary_face:
            mesh.delete_face(0)
        return mesh

    def to_lines(self, filepath):
        raise NotImplementedError

    @classmethod
    def from_polylines(cls, boundary_polylines, other_polylines):
        """Construct mesh from polylines.

        Based on construction from_lines,
        with removal of vertices that are not polyline extremities
        and of faces that represent boundaries.

        This specific method is useful to get the mesh connectivity from a set of (discretised) curves,
        that could overlap and yield a wrong connectivity if using from_lines based on the polyline extremities only.

        Parameters
        ----------
        boundary_polylines : list
            List of polylines representing boundaries as lists of vertex coordinates.
        other_polylines : list
            List of the other polylines as lists of vertex coordinates.

        Returns
        -------
        Mesh
            A mesh object.
        """
        corner_vertices = [geometric_key(xyz) for polyline in boundary_polylines + other_polylines for xyz in [polyline[0], polyline[-1]]]
        boundary_vertices = [geometric_key(xyz) for polyline in boundary_polylines for xyz in polyline]
        mesh = cls.from_lines([(u, v) for polyline in boundary_polylines + other_polylines for u, v in pairwise(polyline)])
        # remove the vertices that are not from the polyline extremities and the faces with all their vertices on the boundary
        vertex_keys = [vkey for vkey in mesh.vertices() if geometric_key(mesh.vertex_coordinates(vkey)) in corner_vertices]
        vertex_map = {vkey: i for i, vkey in enumerate(vertex_keys)}
        vertices = [mesh.vertex_coordinates(vkey) for vkey in vertex_keys]
        faces = []
        for fkey in mesh.faces():
            if sum([geometric_key(mesh.vertex_coordinates(vkey)) not in boundary_vertices for vkey in mesh.face_vertices(fkey)]):
                faces.append([vertex_map[vkey] for vkey in mesh.face_vertices(fkey) if geometric_key(mesh.vertex_coordinates(vkey)) in corner_vertices])
        mesh.cull_vertices()
        return cls.from_vertices_and_faces(vertices, faces)

    def to_polylines(self):
        raise NotImplementedError

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
        >>>
        """
        mesh = cls()
        if sys.version_info[0] < 3:
            mapping = collections.Mapping
        else:
            mapping = collections.abc.Mapping
        if isinstance(vertices, mapping):
            for key, xyz in vertices.items():
                mesh.add_vertex(key=key, attr_dict={i: j for i, j in zip(['x', 'y', 'z'], xyz)})
        else:
            for x, y, z in iter(vertices):
                mesh.add_vertex(x=x, y=y, z=z)
        if isinstance(faces, mapping):
            for fkey, vertices in faces.items():
                mesh.add_face(vertices, fkey)
        else:
            for face in iter(faces):
                mesh.add_face(face)
        return mesh

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
        key_index = self.key_index()
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [[key_index[key] for key in self.face_vertices(fkey)] for fkey in self.faces()]
        return vertices, faces

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
        >>>
        """
        p = Polyhedron.generate(f)
        return cls.from_vertices_and_faces(p.vertices, p.faces)

    @classmethod
    def from_shape(cls, shape, **kwargs):
        """Construct a mesh from a primitive shape.

        Parameters
        ----------
        shape : :class: `compas.geometry.shape`
            The input shape to generate a mesh from.
        kwargs:
            Optional keyword arguments ``u`` and ``v`` for the resolution in u (Torus, Sphere, Cylinder, Cone) and v direction (Torus and Sphere).

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        >>>
        """
        vertices, faces = shape.to_vertices_and_faces(**kwargs)
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

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
        >>>
        """
        from compas.geometry import delaunay_from_points
        faces = delaunay_from_points(points, boundary=boundary, holes=holes)
        return cls.from_vertices_and_faces(points, faces)

    def to_points(self):
        raise NotImplementedError

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

    def to_polygons(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def copy(self, cls=None):
        """Make an independent copy of the mesh object.

        Parameters
        ----------
        cls : compas.datastructures.Mesh, optional
            The type of mesh to return.
            Defaults to the type of the current mesh.

        Returns
        -------
        Mesh
            A separate, but identical mesh object.
        """
        if not cls:
            cls = type(self)
        return cls.from_data(deepcopy(self.data))

    def clear(self):
        """Clear all the mesh data."""
        del self.vertex
        del self.edgedata
        del self.halfedge
        del self.face
        del self.facedata
        self.vertex = {}
        self.edgedata = {}
        self.halfedge = {}
        self.face = {}
        self.facedata = {}
        self._max_int_key = -1
        self._max_int_fkey = -1

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex to the mesh object.

        Parameters
        ----------
        key : int, optional
            The vertex identifier.
        attr_dict : dict, optional
            Vertex attributes.
        kwattr : dict, optional
            Additional named vertex attributes.
            Named vertex attributes overwrite corresponding attributes in the
            attribute dict (``attr_dict``).

        Returns
        -------
        int
            The identifier of the vertex.

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
        if key is None:
            key = self._max_int_key = self._max_int_key + 1
        if key > self._max_int_key:
            self._max_int_key = key
        key = int(key)
        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
        attr = attr_dict or {}
        attr.update(kwattr)
        self.vertex[key].update(attr)
        return key

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face to the mesh object.

        Parameters
        ----------
        vertices : list
            A list of vertex keys.
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
        if len(vertices) < 3:
            return
        if vertices[-1] == vertices[0]:
            vertices = vertices[:-1]
        vertices = [int(key) for key in vertices]
        if fkey is None:
            fkey = self._max_int_fkey = self._max_int_fkey + 1
        if fkey > self._max_int_fkey:
            self._max_int_fkey = fkey
        attr = attr_dict or {}
        attr.update(kwattr)
        self.face[fkey] = vertices
        self.facedata.setdefault(fkey, attr)
        for u, v in pairwise(vertices + vertices[:1]):
            if u == v:
                continue
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
        key : int
            The identifier of the vertex.

        Examples
        --------
        >>>

        In some cases, disconnected vertices can remain after application of this
        method. To remove these vertices as well, combine this method with vertex
        culling (:meth:`cull_vertices`).
        """
        nbrs = self.vertex_neighbors(key)
        for nbr in nbrs:
            fkey = self.halfedge[key][nbr]
            if fkey is None:
                continue
            for u, v in self.face_halfedges(fkey):
                self.halfedge[u][v] = None
            del self.face[fkey]
            if fkey in self.facedata:
                del self.facedata[fkey]
        for nbr in nbrs:
            del self.halfedge[nbr][key]
            if (nbr, key) in self.edgedata:
                del self.edgedata[nbr, key]
            if (key, nbr) in self.edgedata:
                del self.edgedata[key, nbr]
        for nbr in nbrs:
            for n in self.vertex_neighbors(nbr):
                if self.halfedge[nbr][n] is None and self.halfedge[n][nbr] is None:
                    del self.halfedge[nbr][n]
                    del self.halfedge[n][nbr]
                    if (nbr, n) in self.edgedata:
                        del self.edgedata[nbr, n]
                    if (n, nbr) in self.edgedata:
                        del self.edgedata[n, nbr]
        del self.halfedge[key]
        del self.vertex[key]

    def insert_vertex(self, fkey, key=None, xyz=None, return_fkeys=False):
        """Insert a vertex in the specified face.

        Parameters
        ----------
        fkey : int
            The key of the face in which the vertex should be inserted.
        key : int, optional
            The key to be used to identify the inserted vertex.
        xyz : list, optional
            Specific XYZ coordinates for the inserted vertex.
        return_fkeys : bool, optional
            By default, this method returns only the key of the inserted vertex.
            This flag can be used to indicate that the keys of the newly created
            faces should be returned as well.

        Returns
        -------
        int
            The key of the inserted vertex, if ``return_fkeys`` is false.
        tuple
            The key of the newly created vertex
            and a list with the newly created faces, if ``return_fkeys`` is true.

        Examples
        --------
        >>>

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
        fkey : int
            The identifier of the face.

        Examples
        --------
        >>>
        """
        for u, v in self.face_halfedges(fkey):
            self.halfedge[u][v] = None
            if self.halfedge[v][u] is None:
                del self.halfedge[u][v]
                del self.halfedge[v][u]
                if (u, v) in self.edgedata:
                    del self.edgedata[u, v]
                if (v, u) in self.edgedata:
                    del self.edgedata[v, u]
        del self.face[fkey]
        if fkey in self.facedata:
            del self.facedata[fkey]

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
        int or tuple
            The next vertex identifier, if ``data`` is false.
            The next vertex as a (key, attr) tuple, if ``data`` is true.
        """
        for key in self.vertex:
            if not data:
                yield key
            else:
                yield key, self.vertex_attributes(key)

    def faces(self, data=False):
        """Iterate over the faces of the mesh.

        Parameters
        ----------
        data : bool, optional
            Return the face data as well as the face keys.

        Yields
        ------
        int or tuple
            The next face identifier, if ``data`` is ``False``.
            The next face as a (fkey, attr) tuple, if ``data`` is ``True``.
        """
        for key in self.face:
            if not data:
                yield key
            else:
                yield key, self.face_attributes(key)

    def edges(self, data=False):
        """Iterate over the edges of the mesh.

        Parameters
        ----------
        data : bool, optional
            Return the edge data as well as the edge vertex keys.

        Yields
        ------
        tuple
            The next edge as a (u, v) tuple, if ``data`` is false.
            The next edge as a ((u, v), data) tuple, if ``data`` is true.

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
        >>>
        """
        seen = set()
        for u in self.halfedge:
            for v in self.halfedge[u]:
                key = u, v
                ikey = v, u
                if key in seen or ikey in seen:
                    continue
                seen.add(key)
                seen.add(ikey)
                if not data:
                    yield key
                else:
                    yield key, self.edge_attributes(key)

    # --------------------------------------------------------------------------
    # attributes
    # --------------------------------------------------------------------------

    def update_default_vertex_attributes(self, attr_dict=None, **kwattr):
        """Update the default vertex attributes.

        Parameters
        ----------
        attr_dict : dict, optional
            A dictionary of attributes with their default values.
            Defaults to an empty ``dict``.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Note
        ----
        Named arguments overwrite correpsonding key-value pairs in the attribute dictionary,
        if they exist.
        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_vertex_attributes.update(attr_dict)

    def vertex_attribute(self, key, name, value=None):
        """Get or set an attribute of a vertex.

        Parameters
        ----------
        key : int
            The vertex identifier.
        name : str
            The name of the attribute
        value : obj, optional
            The value of the attribute.

        Returns
        -------
        object or None
            The value of the attribute,
            or ``None`` if the vertex does not exist
            or when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the vertex does not exist.
        """
        if key not in self.vertex:
            raise KeyError(key)
        if value is not None:
            self.vertex[key][name] = value
            return None
        if name in self.vertex[key]:
            return self.vertex[key][name]
        else:
            if name in self.default_vertex_attributes:
                return self.default_vertex_attributes[name]

    def unset_vertex_attribute(self, key, name):
        """Unset the attribute of a vertex.

        Parameters
        ----------
        key : int
            The vertex identifier.
        name : str
            The name of the attribute.

        Raises
        ------
        KeyError
            If the vertex does not exist.

        Notes
        -----
        Unsetting the value of a vertex attribute implicitly sets it back to the value
        stored in the default vertex attribute dict.
        """
        if name in self.vertex[key]:
            del self.vertex[key][name]

    def vertex_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        names : list, optional
            A list of attribute names.
        values : list, optional
            A list of attribute values.

        Returns
        -------
        dict, list or None
            If the parameter ``names`` is empty,
            the function returns a dictionary of all attribute name-value pairs of the vertex.
            If the parameter ``names`` is not empty,
            the function returns a list of the values corresponding to the requested attribute names.
            The function returns ``None`` if it is used as a "setter".

        Raises
        ------
        KeyError
            If the vertex does not exist.
        """
        if key not in self.vertex:
            raise KeyError(key)
        if values:
            # use it as a setter
            for name, value in zip(names, values):
                self.vertex[key][name] = value
            return
        # use it as a getter
        if not names:
            # return all vertex attributes as a dict
            return VertexAttributeView(self.default_vertex_attributes, self.vertex[key])
        values = []
        for name in names:
            if name in self.vertex[key]:
                values.append(self.vertex[key][name])
            elif name in self.default_vertex_attributes:
                values.append(self.default_vertex_attributes[name])
            else:
                values.append(None)
        return values

    def vertices_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple vertices.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : obj, optional
            The value of the attribute.
            Default is ``None``.
        keys : list of int, optional
            A list of vertex identifiers.

        Returns
        -------
        list or None
            The value of the attribute for each vertex,
            or ``None`` if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the vertices does not exist.
        """
        if not keys:
            keys = self.vertices()
        if value is not None:
            for key in keys:
                self.vertex_attribute(key, name, value)
            return
        return [self.vertex_attribute(key, name) for key in keys]

    def vertices_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple vertices.

        Parameters
        ----------
        names : list of str, optional
            The names of the attribute.
            Default is ``None``.
        values : list of obj, optional
            The values of the attributes.
            Default is ``None``.
        keys : list of int, optional
            A list of vertex identifiers.

        Returns
        -------
        list or None
            If the parameter ``names`` is ``None``,
            the function returns a list containing an attribute dict per vertex.
            If the parameter ``names`` is not ``None``,
            the function returns a list containing a list of attribute values per vertex corresponding to the provided attribute names.
            The function returns ``None`` if it is used as a "setter".

        Raises
        ------
        KeyError
            If any of the vertices does not exist.
        """
        if not keys:
            keys = self.vertices()
        if values:
            for key in keys:
                self.vertex_attributes(key, names, values)
            return
        return [self.vertex_attributes(key, names) for key in keys]

    def update_default_face_attributes(self, attr_dict=None, **kwattr):
        """Update the default face attributes.

        Parameters
        ----------
        attr_dict : dict (None)
            A dictionary of attributes with their default values.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Note
        ----
        Named arguments overwrite correpsonding key-value pairs in the attribute dictionary,
        if they exist.
        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_face_attributes.update(attr_dict)

    def face_attribute(self, key, name, value=None):
        """Get or set an attribute of a face.

        Parameters
        ----------
        key : int
            The face identifier.
        name : str
            The name of the attribute.
        value : obj, optional
            The value of the attribute.

        Returns
        -------
        object or None
            The value of the attribute, or ``None`` when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the face does not exist.
        """
        if key not in self.face:
            raise KeyError(key)
        if value is not None:
            if key not in self.facedata:
                self.facedata[key] = {}
            self.facedata[key][name] = value
            return
        if key in self.facedata and name in self.facedata[key]:
            return self.facedata[key][name]
        if name in self.default_face_attributes:
            return self.default_face_attributes[name]

    def unset_face_attribute(self, key, name):
        """Unset the attribute of a face.

        Parameters
        ----------
        key : int
            The face identifier.
        name : str
            The name of the attribute.

        Raises
        ------
        KeyError
            If the face does not exist.

        Notes
        -----
        Unsetting the value of a face attribute implicitly sets it back to the value
        stored in the default face attribute dict.
        """
        if key not in self.face:
            raise KeyError(key)
        if key in self.facedata:
            if name in self.facedata[key]:
                del self.facedata[key][name]

    def face_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of a face.

        Parameters
        ----------
        key : int
            The identifier of the face.
        names : list, optional
            A list of attribute names.
        values : list, optional
            A list of attribute values.

        Returns
        -------
        dict, list or None
            If the parameter ``names`` is empty,
            a dictionary of all attribute name-value pairs of the face.
            If the parameter ``names`` is not empty,
            a list of the values corresponding to the provided names.
            ``None`` if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the face does not exist.
        """
        if key not in self.face:
            raise KeyError(key)
        if values:
            # use it as a setter
            for name, value in zip(names, values):
                if key not in self.facedata:
                    self.facedata[key] = {}
                self.facedata[key][name] = value
            return
        # use it as a getter
        if not names:
            return FaceAttributeView(self.default_face_attributes, self.facedata, key)
        values = []
        for name in names:
            value = self.face_attribute(key, name)
            values.append(value)
        return values

    def faces_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple faces.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : obj, optional
            The value of the attribute.
            Default is ``None``.
        keys : list of int, optional
            A list of face identifiers.

        Returns
        -------
        list or None
            A list containing the value per face of the requested attribute,
            or ``None`` if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the faces does not exist.
        """
        if not keys:
            keys = self.faces()
        if value is not None:
            for key in keys:
                self.face_attribute(key, name, value)
            return
        return [self.face_attribute(key, name) for key in keys]

    def faces_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple faces.

        Parameters
        ----------
        names : list of str, optional
            The names of the attribute.
            Default is ``None``.
        values : list of obj, optional
            The values of the attributes.
            Default is ``None``.
        keys : list of int, optional
            A list of face identifiers.

        Returns
        -------
        dict, list or None
            If the parameter ``names`` is ``None``,
            a list containing per face an attribute dict with all attributes (default + custom) of the face.
            If the parameter ``names`` is ``None``,
            a list containing per face a list of attribute values corresponding to the requested names.
            ``None`` if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the faces does not exist.
        """
        if not keys:
            keys = self.faces()
        if values:
            for key in keys:
                self.face_attributes(key, names, values)
            return
        return [self.face_attributes(key, names) for key in keys]

    def update_default_edge_attributes(self, attr_dict=None, **kwattr):
        """Update the default edge attributes.

        Parameters
        ----------
        attr_dict : dict, optional
            A dictionary of attributes with their default values.
            Defaults to an empty ``dict``.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Note
        ----
        Named arguments overwrite correpsonding key-value pairs in the attribute dictionary,
        if they exist.
        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_edge_attributes.update(attr_dict)

    def edge_attribute(self, key, name, value=None):
        """Get or set an attribute of an edge.

        Parameters
        ----------
        key : 2-tuple of int
            The identifier of the edge as a pair of vertex identifiers.
        name : str
            The name of the attribute.
        value : obj, optional
            The value of the attribute.
            Default is ``None``.

        Returns
        -------
        object or None
            The value of the attribute, or ``None`` when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.
        """
        u, v = key
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(key)
        if value is not None:
            if (u, v) not in self.edgedata:
                self.edgedata[u, v] = {}
            if (v, u) not in self.edgedata:
                self.edgedata[v, u] = {}
            self.edgedata[u, v][name] = self.edgedata[v, u][name] = value
            return
        if (u, v) in self.edgedata and name in self.edgedata[u, v]:
            return self.edgedata[u, v][name]
        if (v, u) in self.edgedata and name in self.edgedata[v, u]:
            return self.edgedata[v, u][name]
        if name in self.default_edge_attributes:
            return self.default_edge_attributes[name]

    def unset_edge_attribute(self, key, name):
        """Unset the attribute of an edge.

        Parameters
        ----------
        key : tuple of int
            The edge identifier.
        name : str
            The name of the attribute.

        Raises
        ------
        KeyError
            If the edge does not exist.

        Notes
        -----
        Unsetting the value of an edge attribute implicitly sets it back to the value
        stored in the default edge attribute dict.
        """
        u, v = key
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(key)
        if key in self.edgedata:
            if name in self.edgedata[key]:
                del self.edgedata[key][name]
        key = v, u
        if key in self.edgedata:
            if name in self.edgedata[key]:
                del self.edgedata[key][name]

    def edge_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of an edge.

        Parameters
        ----------
        key : 2-tuple of int
            The identifier of the edge.
        names : list, optional
            A list of attribute names.
        values : list, optional
            A list of attribute values.

        Returns
        -------
        dict, list or None
            If the parameter ``names`` is empty,
            a dictionary of all attribute name-value pairs of the edge.
            If the parameter ``names`` is not empty,
            a list of the values corresponding to the provided names.
            ``None`` if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.
        """
        u, v = key
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(key)
        if values:
            # use it as a setter
            for name, value in zip(names, values):
                self.edge_attribute(key, name, value)
            return
        # use it as a getter
        if not names:
            # get the entire attribute dict
            return EdgeAttributeView(self.default_edge_attributes, self.edgedata, key)
        # get only the values of the named attributes
        values = []
        for name in names:
            value = self.edge_attribute(key, name)
            values.append(value)
        return values

    def edges_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : obj, optional
            The value of the attribute.
            Default is ``None``.
        keys : list of 2-tuple of int, optional
            A list of edge identifiers.

        Returns
        -------
        list or None
            A list containing the value per edge of the requested attribute,
            or ``None`` if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the edges does not exist.
        """
        if not keys:
            keys = self.edges()
        if value is not None:
            for key in keys:
                self.edge_attribute(key, name, value)
            return
        return [self.edge_attribute(key, name) for key in keys]

    def edges_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple edges.

        Parameters
        ----------
        names : list of str, optional
            The names of the attribute.
            Default is ``None``.
        values : list of obj, optional
            The values of the attributes.
            Default is ``None``.
        keys : list of 2-tuple of int, optional
            A list of edge identifiers.

        Returns
        -------
        dict, list or None
            If the parameter ``names`` is ``None``,
            a list containing per edge an attribute dict with all attributes (default + custom) of the edge.
            If the parameter ``names`` is ``None``,
            a list containing per edge a list of attribute values corresponding to the requested names.
            ``None`` if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the edges does not exist.
        """
        if not keys:
            keys = self.edges()
        if values:
            for key in keys:
                self.edge_attributes(key, names, values)
            return
        return [self.edge_attributes(key, names) for key in keys]

    # --------------------------------------------------------------------------
    # mesh info
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
                if fkey is not None:
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
        if self.is_orientable():
            return (2 - (X + B)) / 2
        else:
            return 2 - (X + B)

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    # def has_vertex(self, key):
    #     """Verify that a vertex is in the mesh.

    #     Parameters
    #     ----------
    #     key : int
    #         The identifier of the vertex.

    #     Returns
    #     -------
    #     bool
    #         True if the vertex is in the mesh.
    #         False otherwise.

    #     """
    #     return key in self.vertex

    # def is_vertex(self, key):
    #     """Verify that a vertex is in the mesh.

    #     Parameters
    #     ----------
    #     key : int
    #         The identifier of the vertex.

    #     Returns
    #     -------
    #     bool
    #         True if the vertex is in the mesh.
    #         False otherwise.
    #     """
    #     return key in self.vertex

    def is_vertex_connected(self, key):
        """Verify that a vertex is connected.

        Parameters
        ----------
        key : int
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
        key : int
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
        key : int
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
        >>>
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
        key : int
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
        >>>

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
        key : int
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
        key : int
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
        key : int
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
        key : int
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
        >>>
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

    # def has_edge(self, u, v, directed=True):
    #     """Verify that the mesh contains a specific edge.

    #     Warning
    #     -------
    #     This method may produce unexpected results.

    #     Parameters
    #     ----------
    #     u : int
    #         The identifier of the first vertex.
    #     v : int
    #         The identifier of the second vertex.
    #     directed : bool, optional
    #         Only consider directed edges.
    #         Default is ``True``.

    #     Returns
    #     -------
    #     bool
    #         True if the edge exists.
    #         False otherwise.
    #     """
    #     if directed:
    #         return (u, v) in set(self.edges())
    #     else:
    #         return u in self.halfedge and v in self.halfedge[u]

    # def is_edge(self, key):
    #     """Verify that an edge is part of the mesh.

    #     Parameters
    #     ----------
    #     key : tuple of int
    #         The identifier of the edge.

    #     Returns
    #     -------
    #     bool
    #         True if the edge is part of the mesh.
    #         False otherwise.
    #     """
    #     for uv in self.edges():
    #         if key == uv:
    #             return True
    #     return False

    def is_halfedge(self, key):
        """Verify that a halfedge is part of the mesh.

        Parameters
        ----------
        key : tuple of int
            The identifier of the halfedge.

        Returns
        -------
        bool
            True if the halfedge is part of the mesh.
            False otherwise.
        """
        u, v = key
        return u in self.halfedge and v in self.halfedge[u]

    def edge_faces(self, u, v):
        """Find the two faces adjacent to an edge.

        Parameters
        ----------
        u : int
            The identifier of the first vertex.
        v : int
            The identifier of the second vertex.

        Returns
        -------
        tuple
            The identifiers of the adjacent faces.
            If the edge is on the bboundary, one of the identifiers is ``None``.
        """
        return self.halfedge[u][v], self.halfedge[v][u]

    def halfedge_face(self, u, v):
        """Find the face corresponding to a halfedge.

        Parameters
        ----------
        u : int
            The identifier of the first vertex.
        v : int
            The identifier of the second vertex.

        Returns
        -------
        int or None
            The identifier of the face corresponding to the halfedge.
            None, if the halfedge is on the outside of a boundary.

        Raises
        ------
        KeyError
            If the halfedge does not exist.

        Examples
        --------
        >>>
        """
        return self.halfedge[u][v]

    def is_edge_on_boundary(self, u, v):
        """Verify that an edge is on the boundary.

        Parameters
        ----------
        u : int
            The identifier of the first vertex.
        v : int
            The identifier of the second vertex.

        Returns
        -------
        bool
            True if the edge is on the boundary.
            False otherwise.
        """
        return self.halfedge[v][u] is None or self.halfedge[u][v] is None

    # --------------------------------------------------------------------------
    # polyedge topology
    # --------------------------------------------------------------------------

    # face strips?
    # edge chains?
    # ...?

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    # def is_face(self, fkey):
    #     """Verify that a face is part of the mesh.

    #     Parameters
    #     ----------
    #     fkey : int
    #         The identifier of the face.

    #     Returns
    #     -------
    #     bool
    #         True if the face exists.
    #         False otherwise.

    #     Examples
    #     --------
    #     >>>
    #     """
    #     return fkey in self.face

    def face_vertices(self, fkey):
        """The vertices of a face.

        Parameters
        ----------
        fkey : int
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
        fkey : int
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
        fkey : int
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
        fkey : int
            Identifier of the face.

        Returns
        -------
        list
            The identifiers of the neighboring faces.

        Example
        -------
        >>>

        """
        nbrs = []
        for u, v in self.face_halfedges(fkey):
            nbr = self.halfedge[v][u]
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def face_neighborhood(self, key, ring=1):
        """Return the faces in the neighborhood of a face.

        Parameters
        ----------
        key : int
            The identifier of the face.
        ring : int, optional
            The size of the neighborhood.
            Default is ``1``.

        Returns
        -------
        list
            A list of face identifiers.
        """
        nbrs = set(self.face_neighbors(key))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for key in nbrs:
                temp += self.face_neighbors(key)
            nbrs.update(temp)
            i += 1
        return list(nbrs)

    def face_degree(self, fkey):
        """Count the neighbors of a face.

        Parameters
        ----------
        fkey : int
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
        fkey : int
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
        fkey : int
            Identifier of the face.

        Returns
        -------
        int
            The highest degree.
        """
        if not self.face:
            return 0
        return max(self.face_degree(fkey) for fkey in self.faces())

    def face_vertex_ancestor(self, fkey, key, n=1):
        """Return the n-th vertex before the specified vertex in a specific face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.
        key : int
            The identifier of the vertex.
        n : int, optional
            The index of the vertex ancestor. Default is 1, meaning the previous vertex.

        Returns
        -------
        int
            The identifier of the vertex before the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.
        """
        i = self.face[fkey].index(key)
        return self.face[fkey][(i - n) % len(self.face[fkey])]

    def face_vertex_descendant(self, fkey, key, n=1):
        """Return the n-th vertex after the specified vertex in a specific face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.
        key : int
            The identifier of the vertex.
        n : int, optional
            The index of the vertex descendant. Default is 1, meaning the next vertex.

        Returns
        -------
        int
            The identifier of the vertex after the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.
        """
        i = self.face[fkey].index(key)
        return self.face[fkey][(i + n) % len(self.face[fkey])]

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
        f1 : int
            The identifier of the first face.
        f2 : int
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
        key : int
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

        Returns
        -------
        float
            The area.
        """
        return sum(self.face_area(fkey) for fkey in self.faces())

    def centroid(self):
        """Calculate the mesh centroid.

        Returns
        -------
        list
            The coordinates of the mesh centroid.
        """
        return scale_vector(sum_vectors([scale_vector(self.face_centroid(fkey), self.face_area(fkey)) for fkey in self.faces()]), 1. / self.area())

    def normal(self):
        """Calculate the average mesh normal.

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
        key : int
            The identifier of the vertex.
        axes : str, optional
            The axes along which to take the coordinates.
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
        key : int
            The identifier of the vertex.

        Returns
        -------
        float
            The tributary are.

        Example
        -------
        >>>

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
        key : int
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
        key : int
            The identifier of the vertex.

        Returns
        -------
        list
            The coordinates of the centroid.
        """
        return centroid_points([self.vertex_coordinates(nbr) for nbr in self.vertex_neighbors(key)])

    def vertex_normal(self, key):
        """Return the normal vector at the vertex as the weighted average of the
        normals of the neighboring faces.

        Parameters
        ----------
        key : int
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
        fkey : int
            The face key.

        Returns
        -------
        float
            The dimensionless curvature.

        References
        ----------
        Based on [1]_

        .. [1] Botsch, Mario, et al. *Polygon mesh processing.* AK Peters/CRC Press, 2010.
        """
        C = 0
        for u, v in pairwise(self.vertex_neighbors(vkey, ordered=True) + self.vertex_neighbors(vkey, ordered=True)[:1]):
            C += angle_points(self.vertex_coordinates(vkey), self.vertex_coordinates(u), self.vertex_coordinates(v))
        return 2 * pi - C

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    def edge_coordinates(self, u, v, axes='xyz'):
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.
        axes : str (xyz)
            The axes along which the coordinates should be included.

        Returns
        -------
        tuple
            The coordinates of the start point and the coordinates of the end point.

        """
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    def edge_length(self, u, v):
        """Return the length of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        float
            The length of the edge.

        """
        a, b = self.edge_coordinates(u, v)
        return distance_point_point(a, b)

    def edge_vector(self, u, v):
        """Return the vector of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        list
            The vector from u to v.

        """
        a, b = self.edge_coordinates(u, v)
        ab = subtract_vectors(b, a)
        return ab

    def edge_point(self, u, v, t=0.5):
        """Return the location of a point along an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.
        t : float (0.5)
            The location of the point on the edge.
            If the value of ``t`` is outside the range ``0-1``, the point will
            lie in the direction of the edge, but not on the edge vector.

        Returns
        -------
        list
            The XYZ coordinates of the point.

        """
        a, b = self.edge_coordinates(u, v)
        ab = subtract_vectors(b, a)
        return add_vectors(a, scale_vector(ab, t))

    def edge_midpoint(self, u, v):
        """Return the location of the midpoint of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        list
            The XYZ coordinates of the midpoint.

        """
        a, b = self.edge_coordinates(u, v)
        return midpoint_line((a, b))

    def edge_direction(self, u, v):
        """Return the direction vector of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        list
            The direction vector of the edge.

        """
        return normalize_vector(self.edge_vector(u, v))

    # --------------------------------------------------------------------------
    # face geometry
    # --------------------------------------------------------------------------

    def face_coordinates(self, fkey, axes='xyz'):
        """Compute the coordinates of the vertices of a face.

        Parameters
        ----------
        fkey : int
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
        fkey : int
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
        fkey : int
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
        fkey : int
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
        fkey : int
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
        fkey : int
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
        angles = []
        vertices = self.face_vertices(fkey)
        for u, v, w in window(vertices + vertices[:2], n=3):
            o = self.vertex_coordinates(v)
            a = self.vertex_coordinates(u)
            b = self.vertex_coordinates(w)
            angle = angle_points(o, a, b, deg=True)
            angles.append(angle)
        return max((max(angles) - ideal_angle) / (180 - ideal_angle), (ideal_angle - min(angles)) / ideal_angle)

    def face_curvature(self, fkey):
        """Dimensionless face curvature as the maximum face vertex deviation from
        the best-fit plane of the face vertices divided by the average lengths of
        the face vertices to the face centroid.

        Parameters
        ----------
        fkey : Key
            The face key.

        Returns
        -------
        float
            The dimensionless curvature.
        """
        vertices = self.face_vertices(fkey)
        points = [self.vertex_coordinates(key) for key in vertices]
        centroid = self.face_centroid(fkey)
        plane = bestfit_plane(points)
        max_deviation = max([distance_point_plane(point, plane) for point in points])
        average_distances = average([distance_point_point(point, centroid) for point in points])
        return max_deviation / average_distances

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
        faces = OrderedDict()
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, fkey in iter(nbrs.items()):
                if fkey is None:
                    faces[self.halfedge[nbr][key]] = 1
        return faces.keys()

    def edges_on_boundary(self, chained=False):
        """Find the edges on the boundary.

        Parameters
        ----------
        chained : bool (``False``)
            Indicate whether the boundary edges should be chained head to tail.
            Note that chaining the edges will essentially return half-edges that
            point outwards to the space outside.

        Returns
        -------
        boundary_edges : list
            The boundary edges.

        """
        boundary_edges = [(u, v) for u, v in self.edges() if self.is_edge_on_boundary(u, v)]
        if not chained:
            return boundary_edges
        # this is not "chained"
        # it is "oriented"
        return [(u, v) if self.halfedge[u][v] is None else (v, u) for u, v in boundary_edges]

    # def boundaries(self):
    #     """Collect the mesh boundaries as lists of vertices.

    #     Parameters
    #     ----------
    #     mesh : Mesh
    #         Mesh.

    #     Returns
    #     -------
    #     boundaries : list
    #         List of boundaries as lists of vertex keys.
    #     """
    #     # get all boundary edges pointing outwards
    #     boundary_edges = OrderedDict([(u, v) for u, v in self.edges_on_boundary(True)])
    #     # find the boundaries
    #     boundaries = []
    #     while len(boundary_edges) > 0:
    #         boundary = list(boundary_edges.popitem())
    #         # get consecuvite vertex until the boundary is closed
    #         while boundary[0] != boundary[-1]:
    #             boundary.append(boundary_edges[boundary[-1]])
    #             boundary_edges.pop(boundary[-2])
    #         boundaries.append(boundary[: -1])
    #     return boundaries


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
