from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin

from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas.tolerance import TOL

from .curve import Curve

PI2 = 2.0 * pi


class Arc(Curve):
    """An arc is a segment of a circle, and is defined by a coordinate system, radius, and start and end angles.

    The centre of the underlying circle is at the origin of the coordinate system.
    The start and end angles are measured from the positive X axis towards the positive Y axis.

    The parametrisation of the arc is normalised with respect to the arc angle.
    The value ``t=0.0`` corresponds to the start angle of the arc.
    The value ``t=1.0`` corresponds to the end angle of the arc.
    The value ``t=0.5`` corresponds to the angle halfway between start and end.

    Transformations of the arc are performed by transforming the local coordinate system.

    Parameters
    ----------
    radius : float
        Radius of the arc's circle.
    start_angle : float
        The angle in radians of the start of this Arc.
    end_angle : float
        The angle in radians of the end of this Arc.
    frame : :class:`compas.geometry.Frame`, optional
        Local coordinate system of the arc.
        Defaults to the world XY plane.
    name : str, optional
        The name of the arc.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate frame of the arc.
    transformation : :class:`Transformation`, read-only
        The transformation from the local coordinate system of the arc (:attr:`frame`) to the world coordinate system.
    radius : float
        The radius of the circle.
    start_angle : float
        The start angle of the arc.
    end_angle : float
        The end angle of the arc.
    circle : :class:`compas.geometry.Circle`, read-only
        The underlying circle.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the arc.
    diameter : float, read-only
        The diameter of the underlying circle.
    length : float, read-only
        The length of the arc.
    angle : float, read-only
        The sweep angle in radians between start angle and end angle.
    circumference : float, read-only
        The circumference of the underlying circle.
    is_closed : bool, read-only
        False.
    is_periodic : bool, read-only
        False.

    See Also
    --------
    :class:`compas.geometry.Circle`

    Examples
    --------
    Construct a semicircular arc in the XY plane, with radius 1.0, and compute its length.

    >>> from math import pi
    >>> from compas.geometry import Arc
    >>> arc = Arc(radius=1.0, start_angle=0.0, end_angle=pi)
    >>> arc.length == 1.0 * pi
    True

    Construct a quarter arc in the 3rd quadrant of a frame
    aligned with the world ZX plane at a distance of 1.0 from the world origin along the world Y axis.

    >>> from math import pi
    >>> from compas.geometry import Frame
    >>> from compas.geometry import Arc
    >>> frame = Frame([0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0])
    >>> arc = Arc(radius=1.0, start_angle=pi, end_angle=pi * 1.5, frame=frame)
    >>> arc.length == 1.0 * pi * 0.5
    True

    Visualize the arc using the viewer.

    >>> from compas_viewer import Viewer  # doctest: +SKIP
    >>> viewer = Viewer()  # doctest: +SKIP
    >>> viewer.scene.add(arc.to_polyline(n=20))  # doctest: +SKIP
    >>> viewer.scene.add(arc.frame)  # doctest: +SKIP
    >>> viewer.show()  # doctest: +SKIP

    Visualize only part of the arc.

    >>> from compas_viewer import Viewer  # doctest: +SKIP
    >>> viewer = Viewer()  # doctest: +SKIP
    >>> viewer.scene.add(arc.to_polyline(n=20, domain=(0.25, 0.75)))  # doctest: +SKIP
    >>> viewer.scene.add(arc.frame)  # doctest: +SKIP
    >>> viewer.show()  # doctest: +SKIP

    """

    DATASCHEMA = {
        "value": {
            "type": "object",
            "properties": {
                "radius": {"type": "number", "minimum": 0},
                "start_angle": {"type": "number", "minimum": 0, "optional": True},
                "end_angle": {"type": "number", "minimum": 0},
                "frame": Frame.DATASCHEMA,
            },
            "required": ["frame", "radius", "start_angle", "end_angle"],
        }
    }

    @property
    def __data__(self):
        return {
            "radius": self.radius,
            "start_angle": self.start_angle,
            "end_angle": self.end_angle,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            radius=data["radius"],
            start_angle=data["start_angle"],
            end_angle=data["end_angle"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, radius, start_angle, end_angle, frame=None, name=None):
        super(Arc, self).__init__(frame=frame, name=name)
        self._radius = None
        self._start_angle = None
        self._end_angle = None
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle

    def __repr__(self):
        return "{0}(radius={1}, start_angle={2}, end_angle={3}, frame={4!r})".format(
            type(self).__name__,
            self.radius,
            self.start_angle,
            self.end_angle,
            self.frame,
        )

    def __eq__(self, other):
        try:
            return self.radius == other.radius and self.start_angle == other.start and self.end_angle == other.end and self.frame == other.frame
        except Exception:
            return False

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def radius(self):
        if self._radius is None:
            raise ValueError("Radius is not set.")
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0.0:
            raise ValueError("Radius must be greater than or equal to zero.")
        self._radius = value

    @property
    def start_angle(self):
        if self._start_angle is None:
            self._start_angle = 0.0
        return self._start_angle

    @start_angle.setter
    def start_angle(self, value):
        if value < 0.0 or value > PI2:
            raise ValueError("Start angle must satisfy 0 <= angle <= 2 * pi.")
        self._start_angle = value

    @property
    def end_angle(self):
        if self._end_angle is None:
            raise ValueError("End angle not set.")
        return self._end_angle

    @end_angle.setter
    def end_angle(self, value):
        if value < 0.0 or value > PI2:
            raise ValueError("End angle must satisfy 0 <= angle <= 2 * pi.")
        self._end_angle = value

    @property
    def circle(self):
        return Circle(radius=self.radius, frame=self.frame)

    @property
    def center(self):
        return self.frame.point

    @property
    def length(self):
        return self.radius * self.angle

    @property
    def angle(self):
        return self.end_angle - self.start_angle

    @property
    def diameter(self):
        return 2.0 * self.radius

    @property
    def circumference(self):
        return self.diameter * pi

    @property
    def is_circle(self):
        return TOL.is_close(abs(self.angle), PI2)

    @property
    def is_closed(self):
        return False

    @property
    def is_periodic(self):
        return False

    def _verify(self):
        if self.angle < 0.0 or self.angle > PI2:
            raise ValueError("Sweep angle must satisfy 0 < angle < 2 * Pi. Currently:{}".format(self.angle))

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_circle(cls, circle, start_angle, end_angle):
        """Creates an Arc from a circle and start and end angles.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle`
            The frame and radius of this circle will be used to create an Arc.
        start_angle : float
            The start angle in radians.
        end_angle : float
            The end angle in radians.

        Returns
        -------
        :class:`compas.geometry.Arc`

        """
        return cls(
            frame=circle.frame,
            radius=circle.radius,
            start_angle=start_angle,
            end_angle=end_angle,
        )

    # =============================================================================
    # Conversions
    # =============================================================================

    # =============================================================================
    # Transformations
    # =============================================================================

    # =============================================================================
    # Methods
    # =============================================================================

    def point_at(self, t, world=True):
        """Returns the point at the specified parameter.

        Parameters
        ----------
        t : float
            The parameter at which to evaluate the arc.
        world : bool, optional
            If ``True``, the point is returned in world coordinates.

        Returns
        -------
        :class:`compas.geometry.Point`

        Raises
        ------
        ValueError
            If the parameter is not in the domain of the curve ``[0, 1]``.

        See Also
        --------
        :meth:`normal_at`, :meth:`tangent_at`

        Notes
        -----
        The parametrisation of the arc is normalised with respect to the polar angle domain.
        The value ``t=0.0`` corresponds to the start angle of the arc.
        The value ``t=1.0`` corresponds to the end angle of the arc.
        The value ``t=0.5`` corresponds to the angle halfway between start and end.

        """
        if t < 0.0 or t > 1.0:
            raise ValueError("Parameter t should be between 0.0 and 1.0")

        angle = self.start_angle + t * self.angle
        x = self.radius * cos(angle)
        y = self.radius * sin(angle)

        if not world:
            return Point(x, y, 0.0)

        return self.frame.point + self.frame.xaxis * x + self.frame.yaxis * y

    def normal_at(self, t, world=True):
        """Construct a normal vector to the arc at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter at which to evaluate the arc.
        world : bool, optional
            If ``True``, the normal is returned in world coordinates.

        Returns
        -------
        :class:`compas.geometry.Vector`

        Raises
        ------
        ValueError
            If the parameter is not in the domain of the curve ``[0, 1]``.

        See Also
        --------
        :meth:`point_at`, :meth:`tangent_at`

        Notes
        -----
        The parametrisation of the arc is normalised with respect to the polar angle domain.
        The value ``t=0.0`` corresponds to the start angle of the arc.
        The value ``t=1.0`` corresponds to the end angle of the arc.
        The value ``t=0.5`` corresponds to the angle halfway between start and end.

        """
        if not world:
            point = self.point_at(t, world=False)
            normal = Vector(-point.x, -point.y, 0.0)
            normal.unitize()
            return normal

        normal = self.frame.point - self.point_at(t)
        normal.unitize()
        return normal

    def tangent_at(self, t, world=True):
        """Construct a tangent on the circle at a specific parameter.

        Parameters
        ----------
        t : float
            The parameter at which to evaluate the arc.
        world : bool, optional
            If ``True``, the tangent is returned in world coordinates.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The tangent on the circle at the specified parameter.

        Raises
        ------
        ValueError
            If the parameter is not in the domain of the curve ``[0, 1]``.

        See Also
        --------
        :meth:`point_at`, :meth:`normal_at`, :meth:`binormal_at`

        Notes
        -----
        The parametrisation of the arc is normalised with respect to the polar angle domain.
        The value ``t=0.0`` corresponds to the start angle of the arc.
        The value ``t=1.0`` corresponds to the end angle of the arc.
        The value ``t=0.5`` corresponds to the angle halfway between start and end.

        """
        if t < 0.0 or t > 1.0:
            raise ValueError("Parameter t should be between 0.0 and 1.0")

        angle = self.start_angle + t * self.angle

        x = -self.radius * sin(angle)
        y = +self.radius * cos(angle)

        if not world:
            return Vector(x, y, 0.0)

        return self.frame.xaxis * x + self.frame.yaxis * y
