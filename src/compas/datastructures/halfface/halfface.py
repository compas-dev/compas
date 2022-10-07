from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from random import choice, sample

from compas.datastructures.datastructure import Datastructure
from compas.datastructures.attributes import VertexAttributeView
from compas.datastructures.attributes import EdgeAttributeView
from compas.datastructures.attributes import FaceAttributeView
from compas.datastructures.attributes import CellAttributeView

from compas.utilities import pairwise


class HalfFace(Datastructure):
    """Base half-face data structure for representing volumetric meshes.

    Parameters
    ----------
    name: str, optional
        The name of the graph.
    default_vertex_attributes: dict[str, Any], optional
        Default values for vertex attributes.
    default_edge_attributes: dict[str, Any], optional
        Default values for edge attributes.
    default_face_attributes: dict[str, Any], optional
        Default values for face attributes.
    default_cell_attributes: dict[str, Any], optional
        Default values for cell attributes.

    Attributes
    ----------
    attributes : dict[str, Any]
        General attributes of the data structure which will be included in the data representation.
    default_vertex_attributes : dict[str, Any]
        Default attributes of the vertices.
    default_edge_attributes: dict[str, Any]
        Default values for edge attributes.
    default_face_attributes: dict[str, Any]
        Default values for face attributes.
    default_cell_attributes: dict[str, Any]
        Default values for cell attributes.

    """

    def __init__(
        self,
        name=None,
        default_vertex_attributes=None,
        default_edge_attributes=None,
        default_face_attributes=None,
        default_cell_attributes=None,
    ):
        super(HalfFace, self).__init__()
        self._max_vertex = -1
        self._max_face = -1
        self._max_cell = -1
        self._vertex = {}
        self._halfface = {}
        self._cell = {}
        self._plane = {}
        self._edge_data = {}
        self._face_data = {}
        self._cell_data = {}
        self.attributes = {"name": name or "HalfFace"}
        self.default_vertex_attributes = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.default_edge_attributes = {}
        self.default_face_attributes = {}
        self.default_cell_attributes = {}
        if default_vertex_attributes:
            self.default_vertex_attributes.update(default_vertex_attributes)
        if default_edge_attributes:
            self.default_edge_attributes.update(default_edge_attributes)
        if default_face_attributes:
            self.default_face_attributes.update(default_face_attributes)
        if default_cell_attributes:
            self.default_cell_attributes.update(default_cell_attributes)

    def __str__(self):
        tpl = "<HalfFace with {} vertices, {} faces, {} cells, {} edges>"
        return tpl.format(
            self.number_of_vertices(),
            self.number_of_faces(),
            self.number_of_cells(),
            self.number_of_edges(),
        )

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
    def DATASCHEMA(self):
        import schema

        return schema.Schema(
            {
                "attributes": dict,
                "dva": dict,
                "dea": dict,
                "dfa": dict,
                "dca": dict,
                "vertex": dict,
                "cell": dict,
                "edge_data": dict,
                "face_data": dict,
                "cell_data": dict,
                "max_vertex": schema.And(int, lambda x: x >= -1),
                "max_face": schema.And(int, lambda x: x >= -1),
                "max_cell": schema.And(int, lambda x: x >= -1),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        return "halfface"

    @property
    def data(self):
        cell = {}
        for c in self._cell:
            cell[c] = {}
            for u in self._cell[c]:
                cell[c].setdefault(u, {})
                for v in self._cell[c][u]:
                    cell[c][u][v] = self._halfface[self._cell[c][u][v]]
        data = {
            "attributes": self.attributes,
            "dva": self.default_vertex_attributes,
            "dea": self.default_edge_attributes,
            "dfa": self.default_face_attributes,
            "dca": self.default_cell_attributes,
            "vertex": self._vertex,
            "cell": cell,
            "edge_data": self._edge_data,
            "face_data": self._face_data,
            "cell_data": self._cell_data,
            "max_vertex": self._max_vertex,
            "max_face": self._max_face,
            "max_cell": self._max_cell,
        }
        return data

    @data.setter
    def data(self, data):
        attributes = data.get("attributes") or {}
        dva = data.get("dva") or {}
        dea = data.get("dea") or {}
        dfa = data.get("dfa") or {}
        dca = data.get("dca") or {}
        vertex = data.get("vertex") or {}
        cell = data.get("cell") or {}
        edge_data = data.get("edge_data") or {}
        face_data = data.get("face_data") or {}
        cell_data = data.get("cell_data") or {}
        max_vertex = data.get("max_vertex", -1)
        max_face = data.get("max_face", -1)
        max_cell = data.get("max_cell", -1)

        if not vertex or not cell:
            return

        self.attributes.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_edge_attributes.update(dea)
        self.default_face_attributes.update(dfa)
        self.default_cell_attributes.update(dca)

        self._vertex = {}
        self._halfface = {}
        self._cell = {}
        self._plane = {}
        self._edge_data = {}
        self._face_data = {}
        self._cell_data = {}

        for v in vertex:
            attr = vertex[v] or {}
            self.add_vertex(int(v), attr_dict=attr)

        for c in cell:
            attr = cell_data.get(c) or {}
            faces = []
            for u in cell[c]:
                for v in cell[c][u]:
                    faces.append(cell[c][u][v])
            self.add_cell(faces, ckey=int(c), attr_dict=attr)

        for e in edge_data:
            self._edge_data[e] = edge_data[e] or {}

        for f in face_data:
            self._face_data[f] = face_data[f] or {}

        self._max_vertex = max_vertex
        self._max_face = max_face
        self._max_cell = max_cell

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def clear(self):
        """Clear all the volmesh data.

        Returns
        -------
        None

        """
        del self._vertex
        del self._halfface
        del self._cell
        del self._plane
        del self._edge_data
        del self._face_data
        del self._cell_data
        self._vertex = {}
        self._halfface = {}
        self._cell = {}
        self._plane = {}
        self._edge_data = {}
        self._face_data = {}
        self._cell_data = {}
        self._max_vertex = -1
        self._max_face = -1
        self._max_cell = -1

    def get_any_vertex(self):
        """Get the identifier of a random vertex.

        .. deprecated:: 1.13.3
            Use :meth:`vertex_sample` instead.

        Returns
        -------
        int
            The identifier of the vertex.

        """
        return choice(list(self.vertices()))

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
        """Get the identifiers of a set of random vertices.

        Parameters
        ----------
        size : int, optional
            The size of the sample.

        Returns
        -------
        list[int]
            The identifiers of the vertices.

        """
        return sample(list(self.vertices()), size)

    def edge_sample(self, size=1):
        """Get the identifiers of a set of random edges.

        Parameters
        ----------
        size : int, optional
            The size of the sample.

        Returns
        -------
        list[tuple[int, int]]
            The identifiers of the edges.

        """
        return sample(list(self.edges()), size)

    def face_sample(self, size=1):
        """Get the identifiers of a set of random faces.

        Parameters
        ----------
        size : int, optional
            The size of the sample.

        Returns
        -------
        list[int]
            The identifiers of the faces.

        """
        return sample(list(self.faces()), size)

    def cell_sample(self, size=1):
        """Get the identifiers of a set of random cells.

        Parameters
        ----------
        size : int, optional
            The size of the sample.

        Returns
        -------
        list[int]
            The identifiers of the cells.

        """
        return sample(list(self.cells()), size)

    def vertex_index(self):
        """Returns a dictionary that maps vertex dictionary keys to the
        corresponding index in a vertex list or array.

        Returns
        -------
        dict[int, int]
            A dictionary of vertex-index pairs.

        """
        return {key: index for index, key in enumerate(self.vertices())}

    def index_vertex(self):
        """Returns a dictionary that maps the indices of a vertex list to
        keys in the vertex dictionary.

        Returns
        -------
        dict[int, int]
            A dictionary of index-vertex pairs.

        """
        return dict(enumerate(self.vertices()))

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex to the volmesh object.

        Parameters
        ----------
        key : int, optional
            The vertex identifier.
        attr_dict : dict[str, Any], optional
            dictionary of vertex attributes.
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

        """
        if key is None:
            key = self._max_vertex = self._max_vertex + 1
        if key > self._max_vertex:
            self._max_vertex = key
        key = int(key)
        if key not in self._vertex:
            self._vertex[key] = {}
            self._plane[key] = {}
        attr = attr_dict or {}
        attr.update(kwattr)
        self._vertex[key].update(attr)
        return key

    def add_halfface(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face to the volmesh object.

        Parameters
        ----------
        vertices : list[int]
            A list of ordered vertex keys representing the face.
            For every vertex that does not yet exist, a new vertex is created.
        fkey : int, optional
            The face identifier.
        attr_dict : dict[str, Any], optional
            dictionary of halfface attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The key of the face.

        Notes
        -----
        If no key is provided for the face, one is generated
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
            fkey = self._max_face = self._max_face + 1
        if fkey > self._max_face:
            self._max_face = fkey
        fkey = int(fkey)
        attr = attr_dict or {}
        attr.update(kwattr)
        self._halfface[fkey] = vertices
        for name, value in attr.items():
            self.face_attribute(fkey, name, value)
        for i in range(-2, len(vertices) - 2):
            u = vertices[i]
            v = vertices[i + 1]
            w = vertices[i + 2]
            if u == v or v == w:
                continue
            self.add_vertex(key=u)
            self.add_vertex(key=v)
            self.add_vertex(key=w)
            if v not in self._plane[u]:
                self._plane[u][v] = {}
            self._plane[u][v][w] = None
            if v not in self._plane[w]:
                self._plane[w][v] = {}
            if u not in self._plane[w][v]:
                self._plane[w][v][u] = None
        return fkey

    def add_cell(self, faces, ckey=None, attr_dict=None, **kwattr):
        """Add a cell to the volmesh object.

        Parameters
        ----------
        faces : list[list[int]]
            The faces of the cell defined as lists of vertices.
        ckey : int, optional
            The cell identifier.
        attr_dict : dict[str, Any], optional
            A dictionary of cell attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The key of the cell.

        Raises
        ------
        TypeError
            If the provided cell key is of an unhashable type.

        Notes
        -----
        If no key is provided for the cell, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        """
        if ckey is None:
            ckey = self._max_cell = self._max_cell + 1
        if ckey > self._max_cell:
            self._max_cell = ckey
        ckey = int(ckey)
        attr = attr_dict or {}
        attr.update(kwattr)
        self._cell[ckey] = {}
        for name, value in attr.items():
            self.cell_attribute(ckey, name, value)
        for vertices in faces:
            fkey = self.add_halfface(vertices)
            vertices = self.halfface_vertices(fkey)
            for i in range(-2, len(vertices) - 2):
                u = vertices[i]
                v = vertices[i + 1]
                w = vertices[i + 2]
                if u not in self._cell[ckey]:
                    self._cell[ckey][u] = {}
                self._plane[u][v][w] = ckey
                self._cell[ckey][u][v] = fkey
        return ckey

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    def delete_vertex(self, vertex):
        """Delete a vertex from the volmesh and everything that is attached to it.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        None

        """
        for cell in self.vertex_cells(vertex):
            self.delete_cell(cell)

    def delete_cell(self, cell):
        """Delete a cell from the volmesh.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        None

        """
        cell_vertices = self.cell_vertices(cell)
        cell_faces = self.cell_faces(cell)
        for face in cell_faces:
            for edge in self.halfface_halfedges(face):
                u, v = edge
                if (u, v) in self._edge_data:
                    del self._edge_data[u, v]
                if (v, u) in self._edge_data:
                    del self._edge_data[v, u]
        for vertex in cell_vertices:
            if len(self.vertex_cells(vertex)) == 1:
                del self._vertex[vertex]
        for face in cell_faces:
            vertices = self.halfface_vertices(face)
            for i in range(-2, len(vertices) - 2):
                u = vertices[i]
                v = vertices[i + 1]
                w = vertices[i + 2]
                self._plane[u][v][w] = None
                if self._plane[w][v][u] is None:
                    del self._plane[u][v][w]
                    del self._plane[w][v][u]
            del self._halfface[face]
            key = "-".join(map(str, sorted(vertices)))
            if key in self._face_data:
                del self._face_data[key]
        del self._cell[cell]
        if cell in self._cell_data:
            del self._cell_data[cell]

    def remove_unused_vertices(self):
        """Remove all unused vertices from the volmesh object.

        Returns
        -------
        None

        """
        for vertex in list(self.vertices()):
            if vertex not in self._plane:
                del self._vertex[vertex]
            else:
                if not self._plane[vertex]:
                    del self._vertex[vertex]
                    del self._plane[vertex]

    cull_vertices = remove_unused_vertices

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        """Iterate over the vertices of the volmesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the vertex attributes in addition to the vertex identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex identifier.
            If `data` is True, the next vertex as a (vertex, attr) a tuple.

        """
        for vertex in self._vertex:
            if not data:
                yield vertex
            else:
                yield vertex, self.vertex_attributes(vertex)

    def edges(self, data=False):
        """Iterate over the edges of the volmesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the edge attributes as well as the edge identifiers.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a ((u, v), attr) tuple.

        """
        seen = set()
        for face in self._halfface:
            vertices = self._halfface[face]
            for u, v in pairwise(vertices + vertices[:1]):
                if (u, v) in seen or (v, u) in seen:
                    continue
                seen.add((u, v))
                seen.add((v, u))
                if not data:
                    yield u, v
                else:
                    yield (u, v), self.edge_attributes((u, v))

    def halffaces(self, data=False):
        """Iterate over the halffaces of the volmesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the half-face attributes in addition to half-face identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next halfface identifier.
            If `data` is True, the next halfface as a (halfface, attr) tuple.
        """
        for hface in self._halfface:
            if not data:
                yield hface
            else:
                yield hface, self.face_attributes(hface)

    def faces(self, data=False):
        """ "Iterate over the halffaces of the volmesh and yield faces.

        Parameters
        ----------
        data : bool, optional
            If True, yield the face attributes in addition to the face identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face identifier.
            If `data` is True, the next face as a (face, attr) tuple.

        Notes
        -----
        Volmesh faces have no topological meaning (analogous to an edge of a mesh).
        They are typically used for geometric operations (i.e. planarisation).
        Between the interface of two cells, there are two interior faces (one from each cell).
        Only one of these two interior faces are returned as a "face".
        The unique faces are found by comparing string versions of sorted vertex lists.

        """
        seen = set()
        faces = []
        for face in self._halfface:
            key = "-".join(map(str, sorted(self.halfface_vertices(face))))
            if key not in seen:
                seen.add(key)
                faces.append(face)
        for face in faces:
            if not data:
                yield face
            else:
                yield face, self.face_attributes(face)

    def cells(self, data=False):
        """Iterate over the cells of the volmesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the cell attributes in addition to the cell identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next cell identifier.
            If `data` is True, the next cell as a (cell, attr) tuple.

        """
        for cell in self._cell:
            if not data:
                yield cell
            else:
                yield cell, self.cell_attributes(cell)

    def vertices_where(self, conditions=None, data=False, **kwargs):
        """Get vertices for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the vertex attributes in addition to the identifiers.
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
            The callable takes 2 parameters: the vertex identifier and the vertex attributes, and should return True or False.
        data : bool, optional
            If True, yield the vertex attributes in addition to the identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex that matches the condition.
            If `data` is True, the next vertex and its attributes.

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
            If True, yield the edge attributes in addition to the identifiers.
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
            The callable takes 2 parameters: the edge identifier and the edge attributes, and should return True or False.
        data : bool, optional
            If True, yield the edge attributes in addition to the identifiers.

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
            If True, yield the face attributes in addition to the identifiers.
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
            The callable takes 2 parameters: the face identifier and the the face attributes, and should return True or False.
        data : bool, optional
            If True, yield the face attributes in addition to the identifiers.

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

    def cells_where(self, conditions=None, data=False, **kwargs):
        """Get cells for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the cell attributes in addition to the identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next cell that matches the condition.
            If `data` is True, the next cell and its attributes.

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for ckey in self.cells():
            is_match = True

            attr = self.cell_attributes(ckey)

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if method and callable(method):
                    val = method(ckey)
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
                    yield ckey, attr
                else:
                    yield ckey

    def cells_where_predicate(self, predicate, data=False):
        """Get cells for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate.
            The callable takes 2 parameters: the cell identifier and the cell attributes, and should return True or False.
        data : bool, optional
            If True, yield the cell attributes in addition to the identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next cell that matches the condition.
            If `data` is True, the next cell and its attributes.

        """
        for ckey, attr in self.cells(True):
            if predicate(ckey, attr):
                if data:
                    yield ckey, attr
                else:
                    yield ckey

    # --------------------------------------------------------------------------
    # attributes - vertices
    # --------------------------------------------------------------------------

    def update_default_vertex_attributes(self, attr_dict=None, **kwattr):
        """Update the default vertex attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        Notes
        -----
        Named arguments overwrite correpsonding name-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_vertex_attributes.update(attr_dict)

    def vertex_attribute(self, vertex, name, value=None):
        """Get or set an attribute of a vertex.

        Parameters
        ----------
        vertex : int
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
        if vertex not in self._vertex:
            raise KeyError(vertex)
        if value is not None:
            self._vertex[vertex][name] = value
            return None
        if name in self._vertex[vertex]:
            return self._vertex[vertex][name]
        else:
            if name in self.default_vertex_attributes:
                return self.default_vertex_attributes[name]

    def unset_vertex_attribute(self, vertex, name):
        """Unset the attribute of a vertex.

        Parameters
        ----------
        vertex : int
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
        if name in self._vertex[vertex]:
            del self._vertex[vertex][name]

    def vertex_attributes(self, vertex, names=None, values=None):
        """Get or set multiple attributes of a vertex.

        Parameters
        ----------
        vertex : int
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
        if vertex not in self._vertex:
            raise KeyError(vertex)
        if values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                self._vertex[vertex][name] = value
            return
        # use it as a getter
        if not names:
            # return all vertex attributes as a dict
            return VertexAttributeView(self.default_vertex_attributes, self._vertex[vertex])
        values = []
        for name in names:
            if name in self._vertex[vertex]:
                values.append(self._vertex[vertex][name])
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
        vertices = keys or self.vertices()
        if value is not None:
            for vertex in vertices:
                self.vertex_attribute(vertex, name, value)
            return
        return [self.vertex_attribute(vertex, name) for vertex in vertices]

    def vertices_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple vertices.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        key : list[Any], optional
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
        vertices = keys or self.vertices()
        if values:
            for vertex in vertices:
                self.vertex_attributes(vertex, names, values)
            return
        return [self.vertex_attributes(vertex, names) for vertex in vertices]

    # --------------------------------------------------------------------------
    # attributes - edges
    # --------------------------------------------------------------------------

    def update_default_edge_attributes(self, attr_dict=None, **kwattr):
        """Update the default edge attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        Notes
        -----
        Named arguments overwrite correpsonding key-value pairs in the attribute dictionary.

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
            The edge identifier.
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
            If the edge does not exist.

        """
        u, v = edge
        if u not in self._plane or v not in self._plane[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
        if value is not None:
            if key not in self._edge_data:
                self._edge_data[key] = {}
            self._edge_data[key][name] = value
            return
        if key in self._edge_data and name in self._edge_data[key]:
            return self._edge_data[key][name]
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

        Raises
        ------
        KeyError
            If the edge does not exist.

        Returns
        -------
        None

        Notes
        -----
        Unsetting the value of an edge attribute implicitly sets it back to the value
        stored in the default edge attribute dict.

        """
        u, v = edge
        if u not in self._plane or v not in self._plane[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
        if key in self._edge_data and name in self._edge_data[key]:
            del self._edge_data[key][name]

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
            If the parameter `names` is empty, a dictionary of all attribute name-value pairs of the edge.
            If the parameter `names` is not empty, a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.

        """
        u, v = edge
        if u not in self._plane or v not in self._plane[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
        if values:
            for name, value in zip(names, values):
                if key not in self._edge_data:
                    self._edge_data[key] = {}
                self._edge_data[key][name] = value
            return
        if not names:
            key = str(tuple(sorted(edge)))
            return EdgeAttributeView(self.default_edge_attributes, self._edge_data.setdefault(key, {}))
        values = []
        for name in names:
            value = self.edge_attribute(edge, name)
            values.append(value)
        return values

    def edges_attribute(self, name, value=None, edges=None):
        """Get or set an attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.
        edges : list[tuple[int, int]], optional
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
        edges = edges or self.edges()
        if value is not None:
            for edge in edges:
                self.edge_attribute(edge, name, value)
            return
        return [self.edge_attribute(edge, name) for edge in edges]

    def edges_attributes(self, names=None, values=None, edges=None):
        """Get or set multiple attributes of multiple edges.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
        values : list[Any], optional
            The values of the attributes.
        edges : list[tuple[int, int]], optional
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
        edges = edges or self.edges()
        if values:
            for edge in edges:
                self.edge_attributes(edge, names, values)
            return
        return [self.edge_attributes(edge, names) for edge in edges]

    # --------------------------------------------------------------------------
    # face attributes
    # --------------------------------------------------------------------------

    def update_default_face_attributes(self, attr_dict=None, **kwattr):
        """Update the default face attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        Notes
        -----
        Named arguments overwrite correpsonding key-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_face_attributes.update(attr_dict)

    def face_attribute(self, face, name, value=None):
        """Get or set an attribute of a face.

        Parameters
        ----------
        face : int
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
        if face not in self._halfface:
            raise KeyError(face)
        key = str(tuple(sorted(self.halfface_vertices(face))))
        if value is not None:
            if key not in self._face_data:
                self._face_data[key] = {}
            self._face_data[key][name] = value
            return
        if key in self._face_data and name in self._face_data[key]:
            return self._face_data[key][name]
        if name in self.default_face_attributes:
            return self.default_face_attributes[name]

    def unset_face_attribute(self, face, name):
        """Unset the attribute of a face.

        Parameters
        ----------
        face : int
            The face identifier.
        name : str
            The name of the attribute.

        Raises
        ------
        KeyError
            If the face does not exist.

        Returns
        -------
        None

        Notes
        -----
        Unsetting the value of a face attribute implicitly sets it back to the value
        stored in the default face attribute dict.

        """
        if face not in self._halfface:
            raise KeyError(face)
        key = str(tuple(sorted(self.halfface_vertices(face))))
        if key in self._face_data and name in self._face_data[key]:
            del self._face_data[key][name]

    def face_attributes(self, face, names=None, values=None):
        """Get or set multiple attributes of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty, a dictionary of all attribute name-value pairs of the face.
            If the parameter `names` is not empty, a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the face does not exist.

        """
        if face not in self._halfface:
            raise KeyError(face)
        key = str(tuple(sorted(self.halfface_vertices(face))))
        if values:
            for name, value in zip(names, values):
                if key not in self._face_data:
                    self._face_data[key] = {}
                self._face_data[key][name] = value
            return
        if not names:
            return FaceAttributeView(self.default_face_attributes, self._face_data.setdefault(key, {}))
        values = []
        for name in names:
            value = self.face_attribute(face, name)
            values.append(value)
        return values

    def faces_attribute(self, name, value=None, faces=None):
        """Get or set an attribute of multiple faces.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.
        faces : list[int], optional
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
        faces = faces or self.faces()
        if value is not None:
            for face in faces:
                self.face_attribute(face, name, value)
            return
        return [self.face_attribute(face, name) for face in faces]

    def faces_attributes(self, names=None, values=None, faces=None):
        """Get or set multiple attributes of multiple faces.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        faces : list[int], optional
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
        faces = faces or self.faces()
        if values:
            for face in faces:
                self.face_attributes(face, names, values)
            return
        return [self.face_attributes(face, names) for face in faces]

    # --------------------------------------------------------------------------
    # attributes - cell
    # --------------------------------------------------------------------------

    def update_default_cell_attributes(self, attr_dict=None, **kwattr):
        """Update the default cell attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        Notes
        ----
        Named arguments overwrite corresponding cell-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_cell_attributes.update(attr_dict)

    def cell_attribute(self, cell, name, value=None):
        """Get or set an attribute of a cell.

        Parameters
        ----------
        cell : int
            The cell identifier.
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
            If the cell does not exist.

        """
        if cell not in self._cell:
            raise KeyError(cell)
        if value is not None:
            if cell not in self._cell_data:
                self._cell_data[cell] = {}
            self._cell_data[cell][name] = value
            return
        if cell in self._cell_data and name in self._cell_data[cell]:
            return self._cell_data[cell][name]
        if name in self.default_cell_attributes:
            return self.default_cell_attributes[name]

    def unset_cell_attribute(self, cell, name):
        """Unset the attribute of a cell.

        Parameters
        ----------
        cell : int
            The cell identifier.
        name : str
            The name of the attribute.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the cell does not exist.

        Notes
        -----
        Unsetting the value of a cell attribute implicitly sets it back to the value
        stored in the default cell attribute dict.

        """
        if cell not in self._cell:
            raise KeyError(cell)
        if cell in self._cell_data:
            if name in self._cell_data[cell]:
                del self._cell_data[cell][name]

    def cell_attributes(self, cell, names=None, values=None):
        """Get or set multiple attributes of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty, a dictionary of all attribute name-value pairs of the cell.
            If the parameter `names` is not empty, a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the cell does not exist.

        """
        if cell not in self._cell:
            raise KeyError(cell)
        if values is not None:
            for name, value in zip(names, values):
                if cell not in self._cell_data:
                    self._cell_data[cell] = {}
                self._cell_data[cell][name] = value
            return
        if not names:
            return CellAttributeView(self.default_cell_attributes, self._cell_data.setdefault(cell, {}))
        values = []
        for name in names:
            value = self.cell_attribute(cell, name)
            values.append(value)
        return values

    def cells_attribute(self, name, value=None, cells=None):
        """Get or set an attribute of multiple cells.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
        cells : list[int], optional
            A list of cell identifiers.

        Returns
        -------
        list[Any] | None
            A list containing the value per face of the requested attribute,
            or None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the cells does not exist.

        """
        if not cells:
            cells = self.cells()
        if value is not None:
            for cell in cells:
                self.cell_attribute(cell, name, value)
            return
        return [self.cell_attribute(cell, name) for cell in cells]

    def cells_attributes(self, names=None, values=None, cells=None):
        """Get or set multiple attributes of multiple cells.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        cells : list[int], optional
            A list of cell identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            a list containing per cell an attribute dict with all attributes (default + custom) of the cell.
            If the parameter `names` is empty,
            a list containing per cell a list of attribute values corresponding to the requested names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the faces does not exist.

        """
        if not cells:
            cells = self.cells()
        if values is not None:
            for cell in cells:
                self.cell_attributes(cell, names, values)
            return
        return [self.cell_attributes(cell, names) for cell in cells]

    # --------------------------------------------------------------------------
    # volmesh info
    # --------------------------------------------------------------------------

    def number_of_vertices(self):
        """Count the number of vertices in the volmesh.

        Returns
        -------
        int
            The number of vertices.

        """
        return len(list(self.vertices()))

    def number_of_edges(self):
        """Count the number of edges in the volmesh.

        Returns
        -------
        int
            The number of edges.

        """
        return len(list(self.edges()))

    def number_of_faces(self):
        """Count the number of faces in the volmesh.

        Returns
        -------
        int
            The number of faces.

        """
        return len(list(self.faces()))

    def number_of_cells(self):
        """Count the number of faces in the volmesh.

        Returns
        -------
        int
            The number of cells.

        """
        return len(list(self.cells()))

    def is_valid(self):
        NotImplementedError

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    def has_vertex(self, vertex):
        """Verify that a vertex is in the volmesh.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is in the volmesh.
            False otherwise.

        """
        return vertex in self._vertex

    def vertex_neighbors(self, vertex):
        """Return the vertex neighbors of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list[int]
            The list of neighboring vertices.

        """
        return self._plane[vertex].keys()

    def vertex_neighborhood(self, vertex, ring=1):
        """Return the vertices in the neighborhood of a vertex.

        Parameters
        ----------
        vertex : int
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
        nbrs = set(self.vertex_neighbors(vertex))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr in nbrs:
                temp += self.vertex_neighbors(nbr)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([vertex]))

    def vertex_degree(self, vertex):
        """Count the neighbors of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        int
            The degree of the vertex.

        """
        return len(self.vertex_neighbors(vertex))

    def vertex_min_degree(self):
        """Compute the minimum degree of all vertices.

        Returns
        -------
        int
            The lowest degree of all vertices.

        """
        if not self._vertex:
            return 0
        return min(self.vertex_degree(vertex) for vertex in self.vertices())

    def vertex_max_degree(self):
        """Compute the maximum degree of all vertices.

        Returns
        -------
        int
            The highest degree of all vertices.

        """
        if not self._vertex:
            return 0
        return max(self.vertex_degree(vertex) for vertex in self.vertices())

    def vertex_halffaces(self, vertex):
        """Return all halffaces connected to a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list[int]
            The list of halffaces connected to a vertex.

        """
        cells = self.vertex_cells(vertex)
        nbrs = self.vertex_neighbors(vertex)
        halffaces = set()
        for cell in cells:
            for nbr in nbrs:
                if nbr in self._cell[cell][vertex]:
                    halffaces.add(self._cell[cell][vertex][nbr])
                    halffaces.add(self._cell[cell][nbr][vertex])
        return list(halffaces)

    def vertex_cells(self, vertex):
        """Return all cells connected to a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list[int]
            The list of cells connected to a vertex.

        """
        cells = set()
        for nbr in self._plane[vertex]:
            for cell in self._plane[vertex][nbr].values():
                if cell is not None:
                    cells.add(cell)
        return list(cells)

    def is_vertex_on_boundary(self, vertex):
        """Verify that a vertex is on a boundary.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is on the boundary.
            False otherwise.

        """
        halffaces = self.vertex_halffaces(vertex)
        for halfface in halffaces:
            if self.is_halfface_on_boundary(halfface):
                return True
        return False

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    def has_edge(self, edge):
        """Verify that the volmesh contains a directed edge (u, v).

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        bool
            True if the edge exists.
            False otherwise.

        """
        return edge in set(self.edges())

    def edge_halffaces(self, edge):
        """Ordered halffaces around edge (u, v).

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        list[int]
            Ordered list of halfface identifiers.

        """
        u, v = edge
        cells = [cell for cell in self._plane[u][v].values() if cell is not None]
        cell = cells[0]
        halffaces = []
        if self.is_edge_on_boundary(edge):
            for cell in cells:
                halfface = self._cell[cell][v][u]
                if self.is_halfface_on_boundary(halfface):
                    break
        for i in range(len(cells)):
            halfface = self._cell[cell][u][v]
            w = self.halfface_vertex_descendent(halfface, v)
            cell = self._plane[w][v][u]
            halffaces.append(halfface)
        return halffaces

    def edge_cells(self, edge):
        """Ordered cells around edge (u, v).

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        list[int]
            Ordered list of keys identifying the ordered cells.

        """
        halffaces = self.edge_halffaces(edge)
        return [self.halfface_cell(halfface) for halfface in halffaces]

    def is_edge_on_boundary(self, edge):
        """Verify that an edge is on the boundary.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        bool
            True if the edge is on the boundary.
            False otherwise.

        Note
        ----
        This method simply checks if u-v or v-u is on the edge of the volmesh.
        The direction u-v does not matter.

        """
        u, v = edge
        return None in self._plane[u][v].values()

    # --------------------------------------------------------------------------
    # halfface topology
    # --------------------------------------------------------------------------

    def has_halfface(self, halfface):
        """Verify that a face is part of the volmesh.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        bool
            True if the face exists.
            False otherwise.

        """
        return halfface in self._halfface

    def halfface_vertices(self, halfface):
        """The vertices of a halfface.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list[int]
            Ordered vertex identifiers.

        """
        return self._halfface[halfface]

    def halfface_halfedges(self, halfface):
        """The halfedges of a halfface.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list[tuple[int, int]]
            The halfedges of a halfface.

        """
        vertices = self.halfface_vertices(halfface)
        return list(pairwise(vertices + vertices[0:1]))

    def halfface_cell(self, halfface):
        """The cell to which the halfface belongs to.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        int
            Identifier of the cell.

        """
        u, v, w = self._halfface[halfface][0:3]
        return self._plane[u][v][w]

    def halfface_opposite_cell(self, halfface):
        """The cell to which the opposite halfface belongs to.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        int
            Identifier of the cell.

        """
        u, v, w = self._halfface[halfface][0:3]
        return self._plane[w][v][u]

    def halfface_opposite_halfface(self, halfface):
        """The opposite face of a face.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        int
            Identifier of the opposite face.

        Notes
        -----
        A face and its opposite face share the same vertices, but in reverse order.
        For a boundary face, the opposite face is None.

        """
        u, v, w = self._halfface[halfface][0:3]
        nbr = self._plane[w][v][u]
        if nbr is None:
            return None
        return self._cell[nbr][v][u]

    def halfface_adjacent_halfface(self, halfface, halfedge):
        """Return the halfface adjacent to the halfface across the halfedge.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.
        halfedge : tuple[int, int]
            The identifier of the halfedge.

        Returns
        -------
        int | None
            The identifier of the adjacent half-face, or None if `halfedge` is on the boundary.

        Notes
        -----
        The adjacent face belongs a to one of the cell neighbors over faces of the initial cell.
        A face and its adjacent face share two common vertices.

        """
        u, v = halfedge
        cell = self.halfface_cell(halfface)
        nbr_halfface = self._cell[cell][v][u]
        w = self.face_vertex_ancestor(nbr_halfface, v)
        nbr_cell = self._plane[u][v][w]
        if nbr_cell is None:
            return None
        return self._cell[nbr_cell][v][u]

    def halfface_vertex_ancestor(self, halfface, vertex):
        """Return the vertex before the specified vertex in a specific face.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        int
            The identifier of the vertex before the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.

        """
        i = self._halfface[halfface].index(vertex)
        return self._halfface[halfface][i - 1]

    def halfface_vertex_descendent(self, halfface, vertex):
        """Return the vertex after the specified vertex in a specific face.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        int
            The identifier of the vertex after the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.

        """
        if self._halfface[halfface][-1] == vertex:
            return self._halfface[halfface][0]
        i = self._halfface[halfface].index(vertex)
        return self._halfface[halfface][i + 1]

    def halfface_manifold_neighbors(self, halfface):
        nbrs = []
        cell = self.halfface_cell(halfface)
        for u, v in self.halfface_halfedges(halfface):
            nbr_halfface = self._cell[cell][v][u]
            w = self.halfface_vertex_ancestor(nbr_halfface, v)
            nbr_cell = self._plane[u][v][w]
            if nbr_cell is not None:
                nbr = self._cell[nbr_cell][v][u]
                nbrs.append(nbr)
        return nbrs

    def halfface_manifold_neighborhood(self, hfkey, ring=1):
        """Return the halfface neighborhood of a halfface across their edges.

        Parameters
        ----------
        key : int
            The identifier of the halfface.

        Returns
        -------
        list[int]
            The list of neighboring halffaces.

        Notes
        -----
        Neighboring halffaces on the same cell are not included.

        """
        nbrs = set(self.halfface_manifold_neighbors(hfkey))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr_hfkey in nbrs:
                temp += self.halfface_manifold_neighbors(nbr_hfkey)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([hfkey]))

    def is_halfface_on_boundary(self, halfface):
        """Verify that a face is on the boundary.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.

        """
        u, v, w = self._halfface[halfface][0:3]
        return self._plane[w][v][u] is None

    # --------------------------------------------------------------------------
    # cell topology
    # --------------------------------------------------------------------------

    def cell_vertices(self, cell):
        """The vertices of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list[int]
            The vertex identifiers of a cell.

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.HalfEdge.vertices`,
        but in the context of a cell of the `VolMesh`.

        """
        return list(set([vertex for face in self.cell_faces(cell) for vertex in self.halfface_vertices(face)]))

    def cell_halfedges(self, cell):
        """The halfedges of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list[tuple[int, int]]
            The halfedges of a cell.

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.HalfEdge.halfedges`,
        but in the context of a cell of the `VolMesh`.

        """
        halfedges = []
        for face in self.cell_faces(cell):
            halfedges += self.halfface_halfedges(face)
        return halfedges

    def cell_edges(self, cell):
        """Return all edges of a cell.

        Parameters
        ----------
        cell : int
            The cell identifier.

        Returns
        -------
        list[tuple[int, int]]
            The edges of the cell.

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.HalfEdge.edges`,
        but in the context of a cell of the `VolMesh`.

        """
        raise NotImplementedError

    def cell_faces(self, cell):
        """The faces of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list[int]
            The faces of a cell.

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.HalfEdge.faces`,
        but in the context of a cell of the `VolMesh`.

        """
        faces = set()
        for vertex in self._cell[cell]:
            faces.update(self._cell[cell][vertex].values())
        return list(faces)

    def cell_vertex_neighbors(self, cell, vertex):
        """Ordered vertex neighbors of a vertex of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.
        vertex : int
            Identifier of the vertex.

        Returns
        -------
        list[int]
            The list of neighboring vertices.

        Notes
        -----
        All of the returned vertices are part of the cell.

        This method is similar to :meth:`~compas.datastructures.HalfEdge.vertex_neighbors`,
        but in the context of a cell of the `VolMesh`.

        """
        if vertex not in self.cell_vertices(cell):
            raise KeyError(vertex)
        nbr_vertices = self._cell[cell][vertex].keys()
        v = nbr_vertices[0]
        ordered_vkeys = [v]
        for i in range(len(nbr_vertices) - 1):
            face = self._cell[cell][vertex][v]
            v = self.halfface_vertex_ancestor(face, vertex)
            ordered_vkeys.append(v)
        return ordered_vkeys

    def cell_vertex_faces(self, cell, vertex):
        """Ordered faces connected to a vertex of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.
        vertex : int
            Identifier of the vertex.

        Returns
        -------
        list[int]
            The ordered list of faces connected to a vertex of a cell.

        Notes
        -----
        All of the returned faces should are part of the same cell.

        This method is similar to :meth:`~compas.datastructures.HalfEdge.vertex_faces`,
        but in the context of a cell of the `VolMesh`.

        """
        nbr_vertices = self._cell[cell][vertex].keys()
        u = vertex
        v = nbr_vertices[0]
        ordered_faces = []
        for i in range(len(nbr_vertices)):
            face = self._cell[cell][u][v]
            v = self.halfface_vertex_ancestor(face, u)
            ordered_faces.append(face)
        return ordered_faces

    def cell_halfedge_face(self, cell, halfedge):
        """Find the face corresponding to a specific halfedge of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.
        halfedge : tuple[int, int]
            The identifier of the halfedge.

        Returns
        -------
        int
            The identifier of the face.

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.HalfEdge.halfedge_face`,
        but in the context of a cell of the `VolMesh`.

        """
        u, v = halfedge
        return self._cell[cell][u][v]

    def cell_halfedge_opposite_face(self, cell, halfedge):
        """Find the opposite face corresponding to a specific halfedge of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.
        halfedge : tuple[int, int]
            The identifier of the halfedge.

        Returns
        -------
        int
            The identifier of the face.

        """
        u, v = halfedge
        return self._cell[cell][v][u]

    def cell_face_neighbors(self, cell, face):
        """Find the faces adjacent to a given face of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.
        face : int
            The identifier of the face.

        Returns
        -------
        int
            The identifier of the face.

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.HalfEdge.face_neighbors`,
        but in the context of a cell of the `VolMesh`.

        """
        nbrs = []
        for halfedge in self.halfface_halfedges(face):
            nbr = self.cell_halfedge_opposite_face(cell, halfedge)
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def cell_neighbors(self, cell):
        """Find the neighbors of a given cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        list[int]
            The identifiers of the adjacent cells.

        """
        nbrs = []
        for face in self.cell_faces(cell):
            nbr = self.halfface_opposite_cell(face)
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def is_cell_on_boundary(self, cell):
        """Verify that a cell is on the boundary.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.

        """
        faces = self.cell_faces(cell)
        for face in faces:
            if self.is_halfface_on_boundary(face):
                return True
        return False

    # --------------------------------------------------------------------------
    # boundary
    # --------------------------------------------------------------------------

    def vertices_on_boundaries(self):
        """Find the vertices on the boundary.

        Returns
        -------
        list[int]
            The vertices of the boundary.

        """
        vertices = set()
        for face in self._halfface:
            if self.is_halfface_on_boundary(face):
                vertices.update(self.halfface_vertices(face))
        return list(vertices)

    def halffaces_on_boundaries(self):
        """Find the faces on the boundary.

        Returns
        -------
        list[int]
            The faces of the boundary.

        """
        faces = set()
        for face in self._halfface:
            if self.is_halfface_on_boundary(face):
                faces.add(face)
        return list(faces)

    def cells_on_boundaries(self):
        """Find the cells on the boundary.

        Returns
        -------
        list[int]
            The cells of the boundary.

        """
        cells = set()
        for face in self.halffaces_on_boundaries():
            cells.add(self.halfface_cell(face))
        return list(cells)
