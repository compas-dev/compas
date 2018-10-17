from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

from compas_rhino.geometry import RhinoGeometry
from compas_rhino.utilities import select_point

try:
    import scriptcontext as sc
    find_object = sc.doc.Objects.Find

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['RhinoPoint']


class RhinoPoint(RhinoGeometry):
    """"""

    def __init__(self, guid):
        super(RhinoPoint, self).__init__(guid)

    @classmethod
    def from_selection(cls):
        """Create a ``RhinoPoint`` instance from a selected Rhino point.

        Returns
        -------
        RhinoPoint
            A convenience wrapper around the Rhino point object.

        """
        guid = select_point()
        return cls(guid)

    @property
    def xyz(self):
        """list : The XYZ coordinates of the point."""
        loc = self.geometry.Location
        return [loc.X, loc.Y, loc.Z]

    def closest_point(self, point, maxdist=None):
        """Find the closest point on the ``RhinoGeometry`` object to a test point.

        Parameters
        ----------
        point : list of float, Rhino.Geometry.Point3d
            The XYZ coordinates of the test point.
        maxdist : float, optional
            The maximum distance between the test point and the closest point on the ``RhinoGeometry`` object.
            Default is ``None``.

        Returns
        -------
        list of float
            The XYZ coordinates of the closest point.

        Examples
        --------
        .. code-block:: python

            #

        """
        return self.xyz

    def closest_points(self, points, maxdist=None):
        """Find the closest points to a list of test points on the ``RhinoGeometry`` object.

        Parameters
        ----------
        points : list of list of float
            The list of test points.
        maxdist : float, optional
            The maximum distance between any of the test points and the corresponding closest points on the ``RhinoGeometry`` object.
            Default is ``None``.

        Returns
        -------
        list of list of float
            The XYZ coordinates of the closest points.

        Examples
        --------
        .. code-block:: python

            #

        """
        return [self.closest_point(point, maxdist) for point in points]

    def project_to_curve(self, curve, direction=(0, 0, 1)):
        pass

    def project_to_surface(self, surface, direction=(0, 0, 1)):
        pass

    def project_to_mesh(self, mesh, direction=(0, 0, 1)):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    point = RhinoPoint.from_selection()

    print(point.guid)
    print(point.object)
    print(point.geometry)
    print(point.attributes)
    print(point.type)
    print(point.xyz)
