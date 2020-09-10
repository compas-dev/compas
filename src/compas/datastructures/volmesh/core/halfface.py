from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ast import literal_eval
from random import choice

from compas.datastructures.volmesh.core import VertexAttributeView
from compas.datastructures.volmesh.core import FaceAttributeView
from compas.datastructures.volmesh.core import CellAttributeView

from compas.datastructures import Datastructure
from compas.utilities import pairwise


__all__ = ['HalfFace']


class HalfFace(Datastructure):
    """Base half-face data structure fore representing volumetric meshes.

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

    """

    def __init__(self):
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
        self.attributes = {'name': 'VolMesh'}
        self.default_vertex_attributes = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self.default_edge_attributes = {}
        self.default_face_attributes = {}
        self.default_cell_attributes = {}

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

    # def __str__(self):
    #     """Generate a readable representation of the data of the volmesh."""
    #     return json.dumps(self.data, sort_keys=True, indent=4)

    # def summary(self):
    #     """Print a summary of the volmesh."""
    #     tpl = "\n".join(
    #         ["VolMesh summary",
    #          "===============",
    #          "- vertices: {}",
    #          "- edges   : {}",
    #          "- faces   : {}",
    #          "- cells   : {}"])
    #     s = tpl.format(self.number_of_vertices(),
    #                    self.number_of_edges(),
    #                    self.number_of_faces(),
    #                    self.number_of_cells())
    #     print(s)

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
        """
        edge_data = {}
        for edge in self._edge_data:
            edge_data[repr(edge)] = self._edge_data[edge]
        data = {
            'attributes': self.attributes,
            'dva': self.default_vertex_attributes,
            'dea': self.default_edge_attributes,
            'dfa': self.default_face_attributes,
            'dca': self.default_cell_attributes,
            'vertices': self._vertex,
            'halffaces': self._halfface,
            'cells': self._cell,
            'planes': self._plane,
            'edge_data': edge_data,
            'face_data': self._face_data,
            'cell_data': self._cell_data,
            'max_vertex': self._max_vertex,
            'max_face': self._max_face,
            'max_cell': self._max_cell}
        return data

    @data.setter
    def data(self, data):
        attributes = data.get('attributes') or {}
        dva = data.get('dva') or {}
        dea = data.get('dea') or {}
        dfa = data.get('dfa') or {}
        dca = data.get('dca') or {}
        vertices = data.get('vertices') or {}
        halffaces = data.get('halffaces') or {}
        cells = data.get('cells') or {}
        planes = data.get('planes') or {}
        edge_data = data.get('edge_data') or {}
        face_data = data.get('face_data') or {}
        cell_data = data.get('cell_data') or {}
        max_vertex = data.get('max_vertex', -1)
        max_face = data.get('max_face', -1)
        max_cell = data.get('max_cell', -1)

        if not vertices or not planes or not halffaces or not cells:
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

        for vertex in vertices:
            attr = vertices[vertex] or {}
            self.add_vertex(int(vertex), attr_dict=attr)

        for face in halffaces:
            attr = face_data.get(face) or {}
            self.add_face(halffaces[face], fkey=int(face), attr_dict=attr)

        for cell in cells:
            attr = cell_data.get(cell) or {}
            faces = []
            for u in cells[cell]:
                for v in cells[cell][u]:
                    face = cells[cell][u][v]
                    faces.append(halffaces[face])
            self.add_cell(faces, ckey=int(cell), attr_dict=attr)

        for edge in edge_data:
            self._edge_data[literal_eval(edge)] = edge_data[edge] or {}

        self._max_vertex = max_vertex
        self._max_face = max_face
        self._max_cell = max_cell

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def clear(self):
        """Clear all the volmesh data."""
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

        Returns
        -------
        int
            The identifier of the vertex.

        """
        return choice(list(self.vertices()))

    def get_any_face(self):
        """Get the identifier of a random face.

        Returns
        -------
        int
            The identifier of the face.
        """
        return choice(list(self.faces()))

    def get_any_face_vertex(self, face):
        """Get the identifier of a random vertex of a specific face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        int
            The identifier of the vertex of the face.
        """
        return choice(self.face_vertices(face))

    def vertex_index(self):
        """Returns a dictionary that maps vertex dictionary keys to the
        corresponding index in a vertex list or array.

        Returns
        -------
        dict
            A dictionary of vertex-index pairs.
        """
        return {vertex: index for index, vertex in enumerate(self.vertices())}

    def index_vertex(self):
        """Returns a dictionary that maps the indices of a vertex list to
        keys in the vertex dictionary.

        Returns
        -------
        dict
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
        >>>
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

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face to the volmesh object.

        Parameters
        ----------
        vertices : list
            A list of ordered vertex keys representing the face.
            For every vertex that does not yet exist, a new vertex is created.
        fkey : int, optional
            The face identifier.
        attr_dict : dict, optional
            Halfface attributes.
        kwattr : dict, optional
            Additional named face attributes.
            Named face attributes overwrite corresponding attributes in the
            attribute dict (``attr_dict``).

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
            fkey = self._max_face = self._max_face + 1
        if fkey > self._max_face:
            self._max_face = fkey
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
        faces : list of list of int
            The faces of the cell defined as lists of vertices.
        ckey : int, optional
            The cell identifier.
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

        Examples
        --------
        >>>
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
            fkey = self.add_face(vertices)
            vertices = self.face_vertices(fkey)
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

        Examples
        --------
        >>>
        """
        for cell in self.vertex_cells(vertex):
            self.delete_cell(cell)

    def delete_cell(self, cell):
        """Delete a cell from the volmesh.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Examples
        --------
        >>>
        """
        cell_vertices = self.cell_vertices(cell)
        cell_faces = self.cell_faces(cell)
        for face in cell_faces:
            for edge in self.face_halfedges(face):
                u, v = edge
                if (u, v) in self._edge_data:
                    del self._edge_data[u, v]
                if (v, u) in self._edge_data:
                    del self._edge_data[v, u]
        for vertex in cell_vertices:
            if len(self.vertex_cells(vertex)) == 1:
                del self._vertex[vertex]
        for face in cell_faces:
            vertices = self.face_vertices(face)
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
            Return the vertex data as well as the vertex identifiers if true.

        Yields
        ------
        int or tuple
            The next vertex identifier, if ``data`` is false.
            The next vertex as a (vertex, attr) a tuple, if ``data`` is true.
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
            Return the edge data as well as the edge identifiers if true.

        Yields
        ------
        tuple
            The next edge as a (u, v) tuple, if ``data`` is false.
            The next edge as a ((u, v), attr) tuple, if ``data`` is true.
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
            Return half-face data as well as identifiers if true.

        Yields
        ------
        int or tuple
            The next face identifier, if ``data`` is ``False``.
            The next face as a (face, attr) tuple, if ``data`` is ``True``.
        """
        for face in self._halfface:
            if not data:
                yield face
            else:
                yield face, self.face_attributes(face)

    def faces(self, data=False):
        """"Iterate over the half-faces of the volmesh and yield faces.

        Parameters
        ----------
        data : bool, optional
            Return the face data as well as the face keys.

        Yields
        ------
        int or tuple
            The next face identifier, if ``data`` is ``False``.
            The next face as a (face, attr) tuple, if ``data`` is ``True``.

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
            key = "-".join(map(str, sorted(self.face_vertices(face))))
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
            Return the cell data as well as the cell keys.

        Yields
        ------
        int or tuple
            The next cell identifier, if ``data`` is ``False``.
            The next cell as a (cell, attr) tuple, if ``data`` is ``True``.
        """
        for cell in self._cell:
            if not data:
                yield cell
            else:
                yield cell, self.cell_attributes(cell)

    def vertices_where(self):
        raise NotImplementedError

    def edges_where(self):
        raise NotImplementedError

    def faces_where(self):
        raise NotImplementedError

    def cells_where(self):
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # attributes - vertices
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
        Named arguments overwrite correpsonding vertex-value pairs in the attribute dictionary,
        if they exist.
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
        if vertex not in self._vertex:
            raise KeyError(vertex)
        if values:
            for name, value in zip(names, values):
                self._vertex[vertex][name] = value
            return
        if not names:
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

    def vertices_attribute(self, name, value=None, vertices=None):
        """Get or set an attribute of multiple vertices.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : obj, optional
            The value of the attribute.
            Default is ``None``.
        vertices : list of int, optional
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
        if not vertices:
            vertices = self.vertices()
        if value is not None:
            for vertex in vertices:
                self.vertex_attribute(vertex, name, value)
            return
        return [self.vertex_attribute(vertex, name) for vertex in vertices]

    def vertices_attributes(self, names=None, values=None, vertices=None):
        """Get or set multiple attributes of multiple vertices.

        Parameters
        ----------
        names : list of str, optional
            The names of the attribute.
            Default is ``None``.
        values : list of obj, optional
            The values of the attributes.
            Default is ``None``.
        vertices : list of int, optional
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
        if not vertices:
            vertices = self.vertices()
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
        attr_dict : dict, optional
            A dictionary of attributes with their default values.
            Defaults to an empty ``dict``.
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
        self.default_edge_attributes.update(attr_dict)

    def edge_attribute(self, edge, name, value=None):
        """Get or set an attribute of an edge.

        Parameters
        ----------
        edge : tuple of int
            The edge identifier.
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
        if u not in self._plane or v not in self._plane[u]:
            raise KeyError(edge)
        if value is not None:
            if (u, v) not in self._edge_data:
                self._edge_data[u, v] = {}
            if (v, u) not in self._edge_data:
                self._edge_data[v, u] = {}
            self._edge_data[u, v][name] = self._edge_data[v, u][name] = value
            return
        if (u, v) in self._edge_data and name in self._edge_data[u, v]:
            return self._edge_data[u, v][name]
        if (v, u) in self._edge_data and name in self._edge_data[v, u]:
            return self._edge_data[v, u][name]
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
        if u not in self._plane or v not in self._plane[u]:
            raise KeyError(edge)
        if edge in self._edge_data:
            if name in self._edge_data[edge]:
                del self._edge_data[edge][name]
        edge = v, u
        if edge in self._edge_data:
            if name in self._edge_data[edge]:
                del self._edge_data[edge][name]

    def edges_attribute(self, name, value=None, edges=None):
        """Get or set an attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : obj, optional
            The value of the attribute.
            Default is ``None``.
        edges : list of 2-tuple of int, optional
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
        if not edges:
            edges = self.edges()
        if value is not None:
            for edge in edges:
                self.edge_attribute(edge, name, value)
            return
        return [self.edge_attribute(edge, name) for edge in edges]

    def edges_attributes(self, names=None, values=None, edges=None):
        """Get or set multiple attributes of multiple edges.

        Parameters
        ----------
        names : list of str, optional
            The names of the attribute.
            Default is ``None``.
        values : list of obj, optional
            The values of the attributes.
            Default is ``None``.
        edges : list of 2-tuple of int, optional
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
        if not edges:
            edges = self.edges()
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
        self.default_face_attributes.update(attr_dict)

    def face_attribute(self, face, name, value=None):
        """Get or set an attribute of a face.

        Parameters
        ----------
        face : int
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
        if face not in self._halfface:
            raise KeyError(face)
        key = "-".join(map(str, sorted(self.face_vertices(face))))
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

        Notes
        -----
        Unsetting the value of a face attribute implicitly sets it back to the value
        stored in the default face attribute dict.
        """
        if face not in self._halfface:
            raise KeyError(face)
        key = "-".join(map(str, sorted(self.face_vertices(face))))
        if key in self._face_data:
            if name in self._face_data[key]:
                del self._face_data[key][name]

    def face_attributes(self, face, names=None, values=None):
        """Get or set multiple attributes of a face.

        Parameters
        ----------
        face : int
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
        if face not in self._halfface:
            raise KeyError(face)
        key = "-".join(map(str, sorted(self.face_vertices(face))))
        if values:
            for name, value in zip(names, values):
                if key not in self._face_data:
                    self._face_data[key] = {}
                self._face_data[key][name] = value
            return
        if not names:
            return FaceAttributeView(self.default_face_attributes, self._face_data, key)
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
        value : obj, optional
            The value of the attribute.
            Default is ``None``.
        faces : list of int, optional
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
        if not faces:
            faces = self.faces()
        if value is not None:
            for face in faces:
                self.face_attribute(face, name, value)
            return
        return [self.face_attribute(face, name) for face in faces]

    def faces_attributes(self, names=None, values=None, faces=None):
        """Get or set multiple attributes of multiple faces.

        Parameters
        ----------
        names : list of str, optional
            The names of the attribute.
            Default is ``None``.
        values : list of obj, optional
            The values of the attributes.
            Default is ``None``.
        faces : list of int, optional
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
        if not faces:
            faces = self.faces()
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
        attr_dict : dict (None)
            A dictionary of attributes with their default values.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Notes
        ----
        Named arguments overwrite corresponding cell-value pairs in the attribute dictionary,
        if they exist.
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
        value : obj, optional
            The value of the attribute.

        Returns
        -------
        object or None
            The value of the attribute, or ``None`` when the function is used as a "setter".

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
        names : list, optional
            A list of attribute names.
        values : list, optional
            A list of attribute values.

        Returns
        -------
        dict, list or None
            If the parameter ``names`` is empty,
            a dictionary of all attribute name-value pairs of the cell.
            If the parameter ``names`` is not empty,
            a list of the values corresponding to the provided names.
            ``None`` if the function is used as a "setter".

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
        value : obj, optional
            The value of the attribute.
            Default is ``None``.
        cells : list of int, optional
            A list of cell identifiers.

        Returns
        -------
        list or None
            A list containing the value per face of the requested attribute,
            or ``None`` if the function is used as a "setter".

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
        names : list of str, optional
            The names of the attribute.
            Default is ``None``.
        values : list of obj, optional
            The values of the attributes.
            Default is ``None``.
        cells : list of int, optional
            A list of cell identifiers.

        Returns
        -------
        dict, list or None
            If the parameter ``names`` is ``None``,
            a list containing per cell an attribute dict with all attributes (default + custom) of the cell.
            If the parameter ``names`` is ``None``,
            a list containing per cell a list of attribute values corresponding to the requested names.
            ``None`` if the function is used as a "setter".

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
        vertex : hashable
            The identifier of the vertex.

        Returns
        -------
        list
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
        """Return all half-faces connected to a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list
            The list of faces connected to a vertex.
        """
        cells = self.vertex_cells(vertex)
        nbrs = self.vertex_neighbors(vertex)
        faces = set()
        for cell in cells:
            for nbr in nbrs:
                if nbr in self._cell[cell][vertex]:
                    faces.add(self._cell[cell][vertex][nbr])
                    faces.add(self._cell[cell][nbr][vertex])
        return list(faces)

    def vertex_faces(self, vertex):
        """Return all faces connected to a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list
            The list of faces connected to a vertex.
        """
        halffaces = self.vertex_halffaces(vertex)
        seen = set()
        faces = []
        for face in halffaces:
            if face not in seen:
                faces.append(face)
                opposite = self.face_opposite_face(face)
                seen.add(face)
                seen.add(opposite)
        return faces

    def vertex_cells(self, vertex):
        """Return all cells connected to a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list
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
        faces = self.vertex_faces(vertex)
        for face in faces:
            if self.is_face_on_boundary(face):
                return True
        return False

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    def has_edge(self, edge):
        """Verify that the volmesh contains a directed edge (u, v).

        Parameters
        ----------
        edge : tuple of int
            The identifier of the edge.

        Returns
        -------
        bool
            True if the edge exists.
            False otherwise.
        """
        return edge in set(self.edges())

    def edge_halffaces(self, edge):
        """Ordered half-faces around edge (u, v).

        Parameters
        ----------
        edge : tuple of int
            The identifier of the edge.

        Returns
        -------
        list
            Ordered list of of keys identifying the faces.

        Notes
        -----
        The faces are ordered around the edge (u, v).
        All faces returned should have halfedge (u, v) or (v, u).
        This also means that if edge u-v is shared by four cells, eight faces are returned.
        """
        u, v = edge
        cells = self.edge_cells(edge)
        faces = []
        for cell in cells:
            faces.append(self._cell[cell][v][u])
            faces.append(self._cell[cell][u][v])
        return faces

    def edge_faces(self, edge):
        """Ordered faces around edge (u, v).

        Parameters
        ----------
        edge : tuple of int
            The identifier of the edge.

        Returns
        -------
        list
            Ordered list of of keys identifying faces.

        Notes
        -----
        The faces are ordered around the edge (u, v).
        All faces returned should have halfedge (u, v).
        This also means that if edge u-v is shared by four cells, four faces are returned.
        """
        u, v = edge
        cells = [cell for cell in self._plane[u][v].values() if cell is not None]
        cell = cells[0]
        faces = []
        if self.is_edge_on_boundary(edge):
            for cell in cells:
                face = self._cell[cell][v][u]
                if self.is_face_on_boundary(face):
                    break
        for i in range(len(cells)):
            face = self._cell[cell][u][v]
            w = self.face_vertex_descendent(face, v)
            cell = self._plane[w][v][u]
            faces.append(face)
        return faces

    def edge_cells(self, edge):
        """Ordered cells around edge (u, v).

        Parameters
        ----------
        edge : tuple of int
            The identifier of the edge.

        Returns
        -------
        list
            Ordered list of keys identifying the ordered cells.
        """
        faces = self.edge_faces(edge)
        return [self.face_cell(face) for face in faces]

    def is_edge_on_boundary(self, edge):
        """Verify that an edge is on the boundary.

        Parameters
        ----------
        edge : tuple of int
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
        # if not self.has_edge(edge):
        #     v, u = edge
        return None in self._plane[u][v].values()

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    def has_face(self, face):
        """Verify that a face is part of the volmesh.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the face exists.
            False otherwise.
        """
        return face in self._halfface

    def face_vertices(self, face):
        """The vertices of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list
            Ordered vertex identifiers.
        """
        return self._halfface[face]

    def face_halfedges(self, face):
        """The halfedges of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list
            The halfedges of a face.
        """
        vertices = self.face_vertices(face)
        return list(pairwise(vertices + vertices[0:1]))

    def face_cell(self, face):
        """The cell to which the face belongs to.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        ckey
            Identifier of the cell.
        """
        u, v, w = self._halfface[face][0:3]
        return self._plane[u][v][w]

    def face_opposite_face(self, face):
        """The opposite face of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        face
            Identifier of the opposite face.

        Notes
        -----
        A face and its opposite face share the same vertices, but in reverse order.
        For a boundary face, the opposite face is None.
        """
        u, v, w = self._halfface[face][0:3]
        nbr = self._plane[w][v][u]
        if nbr is None:
            return None
        return self._cell[nbr][v][u]

    # def face_adjacent_face(self, face, edge):
    #     """Return the face adjacent to a face across the halfedge edge.

    #     Parameters
    #     ----------
    #     face : int
    #         The identifier of the face.
    #     edge : tuple of int
    #         The identifier of the common edge.

    #     Returns
    #     -------
    #     int or None
    #         The identifier of the face.
    #         None, if both faces belong to the same cell.

    #     Notes
    #     -----
    #     The adjacent face belongs a to one of the cell neighbors over faces of the initial cell.
    #     A face and its adjacent face share two common vertices.
    #     """
    #     u, v = edge
    #     if (u, v) not in self.face_halfedges(face):
    #         if (v, u) not in self.face_halfedges(face):
    #             raise KeyError(edge)
    #         u, v = v, u
    #     cell = self.face_cell(face)
    #     adj_face = self._cell[cell][v][u]
    #     w = self.face_vertex_ancestor(adj_face, v)
    #     nbr_cell = self._plane[u][v][w]
    #     if nbr_cell is None:
    #         return None
    #     return self._cell[nbr_cell][v][u]

    def face_vertex_ancestor(self, face, vertex):
        """Return the vertex before the specified vertex in a specific face.

        Parameters
        ----------
        face : int
            The identifier of the face.
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
        i = self._halfface[face].index(vertex)
        return self._halfface[face][i - 1]

    def face_vertex_descendent(self, face, vertex):
        """Return the vertex after the specified vertex in a specific face.

        Parameters
        ----------
        face : int
            Identifier of the face.
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
        if self._halfface[face][-1] == vertex:
            return self._halfface[face][0]
        i = self._halfface[face].index(vertex)
        return self._halfface[face][i + 1]

    # def face_neighbors_over_vertices(self, face):
    #     """Return all faces that share at least one vertex with a face.

    #     Parameters
    #     ----------
    #     face : int
    #         The identifier of the face.

    #     Returns
    #     -------
    #     list
    #         The list of faces.

    #     Notes
    #     -----
    #     Neighboring faces on the same cell are not included.
    #     Neighboring faces belong to one of the neighboring cells over faces of the initial cell.
    #     """
    #     nbrs = set()
    #     for u, v in self.face_halfedges(face):
    #         nbr_face = self.face_adjacent_face(face, (u, v))
    #         if nbr_face is not None:
    #             nbrs.add(nbr_face)
    #             while True:
    #                 w = self.face_vertex_ancestor(nbr_face, v)
    #                 nbr_face = self.face_adjacent_face(nbr_face, (w, v))
    #                 if nbr_face is None or nbr_face == face:
    #                     break
    #                 nbrs.add(nbr_face)
    #     return list(nbrs)

    # def face_neighborhood_over_vertices(self, face, ring=1):
    #     """Return the face neighborhood of a face across their vertices.

    #     Parameters
    #     ----------
    #     face : int
    #         The identifier of the face.

    #     Returns
    #     -------
    #     list
    #         The list of neighboring faces.

    #     Notes
    #     -----
    #     Neighboring faces on the same cell are not included.
    #     """
    #     nbrs = set(self.face_neighbors_over_vertices(face))
    #     i = 1
    #     while True:
    #         if i == ring:
    #             break
    #         temp = []
    #         for nbr_face in nbrs:
    #             temp += self.face_neighbors_over_vertices(nbr_face)
    #         nbrs.update(temp)
    #         i += 1
    #     return list(nbrs - set([face]))

    # def face_neighbors_over_edges(self, face):
    #     """Return the face neighbors of a face across its edges (faces that share two vertices).

    #     Parameters
    #     ----------
    #     face : int
    #         The identifier of the face.

    #     Returns
    #     -------
    #     list
    #         The list of neighboring faces.

    #     Notes
    #     -----
    #     * Neighboring faces on the same cell are not included.

    #     """
    #     nbrs = []
    #     for halfedge in self.face_halfedges(face):
    #         nbr_face = self.face_adjacent_face(face, halfedge)
    #         if nbr_face:
    #             nbrs.append(nbr_face)
    #     return nbrs

    # def face_neighborhood_over_edges(self, face, ring=1):
    #     """Return the face neighborhood of a face across their edges.

    #     Parameters
    #     ----------
    #     face : int
    #         The identifier of the face.

    #     Returns
    #     -------
    #     list
    #         The list of neighboring faces.

    #     Notes
    #     -----
    #     Neighboring faces on the same cell are not included.
    #     """
    #     nbrs = set(self.face_neighbors_over_edges(face))
    #     i = 1
    #     while True:
    #         if i == ring:
    #             break
    #         temp = []
    #         for nbr_face in nbrs:
    #             temp += self.face_neighbors_over_edges(nbr_face)
    #         nbrs.update(temp)
    #         i += 1
    #     return list(nbrs - set([face]))

    def is_face_on_boundary(self, face):
        """Verify that a face is on the boundary.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.
        """
        u, v, w = self._halfface[face][0:3]
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
        list
            The vertex identifiers of a cell.
        """
        return list(set([vertex for face in self.cell_faces(cell) for vertex in self.face_vertices(face)]))

    def cell_halfedges(self, cell):
        """The halfedges of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list
            The halfedges of a cell.
        """
        halfedges = []
        for face in self.cell_faces(cell):
            halfedges += self.face_halfedges(face)
        return halfedges

    def cell_faces(self, cell):
        """The faces of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list
            The faces of a cell.
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
        list
            The list of neighboring vertices.

        Notes
        -----
        All of the returned vertices should be part of the cell.
        """
        if vertex not in self.cell_vertices(cell):
            raise KeyError(vertex)
        nbr_vertices = self._cell[cell][vertex].keys()
        v = nbr_vertices[0]
        ordered_vkeys = [v]
        for i in range(len(nbr_vertices) - 1):
            face = self._cell[cell][vertex][v]
            v = self.face_vertex_ancestor(face, vertex)
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
        list
            The ordered list of faces connected to a vertex of a cell.

        Notes
        -----
        All of the returned faces should be part of the cell.
        """
        nbr_vertices = self._cell[cell][vertex].keys()
        u = vertex
        v = nbr_vertices[0]
        ordered_faces = []
        for i in range(len(nbr_vertices)):
            face = self._cell[cell][u][v]
            v = self.face_vertex_ancestor(face, u)
            ordered_faces.append(face)
        return ordered_faces

    # def cell_neighbors_over_vertices(self, cell):
    #     """Return the cell neighbors of a cell across its vertices.

    #     Parameters
    #     ----------
    #     cell : int
    #         Identifier of the cell.

    #     Returns
    #     -------
    #     list
    #         The identifiers of the neighboring cells.
    #     """
    #     cells = set()
    #     for vkey in self.cell_vertices(cell):
    #         cells.update(self.vertex_cells(cell))
    #     return list(cells)

    # def cell_neighborhood_over_vertices(self, cell, ring=1):
    #     """Return the cell neighborhood of a cell across its vertices.

    #     Parameters
    #     ----------
    #     cell : int
    #         Identifier of the cell.
    #     ring : int, optional
    #         The number of neighborhood rings to include. Default is ``1``.

    #     Returns
    #     -------
    #     list
    #         The cells in the neighborhood.
    #     """
    #     nbr_cells = set(self.cell_neighbors_over_vertices(cell))
    #     i = 1
    #     while True:
    #         if i == ring:
    #             break
    #         temp = []
    #         for nbr_cell in nbr_cells:
    #             temp += self.cell_neighbors_over_vertices(nbr_cell)
    #         nbr_cells.update(temp)
    #         i += 1
    #     return list(nbr_cells - set([cell]))

    # def cell_neighbors_over_faces(self, cell):
    #     """Return the cell neighbors of a cell across its faces.

    #     Parameters
    #     ----------
    #     cell : int
    #         Identifier of the cell.

    #     Returns
    #     -------
    #     list
    #         The identifiers of the neighboring cells.
    #     """
    #     cells = []
    #     for face in self.cell_faces(cell):
    #         u, v, w = self._halfface[face][0:3]
    #         nbr_cell = self._plane[w][v][u]
    #         if nbr_cell is not None:
    #             cells.append(nbr_cell)
    #     return cells

    # def cell_neighborhood_over_faces(self, cell, ring=1):
    #     """Return the cells in the neighborhood of a cell across its faces.

    #     Parameters
    #     ----------
    #     cell : int
    #         Identifier of the cell.
    #     ring : int, optional
    #         The number of neighborhood rings to include. Default is ``1``.

    #     Returns
    #     -------
    #     list
    #         The identifiers of the neighboring cells.
    #     """
    #     nbr_cells = set(self.cell_neighbors_over_faces(cell))
    #     i = 1
    #     while True:
    #         if i == ring:
    #             break
    #         temp = []
    #         for nbr_cell in nbr_cells:
    #             temp += self.cell_neighbors_over_faces(nbr_cell)
    #         nbr_cells.update(temp)
    #         i += 1
    #     return list(nbr_cells - set([cell]))

    # def cell_adjacency_faces(self, cell_1, cell_2):
    #     """Given 2 cells, returns the interfacing faces, respectively.

    #     Parameters
    #     ----------
    #     cell_1 : int
    #         Identifier of the cell 1.
    #     cell_2 : int
    #         Identifier of the cell 2.

    #     Returns
    #     -------
    #     face_1
    #         The identifier of the face belonging to cell 1.
    #     face_2
    #         The identifier of the face belonging to cell 2.
    #     """
    #     for face in self.cell_faces(cell_1):
    #         u, v, w = self._halfface[face][0:3]
    #         nbr = self._plane[w][v][u]
    #         if nbr == cell_2:
    #             return face, self.face_opposite_face(face)
    #     return

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
            if self.is_face_on_boundary(face):
                return True
        return False

    # --------------------------------------------------------------------------
    # boundary
    # --------------------------------------------------------------------------

    def vertices_on_boundaries(self):
        """Find the vertices on the boundary.

        Returns
        -------
        list
            The vertices of the boundary.
        """
        vertices = set()
        for face in self._halfface:
            if self.is_face_on_boundary(face):
                vertices.update(self.face_vertices(face))
        return list(vertices)

    def faces_on_boundaries(self):
        """Find the faces on the boundary.

        Returns
        -------
        list
            The faces of the boundary.
        """
        faces = set()
        for face in self._halfface:
            if self.is_face_on_boundary(face):
                faces.add(face)
        return list(faces)

    def cells_on_boundaries(self):
        """Find the cells on the boundary.

        Returns
        -------
        list
            The cells of the boundary.
        """
        cells = set()
        for face in self.faces_on_boundaries():
            cells.add(self.face_cell(face))
        return list(cells)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
