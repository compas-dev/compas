from compas.data import Data


class BrepLoop(Data):
    """An interface for a Brep Loop.

    Attributes
    ----------
    edges : list[:class:`compas.geometry.BrepEdge`], read-only
        Returns the list of deges associated with this loop.
    is_valid : bool, read-only
        Returns True if this loop is valid, False otherwise.
    vertices : list[:class:`compas.geometry.BrepVertex`], read-only
        Returns the list of vertices associated with this loop.
    native_loop : Any
        The underlying loop object. Type is backend-dependent.

    """

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def is_valid(self):
        return NotImplementedError

    @property
    def vertices(self):
        raise NotImplementedError

    @property
    def edges(self):
        raise NotImplementedError

    @property
    def native_loop(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_edges(cls, edges):
        """Construct a loop from a list of edges.

        Parameters
        ----------
        edges : list[:class:`compas.geometry.BrepEdge`]

        Returns
        -------
        :class:`compas.geometry.BrepLoop`

        """
        raise NotImplementedError

    @classmethod
    def from_polyline(cls, polyline):
        """Construct a loop from a polyline.

        Parameters
        ----------
        polyline : :class:`compas.geometry.Polyline`

        Returns
        -------
        :class:`compas.geometry.BrepLoop`

        """
        raise NotImplementedError

    @classmethod
    def from_polygon(cls, polygon):
        """Construct a loop from a polygon.

        Parameters
        ----------
        polygon : :class:`compas.geometry.Polygon`

        Returns
        -------
        :class:`compas.geometry.BrepLoop`

        """
        raise NotImplementedError
