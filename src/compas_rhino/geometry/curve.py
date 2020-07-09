from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Circle

from compas_rhino.geometry import RhinoGeometry

if compas.IPY:
    import Rhino


__all__ = ['RhinoCurve']


class RhinoCurve(RhinoGeometry):
    """Wrapper for Rhino curves.

    Parameters
    ----------
    None

    Attributes
    ----------
    start : Rhino.Geometry.Point3d, read-only
        The start point of the curve.
    end : Rhino.Geometry.Point3d, read-only
        The end point of the curve.
    points : list of RhinoGeometry.Point3d, read-only
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
    def from_guid(cls, guid):
        """Construct a curve from the GUID of an existing Rhino curve object.

        Parameters
        ----------
        guid : str
            The GUID of the Rhino curve object.

        Returns
        -------
        curve : compas_rhino.geometry.RhinoCurve
            The wrapped curve.
        """
        obj = compas_rhino.find_object(guid)
        curve = cls()
        curve.guid = obj.Id
        curve.object = obj
        curve.geometry = obj.Geometry
        return curve

    @classmethod
    def from_object(cls, obj):
        """Construct a curve from an existing Rhino curve object.

        Parameters
        ----------
        obj : Rhino.DocObjects.CurveObject
            The Rhino curve object.

        Returns
        -------
        curve : compas_rhino.geometry.RhinoCurve
            The wrapped curve.
        """
        curve = cls()
        curve.guid = obj.Id
        curve.object = obj
        curve.geometry = obj.Geometry
        return curve

    @classmethod
    def from_selection(cls):
        """Construct a curve by selecting an existing Rhino curve object.

        Parameters
        ----------
        None

        Returns
        -------
        curve : compas_rhino.geometry.RhinoCurve
            The wrapped curve.
        """
        guid = compas_rhino.select_curve()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert the curve to an equivalent geometry object.

        Returns
        -------
        compas.geometry.Line
            If the curve is a line (if it is a linear segment between two points).
        compas.geometry.Polyline
            If the curve is a polyline (if it is comprised of multiple line segments).
        compas.geometry.Circle
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

    def space(self, density):
        space = []
        density = int(density)
        if compas_rhino.rs.IsCurve(self.guid):
            domain = compas_rhino.rs.CurveDomain(self.guid)
            u = (domain[1] - domain[0]) / (density - 1)
            for i in range(density):
                space.append(domain[0] + u * i)
        elif compas_rhino.rs.IsPolyCurve(self.guid):
            compas_rhino.rs.EnableRedraw(False)
            segments = compas_rhino.rs.ExplodeCurves(self.guid)
            for segment in segments:
                domain = compas_rhino.rs.CurveDomain(segment)
                u = (domain[1] - domain[0]) / (density - 1)
                for i in range(density):
                    space.append(domain[0] + u * i)
            compas_rhino.rs.DeleteObjects(segments)
            compas_rhino.rs.EnableRedraw(True)
        else:
            raise Exception('Object is not a curve.')
        return space

    def divide(self, number_of_segments, over_space=False):
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
        compas_rhino.rs.EnableRedraw(False)
        points = compas_rhino.rs.DivideCurveLength(self.guid, length_of_segments, create_points=False, return_points=True)
        points[:] = map(list, points)
        compas_rhino.rs.EnableRedraw(True)
        return points

    def closest_point(self, point, maxdist=None, return_param=False):
        maxdist = maxdist or 0.0
        rc, t = self.geometry.ClosestPoint(Rhino.Geometry.Point3d(*point), maxdist)
        x, y, z = list(self.geometry.PointAt(t))
        if not return_param:
            return x, y, z
        return x, y, z, t

    def closest_points(self, points, maxdist=None):
        return [self.closest_point(point, maxdist) for point in points]

    def tangents(self, points):
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

    # def curvature(self):
    #     raise NotImplementedError

    # def descent(self, points):
    #     tangents = self.tangents(points)
    #     tangents = [
    #         (point, vector) if vector[2] < 0 else (point, [-v for v in vector])
    #         for point, vector in zip(points, tangents)
    #     ]
    #     return tangents

    # def control_points(self):
    #     """Get the control points of a curve.

    #     Returns
    #     -------
    #     list
    #         Control point objects.
    #     """
    #     return self.object.GetGrips()

    # def control_point_coordinates(self):
    #     """Get the coordinates of the control points of a curve.

    #     Returns
    #     -------
    #     list
    #         Control point coordinates.
    #     """
    #     return [control.CurrentLocation for control in self.control_points()]

    # def control_points_on(self):
    #     self.object.GripsOn = True
    #     sc.doc.Views.Redraw()

    # def control_points_off(self):
    #     self.object.GripsOn = False
    #     sc.doc.Views.Redraw()

    # def select_control_point(self):
    #     self.control_points_on()
    #     rc, grip = Rhino.Input.RhinoGet.GetGrip("Select control point.")
    #     if rc != Rhino.Commands.Result.Success:
    #         return
    #     if grip.OwnerId != self.guid:
    #         return
    #     grip.Select(True, True)
    #     sc.doc.Views.Redraw()
    #     return grip


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    curve = RhinoCurve.from_selection()

    print(curve.is_line())
    print(curve.to_compas())
