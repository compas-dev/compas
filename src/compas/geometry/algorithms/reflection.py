from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math

from copy import deepcopy

from compas.geometry.basic import add_vectors
from compas.geometry.basic import add_vectors_xy
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy

from compas.geometry.angles import angle_vectors

from compas.geometry.intersections import intersection_line_plane
from compas.geometry.intersections import intersection_line_triangle

from compas.geometry.orientation import normal_triangle


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    # 'reflect_point_plane',
    # 'reflect_points_plane',

    # 'reflect_point_triangle',
    # 'reflect_points_triangle',
]


def reflect_line_plane(line, plane, epsilon=1e-6):
    """Reflects a line at plane.

    Parameters:
        line (tuple): Two points defining the line.
        plane (tuple): The base point and normal (normalized) defining the plane.

    Returns:
        line (tuple): The reflected line starting at the reflection point on the plane,
        None otherwise.

    Notes:
        The directions of the line and plane are important! The line will only be
        reflected if it points (direction start -> end) in the direction of the plane
        and if the line intersects with the front face of the plane (normal direction
        of the plane).
        For more info, see [1]_.

    References:
        .. [1] Math Stack Exchange. *How to get a reflection vector?*
               Available at: https://math.stackexchange.com/questions/13261/how-to-get-a-reflection-vector.

    Examples:

        .. code-block:: python

            from math import pi, sin, cos, radians

            from compas.geometry import rotate_points
            from compas.geometry import intersection_line_plane
            from compas.geometry import reflect_line_plane

            # planes
            mirror_plane = [(0.0, 0.0, 0.0),(1.0, 0.0, 0.0)]
            projection_plane = [(40.0, 0.0, 0.0),(1.0, 0.0, 0.0)]

            # initial line (starting laser ray)
            line = [(30., 0.0, -10.0),(0.0, 0.0, 0.0)]

            dmax = 75 # steps (resolution)
            angle = radians(12)  # max rotation of mirror plane in degrees
            axis_z = [0.0, 0.0, 1.0] # rotation z-axis of mirror plane
            axis_y = [0.0, 1.0, 0.0] # rotation y-axis of mirror plane

            polyline_projection = []
            for i in range(dmax):
                plane_norm = rotate_points([mirror_plane[1]], axis_z, angle * math.sin(i / dmax * 2 * pi))[0]
                plane_norm = rotate_points([plane_norm], axis_y, angle * math.sin(i / dmax * 4 * pi))[0]
                reflected_line = reflect_line_plane(line, [mirror_plane[0],plane_norm])
                if not reflected_line:
                    continue
                intx_pt = intersection_line_plane(reflected_line,projection_plane)
                if intx_pt:
                    polyline_projection.append(intx_pt)

            print(polyline_projection)


    Notes:
        This example visualized in Rhino:


    .. image:: /_images/reflect_line_plane.*

    """
    intx_pt = intersection_line_plane(line, plane, epsilon)
    if not intx_pt:
        return None
    vec_line = subtract_vectors(line[1], line[0])
    vec_reflect = mirror_vector_vector(vec_line, plane[1])
    if angle_vectors(plane[1], vec_reflect) > 0.5 * math.pi:
        return None
    return [intx_pt, add_vectors(intx_pt, vec_reflect)]


def reflect_line_triangle(line, triangle, epsilon=1e-6):
    """Reflects a line at a triangle.

    Parameters:
        line (tuple): Two points defining the line.
        triangle (sequence of sequence of float): XYZ coordinates of the triangle corners.

    Returns:
        line (tuple): The reflected line starting at the reflection point on the plane,
        None otherwise.

    Notes:
        The directions of the line and triangular face are important! The line will only be
        reflected if it points (direction start -> end) in the direction of the triangular
        face and if the line intersects with the front face of the triangular face (normal
        direction of the face).

    Examples:

        .. code-block:: python

            # tetrahedron points
            pt1 = (0.0, 0.0, 0.0)
            pt2 = (6.0, 0.0, 0.0)
            pt3 = (3.0, 5.0, 0.0)
            pt4 = (3.0, 2.0, 4.0)

            # triangular tetrahedron faces
            tris = []
            tris.append([pt4,pt2,pt1])
            tris.append([pt4,pt3,pt2])
            tris.append([pt4,pt1,pt3])
            tris.append([pt1,pt2,pt3])

            # initial line (starting ray)
            line = [(1.0,1.0,0.0),(1.0,1.0,1.0)]

            # start reflection cycle inside the prism
            polyline = []
            polyline.append(line[0])
            for i in range(10):
                for tri in tris:
                    reflected_line = reflect_line_triangle(line, tri)
                    if reflected_line:
                        line = reflected_line
                        polyline.append(line[0])
                        break

            print(polyline)


    .. figure:: /_images/reflect_line_triangle.*
        :figclass: figure
        :class: figure-img img-fluid

    """
    intx_pt = intersection_line_triangle(line, triangle, epsilon)
    if not intx_pt:
        return None
    vec_line = subtract_vectors(line[1], line[0])
    vec_normal = normal_triangle(triangle, unitized=True)
    vec_reflect = mirror_vector_vector(vec_line, vec_normal)
    if angle_vectors(vec_normal, vec_reflect) > 0.5 * math.pi:
        return None
    return [intx_pt, add_vectors(intx_pt, vec_reflect)]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
