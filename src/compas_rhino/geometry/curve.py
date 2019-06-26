from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

from compas_rhino.geometry import RhinoGeometry

try:
    import Rhino
    from Rhino.Geometry import Point3d

    import rhinoscriptsyntax as rs
    import scriptcontext as sc

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['RhinoCurve']


class RhinoCurve(RhinoGeometry):
    """Wrapper for Rhino curves.

    Parameters
    ----------
    guid : str or System.Guid
        The GUID of the Rhino curve object.

    Examples
    --------
    .. code-block:: python

        import compas_rhino

        from compas_rhino.geometry import RhinoCurve

        curve = RhinoCurve(guid)

        points = curve.divide(10)
        tangents = curve.tangents(points)

        for point, vector in zip(points, tangents):
            print point, tangent

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

    def length(self):
        """Return the length of the curve.

        Returns
        -------
        float
            The curve's length.

        """
        return rs.CurveLength(self.guid)

    def is_line(self):
        """Determine if the curve is a line.

        Returns
        -------
        bool
            Tue if the curve is a line.
            False otherwise.

        Notes
        -----
        A curve is a line if it is a linear segment between two points.

        """
        return (rs.IsLine(self.guid) and
                rs.CurveDegree(self.guid) == 1 and
                len(rs.CurvePoints(self.guid)) == 2)

    def is_polyline(self):
        """Determine if the curve is a polyline.

        Returns
        -------
        bool
            Tue if the curve is a polyline.
            False otherwise.

        Notes
        -----
        A curve is a polyline if it consists of linear segments between a sequence of points.

        """
        return (rs.IsPolyline(self.guid) and
                rs.CurveDegree(self.guid) == 1 and
                len(rs.CurvePoints(self.guid)) > 2)

    def is_closed(self):
        """Assess if the curve is closed.

        Returns
        -------
        bool
            True if the curve is closed. False otherwise.

        """

        return rs.IsCurveClosed(self.guid)

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
        self.object.GripsOn = True
        sc.doc.Views.Redraw()

    def control_points_off(self):
        self.object.GripsOn = False
        sc.doc.Views.Redraw()

    def select_control_point(self):
        self.control_points_on()
        rc, grip = Rhino.Input.RhinoGet.GetGrip("Select control point.")
        if rc != Rhino.Commands.Result.Success:
            return
        if grip.OwnerId != self.guid:
            return
        grip.Select(True, True)
        sc.doc.Views.Redraw()
        return grip

    def space(self, density):
        space = []
        density = int(density)
        if rs.IsCurve(self.guid):
            domain = rs.CurveDomain(self.guid)
            u = (domain[1] - domain[0]) / (density - 1)
            for i in range(density):
                space.append(domain[0] + u * i)
        elif rs.IsPolyCurve(self.guid):
            rs.EnableRedraw(False)
            segments = rs.ExplodeCurves(self.guid)
            for segment in segments:
                domain = rs.CurveDomain(segment)
                u = (domain[1] - domain[0]) / (density - 1)
                for i in range(density):
                    space.append(domain[0] + u * i)
            rs.DeleteObjects(segments)
            rs.EnableRedraw(True)
        else:
            raise Exception('Object is not a curve.')
        return space

    def heightfield(self, density):
        heightfield = []
        space = self.space(density)
        if space:
            xyz = [rs.EvaluateCurve(self.guid, param) for param in space]
            heightfield = map(list, xyz)
        return heightfield

    def curvature(self):
        raise NotImplementedError

    def tangents(self, points):
        tangents = []
        if rs.IsPolyCurve(self.guid):
            pass
        elif rs.IsCurve(self.guid):
            for point in points:
                param = rs.CurveClosestPoint(self.guid, point)
                vector = list(rs.CurveTangent(self.guid, param))
                tangents.append(vector)
        else:
            raise Exception('Object is not a curve.')
        return tangents

    def descent(self, points):
        tangents = self.tangents(points)
        tangents = [
            (point, vector) if vector[2] < 0 else (point, [-v for v in vector])
            for point, vector in zip(points, tangents)
        ]
        return tangents

    def divide(self, number_of_segments, over_space=False):
        points = []
        rs.EnableRedraw(False)
        if over_space:
            space = self.space(number_of_segments + 1)
            if space:
                points = [list(rs.EvaluateCurve(self.guid, param)) for param in space]
        else:
            points = rs.DivideCurve(self.guid, number_of_segments, create_points=False, return_points=True)
            points[:] = map(list, points)
        rs.EnableRedraw(True)
        return points

    def divide_length(self, length_of_segments):
        rs.EnableRedraw(False)
        points = rs.DivideCurveLength(self.guid, length_of_segments, create_points=False, return_points=True)
        points[:] = map(list, points)
        rs.EnableRedraw(True)
        return points

    def closest_point(self, point, maxdist=None, return_param=False):
        maxdist = maxdist or 0.0
        rc, t = self.geometry.ClosestPoint(Point3d(*point), maxdist)
        x, y, z = list(self.geometry.PointAt(t))
        if not return_param:
            return x, y, z
        return x, y, z, t

    def closest_points(self, points, maxdist=None):
        return [self.closest_point(point, maxdist) for point in points]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
