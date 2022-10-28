from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from compas.geometry import Line
from compas.geometry import Circle
from compas.geometry import Ellipse

from ._exceptions import ConversionError

from ._curves import circle_to_rhino_curve
from ._curves import ellipse_to_rhino_curve
from ._curves import line_to_rhino_curve
from ._curves import curve_to_compas_circle
from ._curves import curve_to_compas_ellipse
from ._curves import curve_to_compas_polyline
from ._curves import curve_to_compas_line

from ._geometry import RhinoGeometry


class RhinoCurve(RhinoGeometry):
    """Wrapper for Rhino curves."""

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Set the geometry of the wrapper.

        Parameters
        ----------
        geometry : :rhino:`Rhino_Geometry_Curve` | :class:`~compas.geometry.Line` | :class:`~compas.geometry.Circle` | :class:`~compas.geometry.Ellipse`
            The geometry object defining a curve.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a curve.
        """
        if not isinstance(geometry, Rhino.Geometry.Curve):
            if isinstance(geometry, Line):
                geometry = line_to_rhino_curve(geometry)
            elif isinstance(geometry, Circle):
                geometry = circle_to_rhino_curve(geometry)
            elif isinstance(geometry, Ellipse):
                geometry = ellipse_to_rhino_curve(geometry)
            else:
                raise ConversionError("The geometry cannot be converted to a curve.")
        self._geometry = geometry

    def to_compas(self):
        """Convert the curve to a COMPAS curve.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoNurbsCurve`
        """
        from compas_rhino.geometry import RhinoNurbsCurve

        curve = RhinoNurbsCurve.from_rhino(self.geometry)
        return curve

    def to_compas_circle(self):
        """Convert the curve to a COMPAS circle.

        Returns
        -------
        :class:`~compas.geometry.Circle`
        """
        return curve_to_compas_circle(self.geometry)

    def to_compas_ellipse(self):
        """Convert the curve to a COMPAS ellipse.

        Returns
        -------
        :class:`~compas.geometry.Ellipse`
        """
        return curve_to_compas_ellipse(self.geometry)

    def to_compas_line(self):
        """Convert the curve to a COMPAS line.

        Returns
        -------
        :class:`~compas.geometry.Line`
        """
        return curve_to_compas_line(self.geometry)

    def to_compas_polyline(self):
        """Convert the curve to a COMPAS polyline.

        Returns
        -------
        :class:`~compas.geometry.Polyline`
        """
        return curve_to_compas_polyline(self.geometry)

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
            Default is False.

        Returns
        -------
        list
            The XYZ coordinates of the closest point, if ``return_param`` is False.
            The XYZ coordinates of the closest point and the curve parameter, if ``return_param`` is True.

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
