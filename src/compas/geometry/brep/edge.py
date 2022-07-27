from compas.data import Data


class BrepEdge(Data):
    """
    An interface for a Brep Edge
    """

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def is_line(self):
        """
        Returns True if this edge is a line, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_circle(self):
        """
        Returns True if this edge is a circle, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_ellipse(self):
        """
        Returns True if this edge is an ellipse, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_hyperbola(self):
        """
        Returns True if this edge is a hyperbola, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_parabola(self):
        """
        Returns True if this edge is a parabola, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_bezier(self):
        """
        Returns True if this edge is a bezier, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_bspline(self):
        """
        Returns True if this edge is a bspline, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_other(self):
        """
        Returns True if this edge is of another shape, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_valid(self):
        """
        Returns True if this edge is valid, False otherwise.
        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def vertices(self):
        """
        Gets the list of vertices which compound this edge

        Returns
        -------
        A list of vertices included in this edge
        List[compas.geometry.RhinoVertex]
        """
        raise NotImplementedError

    @property
    def first_vertex(self):
        """
        Returns the first vertex of this edge

        Returns
        -------
        :class:`compas.geometry.BrepVertex`
            First vertex of this edge
        """
        raise NotImplementedError

    @property
    def last_vertex(self):
        """
        Returns the first vertex of this edge

        Returns
        -------
        :class:`compas.geometry.BrepVertex`
            First vertex of this edge
        """
        raise NotImplementedError

    @property
    def curve(self):
        """

        Returns
        -------
        """
        raise NotImplementedError

    @property
    def nurbscurve(self):
        """

        Returns
        -------
        """
        raise NotImplementedError

    @property
    def length(self):
        """

        Returns
        -------
        """
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_vertices(cls):
        raise NotImplementedError

    @classmethod
    def from_points(cls):
        raise NotImplementedError

    @classmethod
    def from_line(cls):
        raise NotImplementedError

    @classmethod
    def from_circle(cls):
        raise NotImplementedError

    @classmethod
    def from_ellipse(cls):
        raise NotImplementedError

    @classmethod
    def from_curve(cls):
        raise NotImplementedError

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_line(self):
        raise NotImplementedError

    def to_circle(self):
        raise NotImplementedError

    def to_ellipse(self):
        raise NotImplementedError

    def to_hyperbola(self):
        raise NotImplementedError

    def to_parabola(self):
        raise NotImplementedError

    def to_bezier(self):
        raise NotImplementedError

    def to_bspline(self):
        raise NotImplementedError

    def to_curve(self):
        raise NotImplementedError
