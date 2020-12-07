from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ast import literal_eval
from random import sample
from random import choice
from distutils.version import LooseVersion

import compas

from ...datastructure import Datastructure
from ...attributes import VertexAttributeView
from ...attributes import EdgeAttributeView
from ...attributes import FaceAttributeView

from compas.utilities import pairwise
from compas.utilities import window


__all__ = ['HalfEdge']


class HalfEdge(Datastructure):
    """Base half-edge data structure for representing meshes.

    Attributes
    ----------
    attributes : dict
        Named attributes related to the data structure as a whole.
    default_vertex_attributes : dict
        Named attributes and default values of the vertices of the data structure.
    default_edge_attributes : dict
        Named attributes and default values of the edges of the data structure.
    default_face_attributes : dict
        Named attributes and default values of the faces of the data structure.
    name : str
        Name of the data structure.
        Defaults to the value of `self.__class__.__name__`.
    data : dict
        The data representation of the data structure.
    adjacency : dict
        Alias for `self.halfedge`.

        .. deprecated:: 0.17.0

    """

    @property
    def DATASCHEMA(self):
        import schema
        if LooseVersion(compas.__version__) < LooseVersion('0.16.5'):
            return schema.Schema({
                "attributes": dict,
                "dva": dict,
                "dea": dict,
                "dfa": dict,
                "vertex": schema.And(
                    dict,
                    lambda x: all(isinstance(key, int) for key in x)
                ),
                "face": schema.And(
                    dict,
                    lambda x: all(isinstance(key, int) for key in x),
                    lambda x: all(all(isinstance(item, int) for item in value) for value in x.values())
                ),
                "facedata": schema.And(
                    dict,
                    lambda x: all(isinstance(key, int) for key in x),
                    lambda x: all(isinstance(value, dict) for value in x.values())
                ),
                "edgedata": dict,
                "max_int_key": schema.And(int, lambda x: x >= -1),
                "max_int_fkey": schema.And(int, lambda x: x >= -1)
            })
        return schema.Schema({
            "compas": str,
            "datatype": str,
            "data": {
                "attributes": dict,
                "dva": dict,
                "dea": dict,
                "dfa": dict,
                "vertex": schema.And(
                    dict,
                    lambda x: all(isinstance(key, int) for key in x)
                ),
                "face": schema.And(
                    dict,
                    lambda x: all(isinstance(key, int) for key in x),
                    lambda x: all(all(isinstance(item, int) for item in value) for value in x.values())
                ),
                "facedata": schema.And(
                    dict,
                    lambda x: all(isinstance(key, int) for key in x),
                    lambda x: all(isinstance(value, dict) for value in x.values())
                ),
                "edgedata": schema.And(
                    dict,
                    lambda x: all(isinstance(key, str) for key in x),
                    lambda x: all(isinstance(value, dict) for value in x.values())
                ),
                "max_vertex": schema.And(int, lambda x: x >= -1),
                "max_face": schema.And(int, lambda x: x >= -1)
            }
        })

    @property
    def JSONSCHEMA(self):
        version = LooseVersion(compas.__version__)
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "$id": "https://github.com/compas-dev/compas/schemas/halfedge.json",
            "$compas": version.vstring.split('-')[0],
        }
        data = {
            "type": "object",
            "properties": {
                "attributes":   {"type": "object"},
                "dva":          {"type": "object"},
                "dea":          {"type": "object"},
                "dfa":          {"type": "object"},
                "vertex":       {"type": "object"},
                "face":         {"type": "object"},
                "facedata":     {"type": "object"},
                "edgedata":     {"type": "object"},
                "max_vertex":   {"type": "number"},
                "max_face":     {"type": "number"}
            },
            "required": ["attributes", "dva", "dea", "dfa", "vertex", "face", "facedata", "edgedata", "max_vertex", "max_face"]
        }
        if version < LooseVersion('0.16.5'):
            schema.update(data)
        else:
            meta = {
                "type": "object",
                "properties": {
                    "compas": {"type": "string"},
                    "datatype": {"type": "string"},
                    "data": data
                },
                "required": ["compas", "datatype", "data"]
            }
            schema.update(meta)
        return schema

    def __init__(self):
        super(HalfEdge, self).__init__()
        self._max_vertex = -1
        self._max_face = -1
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
    # descriptors
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
        """
        data = {
            'attributes': self.attributes,
            'dva': self.default_vertex_attributes,
            'dea': self.default_edge_attributes,
            'dfa': self.default_face_attributes,
            'vertex': self.vertex,
            'face': self.face,
            'facedata': self.facedata,
        }
        version = LooseVersion(compas.__version__)
        if version < LooseVersion('0.16.5'):
            data['edgedata'] = {repr(key): self.edgedata[key] for key in self.edgedata}
            data['max_int_key'] = self._max_vertex
            data['max_int_fkey'] = self._max_face
            return data
        data['edgedata'] = self.edgedata
        data['max_vertex'] = self._max_vertex
        data['max_face'] = self._max_face
        return {
            'compas': version.vstring.split('-')[0],
            'datatype': self.dtype,
            'data': data
        }

    @data.setter
    def data(self, data):
        if 'compas' in data:
            version = LooseVersion(compas.__version__)
            if version < LooseVersion('0.16.5'):
                raise Exception('The data was generated with an incompatible newer version of COMPAS: {}'.format(version.vstring.split('-')[0]))
            # dtype = data['dtype']
            data = data['data']
            attributes = data['attributes']
            dva = data.get('dva') or {}
            dfa = data.get('dfa') or {}
            dea = data.get('dea') or {}
            vertex = data.get('vertex') or {}
            face = data.get('face') or {}
            facedata = data.get('facedata') or {}
            edgedata = data.get('edgedata') or {}
            max_vertex = data.get('max_vertex', -1)
            max_face = data.get('max_face', -1)
            self.attributes.update(attributes)
            self.default_vertex_attributes.update(dva)
            self.default_face_attributes.update(dfa)
            self.default_edge_attributes.update(dea)
            self.vertex = {}
            self.face = {}
            self.halfedge = {}
            self.facedata = {}
            self.edgedata = {}
            # this could be handled by the schema
            # but will not work in IronPython
            for key, attr in iter(vertex.items()):
                self.add_vertex(int(key), attr_dict=attr)
            for fkey, vertices in iter(face.items()):
                attr = facedata.get(fkey) or {}
                self.add_face(vertices, fkey=int(fkey), attr_dict=attr)
            for uv, attr in iter(edgedata.items()):
                self.edgedata[uv] = attr or {}
            self._max_vertex = max_vertex
            self._max_face = max_face
        else:
            attributes = data['attributes']
            dva = data.get('dva') or {}
            dfa = data.get('dfa') or {}
            dea = data.get('dea') or {}
            vertex = data.get('vertex') or {}
            face = data.get('face') or {}
            facedata = data.get('facedata') or {}
            edgedata = data.get('edgedata') or {}
            max_vertex = data.get('max_int_key', -1)
            max_face = data.get('max_int_fkey', -1)
            self.attributes.update(attributes)
            self.default_vertex_attributes.update(dva)
            self.default_face_attributes.update(dfa)
            self.default_edge_attributes.update(dea)
            self.vertex = {}
            self.face = {}
            self.halfedge = {}
            self.facedata = {}
            self.edgedata = {}
            # this could be handled by the schema
            # but will not work in IronPython
            for key, attr in iter(vertex.items()):
                self.add_vertex(int(key), attr_dict=attr)
            for fkey, vertices in iter(face.items()):
                attr = facedata.get(fkey) or {}
                self.add_face(vertices, fkey=int(fkey), attr_dict=attr)
            for edge, attr in iter(edgedata.items()):
                key = "-".join(map(str, sorted(literal_eval(edge))))
                if key not in self.edgedata:
                    self.edgedata[key] = {}
                if attr:
                    self.edgedata[key].update(attr)
            self._max_vertex = max_vertex
            self._max_face = max_face

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

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
        self._max_vertex = -1
        self._max_face = -1

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

    vertex_index = key_index

    def index_key(self):
        """Returns a dictionary that maps the indices of a vertex list to
        keys in a vertex dictionary.

        Returns
        -------
        dict
            A dictionary of index-key pairs.

        """
        return dict(enumerate(self.vertices()))

    index_vertex = index_key

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
            key = self._max_vertex = self._max_vertex + 1
        if key > self._max_vertex:
            self._max_vertex = key
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
        if vertices[-1] == vertices[0]:
            vertices = vertices[:-1]
        vertices = [int(key) for key in vertices]
        vertices[:] = [u for u, v in pairwise(vertices + vertices[:1]) if u != v]
        if len(vertices) < 3:
            return
        if fkey is None:
            fkey = self._max_face = self._max_face + 1
        if fkey > self._max_face:
            self._max_face = fkey
        attr = attr_dict or {}
        attr.update(kwattr)
        self.face[fkey] = vertices
        self.facedata.setdefault(fkey, attr)
        for u, v in pairwise(vertices + vertices[:1]):
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

        Notes
        -----
        In some cases, disconnected vertices can remain after application of this
        method. To remove these vertices as well, combine this method with vertex
        culling (:meth:`cull_vertices`).

        Examples
        --------
        >>>
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
            edge = "-".join(map(str, sorted([nbr, key])))
            if edge in self.edgedata:
                del self.edgedata[edge]
        for nbr in nbrs:
            for n in self.vertex_neighbors(nbr):
                if self.halfedge[nbr][n] is None and self.halfedge[n][nbr] is None:
                    del self.halfedge[nbr][n]
                    del self.halfedge[n][nbr]
                    edge = "-".join(map(str, sorted([nbr, n])))
                    if edge in self.edgedata:
                        del self.edgedata[edge]
        del self.halfedge[key]
        del self.vertex[key]

    def delete_face(self, fkey):
        """Delete a face from the mesh object.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Notes
        -----
        In some cases, disconnected vertices can remain after application of this
        method. To remove these vertices as well, combine this method with vertex
        culling (:meth:`cull_vertices`).

        Examples
        --------
        >>>
        """
        for u, v in self.face_halfedges(fkey):
            self.halfedge[u][v] = None
            if self.halfedge[v][u] is None:
                del self.halfedge[u][v]
                del self.halfedge[v][u]
                edge = "-".join(map(str, sorted([u, v])))
                if edge in self.edgedata:
                    del self.edgedata[edge]
        del self.face[fkey]
        if fkey in self.facedata:
            del self.facedata[fkey]

    def remove_unused_vertices(self):
        """Remove all unused vertices from the mesh object.
        """
        for u in list(self.vertices()):
            if u not in self.halfedge:
                del self.vertex[u]
            else:
                if not self.halfedge[u]:
                    del self.vertex[u]
                    del self.halfedge[u]

    cull_vertices = remove_unused_vertices

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

        Notes
        ----
        Mesh edges have no topological meaning. They are only used to store data.
        Edges are not automatically created when vertices and faces are added to
        the mesh. Instead, they are created when data is stored on them, or when
        they are accessed using this method.

        This method yields the directed edges of the mesh.
        Unless edges were added explicitly using :meth:`add_edge` the order of
        edges is *as they come out*. However, as long as the toplogy remains
        unchanged, the order is consistent.

        Examples
        --------
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

    def vertices_where(self, conditions, data=False):
        """Get vertices for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            Yield the vertices and their data attributes.
            Default is ``False``.

        Yields
        ------
        key: hashable
            The next vertex that matches the condition.
        2-tuple
            The next vertex and its attributes, if ``data=True``.

        """
        for key, attr in self.vertices(True):
            is_match = True

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if callable(method):
                    val = method(key)

                    if isinstance(val, list):
                        if value not in val:
                            is_match = False
                            break
                        break

                    if isinstance(value, (tuple, list)):
                        minval, maxval = value
                        if val < minval or val > maxval:
                            is_match = False
                            break
                    else:
                        if value != val:
                            is_match = False
                            break

                else:
                    if name not in attr:
                        is_match = False
                        break

                    if isinstance(attr[name], list):
                        if value not in attr[name]:
                            is_match = False
                            break
                        break

                    if isinstance(value, (tuple, list)):
                        minval, maxval = value
                        if attr[name] < minval or attr[name] > maxval:
                            is_match = False
                            break
                    else:
                        if value != attr[name]:
                            is_match = False
                            break

            if is_match:
                if data:
                    yield key, attr
                else:
                    yield key

    def vertices_where_predicate(self, predicate, data=False):
        """Get vertices for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate. The callable takes 2 parameters: ``key``, ``attr`` and should return ``True`` or ``False``.
        data : bool, optional
            Yield the vertices and their data attributes.
            Default is ``False``.

        Yields
        ------
        key: hashable
            The next vertex that matches the condition.
        2-tuple
            The next vertex and its attributes, if ``data=True``.

        Examples
        --------
        >>>
        """
        for key, attr in self.vertices(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    def edges_where(self, conditions, data=False):
        """Get edges for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            Yield the edges and their data attributes.
            Default is ``False``.

        Yields
        ------
        2-tuple
            The next edge as a (u, v) tuple, if ``data=False``.
        3-tuple
            The next edge as a (u, v, data) tuple, if ``data=True``.
        """
        for key in self.edges():
            is_match = True

            attr = self.edge_attributes(key)

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if method and callable(method):
                    val = method(key)
                elif name in attr:
                    val = attr[name]
                else:
                    is_match = False
                    break

                if isinstance(val, list):
                    if value not in val:
                        is_match = False
                        break
                elif isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if val < minval or val > maxval:
                        is_match = False
                        break
                else:
                    if value != val:
                        is_match = False
                        break

            if is_match:
                if data:
                    yield key, attr
                else:
                    yield key

    def edges_where_predicate(self, predicate, data=False):
        """Get edges for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate. The callable takes 3 parameters: ``u``, ``v``, ``attr`` and should return ``True`` or ``False``.
        data : bool, optional
            Yield the vertices and their data attributes.
            Default is ``False``.

        Yields
        ------
        2-tuple
            The next edge as a (u, v) tuple, if ``data=False``.
        3-tuple
            The next edge as a (u, v, data) tuple, if ``data=True``.

        Examples
        --------
        >>>
        """
        for key, attr in self.edges(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    def faces_where(self, conditions, data=False):
        """Get faces for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            Yield the faces and their data attributes.
            Default is ``False``.

        Yields
        ------
        key: hashable
            The next face that matches the condition.
        2-tuple
            The next face and its attributes, if ``data=True``.

        """
        for fkey in self.faces():
            is_match = True

            attr = self.face_attributes(fkey)

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if method and callable(method):
                    val = method(fkey)
                elif name in attr:
                    val = attr[name]
                else:
                    is_match = False
                    break

                if isinstance(val, list):
                    if value not in val:
                        is_match = False
                        break
                elif isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if val < minval or val > maxval:
                        is_match = False
                        break
                else:
                    if value != val:
                        is_match = False
                        break

            if is_match:
                if data:
                    yield fkey, attr
                else:
                    yield fkey

    def faces_where_predicate(self, predicate, data=False):
        """Get faces for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate. The callable takes 2 parameters: ``key``, ``attr`` and should return ``True`` or ``False``.
        data : bool, optional
            Yield the faces and their data attributes.
            Default is ``False``.

        Yields
        ------
        key: hashable
            The next face that matches the condition.
        2-tuple
            The next face and its attributes, if ``data=True``.

        Examples
        --------
        >>>
        """
        for fkey, attr in self.faces(True):
            if predicate(fkey, attr):
                if data:
                    yield fkey, attr
                else:
                    yield fkey

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

        Notes
        -----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary,
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
        if values is not None:
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
        if values is not None:
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

        Notes
        ----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary,
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
        if values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                if key not in self.facedata:
                    self.facedata[key] = {}
                self.facedata[key][name] = value
            return
        # use it as a getter
        if not names:
            return FaceAttributeView(self.default_face_attributes, self.facedata.setdefault(key, {}))
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
        if values is not None:
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

        Notes
        ----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary,
        if they exist.
        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_edge_attributes.update(attr_dict)

    def edge_attribute(self, edge, name, value=None):
        """Get or set an attribute of an edge.

        Parameters
        ----------
        edge : 2-tuple of int
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
        u, v = edge
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(edge)
        key = "-".join(map(str, sorted(edge)))
        if value is not None:
            if key not in self.edgedata:
                self.edgedata[key] = {}
            self.edgedata[key][name] = value
            return
        if key in self.edgedata and name in self.edgedata[key]:
            return self.edgedata[key][name]
        if name in self.default_edge_attributes:
            return self.default_edge_attributes[name]

    def unset_edge_attribute(self, edge, name):
        """Unset the attribute of an edge.

        Parameters
        ----------
        edge : tuple of int
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
        u, v = edge
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(edge)
        key = "-".join(map(str, sorted(edge)))
        if key in self.edgedata and name in self.edgedata[key]:
            del self.edgedata[key][name]

    def edge_attributes(self, edge, names=None, values=None):
        """Get or set multiple attributes of an edge.

        Parameters
        ----------
        edge : 2-tuple of int
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
        u, v = edge
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(edge)
        if values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                self.edge_attribute(edge, name, value)
            return
        # use it as a getter
        if not names:
            key = "-".join(map(str, sorted(edge)))
            # get the entire attribute dict
            return EdgeAttributeView(self.default_edge_attributes, self.edgedata.setdefault(key, {}))
        # get only the values of the named attributes
        values = []
        for name in names:
            value = self.edge_attribute(edge, name)
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
        keys : list of edges, optional
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
        edges = keys or self.edges()
        if value is not None:
            for edge in edges:
                self.edge_attribute(edge, name, value)
            return
        return [self.edge_attribute(edge, name) for edge in edges]

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
        keys : list of edges, optional
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
        edges = keys or self.edges()
        if values is not None:
            for edge in edges:
                self.edge_attributes(edge, names, values)
            return
        return [self.edge_attributes(edge, names) for edge in edges]

    # --------------------------------------------------------------------------
    # mesh info
    # --------------------------------------------------------------------------

    def summary(self):
        """Print a summary of the mesh.

        Returns
        -------
        str
        """
        tpl = "\n".join(["{} summary", "=" * (len(self.name) + len(" summary")), "- vertices: {}", "- edges: {}", "- faces: {}"])
        return tpl.format(self.name, self.number_of_vertices(), self.number_of_edges(), self.number_of_faces())

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
        """Calculate the Euler characteristic.

        Returns
        -------
        int
            The Euler characteristic.
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

    def has_vertex(self, key):
        """Verify that a vertex is in the mesh.

        Parameters
        ----------
        key : int
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

        Notes
        -----
        Due to the nature of the ordering algorithm, the neighbors cycle around
        the node in the opposite direction as the cycling direction of the faces.
        For some algorithms this produces the expected results. For others it doesn't.
        For example, a dual mesh constructed relying on these conventions will have
        oposite face cycle directions compared to the original.

        Examples
        --------
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

        Notes
        -----
        The vertices in the neighborhood are unordered.

        Examples
        --------
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

        Examples
        --------
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

    def has_edge(self, key):
        """Verify that the mesh contains a specific edge.

        Warnings
        --------
        This method may produce unexpected results.

        Parameters
        ----------
        key : tuple of int
            The identifier of the edge.

        Returns
        -------
        bool
            True if the edge exists.
            False otherwise.
        """
        return key in set(self.edges())

    def has_halfedge(self, key):
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
            If the edge is on the boundary, one of the identifiers is ``None``.
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

    def edge_loop(self, edge):
        """Find all edges on the same loop as a given edge.

        Parameters
        ----------
        edge : tuple of int
            The identifier of the starting edge.

        Returns
        -------
        list of tuple of int
            The edges on the same loop as the given edge.
        """
        if self.is_edge_on_boundary(*edge):
            return self._edge_loop_on_boundary(edge)
        edges = []
        current, previous = edge
        edges.append((previous, current))
        while True:
            if current == edge[1]:
                break
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
            edges.append((previous, current))
        edges[:] = [(u, v) for v, u in edges[::-1]]
        if edges[0][0] == edges[-1][1]:
            return edges
        previous, current = edge
        while True:
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
            edges.append((previous, current))
        return edges

    def _edge_loop_on_boundary(self, uv):
        """Find all edges on the same loop as a given edge on the boundary."""
        edges = []
        current, previous = uv
        edges.append((previous, current))
        while True:
            if current == uv[1]:
                break
            nbrs = self.vertex_neighbors(current)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == previous:
                    continue
                if self.is_edge_on_boundary(current, temp):
                    nbr = temp
                    break
            if nbr is None:
                break
            previous, current = current, nbr
            edges.append((previous, current))
        edges[:] = [(u, v) for v, u in edges[::-1]]
        if edges[0][0] == edges[-1][1]:
            return edges
        previous, current = uv
        while True:
            nbrs = self.vertex_neighbors(current)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == previous:
                    continue
                if self.is_edge_on_boundary(current, temp):
                    nbr = temp
                    break
            if nbr is None:
                break
            previous, current = current, nbr
            edges.append((previous, current))
        return edges

    def edge_strip(self, edge):
        """Find all edges on the same strip as a given edge.

        Parameters
        ----------
        edge : tuple of int
            The identifier of the starting edge.

        Returns
        -------
        list of tuple of int
            The edges on the same strip as the given edge.
        """
        edges = []
        v, u = edge
        while True:
            edges.append((u, v))
            face = self.halfedge[u][v]
            if face is None:
                break
            vertices = self.face_vertices(face)
            if len(vertices) != 4:
                break
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
        edges[:] = [(u, v) for v, u in edges[::-1]]
        u, v = edge
        while True:
            face = self.halfedge[u][v]
            if face is None:
                break
            vertices = self.face_vertices(face)
            if len(vertices) != 4:
                break
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
            edges.append((u, v))
        return edges

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    def has_face(self, fkey):
        """Verify that a face is part of the mesh.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the face exists.
            False otherwise.

        Examples
        --------
        >>>
        """
        return fkey in self.face

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

        Examples
        --------
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

        Notes
        -----
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

    face_vertex_after = face_vertex_descendant
    face_vertex_before = face_vertex_ancestor

    def halfedge_after(self, u, v):
        face = self.halfedge_face(u, v)
        w = self.face_vertex_after(face, v)
        return v, w

    def halfedge_before(self, u, v):
        face = self.halfedge_face(u, v)
        t = self.face_vertex_before(face, u)
        return t, u


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
