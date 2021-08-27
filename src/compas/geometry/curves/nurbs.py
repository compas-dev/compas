from math import sqrt

from typing import Dict, List
from compas.geometry import Point
from compas.geometry import Transformation
from compas.geometry import Frame
from compas.geometry import Circle
from compas.utilities import linspace

from ._curve import Curve


class NurbsCurve(Curve):
    """Class representing a NURBS curve.

    Attributes
    ----------
    points: List[Point]
        The control points of the curve.
    weights: List[float]
        The weights of the control points.
    knots: List[float]
        The knot vector, without duplicates.
    multiplicities: List[int]
        The multiplicities of the knots in the knot vector.
    knotsequence: List[float]
        The knot vector, with repeating values according to the multiplicities.
    degree: int
        The degree of the polynomials.
    order: int
        The order of the curve.
    domain: Tuple[float, float]
        The parameter domain.
    start: :class:`Point`
        The point corresponding to the start of the parameter domain.
    end: :class:`Point`
        The point corresponding to the end of the parameter domain.
    is_closed: bool
        True if the curve is closed.
    is_periodic: bool
        True if the curve is periodic.
    is_rational: bool
        True is the curve is rational.
    length: float
        Length of the curve.

    """

    @property
    def DATASCHEMA(self):
        from schema import Schema
        from compas.data import is_float3
        from compas.data import is_sequence_of_int
        from compas.data import is_sequence_of_float
        return Schema({
            'points': lambda points: all(is_float3(point) for point in points),
            'weights': is_sequence_of_float,
            'knots': is_sequence_of_float,
            'multiplicities': is_sequence_of_int,
            'degree': int,
            'is_periodic': bool
        })

    @property
    def JSONSCHEMANAME(self):
        raise NotImplementedError

    def __init__(self, name=None) -> None:
        super().__init__(name=name)

    def __eq__(self, other: 'NurbsCurve') -> bool:
        raise NotImplementedError

    def __str__(self):
        lines = [
            'NurbsCurve',
            '------------',
            f'Points: {self.points}',
            f'Weights: {self.weights}',
            f'Knots: {self.knots}',
            f'Mults: {self.multiplicities}',
            f'Degree: {self.degree}',
            f'Order: {self.order}',
            f'Domain: {self.domain}',
            f'Closed: {self.is_closed}',
            f'Periodic: {self.is_periodic}',
            f'Rational: {self.is_rational}',
        ]
        return "\n".join(lines)

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self) -> Dict:
        return {
            'points': [point.data for point in self.points],
            'weights': self.weights,
            'knots': self.knots,
            'multiplicities': self.multiplicities,
            'degree': self.degree,
            'is_periodic': self.is_periodic
        }

    @data.setter
    def data(self, data: Dict):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data: Dict) -> 'NurbsCurve':
        """Construct a NURBS curve from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.NurbsCurve`
            The constructed curve.

        """
        points = [Point.from_data(point) for point in data['points']]
        weights = data['weights']
        knots = data['knots']
        multiplicities = data['multiplicities']
        degree = data['degree']
        is_periodic = data['is_periodic']
        return NurbsCurve.from_parameters(points, weights, knots, multiplicities, degree, is_periodic)

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_parameters(cls,
                        points: List[Point],
                        weights: List[float],
                        knots: List[float],
                        multiplicities: List[int],
                        degree: int,
                        is_periodic: bool = False) -> 'NurbsCurve':
        """Construct a NURBS curve from explicit curve parameters."""
        raise NotImplementedError

    @classmethod
    def from_points(cls, points: List[Point], degree: int = 3) -> 'NurbsCurve':
        """Construct a NURBS curve from control points.

        This construction method is similar to the method ``Create`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/M_Rhino_Geometry_NurbsCurve_Create.htm

        """
        raise NotImplementedError

    @classmethod
    def from_interpolation(cls, points: List[Point], precision: float = 1e-3) -> 'NurbsCurve':
        """Construct a NURBS curve by interpolating a set of points.

        This construction method is similar to the method ``CreateHSpline`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateHSpline.htm

        """
        raise NotImplementedError

    @classmethod
    def from_step(cls, filepath: str) -> 'NurbsCurve':
        """Load a NURBS curve from an STP file."""
        raise NotImplementedError

    @classmethod
    def from_arc(cls, arc):
        raise NotImplementedError

    @classmethod
    def from_circle(cls, circle: Circle) -> 'NurbsCurve':
        """Construct a NURBS curve from a circle.

        This construction method is similar to the method ``CreateFromCircle`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateFromCircle.htm

        """
        frame = Frame.from_plane(circle.plane)
        w = 0.5 * sqrt(2)
        dx = frame.xaxis * circle.radius
        dy = frame.yaxis * circle.radius
        points = [
            frame.point - dy,
            frame.point - dy - dx,
            frame.point - dx,
            frame.point + dy - dx,
            frame.point + dy,
            frame.point + dy + dx,
            frame.point + dx,
            frame.point - dy + dx,
            frame.point - dy
        ]
        knots = [0, 1/4, 1/2, 3/4, 1]
        mults = [3, 2, 2, 2, 3]
        weights = [1, w, 1, w, 1, w, 1, w, 1]
        return cls.from_parameters(
            points=points, weights=weights, knots=knots, multiplicities=mults, degree=2
        )

    @classmethod
    def from_ellipse(cls, ellipse):
        """Construct a NURBS curve from an ellipse.

        This construction method is similar to the method ``CreateFromEllipse`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateFromEllipse.htm

        """
        frame = Frame.from_plane(ellipse.plane)
        frame = Frame.worldXY()
        w = 0.5 * sqrt(2)
        dx = frame.xaxis * ellipse.major
        dy = frame.yaxis * ellipse.minor
        points = [
            frame.point - dy,
            frame.point - dy - dx,
            frame.point - dx,
            frame.point + dy - dx,
            frame.point + dy,
            frame.point + dy + dx,
            frame.point + dx,
            frame.point - dy + dx,
            frame.point - dy
        ]
        knots = [0, 1/4, 1/2, 3/4, 1]
        mults = [3, 2, 2, 2, 3]
        weights = [1, w, 1, w, 1, w, 1, w, 1]
        return cls.from_parameters(
            points=points, weights=weights, knots=knots, multiplicities=mults, degree=2
        )

    @classmethod
    def from_line(cls, line):
        """Construct a NURBS curve from a line.

        This construction method is similar to the method ``CreateFromLine`` of the Rhino API for NURBS curves [1]_.

        References
        ----------
        .. [1] https://developer.rhino3d.com/api/RhinoCommon/html/Overload_Rhino_Geometry_NurbsCurve_CreateFromLine.htm

        """
        return cls.from_parameters(
            points=[line.start, line.end],
            weights=[1.0, 1.0],
            knots=[0.0, 1.0],
            multiplicities=[2, 2],
            degree=1
        )

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_step(self, filepath: str, schema: str = "AP203") -> None:
        """Write the curve geometry to a STP file."""
        raise NotImplementedError

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self) -> List[Point]:
        raise NotImplementedError

    @property
    def weights(self) -> List[float]:
        raise NotImplementedError

    @property
    def knots(self) -> List[float]:
        raise NotImplementedError

    @property
    def knotsequence(self) -> List[float]:
        raise NotImplementedError

    @property
    def multiplicities(self) -> List[int]:
        raise NotImplementedError

    @property
    def degree(self) -> int:
        raise NotImplementedError

    @property
    def dimension(self):
        raise NotImplementedError

    @property
    def domain(self):
        raise NotImplementedError

    @property
    def order(self):
        return self.degree + 1

    @property
    def start(self) -> Point:
        raise NotImplementedError

    @property
    def end(self) -> Point:
        raise NotImplementedError

    @property
    def is_closed(self) -> bool:
        raise NotImplementedError

    @property
    def is_periodic(self) -> bool:
        raise NotImplementedError

    @property
    def is_rational(self) -> bool:
        raise NotImplementedError

    @property
    def bounding_box(self):
        raise NotImplementedError

    @property
    def length(self):
        raise NotImplementedError

    # ==============================================================================
    # Methods
    # ==============================================================================

    def copy(self) -> 'NurbsCurve':
        """Make an independent copy of the current curve."""
        return NurbsCurve.from_parameters(
            self.points,
            self.weights,
            self.knots,
            self.multiplicities,
            self.degree,
            self.is_periodic
        )

    def transform(self, T: Transformation) -> None:
        """Transform this curve."""
        raise NotImplementedError

    def transformed(self, T: Transformation) -> 'NurbsCurve':
        """Transform a copy of the curve."""
        copy = self.copy()
        copy.transform(T)
        return copy

    def space(self, n: int = 10) -> List[float]:
        """Compute evenly spaced parameters over the curve domain."""
        u, v = self.domain
        return linspace(u, v, n)

    def xyz(self, n: int = 10) -> List[Point]:
        """Compute point locations corresponding to evenly spaced parameters over the curve domain."""
        return [self.point_at(param) for param in self.space(n)]

    def locus(self, resolution=100):
        """Compute the locus of all points on the curve.

        Parameters
        ----------
        resolution : int
            The number of intervals at which a point on the
            curve should be computed. Defaults to 100.

        Returns
        -------
        list
            Points along the curve.
        """
        return self.xyz(resolution)

    def point_at(self, u: float) -> Point:
        """Compute a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Point
            the corresponding point on the curve.
        """
        raise NotImplementedError

    def tangent_at(self, t):
        """Compute the tangent vector at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Vector
            The corresponding tangent vector.

        """
        pass

    def curvature_at(self, t):
        """Compute the curvature at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Vector
            The corresponding curvature vector.

        """
        raise NotImplementedError

    def frame_at(self, t):
        """Compute the local frame at a point on the curve.

        Parameters
        ----------
        t : float
            The value of the curve parameter. Must be between 0 and 1.

        Returns
        -------
        Frame
            The corresponding local frame.

        """
        raise NotImplementedError

    def closest_point(self, point, distance=None):
        """Compute the closest point on the curve to a given point."""
        raise NotImplementedError

    def divide_by_count(self, count):
        """Divide the curve into a specific number of equal length segments."""
        raise NotImplementedError

    def divide_by_length(self, length):
        """Divide the curve into segments of specified length."""
        raise NotImplementedError

    def fair(self):
        raise NotImplementedError
