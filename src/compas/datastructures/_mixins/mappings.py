from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import geometric_key


__all__ = [
    'VertexMappings',
    'EdgeMappings',
    'FaceMappings',
]


class VertexMappings(object):

    __module__ = 'compas.datastructures._mixins'

    def key_index(self):
        """Returns a dictionary that maps vertex dictionary keys to the
        corresponding index in a vertex list or array.

        Returns
        -------
        dict
            A dictionary of key-index pairs.

        See Also
        --------
        * :meth:`index_key`

        """
        return {key: index for index, key in enumerate(self.vertices())}

    def index_key(self):
        """Returns a dictionary that maps the indices of a vertex list to
        keys in a vertex dictionary.

        Returns
        -------
        dict
            A dictionary of index-key pairs.

        See Also
        --------
        * :meth:`key_index`

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

        See Also
        --------
        * :meth:`gkey_key`
        * :func:`compas.utilities.geometric_key`

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

        See Also
        --------
        * :meth:`key_gkey`
        * :func:`compas.utilities.geometric_key`

        """
        gkey = geometric_key
        xyz = self.vertex_coordinates
        return {gkey(xyz(key), precision): key for key in self.vertices()}


class EdgeMappings(object):

    __module__ = 'compas.datastructures._mixins'

    def uv_index(self):
        """Returns a dictionary that maps edge keys (i.e. pairs of vertex keys)
        to the corresponding edge index in a list or array of edges.

        Returns
        -------
        dict
            A dictionary of uv-index pairs.

        See Also
        --------
        * :meth:`index_uv`

        """
        return {(u, v): index for index, (u, v) in enumerate(self.edges())}

    def index_uv(self):
        """Returns a dictionary that maps edges in a list to the corresponding
        vertex key pairs.

        Returns
        -------
        dict
            A dictionary of index-uv pairs.

        See Also
        --------
        * :meth:`uv_index`

        """
        return dict(enumerate(self.edges()))


class FaceMappings(object):

    __module__ = 'compas.datastructures._mixins'


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
