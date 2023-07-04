from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi, cos, sin

from compas.geometry import Frame
from .conic import Conic

PI2 = 2 * pi


class Circle(Conic):
    """A circle is a curve defined by a coordinate system and a radius.

    The centre of the circle is at the origin of the coordinate system.
    The z-axis of the coordinate system defines the normal of the circle plane.
    The parameter domain of a circle is ``[0, 2*pi]``.
    Moving along the circle in the parameter direction corresponds to moving counter-clockwise around the origin of the local coordinate system.

    Transformations of the circle are performed by transforming the coordinate system.
    They are limited to (combinations of) translations and rotations.
    All other components of transformations are ignored.

    Parameters
    ----------
    frame : :class:`~compas.geometry.Frame`, optional
        The coordinate frame of the circle.
        The default value is ``None``, in which case the world coordinate system is used.
    radius : float
        The radius of the circle.

    Attributes
    ----------
    frame : :class:`~compas.geometry.Frame`
        The coordinate frame of the circle.
    radius : float
        The radius of the circle.
    center : :class:`~compas.geometry.Point`
        The center of the circle.
    plane : :class:`~compas.geometry.Plane`, read-only
        The plane of the circle.
    normal : :class:`~compas.geometry.Vector`, read-only
        The normal of the circle.
    diameter : float, read-only
        The diameter of the circle.
    area : float, read-only
        The area of the circle.
    circumference : float, read-only
        The circumference of the circle.
    domain : tuple(float, float), read-only
        The parameter domain of the circle.
    start : :class:`~compas.geometry.Point`, read-only
        The start point of the circle.
    end : :class:`~compas.geometry.Point`, read-only
        The end point of the circle.
    transformation : :class:`Transformation`, read-only
        The transformation from the local coordinate system of the circle (:attr:`frame`) to the world coordinate system.

    See Also
    --------
    :class:`compas.geometry.Ellipse`, :class:`compas.geometry.Arc`

    Examples
    --------
    >>> from compas.geometry import Frame, Circle
    >>> circle = Circle(frame=Frame.worldXY(), radius=5)
    >>> circle = Circle(radius=5)

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "frame": Frame.JSONSCHEMA,
            "radius": {"type": "number", "minimum": 0},
        },
        "required": ["frame", "radius"],
    }

    def __init__(self, frame=None, radius=1.0, **kwargs):
        super(Circle, self).__init__(frame=frame, **kwargs)
        self._radius = None
        self.radius = radius

    def __repr__(self):
        return "Circle({0!r}, {1!r})".format(self.frame, self.radius)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.frame
        elif key == 1:
            return self.radius
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.frame = value
        elif key == 1:
            self.radius = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.frame, self.radius])

    def __eq__(self, other):
        try:
            other_frame = other[0]
            other_radius = other[1]
        except Exception:
            return False
        return self.frame == other_frame and self.radius == other_radius

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def data(self):
        return {"frame": self.frame, "radius": self.radius}

    @data.setter
    def data(self, data):
        self.frame = data["frame"]
        self.radius = data["radius"]

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
        return self.radius * 2

    @property
    def area(self):
        return pi * (self.radius**2)

    @property
    def circumference(self):
        return 2 * pi * self.radius

    @property
    def eccentricity(self):
        return 0

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point_and_radius(cls, point, radius):
        """Construct a circle from a point and a radius.

        Parameters
        ----------
        point : :class:`~compas.geometry.Point`
            The center of the circle.
        radius : float
            The radius of the circle.

        Returns
        -------
        :class:`~compas.geometry.Circle`
            The constructed circle.

        """
        frame = Frame(point, [1, 0, 0], [0, 1, 0])
        return cls(frame=frame, radius=radius)

    @classmethod
    def from_plane_and_radius(cls, plane, radius):
        """Construct a circle from a plane and a radius.

        Parameters
        ----------
        plane : :class:`~compas.geometry.Plane`
            The plane of the circle.
        radius : float
            The radius of the circle.

        Returns
        -------
        :class:`~compas.geometry.Circle`
            The constructed circle.

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
    def from_points(cls, points):
        """Construct a circle from a list of at least three points.

        Parameters
        ----------
        points : list of :class:`~compas.geometry.Point`
            A list of three points defining the circle.

        Returns
        -------
        :class:`~compas.geometry.Circle`
            The constructed circle.

        Raises
        ------
        ValueError
            If the list of points contains less than three points.

        Notes
        -----
        If more than three points are provided,
        the constructed cicrle is the one that best fits the points in the least squares sense.

        """
        if len(points) < 3:
            raise ValueError("At least three points are required to define a circle.")

        from compas.geometry import Plane
        from compas.geometry import circle_from_points

        if len(points) == 3:
            (point, normal), radius = circle_from_points(*points)
            plane = Plane(point, normal)
            return cls.from_plane_and_radius(plane, radius)

        # not sure if this makes sense
        # but it will only throw an error if the bestfit is actually needed
        from compas.geometry import bestfit_circle_numpy

        point, normal, radius = bestfit_circle_numpy(points)
        plane = Plane(point, normal)
        return cls.from_plane_and_radius(plane, radius)

    # =============================================================================
    # Methods
    # =============================================================================

    def point_at(self, t):
        """Construct a point on the circle at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter of the point.

        Returns
        -------
        :class:`~compas.geometry.Point`
            The point on the circle at the specified parameter.

        """
        t = t * PI2
        x = self.radius * cos(t)
        y = self.radius * sin(t)
        return self.frame.point + self.frame.xaxis * x + self.frame.yaxis * y

    def normal_at(self, t):
        """Construct a normal on the circle at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter of the normal.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            The normal on the circle at the specified parameter.

        """
        normal = self.point_at(t) - self.center
        normal.unitize()
        return normal

    def tangent_at(self, t):
        """Construct a tangent on the circle at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter of the tangent.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            The tangent on the circle at the specified parameter.

        """
        t = t * PI2
        x = -self.radius * sin(t)
        y = +self.radius * cos(t)
        return self.frame.xaxis * x + self.frame.yaxis * y

    def binormal_at(self, t):
        """Construct a binormal on the circle at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter of the binormal.

        Returns
        -------
        :class:`~compas.geometry.Vector`
            The binormal on the circle at the specified parameter.

        """
        return self.frame.zaxis

    def closest_point(self, point):
        """Compute the closest point on the circle to a given point.

        Parameters
        ----------
        point : :class:`~compas.geometry.Point`
            A point.

        Returns
        -------
        :class:`~compas.geometry.Point`
            The closest point on the circle.

        """
        from compas.geometry import Vector

        projected = self.plane.closest_point(point)
        vector = Vector.from_start_end(self.center, projected)
        vector.unitize()
        vector *= self.radius
        return self.center + vector

    def contains_point(self, point, tol=1e-6, dmax=1e-6):
        """Verify that the circle contains a given point.

        Parameters
        ----------
        point : :class:`~compas.geometry.Point`
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
