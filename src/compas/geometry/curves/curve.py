from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import pluggable
from compas.geometry import Geometry
from compas.geometry import Transformation
from compas.geometry import Point
from compas.geometry import Plane
from compas.geometry import Frame
from compas.utilities import linspace


@pluggable(category="factories")
def new_curve(cls, *args, **kwargs):
    curve = object.__new__(cls)
    curve.__init__(*args, **kwargs)
    return curve


class Curve(Geometry):
    """Class representing a general parametric curve.

    Parameters
    ----------
    name : str, optional
        The name of the curve.

    Attributes
    ----------
    frame : :class:`~compas.geometry.Frame`
        The frame of the curve.
    point : :class:`~compas.geometry.Point`
        The origin of the curve.
        If not explicitly defined, this defaults to the origin of the frame (:attr:`frame`).
    transformation : :class:`~compas.geometry.Transformation`, read-only
        The transformation from the local coordinate system of the curve (:attr:`frame`) to the world coordinate system.
    plane : :class:`~compas.geometry.Plane`, read-only
        The plane of the curve.
    dimension : int, read-only
        The spatial dimension of the curve.
        In most cases this will be 3.
        For curves embedded on a surface, this is 2.
    domain : tuple[float, float]
        The domain of the parameter space of the curve.
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
        return new_curve(cls, *args, **kwargs)

    def __init__(self, frame=None, domain=None, name=None):
        super(Curve, self).__init__(name=name)
        self._frame = None
        self._transformation = None
        self._domain = None
        self._point = None
        if frame:
            self.frame = frame
        self.domain = domain

    def __eq__(self, other):
        raise NotImplementedError

    def __str__(self):
        return "<Curve with parameter domain {}>".format(self.domain)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
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
        return cls(**data)

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
            self._transformation = Transformation.from_frame(self.frame)
        return self._transformation

    @property
    def point(self):
        if not self._point:
            return self.frame.point
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def xaxis(self):
        return self.frame.xaxis

    @property
    def yaxis(self):
        return self.frame.yaxis

    @property
    def zaxis(self):
        return self.frame.zaxis

    @property
    def plane(self):
        return Plane(self.frame.point, self.frame.zaxis)

    @property
    def dimension(self):
        return 3

    @property
    def domain(self):
        if not self._domain:
            self._domain = (0.0, 1.0)
        return self._domain

    @domain.setter
    def domain(self, domain):
        if not domain:
            self._domain = None
        else:
            u, v = domain
            self._domain = u, v

    @property
    def is_closed(self):
        return self.point_at(self.domain[0]) == self.point_at(self.domain[1])

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

    def to_polyline(self, resolution=10):
        """Convert the curve to a polyline.

        Parameters
        ----------
        resolution : int, optional
            The number of segments in the polyline.
            Default is ``10``.

        Returns
        -------
        :class:`~compas.geometry.Polyline`

        """
        from compas.geometry import Polyline

        points = [self.point_at(t) for t in self.space(resolution)]
        return Polyline(points)

    # ==============================================================================
    # Transformations
    # ==============================================================================

    def transform(self, T):
        """Transform the local coordinate system of the curve.

        Parameters
        ----------
        T : :class:`~compas.geometry.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        None
            The curve is modified in-place.

        Notes
        -----
        The transformation matrix is applied to the local coordinate system of the curve.
        Transformations are limited to (combinations of) translations and rotations.
        All other components of the transformation matrix are ignored.

        """
        T[0, 0] = 1
        T[1, 1] = 1
        T[2, 2] = 1
        T[3, 3] = 1

        T[0, 3] = 0
        T[1, 3] = 0
        T[2, 3] = 0

        T[3, 0] = 0
        T[3, 1] = 0
        T[3, 2] = 0

        self.frame.transform(T)

    # ==============================================================================
    # Methods
    # ==============================================================================

    def normalize_parameter(self, t):
        """Normalize a parameter to the domain of the curve.

        Parameters
        ----------
        t : float
            The parameter.

        Returns
        -------
        float
            The normalized parameter.

        """
        t = self.domain[0] + t * (self.domain[1] - self.domain[0])
        return t

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

    def normal_at(self, t):
        """Compute the normal of the curve at a parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            The corresponding normal vector.

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

    def binormal_at(self, t):
        """Compute the binormal vector of the curve at a parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            The corresponding binormal vector.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

        """
        # if not (self.domain[0] <= t <= self.domain[1]):
        #     raise ValueError("Parameter not in curve domain.")
        return self.tangent_at(t).cross(self.normal_at(t))

    def frame_at(self, t):
        """Compute the local frame of the curve at a parameter.

        Parameters
        ----------
        t : float
            The value of the curve parameter.
        world : bool, optional
            If True, return the frame in world coordinates.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The corresponding local frame.

        Raises
        ------
        ValueError
            If the parameter is not in the curve domain.

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
        :class:`~compas.geometry.Vector`
            The corresponding curvature vector.

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
            If `return_parameter` is False (default), only the closest point is returned.
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
