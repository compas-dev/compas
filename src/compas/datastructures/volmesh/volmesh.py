from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import pickle
import json
try:
    from collections.abc import MutableMapping  # python > 3.3
except ImportError:
    from collections import MutableMapping      # python 2.7
from copy import deepcopy
from ast import literal_eval
from random import sample
from random import choice

from compas.files import OBJ

from compas.utilities import geometric_key
from compas.utilities import pairwise

from compas.geometry import normalize_vector
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import centroid_polyhedron
from compas.geometry import area_polygon
from compas.geometry import normal_polygon
from compas.geometry import subtract_vectors
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import distance_point_point
from compas.geometry import midpoint_line

from compas.datastructures import Datastructure
from compas.datastructures import Mesh


__all__ = ['VolMesh']


class AttributeView(object):
    """Mixin for attribute dict views."""

    def __str__(self):
        s = []
        for k, v in self.items():
            s.append("{}: {}".format(repr(k), repr(v)))
        return "{" + ", ".join(s) + "}"

    def __len__(self):
        return len(self.defaults)


class VertexAttributeView(AttributeView, MutableMapping):
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


class FaceAttributeView(AttributeView, MutableMapping):
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


class EdgeAttributeView(AttributeView, MutableMapping):
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


class VolMesh(Datastructure):
    """Class for working with volumetric meshes.

    Attributes
    ----------
    vertex : dict
        The vertices of the volmesh. Each vertex is represented by a key-value pair
        in the vertex dictionary. The key is the unique identifier of the vertex,
        and the value is itself a dictionary of named vertex attributes.
        ``self.vertex[key] -> attribute dict``
    cell : dict
        The cells of the volmesh. Each cell is represted by a key-value pair in
        the cell dictionary. The key is the unique identifier of the cell, and
        the value id itself a dictionary. The keys of this dictionary correspond
        to the vertices that make up the cell. The values are again dictionaries.
        Each key in the latter dictionary is a neighbor of the previous vertex.
        Together they form a halfedge of the cell, pointing at one of the cell's
        halffaces.
        ``self.cell[ckey][u][v] -> fkey``
    halfface : dict
        The halffaces of the volmesh. Each halfface is represented by
        ``self.halfface[fkey] -> vertex cycle``
    plane : dict
        The planes of the volmesh. Every plane is uniquely defined by three
        neighboring vertices of the volmesh in a specific order. At the first level,
        each vertex in the plane dict points at a new dictionary. This keys of this
        dictionary are the (undirected) neighbors of the previous vertex. The values
        are again dictionaries. In combination with the first two keys, the keys
        of the latter identify oriented faces (planes) of the volmesh, finally
        pointing at the cells of the volmesh.
        ``self.plane[u][v][w] -> ckey``.

    Notes
    -----
    Volumetric meshes are 3-mainfold, cellular structures.

    The implementation of *VolMesh* is based on the notion of *x-maps*
    and the concepts behind the *OpenVolumeMesh* library [vci2016]_.
    In short, we add an additional entity compared to polygonal meshes,
    the *cell*, and relate cells not through *half-edges*, but through a combination
    of *half-faces* and *planes*. Each cell consists of a series of vertex pairs,
    forming half-edges. Every half-edge points at a half-face of the cell. The half-
    faces are stored as vertex cycles. Every three adjacent vertices in the cycle,
    through the planes, point at the cell of which they form the boundary.

    References
    ----------
    .. [vci2016] Visual Computing Institute *Open Volum Mesh*.
                 Available at: http://www.openvolumemesh.org

    """

    def __init__(self):
        super(VolMesh, self).__init__()
        self._max_int_vkey = -1
        self._max_int_fkey = -1
        self._max_int_ckey = -1
        self.vertex = {}
        # self.edge = {}
        self.halfface = {}
        self.cell = {}
        self.plane = {}
        self.edgedata = {}
        self.facedata = {}
        self.celldata = {}
        self.attributes = {'name': 'VolMesh'}
        self.default_vertex_attributes = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.default_edge_attributes = {}
        self.default_face_attributes = {}
        self.default_cell_attributes = {}

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

    def __str__(self):
        """Generate a readable representation of the data of the volmesh."""
        return json.dumps(self.data, sort_keys=True, indent=4)

    def summary(self):
        """Print a summary of the mesh."""
        tpl = "\n".join(
            ["VolMesh summary",
             "===============",
             "- vertices: {}",
             "- edges: {}",
             "- faces: {}",
             "- cells: {}"])
        s = tpl.format(self.number_of_vertices(),
                       self.number_of_edges(),
                       self.number_of_faces(),
                       self.number_of_cells())
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
    def data(self):
        """dict: A data dict representing the volmesh data structure for serialisation.

        The dict has the following structure:

        * 'attributes'   => dict
        * 'dva'          => dict
        * 'dea'          => dict
        * 'dfa'          => dict
        * 'vertex'       => dict
        * 'edge'         => dict
        * 'halfface'     => dict
        * 'cell'         => dict
        * 'plane'        => dict
        * 'edgedata'     => dict
        * 'facedata'     => dict
        * 'celldata'     => dict
        * 'max_int_key'  => int
        * 'max_int_fkey' => int
        * 'max_int_ckey' => int

        Note
        ----
        All dictionary keys are converted to their representation value (``repr(key)``)
        to ensure compatibility of all allowed key types with the JSON serialisation
        format, which only allows for dict keys that are strings.

        """
        data = {
            'attributes': self.attributes,
            'dva': self.default_vertex_attributes,
            'dea': self.default_edge_attributes,
            'dfa': self.default_face_attributes,
            'dca': self.default_cell_attributes,
            'vertex': {},
            'edge': {},
            'halfface': {},
            'cell': {},
            'plane': {},
            'edgedata': {},
            'facedata': {},
            'celldata': {},
            'max_int_vkey': self._max_int_vkey,
            'max_int_fkey': self._max_int_fkey,
            'max_int_ckey': self._max_int_ckey, }

        key_rkey = {}

        for vkey in self.vertex:
            rkey = repr(vkey)
            key_rkey[vkey] = rkey
            data['vertex'][rkey] = self.vertex[vkey]
            data['plane'][rkey] = {}
            data['edge'][rkey] = {}

        for u in self.edge:
            ru = key_rkey[u]
            for v in self.edge[u]:
                rv = key_rkey[v]
                data['edge'][ru][rv] = self.edge[u][v]

        for f in self.halfface:
            _f = repr(f)
            data['halfface'][_f] = {}
            for u, v in self.halfface[f].iteritems():
                _u = repr(u)  # use the map?
                _v = repr(v)  # use the map?
                data['halfface'][_f][_u] = _v

        for c in self.cell:
            _c = repr(c)
            data['cell'][_c] = {}
            for u in self.cell[c]:
                _u = repr(u)
                if _u not in data['cell'][_c]:
                    data['cell'][_c][_u] = {}
                for v, f in self.cell[c][u].iteritems():
                    _v = repr(v)
                    _f = repr(f)
                    data['cell'][_c][_u][_v] = _f

        for u in self.plane:
            _u = repr(u)
            for v in self.plane[u]:
                _v = repr(v)
                if _v not in data['plane'][_u]:
                    data['plane'][_u][_v] = {}
                for w, c in self.plane[u][v].iteritems():
                    _w = repr(w)
                    _c = repr(c)
                    data['plane'][_u][_v][_w] = _c

        for uv in self.edgedata:
            data['edgedata'][repr(uv)] = self.edgedata[uv]

        for fkey in self.facedata:
            data['facedata'][repr(fkey)] = self.facedata[fkey]

        for ckey in self.celldata:
            data['celldata'][repr(ckey)] = self.celldata[ckey]

        return data

    @data.setter
    def data(self, data):
        attributes = data.get('attributes') or {}
        dva = data.get('dva') or {}
        dea = data.get('dea') or {}
        dfa = data.get('dfa') or {}
        dca = data.get('dca') or {}
        vertex = data.get('vertex') or {}
        edge = data.get('edge') or {}
        halfface = data.get('halfface') or {}
        cell = data.get('cell') or {}
        plane = data.get('plane') or {}
        edgedata = data.get('edgedata') or {}
        facedata = data.get('facedata') or {}
        celldata = data.get('celldata') or {}
        max_int_vkey = data.get('max_int_vkey', - 1)
        max_int_fkey = data.get('max_int_fkey', - 1)
        max_int_ckey = data.get('max_int_ckey', - 1)

        if not vertex or not edge or not plane or not halfface or not cell:
            return

        self.clear()

        self.attributes.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_edge_attributes.update(dea)
        self.default_face_attributes.update(dfa)
        self.default_cell_attributes.update(dca)

        for _k, attr in vertex.iteritems():
            k = literal_eval(_k)
            self.vertex[k] = self.default_vertex_attributes.copy()
            if attr:
                self.vertex[k].update(attr)
            self.plane[k] = {}
            self.edge[k] = {}

        for _u, nbrs in edge.iteritems():
            nbrs = nbrs or {}
            u = literal_eval(_u)
            for _v, attr in nbrs.iteritems():
                v = literal_eval(_v)
                self.edge[u][v] = self.default_edge_attributes.copy()
                if attr:
                    self.edge[u][v].update(attr)

        for _f in halfface:
            f = literal_eval(_f)
            self.halfface[f] = {}
            for _u, _v in halfface[_f].iteritems():
                u = literal_eval(_u)
                v = literal_eval(_v)
                self.halfface[f][u] = v

        for _c in cell:
            c = literal_eval(_c)
            self.cell[c] = {}
            for _u in cell[_c]:
                u = literal_eval(_u)
                if u not in self.cell[c]:
                    self.cell[c][u] = {}
                for _v, _f in cell[_c][_u].iteritems():
                    v = literal_eval(_v)
                    f = literal_eval(_f)
                    self.cell[c][u][v] = f

        for _u in plane:
            u = literal_eval(_u)
            for _v in plane[_u]:
                v = literal_eval(_v)
                if v not in self.plane[u]:
                    self.plane[u][v] = {}
                for _w, _c in plane[_u][_v].iteritems():
                    w = literal_eval(_w)
                    c = literal_eval(_c)
                    self.plane[u][v][w] = c

        for uv, attr in iter(edgedata.items()):
            self.edgedata[literal_eval(uv)] = attr or {}

        for fkey, attr in iter(facedata.items()):
            self.facedata[literal_eval(fkey)] = attr or {}

        for ckey, attr in iter(celldata.items()):
            self.celldata[literal_eval(ckey)] = attr or {}

        self._max_int_vkey = max_int_vkey
        self._max_int_fkey = max_int_fkey
        self._max_int_ckey = max_int_ckey

    # --------------------------------------------------------------------------
    # serialisation
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # constructors
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
        """Construct a volmesh object from the data described in an OBJ file.

        Parameters
        ----------
        filepath : str
            The path to the file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Volesh
            A volmesh object.

        """
        obj = OBJ(filepath, precision)
        vertices = obj.parser.vertices
        faces = obj.parser.faces
        groups = obj.parser.groups
        cells = []
        for name in groups:
            group = groups[name]
            cell = []
            for item in group:
                if item[0] != 'f':
                    continue
                face = faces[item[1]]
                cell.append(face)
            cells.append(cell)
        return cls.from_vertices_and_cells(vertices, cells)

    def to_obj(self, filepath):
        raise NotImplementedError

    @classmethod
    def from_vertices_and_cells(cls, vertices, cells):
        """Construct a volmesh object from vertices and cells.

        Parameters
        ----------
        vertices : list
            Ordered list of vertices, represented by their XYZ coordinates.
        cells : lists of lists
            List of cells (list of halffaces).

        Returns
        -------
        Volmesh
            A volmesh object.

        """
        volmesh = cls()
        for x, y, z in vertices:
            volmesh.add_vertex(x=x, y=y, z=z)
        for cell in cells:
            volmesh.add_cell(cell)
        return volmesh

    def to_vertices_and_cells(self):
        """Return the vertices and cells of a volmesh.

        Returns
        -------
        tuple
            A 2-tuple containing

            * a list of vertices, represented by their XYZ coordinates, and
            * a list of cells.

            Each cell is a list of halffaces, which are lists of indices referencing the list of vertex coordinates.

        """
        key_index = self.key_index()
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        cells = []
        for ckey in self.cell:
            halffaces = [[key_index[key] for key in self.halfface[fkey]] for fkey in self.halffaces()]
            cells.append(halffaces)
        return vertices, cells

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def copy(self):
        """Make an independent copy of the volmesh object.

        Returns
        -------
        VolMesh
            A separate, but identical volmesh object.

        """
        cls = type(self)
        return cls.from_data(deepcopy(self.data))

    def clear(self):
        """Clear all the volmesh data."""
        del self.vertex
        del self.edge
        del self.halfface
        del self.cell
        del self.plane
        del self.edgedata
        del self.facedata
        del self.celldata
        self.vertex = {}
        self.edge = {}
        self.halfface = {}
        self.cell = {}
        self.plane = {}
        self.edgedata = {}
        self.facedata = {}
        self.celldata = {}
        self._max_int_vkey = -1
        self._max_int_fkey = -1
        self._max_int_ckey = -1

    def get_any_vertex(self):
        """Get the identifier of a random vertex.

        Returns
        -------
        hashable
            The identifier of the vertex.

        """
        return self.get_any_vertices(1)[0]

    def get_any_vertices(self, n, exclude_leaves=False):
        """Get a list of identifiers of a random set of n vertices.

        Parameters
        ----------
        n : int
            The number of random vertices.
        exclude_leaves : bool (False)
            Exclude the leaves (vertices with only one connected edge) from the set.
            Default is to include the leaves.

        Returns
        -------
        list
            The identifiers of the vertices.

        """
        if exclude_leaves:
            vertices = set(self.vertices()) - set(self.leaves())
        else:
            vertices = self.vertices()
        return sample(list(vertices), n)

    def get_any_face(self):
        """Get the identifier of a random face.

        Returns
        -------
        hashable
            The identifier of the face.

        """
        return choice(list(self.faces()))

    def get_any_face_vertex(self, fkey):
        """Get the identifier of a random vertex of a specific face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Returns
        -------
        hashable
            The identifier of the vertex.

        """
        return self.face_vertices(fkey)[0]

    def key_index(self):
        """Returns a dictionary that maps vertex dictionary keys to the
        corresponding index in a vertex list or array.

        Returns
        -------
        dict
            A dictionary of key-index pairs.

        """
        return {key: index for index, key in enumerate(self.vertices())}

    def index_key(self):
        """Returns a dictionary that maps the indices of a vertex list to
        keys in a vertex dictionary.

        Returns
        -------
        dict
            A dictionary of index-key pairs.

        """
        return dict(enumerate(self.vertices()))

    def key_gkey(self, precision=None):
        """Returns a dictionary that maps vertex dictionary keys to the corresponding
        *geometric key* up to a certain precision.

        Parameters
        ----------
        precision : str (3f)
            The float precision specifier used in string formatting.

        Returns
        -------
        dict
            A dictionary of key-geometric key pairs.

        """
        gkey = geometric_key
        xyz = self.vertex_coordinates
        return {key: gkey(xyz(key), precision) for key in self.vertices()}

    def gkey_key(self, precision=None):
        """Returns a dictionary that maps *geometric keys* of a certain precision
        to the keys of the corresponding vertices.

        Parameters
        ----------
        precision : str (3f)
            The float precision specifier used in string formatting.

        Returns
        -------
        dict
            A dictionary of geometric key-key pairs.

        """
        gkey = geometric_key
        xyz = self.vertex_coordinates
        return {gkey(xyz(key), precision): key for key in self.vertices()}

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex to the volmesh object.

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

        """
        if key is None:
            key = self._max_int_vkey = self._max_int_vkey + 1
        if key > self._max_int_vkey:
            self._max_int_vkey = key
        key = int(key)

        if key not in self.vertex:
            self.vertex[key] = {}
            self.plane[key] = {}
            # self.edge[key] = {}

        attr = attr_dict or {}
        attr.update(kwattr)
        self.vertex[key].update(attr)

        return key

    def add_halfface(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a halfface to the volmesh object.

        Parameters
        ----------
        vertices : list
            A list of ordered vertex keys representing the halfface.
            For every vertex that does not yet exist, a new vertex is created.
        attr_dict : dict, optional
            Halfface attributes.
        kwattr : dict, optional
            Additional named halfface attributes.
            Named halfface attributes overwrite corresponding attributes in the
            attribute dict (``attr_dict``).

        Returns
        -------
        int
            The key of the halfface.
            The key is an integer, if no key was provided.
        hashable
            The key of the halfface.
            Any hashable object may be provided as identifier for the halfface.
            Provided keys are returned unchanged.

        Raises
        ------
        TypeError
            If the provided halfface key is of an unhashable type.

        Notes
        -----
        If no key is provided for the halfface, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

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
        self.halfface[fkey] = vertices
        self.facedata.setdefault(fkey, attr)

        for i in range(-2, len(vertices) - 2):
            u = vertices[i]
            v = vertices[i + 1]
            w = vertices[i + 2]
            if u == v or v == w:
                continue

            self.add_vertex(key=u)
            self.add_vertex(key=v)
            self.add_vertex(key=w)

            if v not in self.plane[u]:
                self.plane[u][v] = {}
            self.plane[u][v][w] = None

            if v not in self.plane[w]:
                self.plane[w][v] = {}
            if u not in self.plane[w][v]:
                self.plane[w][v][u] = None

        #     if v not in self.edge[u] and u not in self.edge[v]:
        #         self.edge[u][v] = {}
        #     if w not in self.edge[v] and v not in self.edge[w]:
        #         self.edge[v][w] = {}

        # u = vertices[-1]
        # v = vertices[0]
        # if v not in self.edge[u] and u not in self.edge[v]:
        #     self.edge[u][v] = {}

        return fkey

    def add_cell(self, halffaces, ckey=None, attr_dict=None, **kwattr):
        """Add a cell to the volmesh object.

        Parameters
        ----------
        halffaces : list of lists
            list of lists of vertex keys defining the halffaces of the cell.
        attr_dict : dict, optional
            cell attributes.
        kwattr : dict, optional
            Additional named cell attributes.
            Named cell attributes overwrite corresponding attributes in the
            attribute dict (``attr_dict``).

        Returns
        -------
        int
            The key of the cell.
            The key is an integer, if no key was provided.
        hashable
            The key of the cell.
            Any hashable object may be provided as identifier for the cell.
            Provided keys are returned unchanged.

        Raises
        ------
        TypeError
            If the provided halfface key is of an unhashable type.

        """
        if ckey is None:
            ckey = self._max_int_ckey = self._max_int_ckey + 1
        if ckey > self._max_int_ckey:
            self._max_int_ckey = ckey
        ckey = int(ckey)

        attr = attr_dict or {}
        attr.update(kwattr)
        self.cell[ckey] = {}
        self.celldata.setdefault(ckey, attr)

        for vertices in halffaces:
            fkey = self.add_halfface(vertices)
            vertices = self.halfface[fkey]
            for i in range(-2, len(vertices) - 2):
                u = vertices[i]
                v = vertices[i + 1]
                w = vertices[i + 2]
                if u not in self.cell[ckey]:
                    self.cell[ckey][u] = {}
                self.cell[ckey][u][v] = fkey
                self.plane[u][v][w] = ckey

        return ckey

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    def delete_vertex(self, vkey):
        raise NotImplementedError

    def insert_vertex(self, hfkey, vkey=None, xyz=None):
        raise NotImplementedError

    def delete_halfface(self, fkey):
        raise NotImplementedError

    def delete_cell(self, ckey):
        raise NotImplementedError

    def cull_vertices(self):
        raise NotImplementedError

    def cull_edges(self):
        raise NotImplementedError

    def cull_halffaces(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------

    def number_of_vertices(self):
        """Count the number of vertices in the volmesh."""
        return len(list(self.vertices()))

    def number_of_edges(self):
        """Count the number of edges in the volmesh."""
        return len(list(self.edges()))

    def number_of_faces(self):
        """Count the number of faces in the volmesh."""
        return len(list(self.faces()))

    def number_of_cells(self):
        """Count the number of faces in the volmesh."""
        return len(list(self.cells()))

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        """Iterate over the vertices of the volmesh.

        Parameters
        ----------
        data : bool, optional
            Return the vertex data as well as the vertex identifiers if true.

        Yields
        ------
        int or tuple
            The next vertex identifier, if ``data`` is false.
            The next vertex identifier and attribute dict as a tuple, if ``data`` is true.

        """
        for vkey in self.vertex:
            if data:
                yield vkey, self.vertex_attributes(vkey)
            else:
                yield vkey

    def edges(self, data=False):
        """Iterate over the edges of the volmesh.

        Parameters
        ----------
        data : bool, optional
            Return the edge data as well as the edge identifiers if true.

        Yields
        ------
        tuple
            The next edge identifier as a tuple of vertex identifiers, if ``data`` is false.
            The next edge identifier and attribute dict as a tuple, if ``data`` is true.

        """
        seen = set()
        for fkey in self.halfface:
            vertices = self.halfface[fkey]
            for u, v in pairwise(vertices + vertices[:1]):
                if (u, v) in seen or (v, u) in seen:
                    continue
                seen.add((u, v))
                seen.add((v, u))
                if not data:
                    yield u, v
                else:
                    yield (u, v), self.edge_attributes((u, v))
        # for u in self.edge:
        #     for v in self.edge[u]:
        #         attr = self.edgedata.setdefault((u, v), self.default_edge_attributes.copy())
        #         if data:
        #             yield u, v, attr
        #         else:
        #             yield u, v

    def halffaces(self, data=False):
        """Iterate over the halffaces of the volmesh.

        Parameters
        ----------
        data : bool, optional
            Return half-face data as well as identifiers if true.

        Yields
        ------
        int or tuple
            The next halfface identifier, if ``data`` is ``False``.
            The next halfface identifier and attributes as a tuple, if ``data`` is ``True``.

        """
        for fkey in self.halfface:
            if data:
                yield fkey, self.face_attributes(fkey)
            else:
                yield fkey

    def faces(self, data=False):
        """"Iterate over the halffaces of the volmesh, and yield unique halffaces.

        Parameters
        ----------
        data : bool, optional
            Return the halfface data as well as the halfface keys.

        Yields
        ------
        int or tuple
            The next halfface identifier, if ``data`` is ``False``.
            The next halfface identifier and attribute dict as a tuple, if ``data`` is ``True``.

        Note
        ----
        Volmesh faces have no topological meaning (analogous to an edge of a mesh).
        They are only used to store data or excute geometric operations (i.e. planarisation).
        Between the interface of two cells, there are two interior halffaces (one from each cell).
        Only one of these two interior halffaces are returned.
        The unique faces are found by comparing string versions of sorted vertex lists.

        """
        seen = set()
        fkeys = []

        for fkey in self.halfface:
            vertices = self.halfface_vertices(fkey)
            key = "-".join(map(str, sorted(vertices, key=int)))
            if key not in seen:
                seen.add(key)
                fkeys.append(fkey)

        for fkey in fkeys:
            if data:
                yield fkey, self.face_attributes(fkey)
            else:
                yield fkey

    def cells(self, data=False):
        """Iterate over the cells of the volmesh.

        Parameters
        ----------
        data : bool, optional
            Return the cell data as well as the cell keys.

        Yields
        ------
        hashable
            The next cell identifier, if ``data`` is ``False``.
        2-tuple
            The next cell identifier and attribute dict as a tuple, if ``data`` is ``True``.

        """
        for ckey in self.cell:
            if data:
                yield ckey, self.cell_attributes(ckey)
            else:
                yield ckey

    def planes(self):
        raise NotImplementedError

    def vertices_where(self):
        raise NotImplementedError

    def edges_where(self):
        raise NotImplementedError

    def faces_where(self):
        raise NotImplementedError

    def cells_where(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # vertex attributes
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

    # --------------------------------------------------------------------------
    # edge attributes
    # --------------------------------------------------------------------------

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
    # face attributes
    # --------------------------------------------------------------------------

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
        if key not in self.halfface:
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
        if key not in self.halfface:
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
        if key not in self.halfface:
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

    # --------------------------------------------------------------------------
    # cell attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    def vertex_neighbors(self, vkey):
        """Return the vertex neighbors of a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The list of neighboring vertices.

        """
        return self.plane[vkey].keys()

    def vertex_halffaces(self, vkey):
        """Halffaces connected to a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The list of halffaces connected to a vertex.

        """
        cells = self.vertex_cells(vkey)

        nbr_vkeys = self.plane[vkey].keys()

        hfkeys = []

        for ckey in cells:
            for v in nbr_vkeys:
                if v in self.cell[ckey][vkey]:
                    hfkeys.append(self.cell[ckey][vkey][v])
                    hfkeys.append(self.cell[ckey][v][vkey])

        return hfkeys

    def vertex_cells(self, vkey):
        """Cells connected to a vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The list of cells connected to a vertex.

        """
        ckeys = set()

        for v in self.plane[vkey].keys():
            for w in self.plane[vkey][v].keys():
                if self.plane[vkey][v][w] is not None:
                    ckeys.add(self.plane[vkey][v][w])

        return list(ckeys)

    def is_vertex_on_boundary(self, vkey):
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
        hfkeys = self.vertex_halffaces(vkey)

        for hfkey in hfkeys:
            if self.is_halfface_on_boundary(hfkey):
                return True

        return False

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    def edge_halffaces(self, u, v):
        """Ordered halffaces adjacent to edge u-v.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex.
        v : hashable
            The identifier of the second vertex.

        Returns
        -------
        list
            List of of keys identifying the adjacent halffaces.

        """
        edge_ckeys = self.plane[u][v].values()
        ckey = edge_ckeys[0]
        ordered_hfkeys = []

        for i in range(len(edge_ckeys) - 1):
            hfkey = self.cell[ckey][u][v]
            w = self.halfface_vertex_descendent(hfkey, v)
            ckey = self.plane[w][v][u]
            ordered_hfkeys.append(hfkey)

        return ordered_hfkeys

    def edge_cells(self, u, v):
        """Ordered cells adjacent to edge u-v.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex.
        v : hashable
            The identifier of the second vertex.

        Returns
        -------
        list
            Ordered List of keys identifying the adjacent cells.

        """
        edge_ckeys = self.plane[u][v].values()
        ckey = edge_ckeys[0]
        ordered_ckeys = [ckey]

        for i in range(len(edge_ckeys) - 1):
            hfkey = self.cell[ckey][u][v]
            w = self.halfface_vertex_descendent(hfkey, v)
            ckey = self.plane[w][v][u]
            ordered_ckeys.append(ckey)

        return ordered_ckeys

    # --------------------------------------------------------------------------
    # halfface topology
    # --------------------------------------------------------------------------

    def halfface_vertices(self, hfkey):
        """The vertices of a halfface.

        Parameters
        ----------
        fkey : hashable
            Identifier of the halfface.

        Returns
        -------
        list
            Ordered vertex identifiers.

        """
        return self.halfface[hfkey]

    def halfface_halfedges(self, hfkey):
        """The halfedges of a halfface.

        Parameters
        ----------
        fkey : hashable
            Identifier of the halfface.

        Returns
        -------
        list
            The halfedges of a halfface.

        """
        vertices = self.halfface_vertices(hfkey)

        return list(pairwise(vertices + vertices[0:1]))

    def halfface_opposite_halfface(self, hfkey):
        """The opposite halfface of a halfface.

        Parameters
        ----------
        hfkey : hashable
            Identifier of the halfface.

        Returns
        -------
        hfkey
            Identifier of the opposite halfface.

        Note
        ----
        For a boundary halfface, the opposite hlafface is None.

        """
        u, v, w = self.halfface[hfkey][0:3]

        nbr_ckey = self.plane[w][v][u]

        if not nbr_ckey:
            return None

        return self.cell[nbr_ckey][v][u]

    def halfface_vertex_ancestor(self, hfkey, vkey):
        """Return the vertex before the specified vertex in a specific halfface.

        Parameters
        ----------
        hfkey : hashable
            Identifier of the halfface.
        vkey : hashable
            The identifier of the vertex.

        Returns
        -------
        hashable
            The identifier of the vertex before the given vertex in the halfface cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the halfface.

        """
        i = self.halfface[hfkey].index(vkey)

        return self.halfface[hfkey][i - 1]

    def halfface_vertex_descendent(self, hfkey, vkey):
        """Return the vertex after the specified vertex in a specific halfface.

        Parameters
        ----------
        hfkey : hashable
            Identifier of the halfface.
        vkey : hashable
            The identifier of the vertex.

        Returns
        -------
        hashable
            The identifier of the vertex after the given vertex in the halfface cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the halfface.

        """
        if self.halfface[hfkey][-1] == vkey:
            return self.halfface[hfkey][0]

        i = self.halfface[hfkey].index(vkey)

        return self.halfface[hfkey][i + 1]

    def halfface_cell(self, hfkey):
        """The cell to which the halfface belongs to.

        Parameters
        ----------
        fkey : hashable
            Identifier of the halfface.

        Returns
        -------
        ckey
            Identifier of th cell.

        """
        u, v, w = self.halfface[hfkey][0:3]

        return self.plane[u][v][w]

    def is_halfface_on_boundary(self, hfkey):
        """Verify that a halfface is on a boundary.

        Parameters
        ----------
        key : hashable
            The identifier of the halfface.

        Returns
        -------
        bool
            True if the halfface is on the boundary.
            False otherwise.

        """
        u, v, w = self.halfface[hfkey][0:3]

        if self.plane[w][v][u] is None:
            return True

        return False

    # --------------------------------------------------------------------------
    # cell topology
    # --------------------------------------------------------------------------

    def cell_vertices(self, ckey):
        """The vertices of a cell.

        Parameters
        ----------
        ckey : hashable
            Identifier of the cell.

        Returns
        -------
        list
            The vertex identifiers of a cell.

        """
        return list(set([key for fkey in self.cell_halffaces(ckey) for key in self.halfface_vertices(fkey)]))

    def cell_halfedges(self, ckey):
        """The halfedges of a cell.

        Parameters
        ----------
        ckey : hashable
            Identifier of the cell.

        Returns
        -------
        list
            The halfedges of a cell.

        """
        halfedges = []

        for fkey in self.cell_halffaces(ckey):
            halfedges += self.halfface_halfedges(fkey)

        return halfedges

    def cell_edges(self, ckey):
        """The edges of a cell.

        Parameters
        ----------
        ckey : hashable
            Identifier of the cell.

        Returns
        -------
        list
            The edges of a cell.

        """
        edges = []

        halfedges = self.cell_halfedges(ckey)

        for (u, v) in halfedges:
            if v in self.edge[u]:
                edges.append((u, v))

        return edges

    def cell_halffaces(self, ckey):
        """The halffaces of a cell.

        Parameters
        ----------
        ckey : hashable
            Identifier of the cell.

        Returns
        -------
        list
            The halffaces of a cell.

        """

        hfkeys = []

        for u in self.cell[ckey]:
            for v in self.cell[ckey][u]:
                hfkeys.append(self.cell[ckey][u][v])

        return hfkeys

    def cell_vertex_neighbors(self, ckey, vkey):
        """Ordered vertex neighbors of a vertex of a cell.

        Parameters
        ----------
        ckey : hashable
            Identifier of the cell.

        Returns
        -------
        list
            The list of neighboring vertices.

        """
        nbr_vkeys = self.cell[ckey][vkey].keys()

        u = vkey
        v = nbr_vkeys[0]

        ordered_vkeys = [v]

        for i in range(len(nbr_vkeys) - 1):
            hfkey = self.cell[ckey][u][v]
            v = self.halfface_vertex_ancestor(hfkey, u)
            ordered_vkeys.append(v)

        return ordered_vkeys

    def cell_vertex_halffaces(self, ckey, vkey):
        """Ordered halffaces connected to a vertex of a cell.

        Parameters
        ----------
        ckey : hashable
            Identifier of the cell.

        Returns
        -------
        list
            The ordered list of halffaces connected to a vertex of a cell.

        """
        nbr_vkeys = self.cell[ckey][vkey].keys()

        u = vkey
        v = nbr_vkeys[0]

        ordered_hfkeys = []

        for i in range(len(nbr_vkeys)):
            hfkey = self.cell[ckey][u][v]
            v = self.halfface_vertex_ancestor(hfkey, u)
            ordered_hfkeys.append(hfkey)

        return ordered_hfkeys

    def cell_neighbors(self, ckey):
        """Return the cell neighbors of a cell across its halffaces.

        Parameters
        ----------
        ckey : hashable
            Identifier of the cell.

        Returns
        -------
        list
            The identifiers of the neighboring cells.

        """
        ckeys = []

        for fkey in self.cell_halffaces(ckey):
            u, v, w = self.halfface[fkey][0:3]
            nbr = self.plane[w][v][u]

            if nbr is not None:
                ckeys.append(nbr)

        return ckeys

    def cell_pair_halffaces(self, ckey_1, ckey_2):
        """Given 2 ckeys, returns the interfacing halffaces, respectively.

        Parameters
        ----------
        ckey_1 : hashable
            Identifier of the cell 1.
        ckey_2 : hashable
            Identifier of the cell 2.

        Returns
        -------
        hfkey_1
            The identifier of the halfface belonging to cell 1 .
        hfkey_2
            The identifier of the halfface belonging to cell 2.

        """
        for hfkey in self.cell_halffaces(ckey_1):
            u, v, w = self.halfface[hfkey][0:3]
            nbr = self.plane[w][v][u]

            if nbr == ckey_2:
                return hfkey, self.halfface_opposite_halfface(hfkey)

        return

    def cell_to_mesh(self, ckey):
        """Construct a mesh from a cell.

        Parameters
        ----------
        hfkey : hashable
            Identifier of the cell.

        Returns
        -------
        Mesh
            A mesh object.

        """
        vertices, halffaces = self.cell_to_vertices_and_halffaces(ckey)
        return Mesh.from_vertices_and_faces(vertices, halffaces)

    def cell_to_vertices_and_halffaces(self, ckey):
        """Return the vertices and halffaces of a cell.

        Returns
        -------
        tuple
            A 2-tuple containing

            * a list of vertices, represented by their XYZ coordinates, and
            * a list of halffaces.

            Each halfface is a list of indices referencing the list of vertex coordinates.

        """
        vkeys = self.cell_vertices(ckey)
        hfkeys = self.cell_halffaces(ckey)

        vkey_vindex = dict((vkey, index) for index, vkey in enumerate(vkeys))

        vertices = [self.vertex_coordinates(vkey) for vkey in vkeys]
        halffaces = [[vkey_vindex[vkey] for vkey in self.halfface[fkey]] for fkey in hfkeys]

        return vertices, halffaces

    def cell_tree(self, root):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # volmesh geometry
    # --------------------------------------------------------------------------

    def centroid(self):
        """Compute the centroid of the volmesh.

        Parameters
        ----------

        Returns
        -------
        list
            The coordinates of the centroid.

        """
        xyz = [self.vertex_coordinates(vkey) for vkey in self.vertex]

        return centroid_points(xyz)

    def bounding_box(self):
        """Compute the x, y, z dimensinos of the bounding box of the volmesh.

        Parameters
        ----------

        Returns
        -------
        float
            The x dimension of the bounding box.
        float
            The y dimension of the bounding box.
        float
            The z dimensino of the bounding box.

        """
        xyz = [self.vertex_coordinates(vkey) for vkey in self.vertex]

        x_sorted = sorted(xyz, key=lambda k: k[0])
        y_sorted = sorted(xyz, key=lambda k: k[1])
        z_sorted = sorted(xyz, key=lambda k: k[2])

        x = abs(x_sorted[0][0] - x_sorted[-1][0])
        y = abs(y_sorted[0][1] - y_sorted[-1][1])
        z = abs(z_sorted[0][2] - z_sorted[-1][2])

        return x, y, z

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, vkey, axes='xyz'):
        """Return the coordinates of a vertex.

        Parameters
        ----------
        vkey : hashable
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
        return [self.vertex[vkey][axis] for axis in axes]

    def vertex_normal(self, vkey):
        """Return the normal vector at the vertex as the weighted average of the
        normals of the neighboring halffaces.

        Parameters
        ----------
        vkey : hashable
            The identifier of the vertex.

        Returns
        -------
        list
            The components of the normal vector.

        """
        vectors = []

        for hfkey in self.vertex_halffaces(vkey):
            if self.is_halfface_on_boundary(hfkey):
                vectors.append(self.halfface_normal(hfkey))

        return normalize_vector(centroid_points(vectors))

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

    def halfface_coordinates(self, hfkey):
        """Compute the coordinates of the vertices of a halfface.

        Parameters
        ----------
        hfkey : hashable
            The identifier of the halfface.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of ``'x'``, ``'y'``, ``'z'``.
            Default is ``'xyz'``.

        Returns
        -------
        list of list
            The coordinates of the vertices of the halfface.

        """
        return [self.vertex_coordinates(key) for key in self.halfface_vertices(hfkey)]

    def halfface_normal(self, hfkey, unitized=True):
        """Compute the non-oriented normal of a halfface.

        Parameters
        ----------
        fkey : hashable
            The identifier of the halfface.
        unitized : bool, optional
            Unitize the normal vector.
            Default is ``True``.

        Returns
        -------
        list
            The components of the normal vector.

        """
        return normal_polygon(self.halfface_coordinates(hfkey), unitized=unitized)

    def halfface_centroid(self, hfkey):
        """Compute the location of the centroid of a halfface.

        Parameters
        ----------
        hfkey : hashable
            The identifier of the halfface.

        Returns
        -------
        list
            The coordinates of the centroid.

        """
        return centroid_polygon(self.halfface_coordinates(hfkey))

    def halfface_center(self, hfkey):
        """Compute the location of the center of mass of a halfface.

        Parameters
        ----------
        hfkey : hashable
            The identifier of the halfface.

        Returns
        -------
        list
            The coordinates of the center of mass.

        """
        return centroid_polygon(self.halfface_coordinates(hfkey))

    def halfface_area(self, hfkey):
        """Compute the non-oriented area of a halfface.

        Parameters
        ----------
        fkey : hashable
            The identifier of the face.

        Returns
        -------
        float
            The non-oriented area of the face.

        """
        return area_polygon(self.halfface_coordinates(hfkey))

    def face_coordinates(self, fkey):
        return self.halfface_coordinates(fkey)

    def face_center(self, fkey):
        return centroid_polygon(self.halfface_coordinates(fkey))

    # --------------------------------------------------------------------------
    # cell geometry
    # --------------------------------------------------------------------------

    def cell_centroid(self, ckey):
        """Compute the location of the centroid of a cell.

        Parameters
        ----------
        ckey : hashable
            The identifier of the cell.

        Returns
        -------
        list
            The coordinates of the centroid.

        """
        vkeys = self.cell_vertices(ckey)

        return centroid_points([self.vertex_coordinates(vkey) for vkey in vkeys])

    def cell_center(self, ckey):
        """Compute the location of the center of mass of a cell.

        Parameters
        ----------
        ckey : hashable
            The identifier of the cell.

        Returns
        -------
        list
            The coordinates of the center of mass.

        """
        vertices, halffaces = self.cell_to_vertices_and_halffaces(ckey)

        return centroid_polyhedron((vertices, halffaces))

    # --------------------------------------------------------------------------
    # boundary / interior
    # --------------------------------------------------------------------------

    def halffaces_interior(self):
        """Find all interior halffaces.

        Returns
        -------
        list
            All interior halffaces.

        """
        halffaces = set(self.halfface.keys())
        halffaces_on_boundary = set(self.halffaces_on_boundary())

        return halffaces - halffaces_on_boundary

    def faces_interior(self):
        """Find the interior faces (unique halffaces).

        Returns
        -------
        list
            The unique interior faces (unique halffaces).

        """
        faces = set(self.halfface.keys())
        faces_on_boundary = set(self.halffaces_on_boundary())

        return faces - faces_on_boundary

    def halffaces_on_boundary(self):
        """Find the halffaces on the boundary.

        Returns
        -------
        list
            The halffaces on the boundary.

        """
        hfkeys = set()

        for hfkey in self.faces():
            if self.is_halfface_on_boundary(hfkey):
                hfkeys.add(hfkey)

        return list(hfkeys)

    # --------------------------------------------------------------------------
    # geometric operations
    # --------------------------------------------------------------------------

    def scale(self, factor=1.0):
        """Scale the entire volmesh object.

        Parameters
        ----------
        factor : float
            Scaling factor.

        Returns
        -------
        Volmesh
            The volmesh with updated XYZ coordinates.

        """
        for key in self.vertex:
            attr = self.vertex[key]
            attr['x'] *= factor
            attr['y'] *= factor
            attr['z'] *= factor


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    # import compas

    # volmesh = VolMesh.from_obj(compas.get('boxes.obj'))

    # volmesh.summary()

    # for key, attr in volmesh.vertices(True):
    #     print(key, attr)

    import doctest
    doctest.testmod(globs=globals())
