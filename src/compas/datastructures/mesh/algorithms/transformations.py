""""""

from compas.geometry import scale_points


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['mesh_scale']


def mesh_scale(mesh, scale=1.0):
    points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    points = scale_points(points, scale)
    for index, (key, attr) in enumerate(mesh.vertices(True)):
        x, y, z = points[index]
        attr['x'] = x
        attr['y'] = y
        attr['z'] = z


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
