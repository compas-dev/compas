""""""

try:
    import scriptcontext as sc

    find_object = sc.doc.Objects.Find

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2016, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


class RhinoPoint(object):
    """"""

    def __init__(self, guid):
        self.guid = guid
        self.point = find_object(guid)
        self.geometry = self.point.Geometry
        self.attributes = self.point.Attributes
        self.otype = self.geometry.ObjectType

    def closest_point(self, point, maxdist=None):
        loc = self.geometry.Location
        return (loc.X, loc.Y, loc.Z)

    def closest_points(self, points, maxdist=None):
        return [self.closest_point(point, maxdist) for point in points]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
