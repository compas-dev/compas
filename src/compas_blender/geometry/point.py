from compas_blender.geometry import BlenderGeometry


__all__ = [
    'BlenderPoint',
]


class BlenderPoint(BlenderGeometry):

    def __init__(self, obj):
        super().__init__(obj)

    @property
    def xyz(self):
        return self.location

    def closest_point(self, point, maxdist=None):
        raise NotImplementedError

    def closest_points(self, points, maxdist=None):
        raise NotImplementedError

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

    from compas_blender.utilities import get_object_by_name

    o = get_object_by_name(name='Empty')
    point = BlenderPoint(object=o)

    print(point.xyz)
