from copy import deepcopy


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'VertexAttributesManagement',
    'EdgeAttributesManagement',
    'FaceAttributesManagement',
]


class VertexAttributesManagement(object):

    def update_default_vertex_attributes(self, attr_dict=None, **kwattr):
        """Update the default vertex attributes (this also affects already existing vertices).

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
        self.default_vertex_attributes.update(attr_dict)
        for key in self.vertices():
            attr = deepcopy(attr_dict)
            attr.update(self.vertex[key])
            self.vertex[key] = attr

    def set_vertex_attribute(self, key, name, value):
        """Set one attribute of one vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.

        See Also
        --------
        * :meth:`set_vertex_attributes`
        * :meth:`set_vertices_attribute`
        * :meth:`set_vertices_attributes`

        """
        self.vertex[key][name] = value

    def set_vertex_attributes(self, key, attr_dict=None, **kwattr):
        """Set multiple attributes of one vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        attr_dict : dict (None)
            A dictionary of attributes as name-value pairs.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Note
        ----
        Named arguments overwrite correpsonding name-value pairs in the attribute dictionary,
        if they exist.

        See Also
        --------
        * :meth:`set_vertex_attribute`
        * :meth:`set_vertices_attribute`
        * :meth:`set_vertices_attributes`

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.vertex[key].update(attr_dict)

    def set_vertices_attribute(self, name, value, keys=None):
        """Set one attribute of multiple vertices.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.
        keys : iterable (None)
            A list of vertex identifiers.
            Defaults to all vertices.

        See Also
        --------
        * :meth:`set_vertex_attribute`
        * :meth:`set_vertex_attributes`
        * :meth:`set_vertices_attributes`

        """
        keys = keys or self.vertices()
        for key in keys:
            self.vertex[key][name] = value

    def set_vertices_attributes(self, keys=None, attr_dict=None, **kwattr):
        """Set multiple attributes of multiple vertices.

        Parameters
        ----------
        keys : iterable (None)
            A list of vertex identifiers.
            Defaults to all vertices.
        attr_dict : dict (None)
            A dictionary of attributes as name-value pairs.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Note
        ----
        Named arguments overwrite correpsonding name-value pairs in the attribute dictionary,
        if they exist.

        See Also
        --------
        * :meth:`set_vertex_attribute`
        * :meth:`set_vertex_attributes`
        * :meth:`set_vertices_attribute`

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        if not keys:
            for key, attr in self.vertices(True):
                attr.update(attr_dict)
        else:
            for key in keys:
                self.vertex[key].update(attr_dict)

    def get_vertex_attribute(self, key, name, value=None):
        """Get the value of a named attribute of one vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        name : str
            The name of the attribute.
        value : object (None)
            The default value.

        Returns
        -------
        value
            The value of the attribute,
            or the default value if the attribute does not exist.

        See Also
        --------
        * :meth:`get_vertex_attributes`
        * :meth:`get_vertices_attribute`
        * :meth:`get_vertices_attributes`

        """
        return self.vertex[key].get(name, value)

    def get_vertex_attributes(self, key, names, values=None):
        """Get the value of a named attribute of one vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        names : list
            A list of attribute names.
        values : list (None)
            A list of default values.
            Defaults to a list of ``None`` s.

        Returns
        -------
        values : list
            A list of values.
            Every attribute that does not exist is replaced by the corresponding
            default value.

        See Also
        --------
        * :meth:`get_vertex_attribute`
        * :meth:`get_vertices_attribute`
        * :meth:`get_vertices_attributes`

        """
        if not values:
            values = [None] * len(names)
        return [self.vertex[key].get(name, value) for name, value in zip(names, values)]

    def get_vertices_attribute(self, name, value=None, keys=None):
        """Get the value of a named attribute of multiple vertices.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object (None)
            The default value.
        keys : list (None)
            A list of identifiers.
            Defaults to all vertices.

        Returns
        -------
        values : list
            A list of values of the named attribute of the specified vertices.

        See Also
        --------
        * :meth:`get_vertex_attribute`
        * :meth:`get_vertex_attributes`
        * :meth:`get_vertices_attributes`

        """
        if not keys:
            return [attr.get(name, value) for key, attr in self.vertices(True)]
        return [self.vertex[key].get(name, value) for key in keys]

    def get_vertices_attributes(self, names, values=None, keys=None):
        """Get the values of multiple named attribute of multiple vertices.

        Parameters
        ----------
        names : list
            The names of the attributes.
        values : list (None)
            A list of default values.
            Defaults to a list of ``None`` s.
        keys : list (None)
            A list of vertex identifiers.
            Defaults to all vertices.

        Returns
        -------
        values: list of list
            The values of the attributes of the specified vertices.
            If an attribute does not exist for a specific vertex, it is replaced
            by the default value.

        See Also
        --------
        * :meth:`get_vertex_attribute`
        * :meth:`get_vertex_attributes`
        * :meth:`get_vertices_attribute`

        """
        if not values:
            values = [None] * len(names)
        temp = list(zip(names, values))
        if not keys:
            return [[attr.get(name, value) for name, value in temp] for key, attr in self.vertices(True)]
        return [[self.vertex[key].get(name, value) for name, value in temp] for key in keys]


class EdgeAttributesManagement(object):

    def update_default_edge_attributes(self, attr_dict=None, **kwattr):
        """Update the default edge attributes (this also affects already existing edges).

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
        self.default_edge_attributes.update(attr_dict)
        for u, v in self.edges():
            attr = deepcopy(attr_dict)
            attr.update(self.edge[u][v])
            self.edge[u][v] = attr

    def set_edge_attribute(self, key, name, value, directed=True):
        """Set one attribute of one edge.

        Parameters
        ----------
        key : tuple, list
            The identifier of the edge, in the form of a pair of vertex identifiers.
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.

        See Also
        --------
        * :meth:`set_edge_attributes`
        * :meth:`set_edges_attribute`
        * :meth:`set_edges_attributes`

        """
        u, v = key
        if directed:
            self.edge[u][v][name] = value
        else:
            if u in self.edge and v in self.edge[u]:
                self.edge[u][v][name] = value
            elif v in self.edge and u in self.edge[v]:
                self.edge[v][u][name] = value
            else:
                if v in self.halfedge[u] or u in self.halfedge[v]:
                    self.edge[u] = {}
                    self.edge[u][v] = self.default_edge_attributes.copy()
                    self.edge[u][v][name] = value

    def set_edge_attributes(self, key, attr_dict=None, **kwattr):
        """Set multiple attributes of one edge.

        Parameters
        ----------
        key : tuple, list
            The identifier of the edge, in the form of a pair of vertex identifiers.
        attr_dict : dict (None)
            A dictionary of attributes as name-value pairs.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Note
        ----
        Named arguments overwrite correpsonding name-value pairs in the attribute dictionary,
        if they exist.

        See Also
        --------
        * :meth:`set_edge_attribute`
        * :meth:`set_edges_attribute`
        * :meth:`set_edges_attributes`

        """
        u, v = key
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.edge[u][v].update(attr_dict)

    def set_edges_attribute(self, name, value, keys=None):
        """Set one attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.
        keys : iterable (None)
            A list of edge identifiers.
            Each edge identifier is a pair of vertex identifiers.
            Defaults to all edges.

        See Also
        --------
        * :meth:`set_edge_attribute`
        * :meth:`set_edge_attributes`
        * :meth:`set_edges_attributes`

        """
        if not keys:
            for u, v, attr in self.edges(True):
                attr[name] = value
        else:
            for u, v in keys:
                self.edge[u][v][name] = value

    def set_edges_attributes(self, keys=None, attr_dict=None, **kwattr):
        """Set multiple attributes of multiple edges.

        Parameters
        ----------
        keys : iterable (None)
            A list of edge identifiers.
            Each edge identifier is a pair of vertex identifiers.
            Defaults to all edges.
        attr_dict : dict (None)
            A dictionary of attributes as name-value pairs.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Note
        ----
        Named arguments overwrite correpsonding name-value pairs in the attribute dictionary,
        if they exist.

        See Also
        --------
        * :meth:`set_edge_attribute`
        * :meth:`set_edge_attributes`
        * :meth:`set_edges_attribute`

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        if not keys:
            for u, v, attr in self.edges(True):
                attr.update(attr_dict)
        else:
            for u, v in keys:
                self.edge[u][v].update(attr_dict)

    def get_edge_attribute(self, key, name, value=None):
        """Get the value of a named attribute of one edge.

        Parameters
        ----------
        key : tuple, list
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

        See Also
        --------
        * :meth:`get_edge_attributes`
        * :meth:`get_edges_attribute`
        * :meth:`get_edges_attributes`

        """
        u, v = key
        if u in self.edge[v]:
            return self.edge[v][u].get(name, value)
        return self.edge[u][v].get(name, value)

    def get_edge_attributes(self, key, names, values=None):
        """Get the value of a named attribute of one edge.

        Parameters
        ----------
        key : tuple, list
            The identifier of the edge, in the form of a pair of vertex identifiers.
        names : list
            A list of attribute names.
        values : list (None)
            A list of default values.
            Defaults to a list of ``None`` s.

        Returns
        -------
        values : list
            A list of values.
            Every attribute that does not exist is replaced by the corresponding
            default value.

        See Also
        --------
        * :meth:`get_edge_attribute`
        * :meth:`get_edges_attribute`
        * :meth:`get_edges_attributes`

        """
        u, v = key
        if not names:
            values = [None] * len(names)
        if v in self.edge[u]:
            return [self.edge[u][v].get(name, value) for name, value in zip(names, values)]
        return [self.edge[v][u].get(name, value) for name, value in zip(names, values)]

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

        See Also
        --------
        * :meth:`get_edge_attribute`
        * :meth:`get_edge_attributes`
        * :meth:`get_edges_attributes`

        """
        if not keys:
            return [attr.get(name, value) for u, v, attr in self.edges(True)]
        return [self.edge[u][v].get(name, value) for u, v in keys]

    def get_edges_attributes(self, names, values=None, keys=None):
        """Get the values of multiple named attribute of multiple edges.

        Parameters
        ----------
        names : list
            The names of the attributes.
        values : list (None)
            A list of default values.
            Defaults to a list of ``None`` s.
        keys : iterable (None)
            A list of edge identifiers.
            Each edge identifier is a pair of vertex identifiers.
            Defaults to all edges.

        Returns
        -------
        values: list of list
            The values of the attributes of the specified edges.
            If an attribute does not exist for a specific edge, it is replaced
            by the default value.

        See Also
        --------
        * :meth:`get_edge_attribute`
        * :meth:`get_edge_attributes`
        * :meth:`get_edges_attribute`

        """
        if not values:
            values = [None] * len(names)
        temp = list(zip(names, values))
        if not keys:
            return [[attr.get(name, value) for name, value in temp] for u, v, attr in self.edges(True)]
        return [[self.edge[u][v].get(name, value) for name, value in temp] for u, v in keys]


