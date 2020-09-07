from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from ast import literal_eval
from random import sample
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

        self._max_int_vkey = -1
        self._max_int_hfkey = -1
        self._max_int_ckey = -1

        self.vertex = {}
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
        """Print a summary of the volmesh."""
        tpl = "\n".join(
            ["VolMesh summary",
             "===============",
             "- vertices: {}",
             "- edges   : {}",
             "- faces   : {}",
             "- cells   : {}"])
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
        * 'dca'          => dict
        * 'vertex'       => dict
        * 'halfface'     => dict
        * 'cell'         => dict
        * 'plane'        => dict
        * 'edgedata'     => dict
        * 'facedata'     => dict
        * 'celldata'     => dict
        * 'max_int_key'  => int
        * 'max_int_hfkey' => int
        * 'max_int_ckey' => int

        Notes
        -----
        All dictionary keys are converted to their representation value (``repr(key)``)
        to ensure compatibility of all allowed key types with the JSON serialisation
        format, which only allows for dict keys that are strings.
        """

        edgedata = {}
        facedata = {}
        celldata = {}

        for edge in self.edgedata:
            edgedata[repr(edge)] = self.edgedata[edge]

        for face in self.facedata:
            facedata[str(face)] = self.facedata[face]

        for cell in self.celldata:
            celldata[str(cell)] = self.celldata[cell]

        data = {
            'attributes': self.attributes,
            'dva': self.default_vertex_attributes,
            'dea': self.default_edge_attributes,
            'dfa': self.default_face_attributes,
            'dca': self.default_cell_attributes,
            'vertex': self.vertex,
            'halfface': self.halfface,
            'cell': self.cell,
            'plane': self.plane,
            'edgedata': edgedata,
            'facedata': facedata,
            'celldata': celldata,
            'max_int_vkey': self._max_int_vkey,
            'max_int_hfkey': self._max_int_hfkey,
            'max_int_ckey': self._max_int_ckey}

        return data

    @data.setter
    def data(self, data):
        attributes = data.get('attributes') or {}
        dva = data.get('dva') or {}
        dea = data.get('dea') or {}
        dfa = data.get('dfa') or {}
        dca = data.get('dca') or {}
        vertex = data.get('vertex') or {}
        halfface = data.get('halfface') or {}
        cell = data.get('cell') or {}
        plane = data.get('plane') or {}
        edgedata = data.get('edgedata') or {}
        facedata = data.get('facedata') or {}
        celldata = data.get('celldata') or {}
        max_int_vkey = data.get('max_int_vkey', - 1)
        max_int_hfkey = data.get('max_int_hfkey', - 1)
        max_int_ckey = data.get('max_int_ckey', - 1)

        if not vertex or not plane or not halfface or not cell:
            return

        self.attribute.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_edge_attributes.update(dea)
        self.default_face_attributes.update(dfa)
        self.default_cell_attributes.update(dca)

        self.vertex = {}
        self.halfface = {}
        self.cell = {}
        self.plane = {}
        self.edgedata = {}
        self.facedata = {}
        self.celldata = {}

        for vkey, attr in iter(vertex.items()):
            self.add_vertex(int(vkey), attr_dict=attr)

        for hfkey, vertices in iter(halfface.items()):
            attr = facedata.get(hfkey) or {}
            self.add_halfface(vertices, fkey=int(hfkey), attr_dict=attr)

        for ckey in cell:
            attr = celldata.get(ckey) or {}
            hfkeys = list(set(cell[ckey][u].values() for u in cell[ckey]))
            halffaces = [self.halfface[hfkey] for hfkey in hfkeys]
            self.add_cell(halffaces, ckey=int(ckey), attr_dict=attr)

        for edge, attr in iter(edgedata.items()):
            self.edgedata[literal_eval(edge)] = attr or {}

        self._max_int_vkey = max_int_vkey
        self._max_int_hfkey = max_int_hfkey
        self._max_int_ckey = max_int_ckey

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def clear(self):
        """Clear all the volmesh data."""
        del self.vertex
        del self.halfface
        del self.cell
        del self.plane
        del self.edgedata
        del self.facedata
        del self.celldata
        self.vertex = {}
        self.halfface = {}
        self.cell = {}
        self.planem = {}
        self.edgedata = {}
        self.facedata = {}
        self.celldata = {}
        self._max_int_vkey = -1
        self._max_int_hfkey = -1
        self._max_int_ckey = -1

    def get_any_vertex(self):
        """Get the identifier of a random vertex.

        Returns
        -------
        int
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
            vertices = set(self.vertices()) - set(self.vertices_on_boundaries())
        else:
            vertices = self.vertices()
        return sample(list(vertices), n)

    def get_any_halfface(self):
        """Get the identifier of a random halfface.

        Returns
        -------
        int
            The identifier of the halfface.
        """
        return choice(list(self.halffaces()))

    def get_any_halfface_vertex(self, halfface):
        """Get the identifier of a random vertex of a specific halfface.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        int
            The identifier of the vertex of the halfface.
        """
        return self.halfface_vertices(halfface)[0]

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
            key = self._max_int_vkey = self._max_int_vkey + 1
        if key > self._max_int_vkey:
            self._max_int_vkey = key
        key = int(key)
        if key not in self.vertex:
            self.vertex[key] = {}
            self.plane[key] = {}
        attr = attr_dict or {}
        attr.update(kwattr)
        self.vertex[key].update(attr)
        return key

    def add_halfface(self, vertices, hfkey=None, attr_dict=None, **kwattr):
        """Add a halfface to the volmesh object.

        Parameters
        ----------
        vertices : list
            A list of ordered vertex keys representing the halfface.
            For every vertex that does not yet exist, a new vertex is created.
        hfkey : int, optional
            The halfface identifier.
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

        Notes
        -----
        If no key is provided for the halfface, one is generated
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
        if hfkey is None:
            hfkey = self._max_int_hfkey = self._max_int_hfkey + 1
        if hfkey > self._max_int_hfkey:
            self._max_int_hfkey = hfkey
        attr = attr_dict or {}
        attr.update(kwattr)
        self.halfface[hfkey] = vertices
        self.facedata.setdefault(hfkey, attr)
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
        return hfkey

    def add_cell(self, halffaces, ckey=None, attr_dict=None, **kwattr):
        """Add a cell to the volmesh object.

        Parameters
        ----------
        halffaces : list of lists
            list of lists of vertex keys defining the halffaces of the cell.
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
        cell_halffaces = self.cell_halffaces(cell)
        for halfface in cell_halffaces:
            for edge in self.halfface_halfedges(halfface):
                u, v = edge
                if (u, v) in self.edgedata:
                    del self.edgedata[u, v]
                if (v, u) in self.edgedata:
                    del self.edgedata[v, u]
        for vertex in cell_vertices:
            if len(self.vertex_cells(vertex)) == 1:
                del self.vertex[vertex]
        for halfface in cell_halffaces:
            vertices = self.halfface_vertices(halfface)
            for i in range(-2, len(vertices) - 2):
                u = vertices[i]
                v = vertices[i + 1]
                w = vertices[i + 2]
                self.plane[u][v][w] = None
                if self.plane[w][v][u] is None:
                    del self.plane[u][v][w]
                    del self.plane[w][v][u]
            del self.halfface[halfface]
            if halfface in self.facedata:
                del self.facedata[halfface]
        del self.cell[cell]
        if cell in self.celldata:
            del self.celldata[cell]

    def remove_unused_vertices(self):
        """Remove all unused vertices from the volmesh object.
        """
        for vertex in list(self.vertices()):
            if vertex not in self.plane:
                del self.vertex[vertex]
            else:
                if not self.plane[vertex]:
                    del self.vertex[vertex]
                    del self.plane[vertex]

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
        for vertex in self.vertex:
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
        for halfface in self.halfface:
            vertices = self.halfface[halfface]
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
            The next halfface identifier, if ``data`` is ``False``.
            The next halfface as a (halfface, attr) tuple, if ``data`` is ``True``.
        """
        for halfface in self.halfface:
            if not data:
                yield halfface
            else:
                yield halfface, self.face_attributes(halfface)

    def faces(self, data=False):
        """"Iterate over the halffaces of the volmesh, and yield "faces" (unique halffaces).

        Parameters
        ----------
        data : bool, optional
            Return the face data as well as the halfface keys.

        Yields
        ------
        int or tuple
            The next face identifier, if ``data`` is ``False``.
            The next face as a (face, attr) tuple, if ``data`` is ``True``.

        Notes
        -----
        Volmesh faces have no topological meaning (analogous to an edge of a mesh).
        They are typically used for geometric operations (i.e. planarisation).
        Between the interface of two cells, there are two interior halffaces (one from each cell).
        Only one of these two interior halffaces are returned as a "face".
        The unique faces are found by comparing string versions of sorted vertex lists.
        """
        seen = set()
        faces = []
        for halfface in self.halfface:
            vertices = self.halfface_vertices(halfface)
            key = "-".join(map(str, sorted(vertices, key=int)))
            if key not in seen:
                seen.add(key)
                faces.append(halfface)
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
        for cell in self.cell:
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
        if vertex not in self.vertex:
            raise KeyError(vertex)
        if value is not None:
            self.vertex[vertex][name] = value
            return None
        if name in self.vertex[vertex]:
            return self.vertex[vertex][name]
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
        if name in self.vertex[vertex]:
            del self.vertex[vertex][name]

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
        if vertex not in self.vertex:
            raise KeyError(vertex)
        if values:
            for name, value in zip(names, values):
                self.vertex[vertex][name] = value
            return
        if not names:
            return VertexAttributeView(self.default_vertex_attributes, self.vertex[vertex])
        values = []
        for name in names:
            if name in self.vertex[vertex]:
                values.append(self.vertex[vertex][name])
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
        if u not in self.plane or v not in self.plane[u]:
            raise KeyError(edge)
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
        if u not in self.plane or v not in self.plane[u]:
            raise KeyError(edge)
        if edge in self.edgedata:
            if name in self.edgedata[edge]:
                del self.edgedata[edge][name]
        edge = v, u
        if edge in self.edgedata:
            if name in self.edgedata[edge]:
                del self.edgedata[edge][name]

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
        if face not in self.halfface:
            raise KeyError(face)
        if value is not None:
            if face not in self.facedata:
                self.facedata[face] = {}
            self.facedata[face][name] = value
            return
        if face in self.facedata and name in self.facedata[face]:
            return self.facedata[face][name]
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
        if face not in self.halfface:
            raise KeyError(face)
        if face in self.facedata:
            if name in self.facedata[face]:
                del self.facedata[face][name]

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
        if face not in self.halfface:
            raise KeyError(face)
        if values:
            for name, value in zip(names, values):
                if face not in self.facedata:
                    self.facedata[face] = {}
                self.facedata[face][name] = value
            return
        if not names:
            return FaceAttributeView(self.default_face_attributes, self.facedata, face)
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
        if cell not in self.cell:
            raise KeyError(cell)
        if value is not None:
            if cell not in self.celldata:
                self.celldata[cell] = {}
            self.celldata[cell][name] = value
            return
        if cell in self.celldata and name in self.celldata[cell]:
            return self.celldata[cell][name]
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
        if cell not in self.cell:
            raise KeyError(cell)
        if cell in self.celldata:
            if name in self.celldata[cell]:
                del self.celldata[cell][name]

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
        if cell not in self.cell:
            raise KeyError(cell)
        if values is not None:
            for name, value in zip(names, values):
                if cell not in self.celldata:
                    self.celldata[cell] = {}
                self.celldata[cell][name] = value
            return
        if not names:
            return CellAttributeView(self.default_cell_attributes, self.celldata.setdefault(cell, {}))
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
        return vertex in self.vertex

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
        return self.plane[vertex].keys()

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
        if not self.vertex:
            return 0
        return min(self.vertex_degree(vertex) for vertex in self.vertices())

    def vertex_max_degree(self):
        """Compute the maximum degree of all vertices.

        Returns
        -------
        int
            The highest degree of all vertices.
        """
        if not self.vertex:
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
        list
            The list of halffaces connected to a vertex.
        """
        cells = self.vertex_cells(vertex)
        nbr_vertices = self.vertex_neighbors(vertex)
        halffaces = set()
        for cell in cells:
            for nbr in nbr_vertices:
                if nbr in self.cell[cell][vertex]:
                    halffaces.add(self.cell[cell][vertex][nbr])
                    halffaces.add(self.cell[cell][nbr][vertex])
        return list(halffaces)

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
        for halfface in halffaces:
            if halfface not in seen:
                opp_halfface = self.halfface_opposite_halfface(halfface)
                faces.append(opp_halfface)
            seen.add([halfface, opp_halfface])
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
        for v in self.plane[vertex].keys():
            for cell in self.plane[vertex][v].values():
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
        """Ordered halffaces around edge (u, v).

        Parameters
        ----------
        edge : tuple of int
            The identifier of the edge.

        Returns
        -------
        list
            Ordered list of of keys identifying the halffaces.

        Notes
        -----
        The halffaces are ordered around the edge (u, v).
        All halffaces returned should have halfedge (u, v) or (v, u).
        This also means that if edge u-v is shared by four cells, eight halffaces are returned.
        """
        u, v = edge
        cells = self.edge_cells(edge)
        ordered_halffaces = []
        for cell in cells:
            ordered_halffaces.append(self.cell[cell][v][u])
            ordered_halffaces.append(self.cell[cell][u][v])
        return ordered_halffaces

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
        edge_cells = [cell for cell in self.plane[u][v].values() if cell is not None]
        cell = edge_cells[0]
        ordered_faces = []
        if self.is_edge_on_boundary(edge):
            for bndry_cell in edge_cells:
                halfface = self.cell[bndry_cell][v][u]
                if self.is_halfface_on_boundary(halfface):
                    cell = bndry_cell
                    break
        for i in range(len(edge_cells)):
            face = self.cell[cell][u][v]
            w = self.halfface_vertex_descendent(face, v)
            cell = self.plane[w][v][u]
            ordered_faces.append(face)
        return ordered_faces

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
        if not self.has_edge(edge):
            v, u = edge
        return None in self.plane[u][v].values()

    # --------------------------------------------------------------------------
    # halfface topology
    # --------------------------------------------------------------------------

    def has_halfface(self, halfface):
        """Verify that a halfface is part of the volmesh.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        bool
            True if the halfface exists.
            False otherwise.
        """
        return halfface in self.halfface

    def halfface_vertices(self, halfface):
        """The vertices of a halfface.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list
            Ordered vertex identifiers.
        """
        return self.halfface[halfface]

    def halfface_halfedges(self, halfface):
        """The halfedges of a halfface.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list
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
        ckey
            Identifier of the cell.
        """
        u, v, w = self.halfface[halfface][0:3]
        return self.plane[u][v][w]

    def halfface_opposite_halfface(self, halfface):
        """The opposite halfface of a halfface.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        halfface
            Identifier of the opposite halfface.

        Notes
        -----
        A halfface and its opposite halfface share the same vertices, but in reverse order.
        For a boundary halfface, the opposite halfface is None.
        """
        u, v, w = self.halfface[halfface][0:3]
        nbr_cell = self.plane[w][v][u]
        if nbr_cell is None:
            return None
        return self.cell[nbr_cell][v][u]

    def halfface_adjacent_halfface(self, halfface, edge):
        """Return the halfface adjacent to a halfface across the halfedge edge.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.
        edge : tuple of int
            The identifier of the common edge.

        Returns
        -------
        int or None
            The identifier of the halfface.
            None, if both halffaces belong to the same cell.

        Notes
        -----
        The adjacent halfface belongs a to one of the cell neighbors over halffaces of the initial cell.
        A halfface and its adjacent halfface share two common vertices.
        """
        u, v = edge
        if (u, v) not in self.halfface_halfedges(halfface):
            if (v, u) not in self.halfface_halfedges(halfface):
                raise KeyError(edge)
            u, v = v, u
        cell = self.halfface_cell(halfface)
        adj_halfface = self.cell[cell][v][u]
        w = self.halfface_vertex_ancestor(adj_halfface, v)
        nbr_cell = self.plane[u][v][w]
        if nbr_cell is None:
            return None
        return self.cell[nbr_cell][v][u]

    def halfface_vertex_ancestor(self, halfface, vertex):
        """Return the vertex before the specified vertex in a specific halfface.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        int
            The identifier of the vertex before the given vertex in the halfface cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the halfface.
        """
        i = self.halfface[halfface].index(vertex)
        return self.halfface[halfface][i - 1]

    def halfface_vertex_descendent(self, halfface, vertex):
        """Return the vertex after the specified vertex in a specific halfface.

        Parameters
        ----------
        halfface : int
            Identifier of the halfface.
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        int
            The identifier of the vertex after the given vertex in the halfface cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the halfface.
        """
        if self.halfface[halfface][-1] == vertex:
            return self.halfface[halfface][0]
        i = self.halfface[halfface].index(vertex)
        return self.halfface[halfface][i + 1]

    def halfface_neighbors_over_vertices(self, halfface):
        """Return all halffaces that share at least one vertex with a halfface.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list
            The list of halffaces.

        Notes
        -----
        Neighboring halffaces on the same cell are not included.
        Neighboring halffaces belong to one of the neighboring cells over halffaces of the initial cell.
        """
        nbrs = set()
        for u, v in self.halfface_halfedges(halfface):
            nbr_halfface = self.halfface_adjacent_halfface(halfface, (u, v))
            if nbr_halfface is not None:
                nbrs.add(nbr_halfface)
                while True:
                    w = self.halfface_vertex_ancestor(nbr_halfface, v)
                    nbr_halfface = self.halfface_adjacent_halfface(nbr_halfface, (w, v))
                    if nbr_halfface is None or nbr_halfface == halfface:
                        break
                    nbrs.add(nbr_halfface)
        return list(nbrs)

    def halfface_neighborhood_over_vertices(self, halfface, ring=1):
        """Return the halfface neighborhood of a halfface across their vertices.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list
            The list of neighboring halffaces.

        Notes
        -----
        Neighboring halffaces on the same cell are not included.
        """
        nbrs = set(self.halfface_neighbors_over_vertices(halfface))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr_halfface in nbrs:
                temp += self.halfface_neighbors_over_vertices(nbr_halfface)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([halfface]))

    def halfface_neighbors_over_edges(self, halfface):
        """Return the halfface neighbors of a halfface across its edges (halffaces that share two vertices).

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list
            The list of neighboring halffaces.

        Notes
        -----
        * Neighboring halffaces on the same cell are not included.

        """
        nbrs = []
        for halfedge in self.halfface_halfedges(halfface):
            nbr_halfface = self.halfface_adjacent_halfface(halfface, halfedge)
            if nbr_halfface:
                nbrs.append(nbr_halfface)
        return nbrs

    def halfface_neighborhood_over_edges(self, halfface, ring=1):
        """Return the halfface neighborhood of a halfface across their edges.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list
            The list of neighboring halffaces.

        Notes
        -----
        Neighboring halffaces on the same cell are not included.
        """
        nbrs = set(self.halfface_neighbors_over_edges(halfface))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr_halfface in nbrs:
                temp += self.halfface_neighbors_over_edges(nbr_halfface)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([halfface]))

    def is_halfface_on_boundary(self, halfface):
        """Verify that a halfface is on the boundary.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        bool
            True if the halfface is on the boundary.
            False otherwise.
        """
        u, v, w = self.halfface[halfface][0:3]
        return self.plane[w][v][u] is None

    has_face = has_halfface
    face_vertices = halfface_vertices
    face_halfedges = halfface_halfedges
    face_cell = halfface_cell
    face_vertex_ancestor = halfface_vertex_ancestor
    face_vertex_descendent = halfface_vertex_descendent
    is_face_on_boundary = is_halfface_on_boundary

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
        return list(set([vertex for halfface in self.cell_halffaces(cell) for vertex in self.halfface_vertices(halfface)]))

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
        for halfface in self.cell_halffaces(cell):
            halfedges += self.halfface_halfedges(halfface)
        return halfedges

    def cell_halffaces(self, cell):
        """The halffaces of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list
            The halffaces of a cell.
        """
        halffaces = set()
        for vertex in self.cell[cell]:
            halffaces.update(self.cell[cell][vertex].values())
        return list(halffaces)

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
        nbr_vertices = self.cell[cell][vertex].keys()
        v = nbr_vertices[0]
        ordered_vkeys = [v]
        for i in range(len(nbr_vertices) - 1):
            halfface = self.cell[cell][vertex][v]
            v = self.halfface_vertex_ancestor(halfface, vertex)
            ordered_vkeys.append(v)
        return ordered_vkeys

    def cell_vertex_halffaces(self, cell, vertex):
        """Ordered halffaces connected to a vertex of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.
        vertex : int
            Identifier of the vertex.

        Returns
        -------
        list
            The ordered list of halffaces connected to a vertex of a cell.

        Notes
        -----
        All of the returned halffaces should be part of the cell.
        """
        nbr_vertices = self.cell[cell][vertex].keys()
        u = vertex
        v = nbr_vertices[0]
        ordered_halffaces = []
        for i in range(len(nbr_vertices)):
            halfface = self.cell[cell][u][v]
            v = self.halfface_vertex_ancestor(halfface, u)
            ordered_halffaces.append(halfface)
        return ordered_halffaces

    def cell_neighbors_over_vertices(self, cell):
        """Return the cell neighbors of a cell across its vertices.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list
            The identifiers of the neighboring cells.
        """
        cells = set()
        for vkey in self.cell_vertices(cell):
            cells.update(self.vertex_cells(cell))
        return list(cells)

    def cell_neighborhood_over_vertices(self, cell, ring=1):
        """Return the cell neighborhood of a cell across its vertices.

        Parameters
        ----------
        cell : int
            Identifier of the cell.
        ring : int, optional
            The number of neighborhood rings to include. Default is ``1``.

        Returns
        -------
        list
            The cells in the neighborhood.
        """
        nbr_cells = set(self.cell_neighbors_over_vertices(cell))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr_cell in nbr_cells:
                temp += self.cell_neighbors_over_vertices(nbr_cell)
            nbr_cells.update(temp)
            i += 1
        return list(nbr_cells - set([cell]))

    def cell_neighbors_over_halffaces(self, cell):
        """Return the cell neighbors of a cell across its halffaces.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list
            The identifiers of the neighboring cells.
        """
        cells = []
        for halfface in self.cell_halffaces(cell):
            u, v, w = self.halfface[halfface][0:3]
            nbr_cell = self.plane[w][v][u]
            if nbr_cell is not None:
                cells.append(nbr_cell)
        return cells

    def cell_neighborhood_over_halffaces(self, cell, ring=1):
        """Return the cells in the neighborhood of a cell across its halffaces.

        Parameters
        ----------
        cell : int
            Identifier of the cell.
        ring : int, optional
            The number of neighborhood rings to include. Default is ``1``.

        Returns
        -------
        list
            The identifiers of the neighboring cells.
        """
        nbr_cells = set(self.cell_neighbors_over_halffaces(cell))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr_cell in nbr_cells:
                temp += self.cell_neighbors_over_halffaces(nbr_cell)
            nbr_cells.update(temp)
            i += 1
        return list(nbr_cells - set([cell]))

    def cell_adjacency_halffaces(self, cell_1, cell_2):
        """Given 2 cells, returns the interfacing halffaces, respectively.

        Parameters
        ----------
        cell_1 : int
            Identifier of the cell 1.
        cell_2 : int
            Identifier of the cell 2.

        Returns
        -------
        halfface_1
            The identifier of the halfface belonging to cell 1.
        halfface_2
            The identifier of the halfface belonging to cell 2.
        """
        for halfface in self.cell_halffaces(cell_1):
            u, v, w = self.halfface[halfface][0:3]
            nbr = self.plane[w][v][u]
            if nbr == cell_2:
                return halfface, self.halfface_opposite_halfface(halfface)
        return

    def is_cell_on_boundary(self, cell):
        """Verify that a cell is on the boundary.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        bool
            True if the halfface is on the boundary.
            False otherwise.
        """
        halffaces = self.cell_halffaces(cell)
        for halfface in halffaces:
            if self.is_halfface_on_boundary(halfface):
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
        for halfface in self.halfface:
            if self.is_halfface_on_boundary(halfface):
                vertices.update(self.halfface_vertices(halfface))
        return list(vertices)

    def halffaces_on_boundaries(self):
        """Find the halffaces on the boundary.

        Returns
        -------
        list
            The halffaces of the boundary.
        """
        halffaces = set()
        for halfface in self.halfface:
            if self.is_halfface_on_boundary(halfface):
                halffaces.add(halfface)
        return list(halffaces)

    def cells_on_boundaries(self):
        """Find the cells on the boundary.

        Returns
        -------
        list
            The cells of the boundary.
        """
        cells = set()
        for halfface in self. halffaces_on_boundaries():
            cells.add(self.halfface_cell(halfface))
        return list(cells)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
