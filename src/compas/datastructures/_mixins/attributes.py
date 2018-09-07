from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from copy import deepcopy


__all__ = [
    'VertexAttributesManagement',
    'EdgeAttributesManagement',
    'FaceAttributesManagement',
]


class VertexAttributesManagement(object):
    """Mix-in methods for working getting, setting, and updating vertex attributes."""

    def update_default_vertex_attributes(self, attr_dict=None, **kwattr):
        """Update the default vertex attributes (this also affects already existing vertices).

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

    def set_vertex_attributes(self, key, names, values):
        """Set multiple attributes of one vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        names : list of str
            A list of attribute names.
        values : list
            A list of attribute values.

        See Also
        --------
        * :meth:`set_vertex_attribute`
        * :meth:`set_vertices_attribute`
        * :meth:`set_vertices_attributes`

        """
        for name, value in zip(names, values):
            self.set_vertex_attribute(key, name, value)

    def set_vertices_attribute(self, name, value, keys=None):
        """Set one attribute of multiple vertices.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.
        keys : list of hashable, optional
            Defaults to all vertices.

        See Also
        --------
        * :meth:`set_vertex_attribute`
        * :meth:`set_vertex_attributes`
        * :meth:`set_vertices_attributes`

        """
        if not keys:
            keys = self.vertices()
        for key in keys:
            self.set_vertex_attribute(key, name, value)

    def set_vertices_attributes(self, names, values, keys=None):
        """Set multiple attributes of multiple vertices.

        Parameters
        ----------
        names : list of str
            A list of attribute names.
        values : list
            A list of attribute values.
        keys : list of hashable, optional
            A list of vertex identifiers.
            Defaults to all vertices.

        See Also
        --------
        * :meth:`set_vertex_attribute`
        * :meth:`set_vertex_attributes`
        * :meth:`set_vertices_attribute`

        """
        for name, value in zip(names, values):
            self.set_vertices_attribute(name, value, keys=keys)

    def get_vertex_attribute(self, key, name, value=None):
        """Get the value of a named attribute of one vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.
        name : str
            The name of the attribute.
        value : object, optional
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
        values : list, optional
            A list of default values.
            Defaults to a list of ``None``.

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
        return [self.get_vertex_attribute(key, name, value) for name, value in zip(names, values)]

    def get_vertices_attribute(self, name, value=None, keys=None):
        """Get the value of a named attribute of multiple vertices.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The default value.
            Default is ``None``.
        keys : list, optional
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
            keys = self.vertices()
        return [self.get_vertex_attribute(key, name, value) for key in keys]

    def get_vertices_attributes(self, names, values=None, keys=None):
        """Get the values of multiple named attribute of multiple vertices.

        Parameters
        ----------
        names : list
            The names of the attributes.
        values : list, optional
            A list of default values.
            Defaults to a list of ``None``.
        keys : list, optional
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
            keys = self.vertices()
        return [[self.get_vertex_attribute(key, name, value) for name, value in temp] for key in keys]


class EdgeAttributesManagement(object):
    """Mix-in methods for setting, getting, and updating edge attributes."""

    def update_default_edge_attributes(self, attr_dict=None, **kwattr):
        """Update the default edge attributes (this also affects already existing edges).

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
        for u, v in self.edges():
            attr = deepcopy(attr_dict)
            attr.update(self.edge[u][v])
            self.edge[u][v] = attr

    def set_edge_attribute(self, key, name, value):
        """Set one attribute of one edge.

        Parameters
        ----------
        key : tuple, list
            The identifier of the edge, in the form of a pair of vertex identifiers.
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.

        Raises
        ------
        Exception
            If the edge does not exist in the data structure.

        See Also
        --------
        * :meth:`set_edge_attributes`
        * :meth:`set_edges_attribute`
        * :meth:`set_edges_attributes`

        """
        u, v = key
        if u in self.edge and v in self.edge[u]:
            self.edge[u][v][name] = value
        elif v in self.edge and u in self.edge[v]:
            self.edge[v][u][name] = value
        else:
            raise Exception('The edge does not exist: {}-{}'.format(u, v))

    def set_edge_attributes(self, key, names, values):
        """Set multiple attributes of one edge.

        Parameters
        ----------
        key : tuple, list
            The identifier of the edge, in the form of a pair of vertex identifiers.
        names : list of str
            The names of the attributes to update.
        values : list of object
            The new values of the attributes.

        See Also
        --------
        * :meth:`set_edge_attribute`
        * :meth:`set_edges_attribute`
        * :meth:`set_edges_attributes`

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
            Defaults to ``None``, in which case all edges will be modified.

        See Also
        --------
        * :meth:`set_edge_attribute`
        * :meth:`set_edge_attributes`
        * :meth:`set_edges_attributes`

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
            The new values of the attributes.
        keys : list of hashable, optional
            A list of edge identifiers.
            Each edge identifier is a pair of vertex identifiers.
            Defaults to ``None``, in which case all edges will be modified.

        See Also
        --------
        * :meth:`set_edge_attribute`
        * :meth:`set_edge_attributes`
        * :meth:`set_edges_attribute`

        """
        for name, value in zip(names, values):
            self.set_edges_attribute(name, value, keys=keys)

    def get_edge_attribute(self, key, name, value=None):
        """Get the value of a named attribute of one edge.

        Parameters
        ----------
        key : tuple, list
            The identifier of the edge, in the form of a pair of vertex identifiers.
        name : str
            The name of the attribute.
        value : object, optional
            The default value.
            Default is ``None``.

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
        key : tuple of hashable
            The identifier of the edge, in the form of a pair of vertex identifiers.
        names : list
            A list of attribute names.
        values : list of object, optional
            A list of default values.
            Defaults to a list of ``None``.

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
        if not values:
            values = [None] * len(names)
        return [self.get_edge_attribute(key, name, value) for name, value in zip(names, values)]

    def get_edges_attribute(self, name, value=None, keys=None):
        """Get the value of a named attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The default value.
            Default is ``None``.
        keys : list of tuple of hashable, optional
            A list of edge identifiers.
            Each edge identifier is a pair of vertex identifiers.
            Defaults to ``None``, in which case the value of the specified
            attribute of all edges is returned.

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
            keys = self.edges()
        return [self.get_edge_attribute(key, name, value) for key in keys]

    def get_edges_attributes(self, names, values=None, keys=None):
        """Get the values of multiple named attribute of multiple edges.

        Parameters
        ----------
        names : list
            The names of the attributes.
        values : list of object, optional
            A list of default values.
            Defaults to a list of ``None``.
        keys : list of tuple of hashable, optional
            A list of edge identifiers.
            Each edge identifier is a pair of vertex identifiers.
            Defaults to ``None``, in which case the values of the specified attributes
            of all edges are returned.

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
            keys = self.edges()
        return [[self.get_edge_attribute(key, name, value) for name, value in temp] for key in keys]


