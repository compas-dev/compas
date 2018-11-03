from compas_blender.geometry import BlenderGeometry
from compas_blender.utilities import select_point


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['BlenderPoint']


class BlenderPoint(BlenderGeometry):
    """"""

    def __init__(self, object):
        self.guid = object.name
        self.object = object
        self.geometry = self.object.data
        self.attributes = {}
        self.type = self.object.type

    @classmethod
    def from_selection(cls):
        object = select_point()
        return cls(object)

    @property
    def xyz(self):
        return list(self.object.location)

    def hide(self):
        self.object.hide = True

    def show(self):
        self.object.hide = False

    def select(self):
        self.object.select = True

    def unselect(self):
        self.object.select = False

    def closest_point(self, point, maxdist=None):
        return self.xyz

    def closest_points(self, points, maxdist=None):
        return [self.closest_point(point, maxdist) for point in points]

    def project_to_curve(self, curve, direction=(0, 0, 1)):
        raise NotImplementedError

    def project_to_surface(self, surface, direction=(0, 0, 1)):
        raise NotImplementedError

    def project_to_mesh(self, mesh, direction=(0, 0, 1)):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    point = BlenderPoint.from_selection()

    print(point.guid)
    print(point.object)
    print(point.geometry)
    print(point.attributes)
    print(point.type)
    print(point.xyz)
    
    point.hide()
    point.show()
    point.unselect()
    point.select()
    