from compas.data import Data


class CurveType(object):
    """Enumaration of curve types."""

    LINE = 0
    CIRCLE = 1
    ELLIPSE = 2
    HYPERBOLA = 3
    PARABOLA = 4
    BEZIER = 5
    BSPLINE = 6
    OTHER = 7
    CURVE2D = 8


class BrepEdge(Data):
    """An interface for a Brep Edge

    Attributes
    ----------
    curve : :class:`compas.geometry.Curve`
        Returns the curve geometry of this edge.
    first_vertex : :class:`compas.geometry.BrepVertex`
        Returns the first vertex of this edge.
    is_line : bool, read-only
        Returns True if this edge is a line, False otherwise.
    is_circle : bool, read-only
        Returns True if this edge is a circle, False otherwise.
    is_ellipse : bool, read-only
        Returns True if this edge is an ellipse, False otherwise.
    is_hyperbola : bool, read-only
        Returns True if this edge is a hyperbola, False otherwise.
    is_parabola : bool, read-only
        Returns True if this edge is a parabola, False otherwise.
    is_bezier : bool, read-only
        Returns True if this edge is a bezier, False otherwise.
    is_bspline : bool, read-only
        Returns True if this edge is a bspline, False otherwise.
    is_other : bool, read-only
        Returns True if this edge is of another shape, False otherwise.
    orientation : literal(:class:`~compas.geometry.BrepOrientation`), read-only
        Returns the orientation of this edge. One of: FORWARD, REVERSED, INTERNAL, EXTERNAL.
    type : literal(:class:`~compas.geometry.CurveType`), read-only
        Returns the type of this edge. One of: LINE, CIRCLE, ELLIPSE, HYPERBOLA, PARABOLA, BEZIER, BSPLINE, OTHER.
    vertices : list[:class:`compas.geometry.BrepVertex`], read-only
        Gets the list of vertices which compound this edge.
    last_vertex : :class:`compas.geometry.BrepVertex`
        Returns the last vertex of this edge.
    length : float, read-only
        Returns the length of this edge.
    native_edge : Any
        The underlying edge object. Type is backend-dependent.

    """

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def is_line(self):
        raise NotImplementedError

    @property
    def is_circle(self):
        raise NotImplementedError

    @property
    def is_ellipse(self):
        raise NotImplementedError

    @property
    def is_hyperbola(self):
        raise NotImplementedError

    @property
    def is_parabola(self):
        raise NotImplementedError

    @property
    def is_bezier(self):
        raise NotImplementedError

    @property
    def is_bspline(self):
        raise NotImplementedError

    @property
    def is_other(self):
        raise NotImplementedError

    @property
    def is_valid(self):
        raise NotImplementedError

    @property
    def vertices(self):
        raise NotImplementedError

    @property
    def first_vertex(self):
        raise NotImplementedError

    @property
    def last_vertex(self):
        raise NotImplementedError

    @property
    def length(self):
        raise NotImplementedError

    @property
    def curve(self):
        raise NotImplementedError

    @property
    def orientation(self):
        raise NotImplementedError

    @property
    def type(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_vertices(cls, vertices):
        """Construct an edge from two vertices.

        Parameters
        ----------
        vertices : list[:class:`compas.geometry.BrepVertex`]

        Returns
        -------
        :class:`compas.geometry.BrepVertex`

        """
        raise NotImplementedError

    @classmethod
    def from_points(cls, points):
        """Construct an edge from two points.

        Parameters
        ----------
        points : list[:class:`compas.geometry.Point`]

        Returns
        -------
        :class:`compas.geometry.BrepVertex`

        """
        raise NotImplementedError

    @classmethod
    def from_line(cls, line):
        """Construct an edge from a line.

        Parameters
        ----------
        line : :class:`compas.geometry.Line`

        Returns
        -------
        :class:`compas.geometry.BrepEdge`

        """
        raise NotImplementedError

    @classmethod
    def from_circle(cls, circle):
        """Construct an edge from a circle.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle`

        Returns
        -------
        :class:`compas.geometry.BrepEdge`

        """
        raise NotImplementedError

    @classmethod
    def from_ellipse(cls, ellipse):
        """Construct an edge from an ellipse.

        Parameters
        ----------
        ellipse : :class:`compas.geometry.Ellipse`

        Returns
        -------
        :class:`compas.geometry.BrepEdge`

        """
        raise NotImplementedError

    @classmethod
    def from_curve(cls, curve):
        """Construct an edge from a curve.

        Parameters
        ----------
        curve : :class:`compas.geometry.Curve`

        Returns
        -------
        :class:`compas.geometry.BrepEdge`

        """
        raise NotImplementedError

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_line(self):
        """Get a line from this edge's geometry.

        Returns
        -------
        :class:`compas.geometry.Line`

        """
        raise NotImplementedError

    def to_circle(self):
        """Get a circle from this edge's geometry.

        Returns
        -------
        :class:`compas.geometry.Circle`

        """
        raise NotImplementedError

    def to_ellipse(self):
        """Get an ellipse from this edge's geometry.

        Returns
        -------
        :class:`compas.geometry.Ellipse`

        """
        raise NotImplementedError

    def to_hyperbola(self):
        """Get a hyperbola from this edge's geometry.

        Returns
        -------
        TODO: type?

        """
        raise NotImplementedError

    def to_parabola(self):
        """Get a parabola from this edge's geometry.

        Returns
        -------
        TODO: type?

        """
        raise NotImplementedError

    def to_bezier(self):
        """Get a bezier from this edge's geometry.

        Returns
        -------
        :class:`compas.geometry.Bezier`

        """
        raise NotImplementedError

    def to_bspline(self):
        """Get a bspline from this edge's geometry.

        Returns
        -------
        TODO: type?

        """
        raise NotImplementedError

    def to_curve(self):
        """Get a curve from this edge's geometry.

        Returns
        -------
        :class:`compas.geometry.Curve`

        """
        raise NotImplementedError
