from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import pickle
import json

from copy import deepcopy
from ast import literal_eval

from compas.files import OBJ

from compas.utilities import pairwise

from compas.geometry import normalize_vector
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import centroid_polyhedron
from compas.geometry import area_polygon
from compas.geometry import normal_polygon

from compas.datastructures import Datastructure

from compas.datastructures import Mesh

from compas.datastructures._mixins import VertexAttributesManagement
from compas.datastructures._mixins import VertexHelpers
from compas.datastructures._mixins import VertexFilter

from compas.datastructures._mixins import EdgeAttributesManagement
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


__all__ = ['VolMesh']


TPL = """
================================================================================
Volesh summary
================================================================================

- name: {}
- vertices: {}
- cells: {}

================================================================================
"""


class VolMesh(FromToPickle,
              FromToJson,
              FromToData,
              VertexFilter,
              VertexHelpers,
              VertexMappings,
              EdgeFilter,
              EdgeHelpers,
              EdgeGeometry,
              EdgeMappings,
              FaceFilter,
              FaceHelpers,
              FaceMappings,
              VertexAttributesManagement,
              EdgeAttributesManagement,
              FaceAttributesManagement,
              Datastructure):
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

    __module__ = 'compas.datastructures'

    def __init__(self):
        self._max_int_vkey = -1
        self._max_int_fkey = -1
        self._max_int_ckey = -1
        self._key_to_str   = False

        self.vertex   = {}
        self.edge     = {}
        self.halfface = {}
        self.cell     = {}
        self.plane    = {}

        self.edgedata = {}
        self.facedata = {}
        self.celldata = {}

        self.attributes = {'name'                : 'VolMesh',
                           'color.vertex'        : (255, 255, 255),
                           'color.edge'          : (0, 0, 0),
                           'color.face'          : (200, 200, 200),
                           'color.normal:vertex' : (0, 255, 0),
                           'color.normal:face'   : (0, 255, 0)}

        self.default_vertex_attributes = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.default_edge_attributes   = {}
        self.default_face_attributes   = {}
        self.default_cell_attributes   = {}

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

    def __str__(self):
        """Generate a readable representation of the data of the volmesh."""
        return json.dumps(self.data, sort_keys=True, indent=4)

    def summary(self):
        """Print a summary of the volmesh."""
        numv = self.number_of_vertices()
        numc = self.number_of_cells()
        s    = TPL.format(self.name, numv, numc)
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
            'attributes'  : self.attributes,
            'dva'         : self.default_vertex_attributes,
            'dea'         : self.default_edge_attributes,
            'dfa'         : self.default_face_attributes,
            'dca'         : self.default_cell_attributes,
            'vertex'      : {},
            'edge'        : {},
            'halfface'    : {},
            'cell'        : {},
            'plane'       : {},
            'edgedata'    : {},
            'facedata'    : {},
            'celldata'    : {},
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
        attributes   = data.get('attributes') or {}
        dva          = data.get('dva') or {}
        dea          = data.get('dea') or {}
        dfa          = data.get('dfa') or {}
        dca          = data.get('dca') or {}
        vertex       = data.get('vertex') or {}
        edge         = data.get('edge') or {}
        halfface     = data.get('halfface') or {}
        cell         = data.get('cell') or {}
        plane        = data.get('plane') or {}
        edgedata     = data.get('edgedata') or {}
        facedata     = data.get('facedata') or {}
        celldata     = data.get('celldata') or {}
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

    def dump(self, filepath):
        """Dump the data representing the volmesh to a file using Python's built-in
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
            'dca'         : self.default_cell_attributes,
            'vertex'      : self.vertex,
            'edge'        : self.edge,
            'halfface'    : self.face,
            'cell'        : self.cell,
            'plane'       : self.plane,
            'facedata'    : self.facedata,
            'celldata'    : self.celldata,
            'max_int_vkey': self._max_int_vkey,
            'max_int_fkey': self._max_int_fkey,
            'max_int_ckey': self._max_int_ckey,
        }
        with open(filepath, 'wb+') as fo:
            pickle.dump(data, fo, protocol=pickle.HIGHEST_PROTOCOL)

    def dumps(self):
        """Dump the data representing the volmesh to a string using Python's built-in
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
            'dca'         : self.default_cell_attributes,
            'vertex'      : self.vertex,
            'edge'        : self.edge,
            'halfface'    : self.face,
            'cell'        : self.cell,
            'plane'       : self.plane,
            'facedata'    : self.facedata,
            'celldata'    : self.celldata,
            'max_int_vkey': self._max_int_vkey,
            'max_int_fkey': self._max_int_fkey,
            'max_int_ckey': self._max_int_ckey,
        }
        return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, filepath):
        """Load serialised volmesh data from a pickle file.

        Parameters
        ----------
        filepath : str
            The path to the pickle file.

        """
        with open(filepath, 'rb') as fo:
            data = pickle.load(fo)

        self.attributes                = data['attributes']
        self.default_vertex_attributes = data['dva']
        self.default_edge_attributes   = data['dea']
        self.default_face_attributes   = data['dfa']
        self.default_cell_attributes   = data['dca']
        self.vertex                    = data['vertex']
        self.edge                      = data['edge']
        self.halfface                  = data['halfface']
        self.cell                      = data['cell']
        self.plane                     = data['plane']
        self.edgedata                  = data['edgedata']
        self.facedata                  = data['facedata']
        self.celldata                  = data['celldata']
        self._max_int_vkey             = data['max_int_vkey']
        self._max_int_fkey             = data['max_int_fkey']
        self._max_int_fkey             = data['max_int_fkey']

    def loads(self, s):
        """Load serialised volmesh data from a pickle string.

        Parameters
        ----------
        s : str
            The pickled string.

        """
        data = pickle.loads(s)

        self.attributes                = data['attributes']
        self.default_vertex_attributes = data['dva']
        self.default_edge_attributes   = data['dea']
        self.default_face_attributes   = data['dfa']
        self.default_cell_attributes   = data['dca']
        self.vertex                    = data['vertex']
        self.edge                      = data['edge']
        self.halfface                  = data['halfface']
        self.cell                      = data['cell']
        self.plane                     = data['plane']
        self.edgedata                  = data['edgedata']
        self.facedata                  = data['facedata']
        self.celldata                  = data['celldata']
        self._max_int_vkey             = data['max_int_vkey']
        self._max_int_fkey             = data['max_int_fkey']
        self._max_int_fkey             = data['max_int_fkey']

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

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

        for halffaces in cells:
            volmesh.add_cell(halffaces)

        return volmesh

    @classmethod
    def from_vertices_and_edges(cls, vertices, edges):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_obj(self, filepath):
        raise NotImplementedError

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

        vertices  = [self.vertex_coordinates(vkey) for vkey in self.vertices()]
        cells = []

        for ckey in self.cell:
            halffaces = [[key_index[vkey] for vkey in self.halfface[fkey]] for fkey in self.halffaces()]
            cells.append(halffaces)

        return vertices, halffaces

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def _get_vertex_key(self, vkey):
        if vkey is None:
            vkey = self._max_int_vkey = self._max_int_vkey + 1
        else:
            try:
                i = int(vkey)
            except (ValueError, TypeError):
                pass
            else:
                if i > self._max_int_vkey:
                    self._max_int_vkey = i
        if self._key_to_str:
            return str(vkey)
        return vkey

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

    def _get_cellkey(self, ckey):
        if ckey is None:
            ckey = self._max_int_ckey = self._max_int_ckey + 1
        else:
            try:
                i = int(ckey)
            except (ValueError, TypeError):
                pass
            else:
                if i > self._max_int_ckey:
                    self._max_int_ckey = i
        return ckey

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
        self.vertex        = {}
        self.edge          = {}
        self.halfface      = {}
        self.cell          = {}
        self.plane         = {}
        self.edgedata      = {}
        self.facedata      = {}
        self.celldata      = {}
        self._max_int_vkey  = -1
        self._max_int_fkey = -1
        self._max_int_ckey = -1

    def clear_vertexdict(self):
        """Clear only the vertices."""
        del self.vertex
        self.vertex = {}
        self._max_int_vkey = -1

    def clear_halffacedict(self):
        """Clear only the halffaces."""
        del self.halfface
        del self.facedata
        self.halfface = {}
        self.facedata = {}
        self._max_int_fkey = -1

    def clear_celldict(self):
        """Clear only the cells."""
        del self.cell
        del self.celldata
        self.cell = {}
        self.celldata = {}
        self._max_int_ckey = -1

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_vertex(self, vkey=None, attr_dict=None, **kwattr):
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
        vkey = self._get_vertex_key(vkey)

        attr = self.default_vertex_attributes.copy()
        if attr_dict:
            attr.update(attr_dict)
        attr.update(kwattr)

        if vkey not in self.vertex:
            self.vertex[vkey] = attr
            self.plane[vkey]  = {}
            self.edge[vkey]   = {}

        return vkey

    def add_halfface(self, vertices, hfkey=None, attr_dict=None, **kwattr):
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
        self._clean_vertices(vertices)

        if len(vertices) < 3:
            raise Exception('Corrupt halfface.')

        face_attr = self._compile_fattr(attr_dict, kwattr)
        edge_attr = self.default_edge_attributes.copy()

        hfkey = self._get_face_key(hfkey)

        self.halfface[hfkey] = vertices
        self.facedata[hfkey] = face_attr

        for i in range(-2, len(vertices) - 2):
            u = vertices[i]
            v = vertices[i + 1]
            w = vertices[i + 2]

            self.add_vertex(vkey=u)
            self.add_vertex(vkey=v)
            self.add_vertex(vkey=w)

            if v not in self.plane[u]:
                self.plane[u][v] = {}

            self.plane[u][v][w] = None

            if v not in self.plane[w]:
                self.plane[w][v] = {}
            if u not in self.plane[w][v]:
                self.plane[w][v][u] = None

            if v not in self.edge[u] and u not in self.edge[v]:
                self.edge[u][v] = edge_attr
            if w not in self.edge[v] and v not in self.edge[w]:
                self.edge[v][w] = edge_attr

        u = vertices[-1]
        v = vertices[0]

        if v not in self.edge[u] and u not in self.edge[v]:
            self.edge[u][v] = edge_attr

        return hfkey

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
        ckey = self._get_cellkey(ckey)

        self.cell[ckey]     = {}
        self.celldata[ckey] = self.default_cell_attributes

        for vertices in halffaces:
            hfkey = self.add_halfface(vertices)

            vertices = self.halfface[hfkey]

            for i in range(-2, len(vertices) - 2):
                u = vertices[i]
                v = vertices[i + 1]
                w = vertices[i + 2]

                if u not in self.cell[ckey]:
                    self.cell[ckey][u] = {}

                self.cell[ckey][u][v] = hfkey
                self.plane[u][v][w]   = ckey

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
            Return the vertex data as well as the vertex keys.

        Yields
        ------
        hashable
            The next vertex identifier (*vkey*), if ``data`` is false.
        2-tuple
            The next vertex as a (vkey, attr) tuple, if ``data`` is true.

        """
        for vkey in self.vertex:
            if data:
                yield vkey, self.vertex[vkey]
            else:
                yield vkey

    def edges(self, data=False):
        """Iterate over the edges of the volmesh.

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

        """
        for u in self.edge:
            for v in self.edge[u]:

                attr = self.edgedata.setdefault((u, v), self.default_edge_attributes.copy())

                if data:
                    yield u, v, attr
                else:
                    yield u, v

    def halffaces(self, data=False):
        """Iterate over the halffaces of the volmesh.

        Parameters
        ----------
        data : bool, optional
            Return the halfface data as well as the halfface keys.

        Yields
        ------
        hashable
            The next halfface identifier (*hfkey*), if ``data`` is ``False``.
        2-tuple
            The next halfface as a (hfkey, attr) tuple, if ``data`` is ``True``.

        """
        for hfkey in self.halfface:
            if data:
                yield hfkey, self.facedata.setdefault(hfkey, self.default_face_attributes.copy())
            else:
                yield hfkey

    def faces(self, data=False):
        """"Iterate over the halffaces of the volmesh, and yield unique halffaces.

        Parameters
        ----------
        data : bool, optional
            Return the halfface data as well as the halfface keys.

        Yields
        ------
        hashable
            The next halfface identifier (*fkey*), if ``data`` is ``False``.
        2-tuple
            The next halfface as a (fkey, attr) tuple, if ``data`` is ``True``.

        Note
        ----
        Volmesh faces have no topological meaning (analogous to an edge of a mesh).
        They are only used to store data or excute mass geometric operations (i.e. planarisation).
        Between the interface of two cells, there are two interior halffaces (one from each cell).
        Only one of these two interior halffaces are returned.
        The unique faces are found by comparing string versions of sorted vertex lists

        """
        seen = set()
        unique_hfkeys = []
        for fkey in self.halfface:
            vertices = self.halfface_vertices(fkey)
            key = "-".join(map(str, sorted(vertices, key=int)))
            if key not in seen:
                seen.add(key)
                unique_hfkeys.append(fkey)

        for fkey in unique_hfkeys:
            if data:
                yield fkey, self.facedata.setdefault(fkey, self.default_face_attributes.copy())
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
            The next celle identifier (*ckey*), if ``data`` is ``False``.
        2-tuple
            The next cell as a (ckey, attr) tuple, if ``data`` is ``True``.

        """
        for ckey in self.cell:
            if data:
                yield ckey, self.celldata.setdefault(ckey, self.default_cell_attributes.copy())
            else:
                yield ckey

    def planes(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # special accessors
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
        cells     = self.vertex_cells(vkey)

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
        edge_ckeys     = self.plane[u][v].values()
        ckey           = edge_ckeys[0]
        ordered_hfkeys = []

        for i in range(len(edge_ckeys) - 1):
            hfkey = self.cell[ckey][u][v]
            w     = self.halfface_vertex_descendent(hfkey, v)
            ckey  = self.plane[w][v][u]
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
        edge_ckeys    = self.plane[u][v].values()
        ckey          = edge_ckeys[0]
        ordered_ckeys = [ckey]

        for i in range(len(edge_ckeys) - 1):
            hfkey = self.cell[ckey][u][v]
            w     = self.halfface_vertex_descendent(hfkey, v)
            ckey  = self.plane[w][v][u]
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
            v     = self.halfface_vertex_ancestor(hfkey, u)
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
            v     = self.halfface_vertex_ancestor(hfkey, u)
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

        vertices    = [self.vertex_coordinates(vkey) for vkey in vkeys]
        halffaces   = [[vkey_vindex[vkey] for vkey in self.halfface[fkey]] for fkey in hfkeys]

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

    # inherited from EdgeGeometryMixin

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

    # --------------------------------------------------------------------------
    # vertex attributes
    # --------------------------------------------------------------------------

    # def update_default_vertex_attributes(self, attr_dict=None, **kwattr):
    #     if not attr_dict:
    #         attr_dict = {}
    #     attr_dict.update(kwattr)
    #     self.default_vertex_attributes.update(attr_dict)
    #     for key in self.vertex:
    #         attr = attr_dict.copy()
    #         attr.update(self.vertex[key])
    #         self.vertex[key] = attr

    # def set_vertex_attribute(self, key, name, value):
    #     self.vertex[key][name] = value

    # def set_vertex_attributes(self, key, attr_dict=None, **kwattr):
    #     attr_dict = attr_dict or {}
    #     attr_dict.update(kwattr)
    #     self.vertex[key].update(attr_dict)

    # def set_vertices_attribute(self, name, value, keys=None):
    #     if not keys:
    #         for key, attr in self.vertices_iter(True):
    #             attr[name] = value
    #     else:
    #         for key in keys:
    #             self.vertex[key][name] = value

    # def set_vertices_attributes(self, keys=None, attr_dict=None, **kwattr):
    #     attr_dict = attr_dict or {}
    #     attr_dict.update(kwattr)
    #     if not keys:
    #         for key, attr in self.vertices_iter(True):
    #             attr.update(attr_dict)
    #     else:
    #         for key in keys:
    #             self.vertex[key].update(attr_dict)

    # def get_vertex_attribute(self, key, name, default=None):
    #     return self.vertex[key].get(name, default)

    # def get_vertex_attributes(self, key, names, defaults=None):
    #     if not defaults:
    #         defaults = [None] * len(names)
    #     return [self.vertex[key].get(name, default) for name, default in zip(names, defaults)]

    # def get_vertices_attribute(self, name, default=None, keys=None):
    #     if not keys:
    #         return [attr.get(name, default) for key, attr in self.vertices_iter(True)]
    #     return [self.vertex[key].get(name, default) for key in keys]

    # def get_vertices_attributes(self, names, defaults=None, keys=None):
    #     if not defaults:
    #         defaults = [None] * len(names)
    #     temp = zip(names, defaults)
    #     if not keys:
    #         return [[attr.get(name, default) for name, default in temp] for key, attr in self.vertices_iter(True)]
    #     return [[self.vertex[key].get(name, default) for name, default in temp] for key in keys]

    # --------------------------------------------------------------------------
    # edge attributes
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
    # face attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # cell attributes
    # --------------------------------------------------------------------------


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas
    from compas.viewers import Viewer

    mesh = VolMesh.from_obj(compas.get('boxes.obj'))

    mesh.scale(0.5)

    mesh = VolMesh.from_data(mesh.to_data())

    viewer = Viewer()

    viewer.mesh = mesh

    viewer.show()

    # viewer = VolMeshViewer(mesh, 600, 600, grid_on=False, zoom=5.)

    # viewer.grid_on = False
    # viewer.axes_on = False

    # viewer.axes.x_color = (0.1, 0.1, 0.1)
    # viewer.axes.y_color = (0.1, 0.1, 0.1)
    # viewer.axes.z_color = (0.1, 0.1, 0.1)

    # viewer.setup()

    # viewer.camera.zoom_out(5)
    # viewer.show()
