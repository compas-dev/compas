from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ast import literal_eval as _eval
from copy import deepcopy

from compas.files.obj import OBJ

from compas.geometry import centroid_points

from compas.datastructures import Datastructure
from compas.datastructures import Mesh

from compas.datastructures._mixins import VertexAttributesManagement
from compas.datastructures._mixins import VertexHelpers
from compas.datastructures._mixins import VertexCoordinatesDescriptors
from compas.datastructures._mixins import VertexFilter

from compas.datastructures._mixins import EdgeAttributesManagement
from compas.datastructures._mixins import EdgeHelpers
from compas.datastructures._mixins import EdgeGeometry

from compas.datastructures._mixins import FaceAttributesManagement
from compas.datastructures._mixins import FaceHelpers

from compas.datastructures._mixins import FromToData
from compas.datastructures._mixins import FromToJson


__all__ = ['VolMesh']


class VolMesh(FromToData,
              FromToJson,
              FaceHelpers,
              EdgeHelpers,
              VertexHelpers,
              EdgeGeometry,
              VertexCoordinatesDescriptors,
              FaceAttributesManagement,
              EdgeAttributesManagement,
              VertexAttributesManagement,
              Datastructure,
              VertexFilter):
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
        self._max_int_key  = -1
        self._max_int_fkey = -1
        self._max_int_ckey = -1
        self._key_to_str   = False

        self.vertex   = {}
        self.edge     = {}
        self.halfface = {}
        self.cell     = {}
        self.plane    = {}

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
        """"""
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    @property
    def name(self):
        """The name of the mesh."""
        return self.attributes.get('name', None)

    @name.setter
    def name(self, value):
        self.attributes['name'] = value

    @property
    def color(self):
        return dict(
            (key[6:], self.attributes[key])
            for key in self.attributes if key.startswith('color.')
        )

    @color.setter
    def color(self, value):
        try:
            value[0]
            value[1]
            value[1][2]
        except Exception:
            return
        self.attributes['color.{0}'.format(value[0])] = value[1]

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
            'facedata'    : {},
            'celldata'    : {},
            'max_int_key' : self._max_int_key,
            'max_int_fkey': self._max_int_fkey,
            'max_int_ckey': self._max_int_ckey, }

        key_rkey = {}

        for key in self.vertex:
            rkey = repr(key)
            key_rkey[key] = rkey
            data['vertex'][rkey] = self.vertex[key]
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
        facedata     = data.get('facedata') or {}
        celldata     = data.get('celldata') or {}
        max_int_key  = data.get('max_int_key', - 1)
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
            k = _eval(_k)
            self.vertex[k] = self.default_vertex_attributes.copy()
            if attr:
                self.vertex[k].update(attr)
            self.plane[k] = {}
            self.edge[k] = {}

        for _u, nbrs in edge.iteritems():
            nbrs = nbrs or {}
            u = _eval(_u)
            for _v, attr in nbrs.iteritems():
                v = _eval(_v)
                self.edge[u][v] = self.default_edge_attributes.copy()
                if attr:
                    self.edge[u][v].update(attr)

        for _f in halfface:
            f = _eval(_f)
            self.halfface[f] = {}
            for _u, _v in halfface[_f].iteritems():
                u = _eval(_u)
                v = _eval(_v)
                self.halfface[f][u] = v

        for _u in plane:
            u = _eval(_u)
            for _v in plane[_u]:
                v = _eval(_v)
                if v not in self.plane[u]:
                    self.plane[u][v] = {}
                for _w, _c in plane[_u][_v].iteritems():
                    w = _eval(_w)
                    c = _eval(_c)
                    self.plane[u][v][w] = c

        for _c in cell:
            c = _eval(_c)
            self.cell[c] = {}
            for _u in cell[_c]:
                u = _eval(_u)
                if u not in self.cell[c]:
                    self.cell[c][u] = {}
                for _v, _f in cell[_c][_u].iteritems():
                    v = _eval(_v)
                    f = _eval(_f)
                    self.cell[c][u][v] = f

        for fkey, attr in iter(facedata.items()):
            self.facedata[_eval(fkey)] = attr or {}

        for ckey, attr in iter(celldata.items()):
            self.celldata[_eval(ckey)] = attr or {}

        self._max_int_key = max_int_key
        self._max_int_fkey = max_int_fkey
        self._max_int_ckey = max_int_ckey

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath):
        """Construct a volmesh object from the data described in an OBJ file.

        """
        obj = OBJ(filepath)
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
            List of halffaces (list of vertices).

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
        del self.cell
        del self.halfface
        del self.plane
        del self.facedata
        del self.celldata
        self.vertex        = {}
        self.cell          = {}
        self.halfface      = {}
        self.plane         = {}
        self.edge          = {}
        self.facedata      = {}
        self.celldata      = {}
        self._max_int_key  = -1
        self._max_int_fkey = -1
        self._max_int_ckey = -1

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    # add all vertices of a halfface in one go
    # loop over 3-windows of returned vertex keys
    # store halffaces as lists
    # loop over halfface cycles as 3-windows
    # find unique faces by comparing string versions of sorted vertex lists

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

    def add_halfface(self, vertices, fkey=None):
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
        if vertices[0] == vertices[-1]:
            vertices = vertices[:-1]
        if vertices[-2] == vertices[-1]:
            vertices = vertices[:-1]

        if len(vertices) < 3:
            raise Exception('Corrupt halfface.')

        fkey = self._get_face_key(fkey)
        self.halfface[fkey] = vertices
        self.facedata[fkey] = self.default_face_attributes

        edge_attr = self.default_edge_attributes

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
        ckey = self._get_cellkey(ckey)

        self.cell[ckey]     = {}
        self.celldata[ckey] = self.default_cell_attributes

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

    def number_of_cells(self):
        """Count the number of faces in the mesh."""
        return len(list(self.cells()))

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        for key in self.vertex:
            if data:
                yield key, self.vertex[key]
            else:
                yield key

    def cells(self, data=False):
        for ckey in self.cell:
            if data:
                raise NotImplementedError
            else:
                yield ckey

    def planes(self):
        raise NotImplementedError

    def edges(self, data=False):
        for u in self.edge:
            for v in self.edge[u]:
                if data:
                    yield u, v, self.edge[u][v]
                else:
                    yield u, v

    def faces(self):
        """"Return unique" halfface keys."""
        seen = set()
        faces = []
        for fkey in self.halfface:
            vertices = self.halfface_vertices(fkey)
            key = "-".join(map(str, sorted(vertices, key=int)))
            if key not in seen:
                seen.add(key)
                faces.append(fkey)
        return faces

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    def vertex_neighbors(self, vkey):
        return self.plane[vkey].keys()

    # --------------------------------------------------------------------------
    # halfface topology
    # --------------------------------------------------------------------------

    def halfface_vertices(self, fkey):
        return self.halfface[fkey]

    def halfface_cell(self, fkey):
        u = self.halfface[fkey][0]
        v = self.halfface[fkey][1]
        w = self.halfface[fkey][2]
        return self.plane[u][v][w]

    def halfface_edges(self, fkey):
        vertices = self.halfface[fkey]
        edges = []
        for i in range(-1, len(vertices) - 1):
            edges.append((vertices[i], vertices[i + 1]))
        return edges

    def halfface_adjacency(self, ckey):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # cell topology
    # --------------------------------------------------------------------------

    def cell_neighbors(self, ckey):
        nbrs = []
        for fkey in self.cell_halffaces(ckey):
            u, v, w = self.halfface[fkey][0:3]
            nbr = self.plane[w][v][u]
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def cell_vertex_neighbors(self, ckey):
        raise NotImplementedError

    def cell_halffaces(self, ckey):
        halffaces = set()
        for u in self.cell[ckey]:
            for v in self.cell[ckey][u]:
                fkey = self.cell[ckey][u][v]
                halffaces.add(fkey)
        return list(halffaces)

    def cell_vertices(self, ckey):
        return list(set([key for fkey in self.cell_halffaces(ckey) for key in self.halfface_vertices(fkey)]))

    def cell_edges(self, ckey):
        halfedges = []
        for fkey in self.cell_halffaces(ckey):
            halfedges += self.halfface_edges(fkey)
        edges = set(frozenset(uv) for uv in halfedges)
        return map(list, edges)

    def cell_vertices_and_halffaces(self, ckey):
        vkeys = self.cell_vertices(ckey)
        fkeys = self.cell_halffaces(ckey)
        vkey_vindex = dict((vkey, index) for index, vkey in enumerate(vkeys))
        vertices = [self.vertex_coordinates(vkey) for vkey in vkeys]
        halffaces = [[vkey_vindex[vkey] for vkey in self.halfface[fkey]] for fkey in fkeys]
        return vertices, halffaces

    def cell_adjacency(self):
        raise NotImplementedError

    def cell_tree(self, root):
        raise NotImplementedError

    def cell_mesh(self, ckey):
        vertices, halffaces = self.cell_vertices_and_halffaces(ckey)
        return Mesh.from_vertices_and_faces(vertices, halffaces)

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, vkey, axes='xyz'):
        attr = self.vertex[vkey]
        return [attr[axis] for axis in axes]

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    def edge_coordinates(self, u, v, axes='xyz'):
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    # --------------------------------------------------------------------------
    # face geometry
    # --------------------------------------------------------------------------

    def face_coordinates(self, fkey, axes='xyz'):
        vertices = self.halfface[fkey]
        return [self.vertex_coordinates(key, axes=axes) for key in vertices]

    # --------------------------------------------------------------------------
    # cell geometry
    # --------------------------------------------------------------------------

    def cell_centroid(self, ckey):
        vkeys = self.cell_vertices(ckey)
        return centroid_points([self.vertex_coordinates(vkey) for vkey in vkeys])

    def cell_center(self, ckey):
        edges = self.cell_edges(ckey)
        return center_of_mass([(self.vertex_coordinates(u), self.vertex_coordinates(v)) for u, v in edges])

    # --------------------------------------------------------------------------
    # geometric operations
    # --------------------------------------------------------------------------

    def scale(self, factor=1.0):
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

    # def update_default_edge_attributes(self, attr_dict=None, **kwargs):
    #     if not attr_dict:
    #         attr_dict = {}
    #     attr_dict.update(kwargs)
    #     self.default_edge_attributes.update(attr_dict)
    #     for u, v in self.edges_iter():
    #         attr = attr_dict.copy()
    #         attr.update(self.edge[u][v])
    #         self.edge[u][v] = attr

    # def set_edge_attribute(self, u, v, name, value):
    #     self.edge[u][v][name] = value

    # def set_edge_attributes(self, u, v, attr_dict=None, **kwattr):
    #     attr_dict = attr_dict or kwattr
    #     attr_dict.update(kwattr)
    #     self.edge[u][v].update(attr_dict)

    # def set_edges_attribute(self, name, value, keys=None):
    #     if not keys:
    #         for u, v, attr in self.edges_iter(True):
    #             attr[name] = value
    #     else:
    #         for u, v in keys:
    #             self.edge[u][v][name] = value

    # def set_edges_attributes(self, keys=None, attr_dict=None, **kwattr):
    #     attr_dict = attr_dict or {}
    #     attr_dict.update(kwattr)
    #     if not keys:
    #         for u, v, attr in self.edges_iter(True):
    #             attr.update(attr_dict)
    #     else:
    #         for u, v in keys:
    #             self.edge[u][v].update(attr_dict)

    # def get_edge_attribute(self, u, v, name, default=None):
    #     if u in self.edge[v]:
    #         return self.edge[v][u].get(name, default)
    #     return self.edge[u][v].get(name, default)

    # def get_edge_attributes(self, u, v, names, defaults=None):
    #     if not defaults:
    #         defaults = [None] * len(names)
    #     if v in self.edge[u]:
    #         return [self.edge[u][v].get(name, default) for name, default in zip(names, defaults)]
    #     return [self.edge[v][u].get(name, default) for name, default in zip(names, defaults)]

    # def get_edges_attribute(self, name, default=None, keys=None):
    #     if not keys:
    #         return [attr.get(name, default) for u, v, attr in self.edges_iter(True)]
    #     return [self.edge[u][v].get(name, default) for u, v in keys]

    # def get_edges_attributes(self, names, defaults=None, keys=None):
    #     if not defaults:
    #         defaults = [None] * len(names)
    #     temp = zip(names, defaults)
    #     if not keys:
    #         return [[attr.get(name, default) for name, default in temp] for u, v, attr in self.edges_iter(True)]
    #     return [[self.edge[u][v].get(name, default) for name, default in temp] for u, v in keys]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas
    # from compas.viewers import VolMeshViewer
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
