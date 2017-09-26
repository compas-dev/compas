from __future__ import print_function

from numpy import array
from numpy import asarray
from numpy import argmax
from numpy import argmin
from numpy import argpartition
from numpy import dot
from numpy import sum
from numpy import ptp

from scipy.linalg import solve

from scipy.spatial import ConvexHull
from scipy.spatial import distance_matrix

from scipy.interpolate import griddata

from compas.geometry import cross_vectors
from compas.geometry import normalize_vector


__author__     = ['Tom Van Mele <vanmelet@ethz.ch>',
                  'Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'closest_points_points',
    'project_points_heightfield',
    'iterative_closest_point',
    'bounding_box_xy',
    'bounding_box'
]


def closest_points_points(points, cloud, threshold=10**7, distances=True, num_nbrs=1):
    """Find the closest points in a point cloud to a set of sample points.

    Note:
        Items in cloud further from items in points than threshold return zero
        distance and will affect the indices returned if not set suitably high.

    Parameters:
        points (array, list): The sample points (n,).
        cloud (array, list): The cloud points to compare to (n,).
        threshold (float): Points are checked within this distance.
        distances (boolean): Return distance matrix.

    Returns:
        list: Indices of the closest points in the cloud per point in points.
        array: Distances between points and closest points in cloud (n x n).

    Examples:
        >>> a = np.random.rand(4, 3)
        >>> b = np.random.rand(4, 3)
        >>> indices, distances = closest_points(a, b, distances=True)
        [1, 2, 0, 3]
        array([[ 1.03821946,  0.66226402,  0.67964346,  0.98877891],
               [ 0.4650432 ,  0.54484186,  0.36158995,  0.60385484],
               [ 0.19562088,  0.73240154,  0.50235761,  0.51439644],
               [ 0.84680233,  0.85390316,  0.72154983,  0.50432293]])
    """
    points = asarray(points).reshape((-1, 3))
    cloud = asarray(cloud).reshape((-1, 3))
    d_matrix = distance_matrix(points, cloud, threshold=threshold)
    if num_nbrs == 1:
        indices = argmin(d_matrix, axis=1)
    else:
        indices = argpartition(d_matrix, num_nbrs, axis=1)
        # indices = d_matrix.argsort(axis=1)[:,:num_nbrs].tolist()
    if distances:
        return indices, d_matrix
    return indices


def project_points_heightfield(points, target, interp='linear', rtype='list'):
    """Project the points vertically onto the target represented by xyz points.

    Note:
        Although points can include z coordinates, they are not used.

    Parameters:
        points (array, list): Points to project (m x 3).
        target (array, list): Projection target as a height-field (n x 3).
        interp (str): Interpolation method 'linear', 'nearest', 'cubic'.
        rtype (str): Return results as 'list' else will be returned as array.

    Returns:
        (list, array): Projected points xyz co-ordinates (m x 3).

    This function uses the xyz data from target points to calculate z values
    via interpolation at the xy co-ordinates in points.
    """
    points = asarray(points).reshape((-1, 3))
    target = asarray(target).reshape((-1, 3))
    t_xy = target[:, 0:2]
    t_z  = target[:, 2]
    p_xy = points[:, 0:2]
    p_z  = griddata(t_xy, t_z, p_xy, method=interp, fill_value=0.0)
    points[:, 2] = p_z
    if rtype == 'list':
        return points.tolist()
    return points


def project_points_plane(points, plane):
    pass


def iterative_closest_point(a, b):
    raise NotImplementedError


def bounding_box_xy(points, plot_hull=False):
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

    if plot_hull:
        plt.plot(xy_hull[:, 0], xy_hull[:, 1], 'b-')
        plt.plot(xy_hull[[-1, 0], 0], xy_hull[[-1, 0], 1], 'b-')

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


def bounding_box(points):
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

            from compas.visualization.plotters.core.helpers import Bounds
            from compas.visualization.plotters.core.helpers import Cloud3D
            from compas.visualization.plotters.core.helpers import Box
            from compas.visualization.plotters.core.drawing import create_axes_3d

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
        uvw = _compute_local_axes(abc[0], abc[1], abc[2])
        xyz = points[hull.vertices]
        rst = _compute_local_coords(abc[0], uvw, xyz)
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
            bbox = _compute_global_coords(abc[0], uvw, bbox)
            volume = v

    return hull, bbox, volume


def _compute_local_axes(a, b, c):
    u = b - a
    v = c - a
    w = cross_vectors(u, v)
    v = cross_vectors(w, u)
    return normalize_vector(u), normalize_vector(v), normalize_vector(w)


def _compute_local_coords(o, uvw, xyz):
    uvw = asarray(uvw).T
    xyz = asarray(xyz).T - asarray(o).reshape((-1, 1))
    rst = solve(uvw, xyz)
    return rst.T


def _compute_global_coords(o, uvw, rst):
    uvw = asarray(uvw).T
    rst = asarray(rst).T
    xyz = uvw.dot(rst) + asarray(o).reshape((-1, 1))
    return xyz.T


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from numpy.random import randint
    from numpy.random import rand

    from scipy.cluster.vq import kmeans
    from scipy.cluster.vq import vq

    import matplotlib.pyplot as plt

    from compas.numerical.xforms import rotation_matrix
    from compas.numerical.transformations import transform

    from compas.visualization.plotters.core.helpers import Bounds
    from compas.visualization.plotters.core.helpers import Box
    from compas.visualization.plotters.core.drawing import create_axes_3d

    clouds = []

    for i in range(8):
        angle = randint(1, high=8) * 10 * 3.14159 / 180
        axis = [1, 1, 1]

        cloud = rand(100, 3)

        if i in (1, 2, 5, 6):
            cloud[:, 0] *= - 10.0
            cloud[:, 0] -= 3.0
            axis[0] = -1
        else:
            cloud[:, 0] *= 10.0
            cloud[:, 0] += 3.0

        if i in (2, 3, 6, 7):
            cloud[:, 1] *= - 3.0
            cloud[:, 1] -= 3.0
            axis[1] = -1
        else:
            cloud[:, 1] *= 3.0
            cloud[:, 1] += 3.0

        if i in (4, 5, 6, 7):
            cloud[:, 2] *= - 6.0
            cloud[:, 2] -= 3.0
            axis[2] = -1
        else:
            cloud[:, 2] *= 6.0
            cloud[:, 2] += 3.0

        R = rotation_matrix(angle, axis)
        cloud[:] = transform(cloud, R)

        clouds.append(cloud.tolist())

    cloud = [point for points in clouds for point in points]

    centroids, _ = kmeans(cloud, 8)
    idx, _ = vq(cloud, centroids)

    print(idx)

    for i, point in zip(idx, cloud):
        print(i, point)

    axes = create_axes_3d()

    x = centroids[:, 0]
    y = centroids[:, 1]
    z = centroids[:, 2]

    axes.plot(x, y, z, 'o', color=(0.0, 1.0, 0.0))

    bounds = Bounds([point for points in clouds for point in points])
    bounds.plot(axes)

    for cloud in clouds:
        cloud = asarray(cloud)
        bbox  = bounding_box_3d(cloud)

        # Cloud3D(cloud).plot(axes)
        Box(bbox[1]).plot(axes)

    plt.show()