class FaceAttributesManagement(object):

    def update_default_face_attributes(self, attr_dict=None, **kwattr):
        """Update the default face attributes (this also affects already existing faces).

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
        for fkey in self.faces():
            attr = deepcopy(attr_dict)
            attr.update(self.facedata[fkey])
            self.facedata[fkey] = attr

    def set_face_attribute(self, fkey, name, value):
        """Set one attribute of one face.

        Parameters
        ----------
        key : hashable
            The identifier of the face.
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.

        See Also
        --------
        * :meth:`set_face_attributes`
        * :meth:`set_faces_attribute`
        * :meth:`set_faces_attributes`

        """
        if fkey not in self.facedata:
            self.facedata[fkey] = self.default_face_attributes.copy()
        self.facedata[fkey][name] = value

    def set_face_attributes(self, fkey, attr_dict=None, **kwattr):
        """Set multiple attributes of one face.

        Parameters
        ----------
        key : hashable
            The identifier of the face.
        attr_dict : dict (None)
            A dictionary of attributes as name-value pairs.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Note
        ----
        Named arguments overwrite correpsonding name-value pairs in the attribute dictionary,
        if they exist.

        See Also
        --------
        * :meth:`set_face_attribute`
        * :meth:`set_faces_attribute`
        * :meth:`set_faces_attributes`

        """
        attr_dict = attr_dict or {}
        attr_dict.update(kwattr)
        if fkey not in self.facedata:
            self.facedata[fkey] = self.default_face_attributes.copy()
        self.facedata[fkey].update(attr_dict)

    def set_faces_attribute(self, name, value, fkeys=None):
        """Set one attribute of multiple faces.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.
        keys : iterable (None)
            A list of face identifiers.
            Defaults to all faces.

        See Also
        --------
        * :meth:`set_face_attribute`
        * :meth:`set_face_attributes`
        * :meth:`set_faces_attributes`

        """
        if not fkeys:
            for fkey, attr in self.faces_iter(True):
                attr[name] = value
        else:
            for fkey in fkeys:
                if fkey not in self.facedata:
                    self.facedata[fkey] = self.default_face_attributes.copy()
                self.facedata[fkey][name] = value

    def set_faces_attributes(self, fkeys=None, attr_dict=None, **kwattr):
        """Set multiple attributes of multiple faces.

        Parameters
        ----------
        keys : iterable (None)
            A list of face identifiers.
            Defaults to all faces.
        attr_dict : dict (None)
            A dictionary of attributes as name-value pairs.
        kwattr : dict
            A dictionary compiled of remaining named arguments.
            Defaults to an empty dict.

        Note
        ----
        Named arguments overwrite correpsonding name-value pairs in the attribute dictionary,
        if they exist.

        See Also
        --------
        * :meth:`set_face_attribute`
        * :meth:`set_face_attributes`
        * :meth:`set_faces_attribute`

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        if not fkeys:
            for fkey, attr in self.faces(True):
                attr.update(attr_dict)
        else:
            for fkey in fkeys:
                if fkey not in self.facedata:
                    self.facedata[fkey] = self.default_face_attributes.copy()
                self.facedata[fkey].update(attr_dict)

    def get_face_attribute(self, fkey, name, value=None):
        """Get the value of a named attribute of one face.

        Parameters
        ----------
        key : hashable
            The identifier of the face.
        name : str
            The name of the attribute.
        value : object (None)
            The default value.

        Returns
        -------
        value
            The value of the attribute,
            or the default value if the attribute does not exist.

        See Also
        --------
        * :meth:`get_face_attributes`
        * :meth:`get_faces_attribute`
        * :meth:`get_faces_attributes`

        """
        if not self.facedata:
            return value
        if fkey not in self.facedata:
            return value
        return self.facedata[fkey].get(name, value)

    def get_face_attributes(self, fkey, names, values=None):
        """Get the value of a named attribute of one face.

        Parameters
        ----------
        key : hashable
            The identifier of the face.
        names : list
            A list of attribute names.
        values : list (None)
            A list of default values.
            Defaults to a list of ``None`` s.

        Returns
        -------
        values : list
            A list of values.
            Every attribute that does not exist is replaced by the corresponding
            default value.

        See Also
        --------
        * :meth:`get_face_attribute`
        * :meth:`get_faces_attribute`
        * :meth:`get_faces_attributes`

        """
        if not values:
            values = [None] * len(names)
        if not self.facedata:
            return values
        if fkey not in self.facedata:
            return values
        return [self.facedata[fkey].get(name, value) for name, value in zip(names, values)]

    def get_faces_attribute(self, name, value=None, fkeys=None):
        """Get the value of a named attribute of multiple faces.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object (None)
            The default value.
        keys : list (None)
            A list of identifiers.
            Defaults to all faces.

        Returns
        -------
        values : list
            A list of values of the named attribute of the specified faces.

        See Also
        --------
        * :meth:`get_face_attribute`
        * :meth:`get_face_attributes`
        * :meth:`get_faces_attributes`

        """
        if not fkeys:
            if not self.facedata:
                return [value for fkey in self.face]
            return [self.get_face_attribute(fkey, name, value) for fkey in self.face]
        if not self.facedata:
            return [value for fkey in fkeys]
        return [self.get_face_attribute(fkey, name, value) for fkey in fkeys]

    def get_faces_attributes(self, names, values=None, fkeys=None):
        """Get the values of multiple named attribute of multiple faces.

        Parameters
        ----------
        names : list
            The names of the attributes.
        values : list (None)
            A list of default values.
            Defaults to a list of ``None`` s.
        keys : list (None)
            A list of face identifiers.
            Defaults to all faces.

        Returns
        -------
        values: list of list
            The values of the attributes of the specified faces.
            If an attribute does not exist for a specific face, it is replaced
            by the default value.

        See Also
        --------
        * :meth:`get_face_attribute`
        * :meth:`get_face_attributes`
        * :meth:`get_faces_attribute`

        """
        if not values:
            values = [None] * len(names)
        temp = list(zip(names, values))
        if not fkeys:
            if not self.facedata:
                return [[value for name, value in temp] for fkey in self.face]
            return [[self.get_face_attribute(fkey, name, value) for name, value in temp] for fkey in self.face]
        if not self.facedata:
            return [[value for name, value in temp] for fkey in fkeys]
        return [[self.get_face_attribute(fkey, name, value) for name, value in temp] for fkey in fkeys]


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":
    pass
