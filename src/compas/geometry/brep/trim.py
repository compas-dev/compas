from compas.data import Data


class BrepTrimIsoStatus(object):
    """An enumeration of isoparametric curve direction on the surface."""

    NONE = 0
    X = 1
    Y = 2
    WEST = 3
    SOUTH = 4
    EAST = 5
    NORTH = 6


class BrepTrim(Data):
    """An interface for a Brep Trim

    Attributes
    ----------
    curve : :class:`compas.geometry.NurbsCurve`, read_only
        Returns the geometry for this trim as a 2d curve.
    iso_status : literal(NONE|X|Y|WEST|SOUTH|EAST|NORTH)
        The isoparametric curve direction on the surface.
    is_reversed : bool
        True if this trim is reversed from its associated edge curve and False otherwise.
    native_trim : Any
        The underlying trim object. Type is backend-dependent.
    start_vertex : Any, read-only
        The start vertex of this trim.
    end_vertex : Any, read-only
        The end vertex of this trim.
    vertices : list[Any], read-only

    """

    @property
    def curve(self):
        raise NotImplementedError

    @property
    def iso_status(self):
        raise NotImplementedError

    @property
    def is_reversed(self):
        raise NotImplementedError

    @property
    def native_trim(self):
        raise NotImplementedError

    @property
    def start_vertex(self):
        raise NotImplementedError

    @property
    def end_vertex(self):
        raise NotImplementedError

    @property
    def vertices(self):
        raise NotImplementedError
