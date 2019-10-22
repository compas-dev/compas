from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
from compas_rhino.artists import Artist
from compas_rhino.geometry import RhinoPoint
import compas_rhino


__all__ = ["PointArtist"]


class PointArtist(Artist):
    """A point artist defines functionality for visualising a COMPAS point in Rhino.
    """

    __module__ = "compas_rhino.artists"

    def __init__(self, point=None, attributes=None, layer=None):

        if not isinstance(point, Point):
            raise ValueError("needs a compas.geometry.Point")

        super(PointArtist, self).__init__(point, attributes=attributes, layer=layer)

        self.GUID = self.create_point()

        self.rhino_point = RhinoPoint(self.GUID)

    @property
    def point(self):
        """get the compas point geometry in this artist's local coordinate"""
        return self.geometry

    def create_point(self):
        """create the mirror of the point in Rhino, returns its GUID"""
        if self.attributes:
            point_dict = self.attributes.copy()
        else:
            point_dict = {}
        point_dict['pos'] = self.point[:3]

        return compas_rhino.draw_points([point_dict], layer=self.layer, redraw=False)[0]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas_rhino.utilities import unload_modules

    unload_modules("compas")
    unload_modules("compas_rhino")

    from compas.geometry import Rotation
    import math

    # create with Point
    pa = PointArtist(Point(10, 0, 0))

    # create with Point with attributes
    pa2 = PointArtist(Point(-10, 0, 0), attributes={'color': (255, 0, 0)})
    pa.add(pa2)

    # adding directly point with auto-wraped artist
    pa.add(Point(0, 10, 0), attributes={'color': (0, 255, 0)})

    R = Rotation.from_axis_and_angle([0, 0, 1], math.pi / 40)

    for i in range(0, 20):
        pa.apply_transformation(R)
        pa.draw(0.1)

    print('finished!')
