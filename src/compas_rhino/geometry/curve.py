from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

from compas.geometry import Line
from compas.geometry import Polyline
from compas.geometry import Polygon
from compas.geometry import Circle

from compas_rhino.geometry import RhinoGeometry

if compas.IPY:
    import Rhino


__all__ = ['RhinoCurve']


class RhinoCurve(RhinoGeometry):
    """Wrapper for Rhino curves.

    Parameters
    ----------
    guid : str or System.Guid
        The GUID of the Rhino curve object.

    Examples
    --------
    >>>
    """

    __module__ = 'compas_rhino.geometry'

    def __init__(self, guid):
        super(RhinoCurve, self).__init__(guid)

    @classmethod
    def from_selection(cls):
        """Create a ``RhinoCurve`` instance from a selected Rhino curve.

        Returns
        -------
        RhinoCurve
            A convenience wrapper around the Rhino curve object.
        """
        guid = compas_rhino.select_curve()
        return cls(guid)

    @property
    def start(self):
        return self.geometry.PointAtStart

    @property
    def end(self):
        return self.geometry.PointAtEnd

    @property
    def points(self):
        # https://github.com/mcneel/rhinoscriptsyntax/blob/a131bcbd6761b1346921fcb150f6b776140e4a0e/Scripts/rhinoscript/curve.py#L2044
        return compas_rhino.rs.CurvePoints(self.guid)

    def to_compas(self):
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
        return self.is_polyline() and self.is_closed()

    def is_circle(self):
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
        return rs.IsCurveClosed(self.guid)

    # def length(self):
    #     """Return the length of the curve.

    #     Returns
    #     -------
    #     float
    #         The curve's length.
    #     """
    #     return rs.CurveLength(self.guid)

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

    # def space(self, density):
    #     space = []
    #     density = int(density)
    #     if rs.IsCurve(self.guid):
    #         domain = rs.CurveDomain(self.guid)
    #         u = (domain[1] - domain[0]) / (density - 1)
    #         for i in range(density):
    #             space.append(domain[0] + u * i)
    #     elif rs.IsPolyCurve(self.guid):
    #         rs.EnableRedraw(False)
    #         segments = rs.ExplodeCurves(self.guid)
    #         for segment in segments:
    #             domain = rs.CurveDomain(segment)
    #             u = (domain[1] - domain[0]) / (density - 1)
    #             for i in range(density):
    #                 space.append(domain[0] + u * i)
    #         rs.DeleteObjects(segments)
    #         rs.EnableRedraw(True)
    #     else:
    #         raise Exception('Object is not a curve.')
    #     return space

    # def heightfield(self, density):
    #     heightfield = []
    #     space = self.space(density)
    #     if space:
    #         xyz = [rs.EvaluateCurve(self.guid, param) for param in space]
    #         heightfield = map(list, xyz)
    #     return heightfield

    # def curvature(self):
    #     raise NotImplementedError

    # def tangents(self, points):
    #     tangents = []
    #     if rs.IsPolyCurve(self.guid):
    #         pass
    #     elif rs.IsCurve(self.guid):
    #         for point in points:
    #             param = rs.CurveClosestPoint(self.guid, point)
    #             vector = list(rs.CurveTangent(self.guid, param))
    #             tangents.append(vector)
    #     else:
    #         raise Exception('Object is not a curve.')
    #     return tangents

    # def descent(self, points):
    #     tangents = self.tangents(points)
    #     tangents = [
    #         (point, vector) if vector[2] < 0 else (point, [-v for v in vector])
    #         for point, vector in zip(points, tangents)
    #     ]
    #     return tangents

    # def divide(self, number_of_segments, over_space=False):
    #     points = []
    #     rs.EnableRedraw(False)
    #     if over_space:
    #         space = self.space(number_of_segments + 1)
    #         if space:
    #             points = [list(rs.EvaluateCurve(self.guid, param)) for param in space]
    #     else:
    #         points = rs.DivideCurve(self.guid, number_of_segments, create_points=False, return_points=True)
    #         points[:] = map(list, points)
    #     rs.EnableRedraw(True)
    #     return points

    # def divide_length(self, length_of_segments):
    #     rs.EnableRedraw(False)
    #     points = rs.DivideCurveLength(self.guid, length_of_segments, create_points=False, return_points=True)
    #     points[:] = map(list, points)
    #     rs.EnableRedraw(True)
    #     return points

    # def closest_point(self, point, maxdist=None, return_param=False):
    #     maxdist = maxdist or 0.0
    #     rc, t = self.geometry.ClosestPoint(Point3d(*point), maxdist)
    #     x, y, z = list(self.geometry.PointAt(t))
    #     if not return_param:
    #         return x, y, z
    #     return x, y, z, t

    # def closest_points(self, points, maxdist=None):
    #     return [self.closest_point(point, maxdist) for point in points]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    curve = RhinoCurve.from_selection()

    print(curve.is_line())
    print(curve.to_compas())
