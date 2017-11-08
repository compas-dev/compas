from __future__ import print_function
from __future__ import division

from numpy import array
from numpy import asarray
from numpy import argmax
from numpy import argmin
from numpy import sum
from numpy import dot
from numpy import ptp

from scipy.spatial import ConvexHull


from compas.geometry.transformations import compute_local_axes
from compas.geometry.transformations_num import compute_local_coords_numpy
from compas.geometry.transformations_num import compute_global_coords_numpy


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'bounding_box_numpy',
    'bounding_box_xy_numpy',
]


def bounding_box_numpy(points):
    """Compute the aligned bounding box of a set of points in 3D space.

    Note:
        The implementation is based on the convex hull of the points.

    Parameters:
        points (list): A list of 3D points.

    Returns:
        list: The coordinates of the corners of the bounding box. The list
        can be used to construct a bounding box object for easier plotting.

    Example:

        .. plot::
            :include-source:

            from numpy.random import randint
            from numpy.random import rand

            import matplotlib.pyplot as plt

            from compas.plotters.core.helpers import Bounds
            from compas.plotters.core.helpers import Cloud3D
            from compas.plotters.core.helpers import Box
            from compas.plotters.core.drawing import create_axes_3d

            from compas.numerical.xforms import rotation_matrix
            from compas.numerical.transformations import transform

            from compas.numerical.spatial import bounding_box

            clouds = []

            for i in range(8):
                a = randint(1, high=8) * 10 * 3.14159 / 180
                d = [1, 1, 1]

                cloud = rand(100, 3)

                if i in (1, 2, 5, 6):
                    cloud[:, 0] *= - 10.0
                    cloud[:, 0] -= 3.0
                    d[0] = -1
                else:
                    cloud[:, 0] *= 10.0
                    cloud[:, 0] += 3.0

                if i in (2, 3, 6, 7):
                    cloud[:, 1] *= - 3.0
                    cloud[:, 1] -= 3.0
                    d[1] = -1
                else:
                    cloud[:, 1] *= 3.0
                    cloud[:, 1] += 3.0

                if i in (4, 5, 6, 7):
                    cloud[:, 2] *= - 6.0
                    cloud[:, 2] -= 3.0
                    d[2] = -1
                else:
                    cloud[:, 2] *= 6.0
                    cloud[:, 2] += 3.0

                R = rotation_matrix(a, d)
                cloud[:] = transform(cloud, R)

                clouds.append(cloud.tolist())

            axes = create_axes_3d()

            bounds = Bounds([point for points in clouds for point in points])
            bounds.plot(axes)

            for cloud in clouds:
                bbox = bounding_box(cloud)

                Cloud3D(cloud).plot(axes)
                Box(bbox[1]).plot(axes)

            plt.show()

    """
    points = asarray(points)
    n, dim = points.shape

    assert 2 < dim, "The point coordinates should be at least 3D: %i" % dim

    points = points[:, :3]

    hull = ConvexHull(points)
    volume = None
    bbox = []

    # this can be vectorised!
    for simplex in hull.simplices:
        abc = points[simplex]
        uvw = compute_local_axes(abc[0], abc[1], abc[2])
        xyz = points[hull.vertices]
        rst = compute_local_coords_numpy(abc[0], uvw, xyz)
        dr, ds, dt = ptp(rst, axis=0)
        v = dr * ds * dt

        if volume is None or v < volume:
            rmin, smin, tmin = argmin(rst, axis=0)
            rmax, smax, tmax = argmax(rst, axis=0)
            bbox = [
                [rst[rmin, 0], rst[smin, 1], rst[tmin, 2]],
                [rst[rmax, 0], rst[smin, 1], rst[tmin, 2]],
                [rst[rmax, 0], rst[smax, 1], rst[tmin, 2]],
                [rst[rmin, 0], rst[smax, 1], rst[tmin, 2]],
                [rst[rmin, 0], rst[smin, 1], rst[tmax, 2]],
                [rst[rmax, 0], rst[smin, 1], rst[tmax, 2]],
                [rst[rmax, 0], rst[smax, 1], rst[tmax, 2]],
                [rst[rmin, 0], rst[smax, 1], rst[tmax, 2]],
            ]
            bbox = compute_global_coords_numpy(abc[0], uvw, bbox)
            volume = v

    return hull, bbox, volume


def bounding_box_xy_numpy(points, plot_hull=False):
    """Compute the aligned bounding box of set of points.

    Note:
        The *object-aligned bounding box* (OABB) is computed using the following
        procedure:

            1. Compute the convex hull of the points.
            2. For each of the edges on the hull:
                1. Compute the s-axis as the unit vector in the direction of the edge
                2. Compute the othorgonal t-axis.
                3. Use the start point of the edge as origin.
                4. Compute the spread of the points along the s-axis.
                   (dot product of the point vecor in local coordinates and the s-axis)
                5. Compute the spread along the t-axis.
                6. Determine the side of s on which the points are.
                7. Compute and store the corners of the bbox and its area.
            3. Select the box with the smallest area.

    Parameters:
        points (list): A list of 2D points.

    Returns:
        list: The coordinates of the corners of the bounding box. This list can
              be used to construct a bounding box object to simplify, e.g. plotting.

    Examples:
        >>> from numpy import random
        >>> points = random.rand(100, 2)
        >>> points[:, 0] *= 10.0
        >>> points[:, 1] *= 4.0
        >>> corners, area = BBOX2(points)
    """
    points = asarray(points)
    n, dim = points.shape

    assert 1 < dim, "The point coordinates should be at least 2D: %i" % dim

    points = points[:, :2]

    hull = ConvexHull(points)
    xy_hull = points[hull.vertices].reshape((-1, 2))

    # if plot_hull:
    #     plt.plot(xy_hull[:, 0], xy_hull[:, 1], 'b-')
    #     plt.plot(xy_hull[[-1, 0], 0], xy_hull[[-1, 0], 1], 'b-')

    boxes = []
    m = sum(xy_hull, axis=0) / n

    for simplex in hull.simplices:
        p0 = points[simplex[0]]
        p1 = points[simplex[1]]
        # s direction
        s  = p1 - p0
        sl = sum(s ** 2) ** 0.5
        su = s / sl
        vn = xy_hull - p0
        sc = (sum(vn * s, axis=1) / sl).reshape((-1, 1))
        scmax = argmax(sc)
        scmin = argmin(sc)
        # box corners
        b0 = p0 + sc[scmin] * su
        b1 = p0 + sc[scmax] * su
        # t direction
        t  = array([-s[1], s[0]])
        tl = sum(t ** 2) ** 0.5
        tu = t / tl
        vn = xy_hull - p0
        tc = (sum(vn * t, axis=1) / tl).reshape((-1, 1))
        tcmax = argmax(tc)
        tcmin = argmin(tc)
        # area
        w = sc[scmax] - sc[scmin]
        h = tc[tcmax] - tc[tcmin]
        a = w * h
        # box corners
        if dot(t, m - p0) < 0:
            b3 = b0 - h * tu
            b2 = b1 - h * tu
        else:
            b3 = b0 + h * tu
            b2 = b1 + h * tu
        # box
        boxes.append([[b0, b1, b2, b3], a[0]])

    # return the box with the smallest area
    return min(boxes, key=lambda b: b[1])


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
