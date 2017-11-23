__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'MagicMethods'
]


class MagicMethods(object):

    def __contains__(self, key):
        """Verify if the data structure contains a specific vertex.

        Parameters
        ----------
        key : hashable
            The identifier of the vertex.

        Returns
        -------
        bool
            ``True`` if the data structure contains the vertex.
            ``False`` otherwise.

        """
        return key in self.vertex

    def __len__(self):
        """Defines the length of the data structure as the number of vertices.

        Returns
        -------
        int
            The *length* of the data structure.

        """
        return len(self.vertex)

    def __iter__(self):
        """Defines iteration over the contents of the data structure as iteration over the vertex keys.

        Returns
        -------
        iterable
            Vertex iterator.

        """
        return iter(self.vertex)

    def __getitem__(self, key):
        """Provides access to the data of the vertices

        """
        return self.vertex[key]


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":
    pass
