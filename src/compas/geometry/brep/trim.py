from compas.data import Data


class TrimIsoStatus(object):
    """An enumeration of isoparametric curve direction on the surface."""
    NONE = 0 
    X = 1 
    Y = 2
    West = 3
    South = 4
    East = 5
    North = 6


class BrepTrim(Data):
    """An interface for a Brep Trim

    Attributes
    ----------
    curve : :class:`~compas.geometry.NurbsCurve`, read_only
        Returns the geometry for this trim as a 2d curve.
    iso_status : literal(NONE|X|Y|West|South|East|North)
        The isoparametric curve direction on the surface.
    is_reversed : bool
        True if this trim is reversed from its associated edge curve and False otherwise.

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

