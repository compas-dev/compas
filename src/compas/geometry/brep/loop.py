from compas.data import Data


class BrepLoop(Data):
    """
    An interface for a Brep Loop
    """

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def is_valid(self):
        """
        Returns True if this loop is valid, False otherwise.

        Returns
        -------
        bool
        """
        return NotImplementedError

    @property
    def vertices(self):
        """
        Returns a list of the vertices comprising this loop.

        Returns
        -------
        list[:class:`compas.geometry.BrepVertex`]
        """
        raise NotImplementedError

    @property
    def edges(self):
        """
        Returns a list of the edges comprising this loop.

        Returns
        -------
        list[:class:`compas.geometry.BrepEdge`]
        """
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_edges(cls):
        raise NotImplementedError

    @classmethod
    def from_polyline(cls):
        raise NotImplementedError

    @classmethod
    def from_polygon(cls):
        raise NotImplementedError
