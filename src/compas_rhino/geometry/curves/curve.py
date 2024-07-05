from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Curve
from compas.geometry import Plane
from compas_rhino.conversions import box_to_compas
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import plane_to_rhino
from compas_rhino.conversions import point_to_compas
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import vector_to_compas


class RhinoCurve(Curve):
    """Class representing a general curve object.

    Parameters
    ----------
    native_curve : :rhino:`Curve`
        A Rhino curve.
    name : str, optional
        Name of the curve.

    Attributes
    ----------
    dimension : int, read-only
        The spatial dimension of the curve.
    domain : tuple[float, float], read-only
        The parameter domain.
    start : :class:`compas.geometry.Point`, read-only
        The point corresponding to the start of the parameter domain.
    end : :class:`compas.geometry.Point`, read-only
        The point corresponding to the end of the parameter domain.
    is_closed : bool, read-only
        True if the curve is closed.
    is_periodic : bool, read-only
        True if the curve is periodic.

    Other Attributes
    ----------------
    native_curve : :rhino:`Curve`
        The underlying Rhino curve.

    """

    def __init__(self, native_curve, name=None):
        super(RhinoCurve, self).__init__(name=name)
        self._native_curve = native_curve

    def __eq__(self, other):
        return self.native_curve.IsEqual(other.native_curve)  # type: ignore

    # ==============================================================================
    # Data
    # ==============================================================================

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def rhino_curve(self):
        return self._native_curve

    @property
    def native_curve(self):
        return self._native_curve

    @native_curve.setter
    def native_curve(self, curve):
        self._native_curve = curve

    @property
    def dimension(self):
        if self.native_curve:
            return self.native_curve.Dimension

    @property
    def domain(self):
        if self.native_curve:
            return self.native_curve.Domain.T0, self.native_curve.Domain.T1

    @property
    def start(self):
        if self.native_curve:
            return point_to_compas(self.native_curve.PointAtStart)

    @property
    def end(self):
        if self.native_curve:
            return point_to_compas(self.native_curve.PointAtEnd)

    @property
    def is_closed(self):
        if self.native_curve:
            return self.native_curve.IsClosed

    @property
    def is_periodic(self):
        if self.native_curve:
            return self.native_curve.IsPeriodic

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_native(cls, native_curve):
        """Construct a curve from an existing Rhino curve.

        Parameters
        ----------
        native_curve : Rhino.Geometry.Curve

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoCurve`

        """
        return cls(native_curve)

    @classmethod
    def from_rhino(cls, native_curve):
        """Construct a curve from an existing Rhino curve.

        Parameters
        ----------
        native_curve : Rhino.Geometry.Curve

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoCurve`

        Warnings
        --------
        .. deprecated:: 2.3
            Use `from_native` instead.

        """
        return cls(native_curve)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self):
        """Make an independent copy of the current curve.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoCurve`

        """
        cls = type(self)
        native_curve = self.native_curve.Duplicate()
        return cls.from_native(native_curve)

    def transform(self, T):
        """Transform this curve.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation`
            A COMPAS transformation.

        Returns
        -------
        None

        """
        self.native_curve.Transform(transformation_to_rhino(T))  # type: ignore

    def reverse(self):
        """Reverse the parametrisation of the curve.

        Returns
        -------
        None

        """
        self.native_curve.Reverse()  # type: ignore

    def point_at(self, t):
        """Compute a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`compas.geometry.Point`
            the corresponding point on the curve.

        """
        point = self.native_curve.PointAt(t)  # type: ignore
        return point_to_compas(point)

    def tangent_at(self, t):
        """Compute the tangent vector at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The corresponding tangent vector.

        """
        vector = self.native_curve.TangentAt(t)  # type: ignore
        return vector_to_compas(vector)

    def curvature_at(self, t):
        """Compute the curvature at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The corresponding curvature vector.

        """
        vector = self.native_curve.CurvatureAt(t)  # type: ignore
        return vector_to_compas(vector)

    def frame_at(self, t):
        """Compute the local frame at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The corresponding local frame.

        """
        t, plane = self.native_curve.FrameAt(t)  # type: ignore
        return plane_to_compas_frame(plane)

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

        """
        return self.native_curve.TorsionAt(t)  # type: ignore

    # ==============================================================================
    # Methods continued
    # ==============================================================================

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
            If `return_parameter` is False, only the closest point is returned.
            If `return_parameter` is True, the closest point and the corresponding parameter are returned.

        """
        result, t = self.native_curve.ClosestPoint(point_to_rhino(point))  # type: ignore
        if not result:
            return
        point = self.point_at(t)
        if return_parameter:
            return point, t
        return point

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
        list[float] | tuple[list[float], list[:class:`compas.geometry.Point`]]
            If `return_points` is False, the parameters of the discretisation.
            If `return_points` is True, a list of points in addition to the parameters of the discretisation.

        """
        params = self.native_curve.DivideByCount(count, True)  # type: ignore
        if return_points:
            points = [self.point_at(t) for t in params]
            return params, points
        return params

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
        list[float] | tuple[list[float], list[:class:`compas.geometry.Point`]]
            If `return_points` is False, the parameters of the discretisation.
            If `return_points` is True, a list of points in addition to the parameters of the discretisation.

        """
        params = self.native_curve.DivideByLength(length, True)  # type: ignore
        if return_points:
            points = [self.point_at(t) for t in params]
            return params, points
        return params

    def aabb(self):
        """Compute the axis aligned bounding box of the curve.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        box = self.native_curve.getBoundingBox(True)  # type: ignore
        return box_to_compas(box)

    def length(self, precision=1e-8):
        """Compute the length of the curve.

        Parameters
        ----------
        precision : float, optional
            Required precision of the calculated length.

        """
        return self.native_curve.GetLength(precision)  # type: ignore

    def fair(self, tol=1e-3):
        raise NotImplementedError

    def offset(self, distance, direction, tolerance=1e-3):
        """Compute the length of the curve.

        Parameters
        ----------
        distance : float
            The offset distance.
        direction : :class:`compas.geometry.Vector`
            The normal direction of the offset plane.
        tolerance : float, optional

        Returns
        -------
        None

        """
        point = self.point_at(self.domain[0])  # type: ignore
        plane = Plane(point, direction)
        plane = plane_to_rhino(plane)
        self.native_curve = self.native_curve.Offset(plane, distance, tolerance, 0)[0]  # type: ignore

    def smooth(self):
        raise NotImplementedError

    def split(self):
        raise NotImplementedError

    def trim(self):
        raise NotImplementedError
