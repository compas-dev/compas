from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import cos
from math import pi
from math import sin
from math import sqrt

from compas.geometry import Frame
from compas.geometry import Point

from .conic import Conic

PI2 = 2 * pi


class Hyperbola(Conic):
    r"""
    A hyperbola is defined by a coordinate frame and a major and minor axis.

    It is implemented using the equation

    .. math::

        \frac{x^2}{a^2} - \frac{y^2}{b^2} = 1

    and with parametric form

    .. math::

        x(t) &= a \times \sec(t) \\
        y(t) &= b \times \tan(t)

    This means that the center of the hyperbola is at the center of the coordinate frame,
    the vertices of the left and right branches are at (0, -a) and (0, +a) respectively,
    the linear eccentricity is math::`\sqrt{a^2 + b^2}`,
    and the eccentricity math::`\fraq{\sqrt{a^2 + b^2}}{a}`.

    Parameters
    ----------
    major : float
        The major of the hyperbola.
    minor : float
        The minor of the hyperbola.
    frame : :class:`compas.geometry.Frame`, optional
        The local coordinate system of the hyperbola.
        The default value is ``None``, in which case the hyperbola is constructed in the XY plane of the world coordinate system.
    name : str, optional
        The name of the hyperbola.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`
        The coordinate frame of the hyperbola.
    transformation : :class:`Transformation`, read-only
        The transformation from the local coordinate system of the hyperbola (:attr:`frame`) to the world coordinate system.
    major : float
        The major radius of the hyperbola.
    minor : float
        The minor radius of the hyperbola.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the hyperbola.
    semifocal : float, read-only
        The distance between the center and the focus points.
    focal : float, read-only
        The distance between the two focus points.
    eccentricity : float, read-only
        This is the ratio between the semifocal length to the length of the semi-major axis.
        The eccentricity of a hyperbola is a number higher than 1.
    vertex1 : :class:`compas.geometry.Point`, read-only
        The first vertex of the hyperbola is on the positive x axis.
    vertex2 : :class:`compas.geometry.Point`, read-only
        The second vertex of the hyperbola is on the negative x axis.
    focus1 : :class:`compas.geometry.Point`, read-only
        The first focus of the hyperbola is on the positive x axis.
    focus2 : :class:`compas.geometry.Point`, read-only
        The second focus of the hyperbola is on the negative x axis.
    asymptote1 : :class:`compas.geometry.Line`, read-only
        The first asymptote of the hyperbola.
    asymptote2 : :class:`compas.geometry.Line`, read-only
        The second asymptote of the hyperbola.
    is_closed : bool, read-only
        False.
    is_periodic : bool, read-only
        False.

    See Also
    --------
    :class:`compas.geometry.Circle`, :class:`compas.geometry.Ellipse`, :class:`compas.geometry.Parabola`

    Examples
    --------
    Construct a hyperbola in the world XY plane.

    >>> from compas.geometry import Frame, Hyperbola
    >>> hyperbola = Hyperbola(major=3, minor=2, frame=Frame.worldXY())
    >>> hyperbola = Hyperbola(major=3, minor=2)

    Construct a hyperbola such that the Z axis of its frame aligns with a given line.

    >>> from compas.geometry import Line, Plane, Frame, Hyperbola
    >>> line = Line([0, 0, 0], [1, 1, 1])
    >>> plane = Plane(line.end, line.direction)
    >>> hyperbola = Hyperbola(major=3, minor=2, frame=Frame.from_plane(plane))

    Visualise the line, hyperbola, and frame of the hyperbola with the COMPAS viewer.

    >>> from compas_viewer import Viewer          # doctest: +SKIP
    >>> viewer = Viewer()                         # doctest: +SKIP
    >>> viewer.scene.add(line)                    # doctest: +SKIP
    >>> viewer.scene.add(hyperbola)               # doctest: +SKIP
    >>> viewer.scene.add(hyperbola.frame)         # doctest: +SKIP
    >>> viewer.show()                             # doctest: +SKIP

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "major": {"type": "number", "minimum": 0},
            "minor": {"type": "number", "minimum": 0},
            "frame": Frame.DATASCHEMA,
        },
        "required": ["major", "minor", "frame"],
    }

    @property
    def __data__(self):
        return {
            "major": self.major,
            "minor": self.minor,
            "frame": self.frame.__data__,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            major=data["major"],
            minor=data["minor"],
            frame=Frame.__from_data__(data["frame"]),
        )

    def __init__(self, major, minor, frame=None, name=None):
        super(Hyperbola, self).__init__(frame=frame, name=name)
        self._major = None
        self._minor = None
        self.major = major
        self.minor = minor

    def __repr__(self):
        return "{0}(major={1}, minor={2}, frame={3!r})".format(
            type(self).__name__,
            self.major,
            self.minor,
            self.frame,
        )

    def __eq__(self, other):
        try:
            return self.major == other.major and self.minor == other.minor, self.frame == other.frame
        except AttributeError:
            return False

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
    def major(self):
        if self._major is None:
            raise ValueError("Length of major axis is not set.")
        return self._major

    @major.setter
    def major(self, major):
        if major < 0:
            raise ValueError("Major axis length cannot be negative.")
        self._major = float(major)

    @property
    def minor(self):
        if self._minor is None:
            raise ValueError("Length of minor axis is not set.")
        return self._minor

    @minor.setter
    def minor(self, minor):
        if minor < 0:
            raise ValueError("Minor axis length cannot be negative.")
        self._minor = float(minor)

    @property
    def semifocal(self):
        return sqrt(self.major**2 + self.minor**2)

    @property
    def focal(self):
        return 2 * self.semifocal

    @property
    def eccentricity(self):
        return self.semifocal / self.major

    @property
    def focus1(self):
        return self.frame.point + self.frame.xaxis * self.semifocal

    @property
    def focus2(self):
        return self.frame.point + self.frame.xaxis * -self.semifocal

    @property
    def vertex1(self):
        return self.frame.point + self.frame.xaxis * self.major

    @property
    def vertex2(self):
        return self.frame.point + self.frame.xaxis * -self.major

    @property
    def asymptote1(self):
        pass

    @property
    def asymptote2(self):
        pass

    @property
    def is_closed(self):
        return True

    @property
    def is_periodic(self):
        return True

    # ==========================================================================
    # Constructors
    # ==========================================================================

    # ==========================================================================
    # Methods
    # ==========================================================================

    def point_at(self, t, world=True):
        """
        Point at the parameter.

        Parameters
        ----------
        t : float
            The curve parameter.
        world : bool, optional
            If ``True``, the point is transformed to the world coordinate system.

        Returns
        -------
        :class:`compas_future.geometry.Point`

        See Also
        --------
        :meth:`tangent_at`, :meth:`normal_at`

        Notes
        -----
        The location of the point is expressed with respect to the world coordinate system.

        """
        t = t * PI2
        sec_t = 1 / cos(t)
        x = self.major * sec_t
        y = self.minor * sin(t) * sec_t
        point = Point(x, y, 0)
        if world:
            point.transform(self.transformation)
        return point

    def tangent_at(self, t, world=True):
        """
        Tangent vector at the parameter.

        Parameters
        ----------
        t : float
            The curve parameter.
        world : bool, optional
            If ``True``, the tangent vector is transformed to the world coordinate system.

        Returns
        -------
        :class:`compas_future.geometry.Vector`

        See Also
        --------
        :meth:`point_at`, :meth:`normal_at`

        Notes
        -----
        The orientation of the vector is expressed with respect to the world coordinate system.

        """
        raise NotImplementedError

    def normal_at(self, t, world=True):
        """
        Normal at a specific normalized parameter.

        Parameters
        ----------
        t : float
            The curve parameter.
        world : bool, optional
            If ``True``, the normal vector is transformed to the world coordinate system.

        Returns
        -------
        :class:`compas_future.geometry.Vector`

        See Also
        --------
        :meth:`point_at`, :meth:`tangent_at`

        Notes
        -----
        The orientation of the vector is expressed with respect to the world coordinate system.

        """
        raise NotImplementedError
