from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

try:
    from numpy import array
    from numpy import asarray
    from numpy import argmax
    from numpy import argmin
    from numpy import dot
    from numpy import ptp
    from numpy import sum

    from scipy.spatial import ConvexHull

except ImportError:
    compas.raise_if_not_ironpython()

from compas.geometry import local_axes
from compas.geometry import local_coords_numpy
from compas.geometry import global_coords_numpy


__all__ = [
    'oriented_bounding_box_numpy',
    'oriented_bounding_box_xy_numpy',
]


def oriented_bounding_box_numpy(points):
    """Compute the oriented minimum bounding box of a set of points in 3D space.

    Notes
    -----
    The implementation is based on the convex hull of the points.

    Parameters
    ----------
    points : list
        XYZ coordinates of the points.

    Returns
    -------
    3-tuple
        1. The convex hull of the points.
        2. The coordinates of the bounding box.
        3. The volume of the box.

    Examples
    --------
    .. plot::
        :include-source:

        from numpy.random import randint
        from numpy.random import rand

        import matplotlib.pyplot as plt

        from compas.plotters import Bounds
        from compas.plotters import Cloud3D
        from compas.plotters import Box
        from compas.plotters import create_axes_3d
        from compas.geometry import matrix_from_axis_and_angle
        from compas.geometry import transform_points
        from compas.geometry import oriented_bounding_box_numpy

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

            R = matrix_from_axis_and_angle(d, a)
            cloud[:] = transform_points(cloud, R)

            clouds.append(cloud.tolist())

        axes = create_axes_3d()

        bounds = Bounds([point for points in clouds for point in points])
        bounds.plot(axes)

        for cloud in clouds:
            bbox = oriented_bounding_box_numpy(cloud)

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
        uvw = local_axes(abc[0], abc[1], abc[2])
        xyz = points[hull.vertices]
        rst = local_coords_numpy(abc[0], uvw, xyz)
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
            bbox = global_coords_numpy(abc[0], uvw, bbox)
            volume = v

    return hull, bbox, volume


def oriented_bounding_box_xy_numpy(points):
    """Compute the oriented minimum bounding box of set of points in the XY plane.

    Notes
    -----
    The *oriented (minimum) bounding box* (OBB) is computed using the following
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

    Parameters
    ----------
    points : list
        XY(Z) coordinates of the points.

    Returns
    -------
    2-tuple
        1. The coordinates of the corners of the bounding box.
        2. The area of the box.

    Examples
    --------
    .. code-block:: python

        #

    """
    points = asarray(points)
    n, dim = points.shape

    assert 1 < dim, "The point coordinates should be at least 2D: %i" % dim

    points = points[:, :2]

    hull = ConvexHull(points)
    xy_hull = points[hull.vertices].reshape((-1, 2))

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
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
