from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from random import sample
from random import choice

from compas.datastructures.datastructure import Datastructure
from compas.datastructures.attributes import VertexAttributeView
from compas.datastructures.attributes import EdgeAttributeView
from compas.datastructures.attributes import FaceAttributeView

from compas.utilities import pairwise
from compas.utilities import window


class HalfEdge(Datastructure):
    """Base half-edge data structure for representing the topology of open oor closed surface meshes.

    Parameters
    ----------
    name: str, optional
        The name of the datastructure.
    default_vertex_attributes: dict, optional
        Default values for vertex attributes.
    default_edge_attributes: dict, optional
        Default values for edge attributes.
    default_face_attributes: dict, optional
        Default values for face attributes.

    Attributes
    ----------
    attributes : dict[str, Any]
        General attributes of the data structure that are included in the data representation and serialization.
    default_vertex_attributes : dict[str, Any]
        Dictionary containing default values for the attributes of vertices.
        It is recommended to add a default to this dictionary using :meth:`update_default_vertex_attributes`
        for every vertex attribute used in the data structure.
    default_edge_attributes : dict[str, Any]
        Dictionary containing default values for the attributes of edges.
        It is recommended to add a default to this dictionary using :meth:`update_default_edge_attributes`
        for every edge attribute used in the data structure.
    default_face_attributes : dict[str, Any]
        Dictionary contnaining default values for the attributes of faces.
        It is recommended to add a default to this dictionary using :meth:`update_default_face_attributes`
        for every face attribute used in the data structure.

    """

    def __init__(
        self,
        name=None,
        default_vertex_attributes=None,
        default_edge_attributes=None,
        default_face_attributes=None,
    ):
        super(HalfEdge, self).__init__()
        self._max_vertex = -1
        self._max_face = -1
        self.vertex = {}
        self.halfedge = {}
        self.face = {}
        self.facedata = {}
        self.edgedata = {}
        self.attributes = {"name": name or "HalfEdge"}
        self.default_vertex_attributes = {}
        self.default_edge_attributes = {}
        self.default_face_attributes = {}
        if default_vertex_attributes:
            self.default_vertex_attributes.update(default_vertex_attributes)
        if default_edge_attributes:
            self.default_edge_attributes.update(default_edge_attributes)
        if default_face_attributes:
            self.default_face_attributes.update(default_face_attributes)

    def __str__(self):
        tpl = "<HalfEdge with {} vertices, {} faces, {} edges>"
        return tpl.format(self.number_of_vertices(), self.number_of_faces(), self.number_of_edges())

    # --------------------------------------------------------------------------
    # descriptors
    # --------------------------------------------------------------------------

    @property
    def name(self):
        return self.attributes.get("name") or self.__class__.__name__

    @name.setter
    def name(self, value):
        self.attributes["name"] = value

    @property
    def adjacency(self):
        return self.halfedge

    @property
    def DATASCHEMA(self):
        import schema
        from compas.data import is_sequence_of_uint

        return schema.Schema(
            {
                "attributes": dict,
                "dva": dict,
                "dea": dict,
                "dfa": dict,
                "vertex": schema.And(
                    dict,
                    is_sequence_of_uint,
                ),
                "face": schema.And(
                    dict,
                    is_sequence_of_uint,
                    lambda x: all(all(isinstance(item, int) for item in value) for value in x.values()),
                    lambda x: all(all(item >= 0 for item in value) for value in x.values()),
                    lambda x: all(len(value) > 2 for value in x.values()),
                    lambda x: all(len(value) == len(set(value)) for value in x.values()),
                ),
                "facedata": schema.And(
                    dict,
                    is_sequence_of_uint,
                    lambda x: all(isinstance(value, dict) for value in x.values()),
                ),
                "edgedata": schema.And(
                    dict,
                    lambda x: all(isinstance(key, str) for key in x),
                    lambda x: all(isinstance(value, dict) for value in x.values()),
                ),
                "max_vertex": schema.And(int, lambda x: x >= -1),
                "max_face": schema.And(int, lambda x: x >= -1),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        return "halfedge"

    @property
    def data(self):
        return {
            "attributes": self.attributes,
            "dva": self.default_vertex_attributes,
            "dea": self.default_edge_attributes,
            "dfa": self.default_face_attributes,
            "vertex": self.vertex,
            "face": self.face,
            "facedata": self.facedata,
            "edgedata": self.edgedata,
            "max_vertex": self._max_vertex,
            "max_face": self._max_face,
        }

    @data.setter
    def data(self, data):
        if "data" in data:
            data = data["data"]
        self.attributes.update(data.get("attributes") or {})
        self.default_vertex_attributes.update(data.get("dva") or {})
        self.default_face_attributes.update(data.get("dfa") or {})
        self.default_edge_attributes.update(data.get("dea") or {})
        self.vertex = {}
        self.face = {}
        self.halfedge = {}
        self.facedata = {}
        self.edgedata = {}
        vertex = data.get("vertex") or {}
        face = data.get("face") or {}
        facedata = data.get("facedata") or {}
        edgedata = data.get("edgedata") or {}
        for key, attr in iter(vertex.items()):
            self.add_vertex(int(key), attr_dict=attr)
        for fkey, vertices in iter(face.items()):
            attr = facedata.get(fkey) or {}
            self.add_face(vertices, fkey=int(fkey), attr_dict=attr)
        for uv, attr in iter(edgedata.items()):
            self.edgedata[uv] = attr or {}
        self._max_vertex = data.get("max_vertex", -1)
        self._max_face = data.get("max_face", -1)

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def clear(self):
        """Clear all the mesh data.

        Returns
        -------
        None

        """
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

        .. deprecated:: 1.13.3
            Use :meth:`vertex_sample` instead.

        Returns
        -------
        int
            The identifier of the vertex.

        """
        return self.get_any_vertices(1)[0]

    def get_any_vertices(self, n, exclude_leaves=False):
        """Get a list of identifiers of a random set of n vertices.

        .. deprecated:: 1.13.3
            Use :meth:`vertex_sample` instead.

        Parameters
        ----------
        n : int
            The number of random vertices.
        exclude_leaves : bool, optional
            If True, exclude the leaves (vertices with only one connected edge) from the set.

        Returns
        -------
        list[int]
            The identifiers of the vertices.

        """
        if exclude_leaves:
            vertices = set(self.vertices()) - set(self.leaves())
        else:
            vertices = self.vertices()
        return sample(list(vertices), n)

    def get_any_face(self):
        """Get the identifier of a random face.

        .. deprecated:: 1.13.3
            Use :meth:`face_sample` instead.

        Returns
        -------
        int
            The identifier of the face.

        """
        return choice(list(self.faces()))

    def vertex_sample(self, size=1):
        """A random sample of the vertices.

        Parameters
        ----------
        size : int, optional
            The number of vertices in the random sample.

        Returns
        -------
        list[int]
            The identifiers of the vertices.

        """
        return sample(list(self.vertices()), size)

    def edge_sample(self, size=1):
        """A random sample of the edges.

        Parameters
        ----------
        size : int, optional
            The number of edges in the random sample.

        Returns
        -------
        list[tuple[int, int]]
            The identifiers of the edges.

        """
        return sample(list(self.edges()), size)

    def face_sample(self, size=1):
        """A random sample of the faces.

        Parameters
        ----------
        size : int, optional
            The number of faces in the random sample.

        Returns
        -------
        list[int]
            The identifiers of the faces.

        """
        return sample(list(self.faces()), size)

    def key_index(self):
        """Returns a dictionary that maps vertex dictionary keys to the
        corresponding index in a vertex list or array.

        Returns
        -------
        dict[int, int]
            A dictionary of key-index pairs.

        """
        return {key: index for index, key in enumerate(self.vertices())}

    vertex_index = key_index

    def index_key(self):
        """Returns a dictionary that maps the indices of a vertex list to
        keys in a vertex dictionary.

        Returns
        -------
        dict[int, int]
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
        attr_dict : dict[str, Any], optional
            A dictionary of vertex attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

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
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh()
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
        vertices : list[int]
            A list of vertex keys.
        attr_dict : dict[str, Any], optional
            A dictionary of face attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

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

        Returns
        -------
        None

        Notes
        -----
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

        Returns
        -------
        None

        Notes
        -----
        In some cases, disconnected vertices can remain after application of this
        method. To remove these vertices as well, combine this method with vertex
        culling (:meth:`cull_vertices`).

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

        Returns
        -------
        None

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
            If True, yield the vertex attributes in addition to the vertex identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex identifier.
            If `data` is True, the next vertex as a (key, attr) tuple.

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
            If True, yield the face attributes in addition to the face identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face identifier.
            If `data` is True, the next face as a (fkey, attr) tuple.

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
            If True, yield the edge attributes in addition to the edge identifiers.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a ((u, v), data) tuple.

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

    def vertices_where(self, conditions=None, data=False, **kwargs):
        """Get vertices for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the vertex attributes in addition to the vertex identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex that matches the condition.
            If `data` is True, the next vertex and its attributes.

        """
        conditions = conditions or {}
        conditions.update(kwargs)

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
            The condition you want to evaluate.
            The callable takes 2 parameters: the vertex identifier and the vertex attributes,
            and should return True or False.
        data : bool, optional
            If True, yield the vertex attributes in addition to the vertex identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex that matches the condition.
            If `data` is True, the next vertex and its attributes.

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

    def edges_where(self, conditions=None, data=False, **kwargs):
        """Get edges for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the edge attributes in addition to the edge identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a (u, v, data) tuple.

        """
        conditions = conditions or {}
        conditions.update(kwargs)

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
            The condition you want to evaluate.
            The callable takes 3 parameters:
            the identifier of the first vertex, the identifier of the second vertex, and the edge attributes,
            and should return True or False.
        data : bool, optional
            If True, yield the vertex attributes in addition ot the vertex identifiers.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a (u, v, data) tuple.

        """
        for key, attr in self.edges(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    def faces_where(self, conditions=None, data=False, **kwargs):
        """Get faces for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the face attributes in addition to face identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face that matches the condition.
            If `data` is True, the next face and its attributes.

        """
        conditions = conditions or {}
        conditions.update(kwargs)

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
            The condition you want to evaluate.
            The callable takes 2 parameters: the face identifier and the face attributes,
            and should return True or False.
        data : bool, optional
            If True, yield the face attributes in addition to the face identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face that matches the condition.
            If `data` is True, the next face and its attributes.

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
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary compiled of remaining named arguments.

        Returns
        -------
        None

        Notes
        -----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary.

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
        value : object, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute,
            or None when the function is used as a "setter".

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

        Returns
        -------
        None

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
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty,
            the function returns a dictionary of all attribute name-value pairs of the vertex.
            If the parameter `names` is not empty,
            the function returns a list of the values corresponding to the requested attribute names.
            The function returns None if it is used as a "setter".

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
        value : object, optional
            The value of the attribute.
            Default is None.
        keys : list[int], optional
            A list of vertex identifiers.

        Returns
        -------
        list[Any] | None
            The value of the attribute for each vertex,
            or None if the function is used as a "setter".

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
        names : list[str], optional
            The names of the attribute.
        values : list[Any], optional
            The values of the attributes.
        keys : list[int], optional
            A list of vertex identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            the function returns a list containing an attribute dict per vertex.
            If the parameter `names` is not empty,
            the function returns a list containing a list of attribute values per vertex corresponding to the provided attribute names.
            The function returns None if it is used as a "setter".

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
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary compiled of remaining named arguments.

        Returns
        -------
        None

        Notes
        ----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary.

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
        value : object, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute, or None when the function is used as a "setter".

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

        Returns
        -------
        None

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
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty,
            a dictionary of all attribute name-value pairs of the face.
            If the parameter `names` is not empty,
            a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

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
        value : object, optional
            The value of the attribute.
            Default is None.
        keys : list[int], optional
            A list of face identifiers.

        Returns
        -------
        list[Any] | None
            A list containing the value per face of the requested attribute,
            or None if the function is used as a "setter".

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
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        keys : list[int], optional
            A list of face identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            a list containing per face an attribute dict with all attributes (default + custom) of the face.
            If the parameter `names` is not empty,
            a list containing per face a list of attribute values corresponding to the requested names.
            None if the function is used as a "setter".

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
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary compiled of remaining named arguments.

        Returns
        -------
        None

        Notes
        ----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_edge_attributes.update(attr_dict)

    def edge_attribute(self, edge, name, value=None):
        """Get or set an attribute of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge as a pair of vertex identifiers.
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.

        Returns
        -------
        object | None
            The value of the attribute, or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.

        """
        u, v = edge
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
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
        edge : tuple[int, int]
            The edge identifier.
        name : str
            The name of the attribute.

        Returns
        -------
        None

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
        key = str(tuple(sorted(edge)))
        if key in self.edgedata and name in self.edgedata[key]:
            del self.edgedata[key][name]

    def edge_attributes(self, edge, names=None, values=None):
        """Get or set multiple attributes of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty,
            a dictionary of all attribute name-value pairs of the edge.
            If the parameter `names` is not empty,
            a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

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
            key = str(tuple(sorted(edge)))
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
        value : object, optional
            The value of the attribute.
            Default is None.
        keys : list[tuple[int, int]], optional
            A list of edge identifiers.

        Returns
        -------
        list[Any] | None
            A list containing the value per edge of the requested attribute,
            or None if the function is used as a "setter".

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
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        keys : list[tuple[int, int]], optional
            A list of edge identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            a list containing per edge an attribute dict with all attributes (default + custom) of the edge.
            If the parameter `names` is not empty,
            a list containing per edge a list of attribute values corresponding to the requested names.
            None if the function is used as a "setter".

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
            The formatted summary text.

        """
        tpl = "\n".join(
            [
                "{} summary",
                "=" * (len(self.name) + len(" summary")),
                "- vertices: {}",
                "- edges: {}",
                "- faces: {}",
            ]
        )
        return tpl.format(
            self.name,
            self.number_of_vertices(),
            self.number_of_edges(),
            self.number_of_faces(),
        )

    def number_of_vertices(self):
        """Count the number of vertices in the mesh.

        Returns
        -------
        int

        """
        return len(list(self.vertices()))

    def number_of_edges(self):
        """Count the number of edges in the mesh.

        Returns
        -------
        int

        """
        return len(list(self.edges()))

    def number_of_faces(self):
        """Count the number of faces in the mesh.

        Returns
        -------
        int

        """
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

        A manifold mesh is orientable if any two adjacent faces have compatible orientation,
        i.e. the faces have a unified cycle direction.

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
        """Verify that the mesh is empty.

        Returns
        -------
        bool
            True if the mesh has no vertices.
            False otherwise.

        """
        if self.number_of_vertices() == 0:
            return True
        return False

    def is_closed(self):
        """Verify that the mesh is closed.

        Returns
        -------
        bool
            True if the mesh is not empty and has no naked edges.
            False otherwise.

        """
        if self.is_empty():
            return False
        for edge in self.edges():
            if self.is_edge_on_boundary(*edge):
                return False
        return True

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
            If True, return the neighbors in the cycling order of the faces.

        Returns
        -------
        list[int]
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
            The number of neighborhood rings to include.

        Returns
        -------
        list[int]
            The vertices in the neighborhood.

        Notes
        -----
        The vertices in the neighborhood are unordered.

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
            If True, return the faces in cycling order.
        include_none : bool, optional
            If True, include *outside* faces in the list.

        Returns
        -------
        list[int]
            The faces connected to a vertex.

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
        key : tuple[int, int]
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
        key : tuple[int, int]
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
        tuple[int, int]
            The identifiers of the adjacent faces.
            If the edge is on the boundary, one of the identifiers is None.

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
        int | None
            The identifier of the face corresponding to the halfedge.
            None, if the halfedge is on the outside of a boundary.

        Raises
        ------
        KeyError
            If the halfedge does not exist.

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
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same loop as the given edge.

        """
        u, v = edge
        uv_loop = self.halfedge_loop((u, v))
        if uv_loop[0][0] == uv_loop[-1][1]:
            return uv_loop
        vu_loop = self.halfedge_loop((v, u))
        vu_loop[:] = [(u, v) for v, u in vu_loop[::-1]]
        return vu_loop + uv_loop[1:]

    def halfedge_loop(self, edge):
        """Find all edges on the same loop as the halfedge, in the direction of the halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same loop as the given edge.

        """
        u, v = edge
        if self.is_edge_on_boundary(u, v):
            return self._halfedge_loop_on_boundary(edge)
        edges = [(u, v)]
        while True:
            nbrs = self.vertex_neighbors(v, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(u)
            u = v
            v = nbrs[i - 2]
            edges.append((u, v))
            if v == edges[0][0]:
                break
        return edges

    def _halfedge_loop_on_boundary(self, edge):
        """Find all edges on the same loop as the halfedge, in the direction of the halfedge, if the halfedge is on the boundary.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same loop as the given edge.

        """
        u, v = edge
        edges = [(u, v)]
        while True:
            nbrs = self.vertex_neighbors(v)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == u:
                    continue
                if self.is_edge_on_boundary(v, temp):
                    nbr = temp
                    break
            if nbr is None:
                break
            u, v = v, nbr
            edges.append((u, v))
            if v == edges[0][0]:
                break
        return edges

    def edge_strip(self, edge, return_faces=False):
        """Find all edges on the same strip as a given edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.
        return_faces : bool, optional
            Return the faces on the strip in addition to the edges.

        Returns
        -------
        list[tuple[int, int]] | tuple[list[tuple[int, int]], list[int]]
            If `return_faces` is False, the edges on the same strip as the given edge.
            If `return_faces` is False, the edges on the same strip and the corresponding faces.

        """
        u, v = edge
        if self.halfedge[v][u] is None:
            strip = self.halfedge_strip((u, v))
        elif self.halfedge[u][v] is None:
            edges = self.halfedge_strip((v, u))
            strip = [(u, v) for v, u in edges[::-1]]
        else:
            vu_strip = self.halfedge_strip((v, u))
            vu_strip[:] = [(u, v) for v, u in vu_strip[::-1]]
            if vu_strip[0] == vu_strip[-1]:
                strip = vu_strip
            else:
                uv_strip = self.halfedge_strip((u, v))
                strip = vu_strip[:-1] + uv_strip
        if not return_faces:
            return strip
        faces = [self.halfedge_face(u, v) for u, v in strip[:-1]]
        return strip, faces

    def halfedge_strip(self, edge):
        """Find all edges on the same strip as a given halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same strip as the given halfedge.

        """
        u, v = edge
        edges = [(u, v)]
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
            if (u, v) == edge:
                break
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
        list[int]
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
        list[tuple[int, int]]
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
        list[int]
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
        list[int]
            The identifiers of the neighboring faces.

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

        Returns
        -------
        list[int]
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
            The index of the vertex ancestor.
            Default is 1, meaning the previous vertex.

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
            The index of the vertex descendant.
            Default is 1, meaning the next vertex.

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
        f1 : int
            The identifier of the first face.
        f2 : int
            The identifier of the second face.

        Returns
        -------
        tuple[int, int] | None
            The half-edge separating face 1 from face 2,
            or None, if the faces are not adjacent.

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
        list[int] | None
            The vertices separating face 1 from face 2,
            or None, if the faces are not adjacent.

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
        """Find the halfedge after the given halfedge in the same face.

        Parameters
        ----------
        u : int
            The first vertex of the halfedge.
        v : int
            The second vertex of the halfedge.

        Returns
        -------
        tuple[int, int]
            The next halfedge.

        """
        face = self.halfedge_face(u, v)
        if face is not None:
            w = self.face_vertex_after(face, v)
            return v, w
        nbrs = self.vertex_neighbors(v, ordered=True)
        w = nbrs[0]
        return v, w

    def halfedge_before(self, u, v):
        """Find the halfedge before the given halfedge in the same face.

        Parameters
        ----------
        u : int
            The first vertex of the halfedge.
        v : int
            The second vertex of the halfedge.

        Returns
        -------
        tuple[int, int]
            The previous halfedge.

        """
        face = self.halfedge_face(u, v)
        if face is not None:
            t = self.face_vertex_before(face, u)
            return t, u
        nbrs = self.vertex_neighbors(u, ordered=True)
        t = nbrs[-1]
        return t, u

    def vertex_edges(self, vertex):
        """Find all edges connected to a given vertex.

        Parameters
        ----------
        vertex : int

        Returns
        -------
        list[tuple[int, int]]

        """
        edges = []
        for nbr in self.vertex_neighbors(vertex):
            if self.has_edge((vertex, nbr)):
                edges.append((vertex, nbr))
            else:
                edges.append((nbr, vertex))
        return edges