class FaceAttributesManagement(object):
    """Mix-in methods for setting, getting, and updating face attributes."""

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

    def set_face_attribute(self, key, name, value):
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
        if key not in self.facedata:
            self.facedata[key] = self.default_face_attributes.copy()
        self.facedata[key][name] = value

    def set_face_attributes(self, key, names, values):
        """Set multiple attributes of one face.

        Parameters
        ----------
        key : hashable
            The identifier of the face.
        names : list of str
            The names of the attributes.
        values : list of object
            The new values of the attributes.

        See Also
        --------
        * :meth:`set_face_attribute`
        * :meth:`set_faces_attribute`
        * :meth:`set_faces_attributes`

        """
        for name, value in zip(names, values):
            self.set_face_attribute(key, name, value)

    def set_faces_attribute(self, keys, name, value):
        """Set one attribute of multiple faces.

        Parameters
        ----------
        keys : list of hashable
            A list of face identifiers.
        name : str
            The name of the attribute.
        value : object
            The value of the attribute.

        See Also
        --------
        * :meth:`set_face_attribute`
        * :meth:`set_face_attributes`
        * :meth:`set_faces_attributes`

        """
        for key in keys:
            self.set_face_attribute(key, name, value)

    def set_faces_attributes(self, keys, names, values):
        """Set multiple attributes of multiple faces.

        Parameters
        ----------
        keys : list of hashable
            A list of face identifiers.
        names : list of str
            A list of attribute names,
        values : list of object
            The new values of the attributes.

        See Also
        --------
        * :meth:`set_face_attribute`
        * :meth:`set_face_attributes`
        * :meth:`set_faces_attribute`

        """
        for name, value in zip(names, values):
            self.set_faces_attribute(keys, name, value)

    def get_face_attribute(self, key, name, value=None):
        """Get the value of a named attribute of one face.

        Parameters
        ----------
        key : hashable
            The identifier of the face.
        name : str
            The name of the attribute.
        value : object, optional
            The default value.
            Default is ``None``.

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
        if key not in self.facedata:
            return value
        return self.facedata[key].get(name, value)

    def get_face_attributes(self, key, names, values=None):
        """Get the value of a named attribute of one face.

        Parameters
        ----------
        key : hashable
            The identifier of the face.
        names : list of str
            A list of attribute names.
        values : list of object, optional
            A list of default values.
            Defaults to a list of ``None``.

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
        return [self.get_face_attribute(key, name, value) for name, value in zip(names, values)]

    def get_faces_attribute(self, keys, name, value=None):
        """Get the value of a named attribute of multiple faces.

        Parameters
        ----------
        keys : list of hashable
            A list of identifiers.
        name : str
            The name of the attribute.
        value : object, optional
            The default value.
            Defaults to ``None``.

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
        return [self.get_face_attribute(key, name, value) for key in keys]

    def get_faces_attributes(self, keys, names, values=None):
        """Get the values of multiple named attribute of multiple faces.

        Parameters
        ----------
        keys : list of hashable
            A list of identifiers.
        names : list
            The names of the attributes.
        values : list of object, optional
            A list of default values.
            Defaults to a list of ``None``.

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
        return [[self.get_face_attribute(fkey, name, value) for name, value in temp] for fkey in fkeys]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
