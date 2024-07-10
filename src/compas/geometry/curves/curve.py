from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Plane
from compas.geometry import Transformation
from compas.itertools import linspace
from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable


@pluggable(category="factories")
def curve_from_native(cls, *args, **kwargs):
    raise PluginNotInstalledError


class Curve(Geometry):
    """Class representing a general parametric curve.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`, optional
        The local coordinate system of the curve.
        Default is the world coordinate system.
    name : str, optional
        The name of the curve.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`
        The frame of the curve.
    transformation : :class:`compas.geometry.Transformation`, read-only
        The transformation from the local coordinate system of the curve (:attr:`frame`) to the world coordinate system.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the curve.
    dimension : int, read-only
        The spatial dimension of the curve.
        In most cases this will be 3.
        For curves embedded on a surface, this is 2.
    domain : tuple[float, float], read-only
        The domain of the parameter space of the curve is the interval ``[0.0, 1.0]``.
    is_closed : bool, read-only
        True if the curve is closed.
    is_periodic : bool, read-only
        True if the curve is periodic.

    See Also
    --------
    :class:`compas.geometry.Arc`, :class:`compas.geometry.Circle`,
    :class:`compas.geometry.Ellipse`, :class:`compas.geometry.Line`,
    :class:`compas.geometry.NurbsCurve`, :class:`compas.geometry.Polyline`

    Notes
    -----
    The curve is a "pluggable". This means that it does not provide an actual implementation
    of a parametric curve, but rather serves as an interface for different backends.
    If a backend is available, it will be used to construct the curve and provide its functionality.
    This backend is referred to as the "plugin" implementation of the curve.

    To activate the plugin mechanism, the backend should provide an implementation of the :func:`new_curve` function,
    and of any other function that can be implemented through the functionality available in the backend.

    """

    def __new__(cls, *args, **kwargs):
        if cls is Curve:
            raise TypeError("Making an instance of `Curve` using `Curve()` is not allowed. Please use one of the factory methods instead (`Curve.from_...`)")
        return object.__new__(cls)

    def __init__(self, frame=None, name=None):
        super(Curve, self).__init__(name=name)
        self._frame = None
        self._transformation = None
        self._domain = None
        if frame:
            self.frame = frame

    def __repr__(self):
        return "{0}(frame={1!r}, domain={2})".format(
            type(self).__name__,
            self.frame,
            self.domain,
        )

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def frame(self):
        if not self._frame:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, frame):
        if not frame:
            self._frame = None
        else:
            self._frame = Frame(frame[0], frame[1], frame[2])
        self._transformation = None

    @property
    def transformation(self):
        if not self._transformation:
            self._transformation = Transformation.from_frame_to_frame(Frame.worldXY(), self.frame)
        return self._transformation

    @property
    def plane(self):
        return Plane(self.frame.point, self.frame.zaxis)

    @property
    def dimension(self):
        return 3

    @property
    def domain(self):
        return 0.0, 1.0

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
    def from_native(cls, curve):
        """Construct a parametric curve from a native curve geometry.

        Parameters
        ----------
        curve
            A native curve object.

        Returns
        -------
        :class:`compas.geometry.Curve`
            A COMPAS curve.

        """
        return curve_from_native(cls, curve)

    @classmethod
    def from_obj(cls, filepath):
        """Load a curve from an OBJ file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`compas.geometry.Curve`

        """
        raise NotImplementedError

    @classmethod
    def from_step(cls, filepath):
        """Load a curve from a STP file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`compas.geometry.Curve`

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
        schema : str, optional
            The STEP schema to use. Default is ``"AP203"``.

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

    def to_points(self, n=10, domain=None):
        """Convert the curve to a list of points.

        Parameters
        ----------
        n : int, optional
            The number of points in the list.
            Default is ``10``.
        domain : tuple, optional
            Subset of the domain to use for the discretisation.
            Default is ``None``, in which case the entire curve domain is used.

        Returns
        -------
        list[:class:`compas.geometry.Point`]

        """
        domain = domain or self.domain
        start, end = domain
        points = [self.point_at(t) for t in linspace(start, end, n)]
        return points

    def to_polyline(self, n=128, domain=None):
        """Convert the curve to a polyline.

        Parameters
        ----------
        n : int, optional
            The number of line segments in the polyline.
            Default is ``16``.
        domain : tuple, optional
            Subset of the domain to use for the discretisation.
            Default is ``None``, in which case the entire curve domain is used.

        Returns
        -------
        :class:`compas.geometry.Polyline`

        """
        from compas.geometry import Polyline

        points = self.to_points(n=n + 1, domain=domain)
        return Polyline(points)

    def to_polygon(self, n=16):
        """Convert the curve to a polygon.

        Parameters
        ----------
        n : int, optional
            The number of sides of the polygon.
            Default is ``16``.

        Returns
        -------
        :class:`compas.geometry.Polygon`

        Raises
        ------
        ValueError
            If the curve is not closed.

        """
        if not self.is_closed:
            raise ValueError("The curve is not closed.")

        from compas.geometry import Polygon

        points = self.to_points(n=n + 1)
        return Polygon(points[:-1])

    # ==============================================================================
    # Transformations
    # ==============================================================================

    def transform(self, T):
        """Transform the local coordinate system of the curve.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        None
            The (local coordinate system of the) curve is modified in-place.

        Notes
        -----
        Transformations of frames are limited to rotations and translations.
        All other transformations have no effect.
        See :meth:`~compas.geometry.Frame.transform` for more info.

        """
        self.frame.transform(T)
        self._transformation = None

    # ==============================================================================
    # Methods
    # ==============================================================================

    def point_at(self, t):
        """Compute a point of the curve at a parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`compas.geometry.Point`
            the corresponding point on the curve.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        See Also
        --------
        :meth:`normal_at`, :meth:`tangent_at`, :meth:`binormal_at`, :meth:`frame_at`, :meth:`curvature_at`

        """
        raise NotImplementedError

    def normal_at(self, t):
        """Compute the normal of the curve at a parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The corresponding normal vector.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        See Also
        --------
        :meth:`point_at`, :meth:`tangent_at`, :meth:`binormal_at`, :meth:`frame_at`, :meth:`curvature_at`

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
        :class:`compas.geometry.Vector`
            The corresponding tangent vector.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        See Also
        --------
        :meth:`point_at`, :meth:`normal_at`, :meth:`binormal_at`, :meth:`frame_at`, :meth:`curvature_at`

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
        :class:`compas.geometry.Frame`
            The corresponding local frame.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        See Also
        --------
        :meth:`point_at`, :meth:`normal_at`, :meth:`tangent_at`, :meth:`binormal_at`, :meth:`curvature_at`

        """
        return Frame(self.point_at(t), self.tangent_at(t), self.normal_at(t))

    def curvature_at(self, t):
        """Compute the curvature vector of the curve at a parameter.

        This is a vector pointing from the point on the curve at the specified parameter,
        to the center of the oscillating circle of the curve at that location.

        Note that this vector is parallel to the normal vector of the curve at that location.

        Parameters
        ----------
        t : float
            The value of the curve parameter.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The corresponding curvature vector.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        See Also
        --------
        :meth:`point_at`, :meth:`normal_at`, :meth:`tangent_at`, :meth:`binormal_at`, :meth:`frame_at`

        """
        raise NotImplementedError

    # ==============================================================================
    # Methods continued
    # ==============================================================================

    def reverse(self):
        """Reverse the parametrisation of the curve.

        Returns
        -------
        None

        See Also
        --------
        :meth:`reversed`

        """
        raise NotImplementedError

    def reversed(self):
        """Reverse a copy of the curve.

        Returns
        -------
        :class:`compas.geometry.Curve`

        See Also
        --------
        :meth:`reverse`

        """
        copy = self.copy()
        copy.reverse()
        return copy

    def closest_point(self, point, return_parameter=False):
        """Compute the closest point on the curve to a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The test point.
        return_parameter : bool, optional
            If True, the parameter corresponding to the closest point should be returned in addition to the point.

        Returns
        -------
        :class:`compas.geometry.Point` | tuple[:class:`compas.geometry.Point`, float]
            If `return_parameter` is False (default), only the closest point is returned.
            If `return_parameter` is True, the closest point and the corresponding parameter are returned.

        """
        raise NotImplementedError

    def divide_by_count(self, count, return_points=False):
        """Compute the curve parameters that divide the curve into a specific number of equal length segments.

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
        list[float] | tuple[list[float], list[:class:`compas.geometry.Point`]]
            If `return_points` is False, the parameters of the discretisation.
            If `return_points` is True, a list of points in addition to the parameters of the discretisation.

        See Also
        --------
        :meth:`divide_by_length`
        :meth:`split`

        """
        raise NotImplementedError

    def divide_by_length(self, length, return_points=False):
        """Compute the curve parameters that divide the curve into segments of specified length.

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
        list[float] | tuple[list[float], list[:class:`compas.geometry.Point`]]
            If `return_points` is False, the parameters of the discretisation.
            If `return_points` is True, a list of points in addition to the parameters of the discretisation.

        See Also
        --------
        :meth:`divide_by_count`
        :meth:`split`

        """
        raise NotImplementedError

    def aabb(self):
        """Compute the axis-aligned bounding box of the curve.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        raise NotImplementedError

    def length(self, tol=None):
        """Compute the length of the curve.

        Parameters
        ----------
        precision : float, optional
            Required precision of the calculated length.

        """
        raise NotImplementedError

    def fair(self, tol=None):
        raise NotImplementedError

    def offset(self):
        raise NotImplementedError

    def smooth(self):
        raise NotImplementedError

    def split(self):
        raise NotImplementedError

    def trim(self):
        raise NotImplementedError
