from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import scriptcontext as sc

import compas_rhino

from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Circle

from ._geometry import BaseRhinoGeometry


__all__ = ['RhinoCurve']


class RhinoCurve(BaseRhinoGeometry):
    """Wrapper for Rhino curve objects.

    Parameters
    ----------
    None

    Attributes
    ----------
    start (read-only) : Rhino.Geometry.Point3d
        The start point of the curve.
    end (read-only) : Rhino.Geometry.Point3d
        The end point of the curve.
    points (read-only) : list of RhinoGeometry.Point3d
        List of points between start and end, defining the geometry of the curve.

    Examples
    --------
    >>> rhinocurve = RhinoCurve.from_guid(guid)
    >>> curve = rhinocurve.to_compas()
    >>> if rhinocurve.is_line():
    ...     isinstance(curve, compas.geometry.Line)
    ...
    True
    >>> if rhinocurve.is_polyline():
    ...     isinstance(curve, compas.geometry.Polyline)
    ...
    True
    """

    def __init__(self):
        super(RhinoCurve, self).__init__()

    @property
    def start(self):
        return self.geometry.PointAtStart

    @property
    def end(self):
        return self.geometry.PointAtEnd

    @property
    def points(self):
        return compas_rhino.rs.CurvePoints(self.guid)

    @classmethod
    def from_geometry(cls, geometry):
        raise NotImplementedError

    @classmethod
    def from_selection(cls):
        """Construct a curve wrapper by selecting an existing Rhino curve object.

        Parameters
        ----------
        None

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoCurve`
            The wrapped curve.
        """
        guid = compas_rhino.select_curve()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert the curve to an equivalent geometry object.

        Returns
        -------
        :class:`compas.geometry.Line`
            If the curve is a line (if it is a linear segment between two points).
        :class:`compas.geometry.Polyline`
            If the curve is a polyline (if it is comprised of multiple line segments).
        :class:`compas.geometry.Circle`
            If the curve is a circle.

        """
        if self.is_line():
            return Line(self.start, self.end)
        if self.is_polyline():
            return Polyline(self.points)
        if self.is_circle():
            success, circle = self.geometry.TryGetCircle()
            if not success:
                raise Exception("not a circle")
            plane = circle.Plane
            center = plane.Origin
            normal = plane.Normal
            radius = circle.Radius
            return Circle([center, normal], radius)

    def is_line(self):
        """Determine if the curve is a line.

        Returns
        -------
        bool
            True if the curve is a line.
            False otherwise.

        Notes
        -----
        A curve is a line if it is a linear segment between two points.
        """
        if self.geometry.Degree != 1:
            return False
        if isinstance(self.geometry, Rhino.Geometry.LineCurve):
            return True
        success, polyline = self.geometry.TryGetPolyline()
        return success and polyline.Count == 2

    def is_polyline(self):
        """Determine if the curve is a polyline.

        Returns
        -------
        bool
            True if the curve is a polyline.
            False otherwise.

        Notes
        -----
        A curve is a polyline if it consists of linear segments between a sequence of points.
        """
        if self.geometry.Degree != 1:
            return False
        if isinstance(self.geometry, Rhino.Geometry.PolylineCurve):
            return True
        success, polyline = self.geometry.TryGetPolyline()
        return success and polyline.Count >= 2

    def is_polygon(self):
        """Determine if the curve is the boundary of a polygon.

        Returns
        -------
        bool
            True if the curve is a polygon.
            False otherwise.

        Notes
        -----
        A curve is a polygon if it consists of linear segments between a sequence of points,
        without self-intersections and if it is closed.
        """
        return self.is_polyline() and self.is_closed()

    def is_circle(self):
        """Determine if the curve is a circle.

        Returns
        -------
        bool
            True if the curve is a polygon.
            False otherwise.
        """
        return self.geometry.IsCircle()

    def is_nurbs(self):
        raise NotImplementedError

    def is_closed(self):
        """Assess if the curve is closed.

        Returns
        -------
        bool
            True if the curve is closed.
            False otherwise.
        """
        return compas_rhino.rs.IsCurveClosed(self.guid)

    def length(self):
        """Return the length of the curve.

        Returns
        -------
        float
            The curve's length.
        """
        return compas_rhino.rs.CurveLength(self.guid)

    def space(self, n):
        """Construct a list of parameter values along the curve's parameter space.

        Parameters
        ----------
        n : {2, 3, ...}
            The number of parameter values in the list.
            Minimum is ``2``.

        Raises
        ------
        ValueError
            If the number of requested parameters is smaller than 2.

        Returns
        -------
        list
            A list of parameter values in the curve's parameter space between its start and end.
            The number of values in the list is equal to ``n``.

        Notes
        -----
        If the curve is a polycurve, ``n`` values are returned per segment.
        """
        space = []
        n = int(n)
        if n < 2:
            raise ValueError("The number of parameters should be at least two: {}".format(n))
        if compas_rhino.rs.IsCurve(self.guid):
            domain = compas_rhino.rs.CurveDomain(self.guid)
            du = (domain[1] - domain[0]) / (n - 1)
            for i in range(n):
                space.append(domain[0] + i * du)
        elif compas_rhino.rs.IsPolyCurve(self.guid):
            compas_rhino.rs.EnableRedraw(False)
            segments = compas_rhino.rs.ExplodeCurves(self.guid)
            for segment in segments:
                domain = compas_rhino.rs.CurveDomain(segment)
                du = (domain[1] - domain[0]) / (n - 1)
                for i in range(n):
                    space.append(domain[0] + i * du)
            compas_rhino.rs.DeleteObjects(segments)
            compas_rhino.rs.EnableRedraw(True)
        else:
            raise Exception('Object is not a curve.')
        return space

    def divide(self, number_of_segments, over_space=False):
        """Divide the curve into a numer of segments.

        Parameters
        ----------
        number_of_segments : int
            The number of curve segments after division.
        over_space : bool, optional
            Use the parameter space to divide the curve.
            Default is ``False``.

        Returns
        -------
        list
            A list of point locations.
        """
        points = []
        compas_rhino.rs.EnableRedraw(False)
        if over_space:
            space = self.space(number_of_segments + 1)
            if space:
                points = [list(compas_rhino.rs.EvaluateCurve(self.guid, param)) for param in space]
        else:
            points = compas_rhino.rs.DivideCurve(self.guid, number_of_segments, create_points=False, return_points=True)
            points[:] = map(list, points)
        compas_rhino.rs.EnableRedraw(True)
        return points

    def divide_length(self, length_of_segments):
        """Divide a curve into segments of specific length.

        Parameters
        ----------
        length_of_segments : float
            The length of each segment.

        Returns
        -------
        list
            A list of point locations.
        """
        compas_rhino.rs.EnableRedraw(False)
        points = compas_rhino.rs.DivideCurveLength(self.guid, length_of_segments, create_points=False, return_points=True)
        points[:] = map(list, points)
        compas_rhino.rs.EnableRedraw(True)
        return points

    def closest_point(self, point, maxdist=0.0, return_param=False):
        """Compute the closest point on a curve to a point in space.

        Parameters
        ----------
        point : point
            A point location.
        maxdist : float, optional
            The maximum distance between the point on the curve and the curve.
            Default is ``0.0``.
        return_param : bool, optional
            Return not only the point coordinates, but also the parameter of the point on the curve.
            Default is ``False``.

        Returns
        -------
        list
            The XYZ coordinates of the closest point, if ``return_param`` is ``False``.
            The XYZ coordinates of the closest point and the curve parameter, if ``return_param`` is ``True``.

        """
        rc, t = self.geometry.ClosestPoint(Rhino.Geometry.Point3d(*point), maxdist)
        x, y, z = list(self.geometry.PointAt(t))
        if not return_param:
            return [x, y, z]
        return [x, y, z, t]

    def closest_points(self, points, maxdist=0.0):
        """Compute the closest points on the curve to a list of point locations.

        Parameters
        ----------
        points : list
            The point locations.
        maxdist : float, optional
            The maximum distance between the closest points and the curve.
            Default is ``0.0``.

        Returns
        -------
        list
            A list of closest point locations.
        """
        return [self.closest_point(point, maxdist) for point in points]

    def tangents(self, points):
        """Compute the curve tangent vectors at specified points on the curve.

        Parameters
        ----------
        points : list
            The points where the tangents should be computed.

        Returns
        -------
        list
            A list of tangent vectors.
        """
        tangents = []
        if compas_rhino.rs.IsPolyCurve(self.guid):
            pass
        elif compas_rhino.rs.IsCurve(self.guid):
            for point in points:
                param = compas_rhino.rs.CurveClosestPoint(self.guid, point)
                vector = list(compas_rhino.rs.CurveTangent(self.guid, param))
                tangents.append(vector)
        else:
            raise Exception('Object is not a curve.')
        return tangents

    def descent(self, points):
        """Compute descent vectors at the specified points.

        Parameters
        ----------
        points : list
            The points where the descent vectors have to be computed.

        Returns
        -------
        list
            A list of descent vectors.
        """
        tangents = self.tangents(points)
        tangents = [
            (point, vector) if vector[2] < 0 else (point, [-v for v in vector])
            for point, vector in zip(points, tangents)
        ]
        return tangents

    def control_points(self):
        """Get the control points of a curve.

        Returns
        -------
        list
            Control point objects.
        """
        return self.object.GetGrips()

    def control_point_coordinates(self):
        """Get the coordinates of the control points of a curve.

        Returns
        -------
        list
            Control point coordinates.
        """
        return [control.CurrentLocation for control in self.control_points()]

    def control_points_on(self):
        """Turn the control points on."""
        self.object.GripsOn = True
        sc.doc.Views.Redraw()

    def control_points_off(self):
        """Turn the control points off."""
        self.object.GripsOn = False
        sc.doc.Views.Redraw()

    def select_control_point(self):
        """Select a control point of the curve.

        Returns
        -------
        GUID
            The id of the selected control point.
        """
        self.control_points_on()
        rc, grip = Rhino.Input.RhinoGet.GetGrip("Select control point.")
        if rc != Rhino.Commands.Result.Success:
            return
        if grip.OwnerId != self.guid:
            return
        grip.Select(True, True)
        sc.doc.Views.Redraw()
        return grip


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
