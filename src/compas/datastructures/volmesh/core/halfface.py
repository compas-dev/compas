from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import pickle
import deepcopy

from ast import literal_eval
from random import sample
from random import choice

from compas.datastructures.volmesh.core import VertexAttributeView
from compas.datastructures.volmesh.core import FaceAttributeView
from compas.datastructures.volmesh.core import CellAttributeView

from compas.datastructures import Datastructure
from compas.utilities import geometric_key
from compas.utilities import pairwise


__all__ = ['HalfFace']


class HalfFace(Datastructure):
    """Base half-face data structure fore representing volumetric meshes.

    Attributes
    ----------
    attributes
    default_vertex_attributes
    default_edge_attributes
    default_face_attributes
    default_cell_attributes
    name
    adjacency
    data

    """

    def __init__(self):
        super(HalfFace, self).__init__()

        self._max_int_vkey = -1
        self._max_int_fkey = -1
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
    def adjacency(self):
        return self.halfface

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
        * 'max_int_fkey' => int
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

        for uv in self.edgedata:
            edgedata[repr(uv)] = self.edgedata[uv]

        for fkey in self.facedata:
            facedata[str(fkey)] = self.facedata[fkey]

        for ckey in self.celldata:
            celldata[str(ckey)] = self.celldata[ckey]

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
            'max_int_fkey': self._max_int_fkey,
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
        max_int_fkey = data.get('max_int_fkey', - 1)
        max_int_ckey = data.get('max_int_ckey', - 1)

        if not vertex or not plane or not halfface or not cell:
            return

        self.attribute.update(attributes)
        self.default_vertex_attributes.update(dva)
        self.default_edge_attributes.update(dea)
        self.default_face_attributes.update(dfa)
        self.default_cell_attributes.update(dca)

        self.vertex = {}
        self.halfedge = {}
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

        for uv, attr in iter(edgedata.items()):
            self.edgedata[literal_eval(uv)] = attr or {}

        self._max_int_vkey = max_int_vkey
        self._max_int_fkey = max_int_fkey
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

    def delete_vertex(self, vkey):
        """Delete a vertex from the volmesh and everything that is attached to it.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Examples
        --------
        >>>
        """
        for ckey in self.vertex_cells(vkey):
            self.delete_cell(ckey)

    # def delete_halfface(self, hfkey):
    #     """Delete a halfface.
    #     """
    #     vertices = self.halfface_vertices(hfkey)
    #     for i in range(-2, len(vertices) - 2):
    #         u = vertices[i]
    #         v = vertices[i + 1]
    #         w = vertices[i + 2]
    #         del self.plane[u][v][w]
    #         if self.plane[w][v][u] is None:
    #             del self.plane[w][v][u]
    #     del self.halfface[hfkey]
    #     if hfkey in self.facedata:
    #         del self.facedata[hfkey]

    def delete_cell(self, ckey):
        """Delete a cell from the volmesh.

        Parameters
        ----------
        fkey : int
            The identifier of the cell.

        Notes
        -----
        In some cases (although very unlikely), disconnected vertices can remain after application of this
        method. To remove these vertices as well, combine this method with vertex
        culling (:meth:`cull_vertices`).

        Examples
        --------
        >>>
        """
        for hfkey in self.cell_halffaces(ckey):

            # edges
            for u, v in self.halfface_halfedges(hfkey):
                if (u, v) in self.edgedata:
                    del self.edgedata[u, v]
                if (v, u) in self.edgedata:
                    del self.edgedata[v, u]

            # planes
            vertices = self.halfface_vertices(hfkey)
            for i in range(-2, len(vertices - 2)):
                u = vertices[i]
                v = vertices[i + 1]
                w = vertices[i + 2]
                self.plane[u][v][w] = None
                if self.plane[w][v][u] is None:
                    del self.plane[u][v][w]
                    del self.plane[w][v][u]

            # halfface
            del self.halfface[hfkey]
            if hfkey in self.facedata:
                del self.facedata[hfkey]

        # vertices
        for vkey in self.cell_vertices(ckey):
            if len(self.vertex_cells(vkey)) == 1:
                del self.vertex[vkey]

        # cell
        del self.cell[ckey]
        if ckey in self.celldata:
            del self.celldata[ckey]

    def remove_unused_vertices(self):
        """Remove all unused vertices from the volmesh object.
        """
        for u in list(self.vertices()):
            if u not in self.plane:
                del self.vertex[u]
            else:
                if not self.plane[u]:
                    del self.vertex[u]
                    del self.plane[u]

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
            if not data:
                yield vkey
            else:
                yield vkey, self.vertex_attributes(vkey)

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

        Notes
        -----
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
            if not data:
                yield fkey
            else:
                yield fkey, self.face_attributes(fkey)

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
            if not data:
                yield ckey
            else:
                yield ckey, self.cell_attributes(ckey)

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
        if u not in self.plane or v not in self.plane[u]:
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
        if u not in self.plane or v not in self.plane[u]:
            raise KeyError(key)
        if key in self.edgedata:
            if name in self.edgedata[key]:
                del self.edgedata[key][name]
        key = v, u
        if key in self.edgedata:
            if name in self.edgedata[key]:
                del self.edgedata[key][name]

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

        Notes
        -----
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
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary,
        if they exist.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_cell_attributes.update(attr_dict)

    def cell_attribute(self, key, name, value=None):
        """Get or set an attribute of a cell.

        Parameters
        ----------
        key : int
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
        if key not in self.cell:
            raise KeyError(key)
        if value is not None:
            if key not in self.celldata:
                self.celldata[key] = {}
            self.celldata[key][name] = value
            return
        if key in self.celldata and name in self.celldata[key]:
            return self.celldata[key][name]
        if name in self.default_cell_attributes:
            return self.default_cell_attributes[name]

    def unset_cell_attribute(self, key, name):
        """Unset the attribute of a cell.

        Parameters
        ----------
        key : int
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
        if key not in self.cell:
            raise KeyError(key)
        if key in self.celldata:
            if name in self.celldata[key]:
                del self.celldata[key][name]

    def cell_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of a cell.

        Parameters
        ----------
        key : int
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
        if key not in self.cell:
            raise KeyError(key)
        if values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                if key not in self.celldata:
                    self.celldata[key] = {}
                self.celldata[key][name] = value
            return
        # use it as a getter
        if not names:
            return CellAttributeView(self.default_cell_attributes, self.celldata.setdefault(key, {}))
        values = []
        for name in names:
            value = self.cell_attribute(key, name)
            values.append(value)
        return values

    def cells_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple cells.

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
            If any of the cells does not exist.

        """
        if not keys:
            keys = self.cells()
        if value is not None:
            for key in keys:
                self.cell_attribute(key, name, value)
            return
        return [self.cell_attribute(key, name) for key in keys]

    def cells_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple cells.

        Parameters
        ----------
        names : list of str, optional
            The names of the attribute.
            Default is ``None``.
        values : list of obj, optional
            The values of the attributes.
            Default is ``None``.
        keys : list of int, optional
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
        if not keys:
            keys = self.cells()
        if values is not None:
            for key in keys:
                self.cell_attributes(key, names, values)
            return
        return [self.cell_attributes(key, names) for key in keys]

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

    def has_vertex(self, key):
        """Verify that a vertex is in the volmesh.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is in the volmesh.
            False otherwise.

        """
        return key in self.vertex

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
            for nbr_key in nbrs:
                temp += self.vertex_neighbors(nbr_key)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([key]))

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

    def vertex_halffaces(self, vkey):
        """Return all halffaces connected to a vertex.

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
        nbr_vkeys = self.vertex_neighbors(vkey)
        hfkeys = set()
        for ckey in cells:
            for v in nbr_vkeys:
                if v in self.cell[ckey][vkey]:
                    hfkeys.add(self.cell[ckey][vkey][v])
                    hfkeys.add(self.cell[ckey][v][vkey])
        return list(hfkeys)

    def vertex_cells(self, vkey):
        """Return all cells connected to a vertex.

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
            for ckey in self.plane[vkey][v].values():
                if ckey:
                    ckeys.add(ckey)
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

    def has_edge(self, key):
        """Verify that the volmesh contains a specific edge.

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

    def edge_halffaces(self, u, v):
        """Ordered halffaces around edge u-v.

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

        Notes
        -----
        The halffaces are ordered around the halfedge u-v.

        All halffaces returned should have halfedge u-v; this also means that if edge u-v is shared by four cells, four halffaces are returned, not eight.

        """
        edge_ckeys = self.plane[u][v].values()
        ckey = edge_ckeys[0]
        ordered_hfkeys = []
        for i in range(len(edge_ckeys)):
            hfkey = self.cell[ckey][u][v]
            w = self.halfface_vertex_descendent(hfkey, v)
            ckey = self.plane[w][v][u]
            ordered_hfkeys.append(hfkey)
        return ordered_hfkeys

    def edge_cells(self, u, v):
        """Ordered cells around edge u-v.

        Parameters
        ----------
        u : hashable
            The identifier of the first vertex.
        v : hashable
            The identifier of the second vertex.

        Returns
        -------
        list
            Ordered list of keys identifying the adjacent cells.

        """
        edge_ckeys = self.plane[u][v].values()
        ckey = edge_ckeys[0]
        ordered_ckeys = []
        for i in range(len(edge_ckeys)):
            hfkey = self.cell[ckey][u][v]
            w = self.halfface_vertex_descendent(hfkey, v)
            ckey = self.plane[w][v][u]
            ordered_ckeys.append(ckey)
        return ordered_ckeys

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
        return None in self.plane[u][v].values()

    # --------------------------------------------------------------------------
    # halfface topology
    # --------------------------------------------------------------------------

    def has_face(self, hfkey):
        """Verify that a halfface is part of the volmesh.

        Parameters
        ----------
        hfkey : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the face exists.
            False otherwise.

        """
        return hfkey in self.halfface

    def halfface_vertices(self, hfkey):
        """The vertices of a halfface.

        Parameters
        ----------
        hfkey : hashable
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
        hfkey : hashable
            Identifier of the halfface.

        Returns
        -------
        list
            The halfedges of a halfface.

        """
        vertices = self.halfface_vertices(hfkey)
        return list(pairwise(vertices + vertices[0:1]))

    def halfface_cell(self, hfkey):
        """The cell to which the halfface belongs to.

        Parameters
        ----------
        hfkey : hashable
            Identifier of the halfface.

        Returns
        -------
        ckey
            Identifier of the cell.

        """
        u, v, w = self.halfface[hfkey][0:3]
        return self.plane[u][v][w]

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

        Notes
        -----
        A halfface and its opposite halfface share the same vertices, but in reverse order.

        For a boundary halfface, the opposite halfface is None.

        """
        u, v, w = self.halfface[hfkey][0:3]
        nbr_ckey = self.plane[w][v][u]
        if nbr_ckey is None:
            return None
        return self.cell[nbr_ckey][v][u]

    def halfface_adjacent_halfface(self, hfkey, uv):
        """Return the halfface adjacent to a halfface across the halfedge uv.

        Parameters
        ----------
        hfkey : hashable
            The identifier of the halfface.
        uv : tuple of int
            The identifier of the halfedge.

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
        if uv not in self.halfface_halfedges(hfkey):
            raise KeyError(uv)
        u, v = uv
        ckey = self.halfface_cell(hfkey)
        adj_hfkey = self.cell[ckey][v][u]
        w = self.halfface_vertex_ancestor(adj_hfkey, v)
        nbr_ckey = self.plane[u][v][w]
        if nbr_ckey is None:
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

    def halfface_neighbors_over_vertices(self, hfkey):
        """Return all halffaces that share at least one vertex with a halfface.

        Parameters
        ----------
        hfkey : hashable
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
        for u, v in self.halfface_halfedges(hfkey):
            nbr_hfkey = self.halfface_adjacent_halfface(hfkey, (u, v))
            if nbr_hfkey is not None:
                nbrs.add(nbr_hfkey)
                while True:
                    w = self.halfface_vertex_ancestor(nbr_hfkey, v)
                    nbr_hfkey = self.halfface_adjacent_halfface(nbr_hfkey, (w, v))
                    if nbr_hfkey is None or nbr_hfkey == hfkey:
                        break
                    nbrs.add(nbr_hfkey)
        return list(nbrs)

    def halfface_neighborhood_over_vertices(self, hfkey, ring=1):
        """Return the halfface neighborhood of a halfface across their vertices.

        Parameters
        ----------
        key : hashable
            The identifier of the halfface.

        Returns
        -------
        list
            The list of neighboring halffaces.

        Notes
        -----
        Neighboring halffaces on the same cell are not included.

        """
        nbrs = set(self.halfface_neighbors_over_vertices(hfkey))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr_hfkey in nbrs:
                temp += self.halfface_neighbors_over_vertices(nbr_hfkey)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([hfkey]))

    def halfface_neighbors_over_edges(self, hfkey):
        """Return the halfface neighbors of a halfface across its edges (halffaces that share two vertices).

        Parameters
        ----------
        key : hashable
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
        for u, v in self.halfface_halfedges(hfkey):
            nbr_hfkey = self.halfface_adjacent_halfface(hfkey, (u, v))
            if nbr_hfkey:
                nbrs.append(nbr_hfkey)
        return nbrs

    def halfface_neighborhood_over_edges(self, hfkey, ring=1):
        """Return the halfface neighborhood of a halfface across their edges.

        Parameters
        ----------
        key : hashable
            The identifier of the halfface.

        Returns
        -------
        list
            The list of neighboring halffaces.

        Notes
        -----
        Neighboring halffaces on the same cell are not included.

        """
        nbrs = set(self.halfface_neighbors_over_edges(hfkey))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr_hfkey in nbrs:
                temp += self.halfface_neighbors_over_edges(nbr_hfkey)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([hfkey]))

    def is_halfface_on_boundary(self, hfkey):
        """Verify that a halfface is on the boundary.

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
        return self.plane[w][v][u] is None

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
        hfkeys = set()
        for u in self.cell[ckey]:
            hfkeys.update(self.cell[ckey][u].values())
        return list(hfkeys)

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

        Notes
        -----
        All of the returned vertices should be part of the cell.

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

        Notes
        -----
        All of the returned halffaces should be part of the cell.

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

    def cell_neighbors_over_vertices(self, ckey):
        """Return the cell neighbors of a cell across its vertices.

        Parameters
        ----------
        ckey : hashable
            Identifier of the cell.

        Returns
        -------
        list
            The identifiers of the neighboring cells.

        """
        ckeys = set()
        for vkey in self.cell_vertices(ckey):
            ckeys.update(self.vertex_cells(vkey))
        return list(ckeys)

    def cell_neighborhood_over_vertices(self, ckey, ring=1):
        """Return the cell neighborhood of a cell across its vertices.

        Parameters
        ----------
        ckey : hashable
            Identifier of the cell.
        ring : int, optional
            The number of neighborhood rings to include. Default is ``1``.

        Returns
        -------
        list
            The cells in the neighborhood.

        """
        nbrs = set(self.cell_neighbors_over_vertices(ckey))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for key in nbrs:
                temp += self.cell_neighbors_over_vertices(key)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([ckey]))

    def cell_neighbors_over_halffaces(self, ckey):
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
        for hfkey in self.cell_halffaces(ckey):
            u, v, w = self.halfface[hfkey][0:3]
            nbr = self.plane[w][v][u]
            if nbr is not None:
                ckeys.append(nbr)
        return ckeys

    def cell_neighborhood_over_halffaces(self, ckey, ring=1):
        """Return the cells in the neighborhood of a cell across its halffaces.

        Parameters
        ----------
        ckey : hashable
            Identifier of the cell.
        ring : int, optional
            The number of neighborhood rings to include. Default is ``1``.

        Returns
        -------
        list
            The identifiers of the neighboring cells.

        """
        nbrs = set(self.cell_neighbors_over_halffaces(ckey))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for key in nbrs:
                temp += self.cell_neighbors_over_halffaces(key)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([ckey]))

    def cell_adjacency_halffaces(self, ckey_1, ckey_2):
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
            The identifier of the halfface belonging to cell 1.
        hfkey_2
            The identifier of the halfface belonging to cell 2.

        """
        for hfkey in self.cell_halffaces(ckey_1):
            u, v, w = self.halfface[hfkey][0:3]
            nbr = self.plane[w][v][u]
            if nbr == ckey_2:
                return hfkey, self.halfface_opposite_halfface(hfkey)
        return

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
        for hfkey in self.halfface:
            if self.is_halfface_on_boundary(hfkey):
                vertices.update(self.halfface_vertices(hfkey))
        return list(vertices)

    def halffaces_on_boundaries(self):
        """Find the halffaces on the boundary.

        Returns
        -------
        list
            The halffaces of the boundary.

        """
        halffaces = set()
        for hfkey in self.halfface:
            if self.is_halfface_on_boundary(hfkey):
                halffaces.add(hfkey)
        return list(halffaces)

    def cells_on_boundaries(self):
        """Find the cells on the boundary.

        Returns
        -------
        list
            The cells of the boundary.

        """
        cells = set()
        for hfkey in self. halffaces_on_boundaries():
            cells.add(self.halfface_cell(hfkey))
        return list(cells)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
