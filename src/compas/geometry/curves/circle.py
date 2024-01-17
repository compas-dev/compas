from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi, cos, sin

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Plane
from .conic import Conic

PI2 = 2 * pi


class Circle(Conic):
    """A circle is a curve defined by a coordinate system and a radius.

    The centre of the circle is at the origin of the coordinate system.
    The z-axis of the coordinate system defines the normal of the circle plane.
    The parameter domain is normalized with respect to the polar angle.
    A parameter value of ``t = 0`` corresponds to the point on the circle at angle ``0``.
    A parameter value of ``t = 1`` corresponds to the point on the circle at angle ``2 * pi``.
    Moving along the circle in the parameter direction corresponds to moving counter-clockwise around the origin of the local coordinate system.

    Parameters
    ----------
    radius : float
        The radius of the circle.
    frame : :class:`compas.geometry.Frame`, optional
        The coordinate frame of the circle.
        The default value is ``None``, in which case the world coordinate system is used.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate frame of the circle.
    transformation : :class:`Transformation`, read-only
        The transformation from the local coordinate system of the circle (:attr:`frame`) to the world coordinate system.
    center : :class:`compas.geometry.Point`
        The center of the circle.
    radius : float
        The radius of the circle.
    diameter : float, read-only
        The diameter of the circle.
    area : float, read-only
        The area of the circle.
    circumference : float, read-only
        The circumference of the circle.
    eccentricity : float, read-only
        The eccentricity of the circle is zero.
    is_closed : bool, read-only
        True.
    is_periodic : bool, read-only
        True.

    See Also
    --------
    :class:`compas.geometry.Ellipse`, :class:`compas.geometry.Arc`

    Examples
    --------
    Construct a circle in the world XY plane.

    >>> from compas.geometry import Frame, Circle
    >>> circle = Circle(radius=5, frame=Frame.worldXY())
    >>> circle = Circle(radius=5)

    Construct a circle such that the Z axis of its frame such that it aligns with a given line.

    >>> from compas.geometry import Line, Frame, Plane, Circle
    >>> line = Line([0, 0, 0], [1, 1, 1])
    >>> plane = Plane(line.end, line.direction)
    >>> circle = Circle.from_plane_and_radius(plane, 5)
    >>> circle = Circle(radius=5, frame=Frame.from_plane(plane))

    Visualise the line, circle, and frame of the circle with the COMPAS viewer.

    >>> from compas_view2.app import App  # doctest: +SKIP
    >>> viewer = App()                    # doctest: +SKIP
    >>> viewer.add(line)                  # doctest: +SKIP
    >>> viewer.add(circle)                # doctest: +SKIP
    >>> viewer.add(circle.frame)          # doctest: +SKIP
    >>> viewer.run()                      # doctest: +SKIP

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "frame": Frame.JSONSCHEMA,
            "radius": {"type": "number", "minimum": 0},
        },
        "required": ["frame", "radius"],
    }

    @property
    def __data__(self):
        return {
            "radius": self.radius,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __before_init__(cls, data):
        data["frame"] = Frame(**data["frame"])

    def __init__(self, radius, frame=None, **kwargs):
        super(Circle, self).__init__(frame=frame, **kwargs)
        self._radius = None
        self.radius = radius

    def __repr__(self):
        return "{0}(radius={1!r}, frame={2!r})".format(
            type(self).__name__,
            self.radius,
            self.frame,
        )

    def __eq__(self, other):
        try:
            other_frame = other.frame
            other_radius = other.radius
        except Exception:
            return False
        return self.frame == other_frame and self.radius == other_radius

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def center(self):
        return self.frame.point

    @center.setter
    def center(self, point):
        self.frame.point = point

    @property
    def radius(self):
        if self._radius is None:
            raise ValueError("The radius of the circle has not been set yet.")
        return self._radius

    @radius.setter
    def radius(self, radius):
        if radius < 0:
            raise ValueError("The radius of a circle should be larger than or equal to zero.")
        self._radius = float(radius)

    @property
    def diameter(self):
        return 2 * self.radius

    @property
    def area(self):
        return pi * (self.radius**2)

    @property
    def circumference(self):
        return 2 * pi * self.radius

    @property
    def eccentricity(self):
        return 0

    @property
    def is_closed(self):
        return True

    @property
    def is_periodic(self):
        return True

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point_and_radius(cls, point, radius):
        """Construct a circle from a point and a radius.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The center of the circle.
        radius : float
            The radius of the circle.

        Returns
        -------
        :class:`compas.geometry.Circle`
            The constructed circle.

        See Also
        --------
        :meth:`from_plane_and_radius`, :meth:`from_three_points`, :meth:`from_points`

        """
        frame = Frame(point, [1, 0, 0], [0, 1, 0])
        return cls(frame=frame, radius=radius)

    @classmethod
    def from_plane_and_radius(cls, plane, radius):
        """Construct a circle from a plane and a radius.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane of the circle.
        radius : float
            The radius of the circle.

        Returns
        -------
        :class:`compas.geometry.Circle`
            The constructed circle.

        See Also
        --------
        :meth:`from_point_and_radius`, :meth:`from_three_points`, :meth:`from_points`

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Circle
        >>> plane = Plane([0, 0, 0], [0, 0, 1])
        >>> circle = Circle.from_plane_and_radius(plane, 5)

        """
        frame = Frame.from_plane(plane)
        return cls(frame=frame, radius=radius)

    @classmethod
    def from_three_points(cls, a, b, c):
        """Construct a circle from three points.

        Parameters
        ----------
        a : :class:`compas.geometry.Point`
            The first point.
        b : :class:`compas.geometry.Point`
            The second point.
        c : :class:`compas.geometry.Point`
            The third point.

        Returns
        -------
        :class:`compas.geometry.Circle`
            The constructed circle.

        See Also
        --------
        :meth:`from_point_and_radius`, :meth:`from_plane_and_radius`, :meth:`from_points`

        """
        from compas.geometry import Plane
        from compas.geometry import circle_from_points

        (point, normal), radius = circle_from_points(a, b, c)
        plane = Plane(point, normal)
        return cls.from_plane_and_radius(plane, radius)

    @classmethod
    def from_points(cls, points):
        """Construct a circle from a list of at least three points.

        Parameters
        ----------
        points : list of :class:`compas.geometry.Point`
            A list of three points defining the circle.

        Returns
        -------
        :class:`compas.geometry.Circle`
            The constructed circle.

        Raises
        ------
        ValueError
            If the list of points contains less than three points.

        See Also
        --------
        :meth:`from_point_and_radius`, :meth:`from_plane_and_radius`, :meth:`from_three_points`

        Notes
        -----
        If more than three points are provided,
        the constructed cicrle is the one that best fits the points in the least squares sense.

        """
        if len(points) < 3:
            raise ValueError("At least three points are required to define a circle.")

        if len(points) == 3:
            return cls.from_three_points(*points)

        # not sure if this makes sense
        # but it will only throw an error if the bestfit is actually needed
        from compas.geometry import bestfit_circle_numpy

        point, normal, radius = bestfit_circle_numpy(points)
        plane = Plane(point, normal)
        return cls.from_plane_and_radius(plane, radius)

    # =============================================================================
    # Methods
    # =============================================================================

    def point_at(self, t, world=True):
        """Construct a point on the circle at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter of the point.
            The parameter is expected to be normalized,
            and will be mapped to the corresponding angle in the interval ``[0, 2 * pi]``.
        world : bool, optional
            If ``True``, the point is returned in world coordinates.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point on the circle at the specified parameter.

        See Also
        --------
        :meth:`normal_at`, :meth:`tangent_at`, :meth:`binormal_at`

        Notes
        -----
        The location of the point is expressed with respect to the world coordinate system.

        """
        t = t * PI2
        x = self.radius * cos(t)
        y = self.radius * sin(t)
        point = Point(x, y, 0)
        if world:
            point.transform(self.transformation)
        return point

    def normal_at(self, t, world=True):
        """Construct a normal on the circle at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter of the normal vector.
            The parameter is expected to be normalized,
            and will be mapped to the corresponding angle in the interval ``[0, 2 * pi]``.
        world : bool, optional
            If ``True``, the normal is returned in world coordinates.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The normal on the circle at the specified parameter.

        See Also
        --------
        :meth:`point_at`, :meth:`tangent_at`, :meth:`binormal_at`

        Notes
        -----
        The orientation of the vector is expressed with respect to the world coordinate system.

        """
        if world:
            normal = self.center - self.point_at(t, world=True)
            normal.unitize()
            return normal
        point = self.point_at(t, world=False)
        return Vector(-point.x, -point.y, 0)

    def tangent_at(self, t, world=True):
        """Construct a tangent on the circle at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter of the tangent vector.
            The parameter is expected to be normalized,
            and will be mapped to the corresponding angle in the interval ``[0, 2 * pi]``.
        world : bool, optional
            If ``True``, the tangent is returned in world coordinates.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The tangent on the circle at the specified parameter.

        See Also
        --------
        :meth:`point_at`, :meth:`normal_at`, :meth:`binormal_at`

        Notes
        -----
        The orientation of the vector is expressed with respect to the world coordinate system.

        """
        t = t * PI2
        x = -self.radius * sin(t)
        y = +self.radius * cos(t)
        vector = Vector(x, y, 0)
        vector.unitize()
        if world:
            vector.transform(self.transformation)
        return vector

    def closest_point(self, point, return_parameter=False):
        """Compute the closest point on the circle to a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            A point.
        return_parameter : bool, optional
            Return the parameter of the closest point as well.

        Returns
        -------
        :class:`compas.geometry.Point`
            The closest point on the circle.

        Notes
        -----
        The location of the point is expressed with respect to the world coordinate system.

        """
        from compas.geometry import Vector

        projected = self.plane.closest_point(point)
        vector = Vector.from_start_end(self.center, projected)
        vector.unitize()
        vector *= self.radius

        if return_parameter:
            raise NotImplementedError

        return self.center + vector

    def contains_point(self, point, tol=1e-6, dmax=1e-6):
        """Verify that the circle contains a given point.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The point.
        tol : float, optional
            The tolerance for the verification.
        dmax : float, optional
            The maximum allowed distance between the plane of the circle and the point.

        Returns
        -------
        bool
            True if the point is on the circle.
            False otherwise.

        Notes
        -----
        By default, the verification will fail if the point is not exactly in the plane of the circle.
        To allow for a certain tolerance, use the ``dmax`` parameter.
        Like with apparent intersections, using a ``dmax`` higher than zero, allows for "apparent containment" checks

        """
        point = self.frame.to_local_coordinates(point)
        x, y, z = point.x, point.y, point.z  # type: ignore
        if abs(z) > dmax:
            return False
        return x**2 + y**2 <= (self.radius + tol) ** 2
