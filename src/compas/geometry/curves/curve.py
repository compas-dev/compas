from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable
from compas.geometry import Geometry
from compas.utilities import linspace


@pluggable(category="factories")
def new_curve(cls, *args, **kwargs):
    raise NotImplementedError


class Curve(Geometry):
    """Class representing a general curve object.

    Parameters
    ----------
    name : str, optional
        The name of the curve.

    Attributes
    ----------
    dimension : int, read-only
        The spatial dimension of the curve.
    domain : tuple[float, float], read-only
        The domain of the parameter space of the curve.
    start : :class:`~compas.geometry.Point`, read-only
        The start point of the curve.
    end : :class:`~compas.geometry.Point`, read-only
        The end point of the curve.
    is_closed : bool, read-only
        True if the curve is closed.
    is_periodic : bool, read-only
        True if the curve is periodic.

    """

    def __new__(cls, *args, **kwargs):
        return new_curve(cls, *args, **kwargs)

    def __init__(self, name=None):
        super(Curve, self).__init__(name=name)

    def __eq__(self, other):
        raise NotImplementedError

    def __str__(self):
        return "<Curve with parameter domain {}>".format(self.domain)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data."""
        raise NotImplementedError

    @property
    def JSONSCHEMANAME(self):
        """dict : Schema of the curve data in JSON format."""
        raise NotImplementedError

    @property
    def dtype(self):
        """str : The type of the object in the form of a '2-level' import and a class name."""
        return "compas.geometry/Curve"

    @property
    def data(self):
        """dict : Representation of the curve as a dict containing only native Python data."""
        raise NotImplementedError

    @data.setter
    def data(self, data):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data):
        """Construct a curve from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Curve`
            The constructed curve.

        """
        raise NotImplementedError

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def dimension(self):
        raise NotImplementedError

    @property
    def domain(self):
        raise NotImplementedError

    @property
    def start(self):
        raise NotImplementedError

    @property
    def end(self):
        raise NotImplementedError

    @property
    def is_closed(self):
        raise NotImplementedError

    @property
    def is_periodic(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_step(cls, filepath):
        """Load a curve from a STP file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`~compas.geometry.Curve`

        """
        raise NotImplementedError

    @classmethod
    def from_obj(cls, filepath):
        """Load a curve from an OBJ file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`~compas.geometry.Curve`

        """
        raise NotImplementedError

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath, schema="AP203"):
        """Write the curve geometry to a STP file.

        Parameters
        ----------
        filepath : str
            The path of the output file.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def to_obj(self, filepath):
        """Write the curve geometry to an OBJ file.

        Parameters
        ----------
        filepath : str
            The path of the output file.

        Returns
        -------
        None

        """
        raise NotImplementedError

    # ==============================================================================
    # Methods
    # ==============================================================================

    def reverse(self):
        """Reverse the parametrisation of the curve.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def reversed(self):
        """Reverse a copy of the curve.

        Returns
        -------
        :class:`~compas.geometry.Curve`

        """
        copy = self.copy()
        copy.reverse
        return copy

    def point_at(self, t):
        """Compute a point of the curve at a parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`~compas.geometry.Point`
            the corresponding point on the curve.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        """
        raise NotImplementedError

    def tangent_at(self, t):
        """Compute the tangent vector of the curve at a parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            The corresponding tangent vector.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        """
        raise NotImplementedError

    def curvature_at(self, t):
        """Compute the curvature of the curve at a parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            The corresponding curvature vector.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        """
        raise NotImplementedError

    def frame_at(self, t):
        """Compute the local frame of the curve at a parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The corresponding local frame.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        """
        raise NotImplementedError

    def torsion_at(self, t):
        """Compute the torsion of the curve at a parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter.

        Returns
        -------
        float
            The torsion value.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        """
        raise NotImplementedError

    # ==============================================================================
    # Methods continued
    # ==============================================================================

    def space(self, n=10):
        """Compute evenly spaced parameters over the curve domain.

        Parameters
        ----------
        n : int, optional
            The number of values in the parameter space.

        Returns
        -------
        list[float]

        """
        start, end = self.domain
        return linspace(start, end, n)

    def locus(self, resolution=100):
        """Compute the locus of points on the curve.

        Parameters
        ----------
        resolution : int
            The number of intervals at which a point on the
            curve should be computed.

        Returns
        -------
        list[:class:`~compas.geometry.Point`]
            Points along the curve.

        """
        return [self.point_at(t) for t in self.space(resolution)]

    def closest_point(self, point, return_parameter=False):
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point : :class:`~compas.geometry.Point`
            The test point.
        return_parameter : bool, optional
            If True, the parameter corresponding to the closest point should be returned in addition to the point.

        Returns
        -------
        :class:`~compas.geometry.Point` | tuple[:class:`~compas.geometry.Point`, float]
            If `return_parameter` is False, only the closest point is returned.
            If `return_parameter` is True, the closest point and the corresponding parameter are returned.

        """
        raise NotImplementedError

    def divide_by_count(self, count, return_points=False):
        """Divide the curve into a specific number of equal length segments.

        Parameters
        ----------
        count : int
            The number of segments.
        return_points : bool, optional
            If True, return the list of division parameters,
            and the points corresponding to those parameters.
            If False, return only the list of parameters.

        Returns
        -------
        list[float] | tuple[list[float], list[:class:`~compas.geometry.Point`]]
            If `return_points` is False, the parameters of the discretisation.
            If `return_points` is True, a list of points in addition to the parameters of the discretisation.

        """
        raise NotImplementedError

    def divide_by_length(self, length, return_points=False):
        """Divide the curve into segments of specified length.

        Parameters
        ----------
        length : float
            The length of the segments.
        return_points : bool, optional
            If True, return the list of division parameters,
            and the points corresponding to those parameters.
            If False, return only the list of parameters.

        Returns
        -------
        list[float] | tuple[list[float], list[:class:`~compas.geometry.Point`]]
            If `return_points` is False, the parameters of the discretisation.
            If `return_points` is True, a list of points in addition to the parameters of the discretisation.

        """
        raise NotImplementedError

    def aabb(self):
        """Compute the axis aligned bounding box of the curve.

        Returns
        -------
        :class:`~compas.geometry.Box`

        """
        raise NotImplementedError

    def length(self, precision=1e-8):
        """Compute the length of the curve.

        Parameters
        ----------
        precision : float, optional
            Required precision of the calculated length.

        """
        raise NotImplementedError

    def fair(self, tol=1e-3):
        raise NotImplementedError

    def offset(self):
        raise NotImplementedError

    def smooth(self):
        raise NotImplementedError

    def split(self):
        raise NotImplementedError

    def trim(self):
        raise NotImplementedError
