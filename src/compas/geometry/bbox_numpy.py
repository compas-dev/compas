from numpy import amax
from numpy import amin
from numpy import argmax
from numpy import argmin
from numpy import array
from numpy import asarray
from numpy import dot
from numpy import sum
from numpy import vstack
from numpy import zeros
from scipy.spatial import ConvexHull

from compas.geometry import length_vector
from compas.geometry import local_axes
from compas.geometry import local_to_world_coordinates_numpy
from compas.geometry import pca_numpy
from compas.geometry import world_to_local_coordinates_numpy
from compas.tolerance import TOL

from .bbox import bounding_box


def oriented_bounding_box_numpy(points, tol=None):
    r"""Compute the oriented minimum bounding box of a set of points in 3D space.

    Parameters
    ----------
    points : array_like[point]
        XYZ coordinates of the points.
    tol : float, optional
        Tolerance for evaluating if the length of the local z-axis is (close to) zero.
        In that case, the points are essentially 2D and the minimum area rectangle is computed instead.
        Default is :attr:`TOL.absolute`

    Returns
    -------
    list[[float, float, float]]
        XYZ coordinates of 8 points defining a box.

    Raises
    ------
    ValueError
        If the input data is not 3D.

    See Also
    --------
    :func:`compas.geometry.bounding_box`
    :func:`compas.geometry.oriented_bounding_box_xy_numpy`

    Examples
    --------
    Generate a random set of points with
    :math:`x \in [0, 10]`, :math:`y \in [0, 1]` and :math:`z \in [0, 3]`.
    Add the corners of the box such that we now the volume is supposed to be :math:`30.0`.

    >>> points = np.random.rand(10000, 3)
    >>> bottom = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]])
    >>> top = np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 1.0]])
    >>> points = np.concatenate((points, bottom, top))
    >>> points[:, 0] *= 10
    >>> points[:, 2] *= 3

    Rotate the points around an arbitrary axis by an arbitrary angle.

    >>> from compas.geometry import Rotation
    >>> from compas.geometry import transform_points_numpy
    >>> R = Rotation.from_axis_and_angle([1.0, 1.0, 0.0], 0.3 * 3.14159)
    >>> points = transform_points_numpy(points, R)

    Compute the volume of the oriented bounding box.

    >>> from compas.geometry import length_vector, subtract_vectors, close
    >>> bbox = oriented_bounding_box_numpy(points)
    >>> a = length_vector(subtract_vectors(bbox[1], bbox[0]))
    >>> b = length_vector(subtract_vectors(bbox[3], bbox[0]))
    >>> c = length_vector(subtract_vectors(bbox[4], bbox[0]))
    >>> close(a * b * c, 30.0)
    True

    """
    points = asarray(points)
    n, dim = points.shape

    if dim != 3:
        raise ValueError("The point coordinates should be 3D: %i" % dim)

    points = points[:, :3]

    mean, vectors, values = pca_numpy(points)
    frame = mean, vectors[0], vectors[1]

    if TOL.is_zero(values[2], tol):
        # the points are essentially 2D
        # therefore compute the minimum area rectangle instead of the minimum volume box
        # also compute the axis aligned bounding box
        # and compare the areas of the two

        points = world_to_local_coordinates_numpy(frame, points)
        rect1, area1 = minimum_area_rectangle_xy(points, return_size=True)
        rect2 = bounding_box(points)[:4]
        area2 = (rect2[1][0] - rect2[0][0]) * (rect2[3][1] - rect2[0][1])

        if area1 < area2:
            rect = [[pt[0], pt[1], 0.0] for pt in rect1]
            bbox = local_to_world_coordinates_numpy(frame, rect)
            bbox = vstack((bbox, bbox)).tolist()
        else:
            rect = [[pt[0], pt[1], 0.0] for pt in rect2]
            bbox = local_to_world_coordinates_numpy(frame, rect)
            bbox = vstack((bbox, bbox)).tolist()

        # return a box with identical top and bottom faces
        return bbox

    # the points are truly 3D
    # therefore compute the minimum volume box instead of the minimum area rectangle
    # also compute the axis aligned bounding box
    # and compare the volumes of the two

    box1, volume1 = minimum_volume_box(points, return_size=True)

    points = world_to_local_coordinates_numpy(frame, points)
    box2 = bounding_box(points)
    volume2 = (box2[1][0] - box2[0][0]) * (box2[3][1] - box2[0][1]) * (box2[4][2] - box2[0][2])

    if volume1 < volume2:
        bbox = box1.tolist()
    else:
        bbox = local_to_world_coordinates_numpy(frame, box2).tolist()

    # return the transformed box
    return bbox


def oriented_bounding_box_xy_numpy(points):
    """Compute the oriented minimum bounding box of set of points in the XY plane.

    Parameters
    ----------
    points : array_like[point]
        XY(Z) coordinates of the points.

    Returns
    -------
    list[[float, float, float]]
        XYZ coordinates of 8 points defining a box.

    Raises
    ------
    ValueError
        If the input data is not at least 2D.

    See Also
    --------
    :func:`compas.geometry.bounding_box_xy`
    :func:`compas.geometry.oriented_bounding_box_numpy`

    """
    points = asarray(points)
    n, dim = points.shape

    if dim < 2:
        raise ValueError("The point coordinates should be at least 2D: %i" % dim)

    if dim == 2:
        temp = zeros((n, 3))
        temp[:, :2] = points
        points = temp

    elif dim == 3:
        points[:, 2] = 0

    rect1 = minimum_area_rectangle_xy(points)

    bbox = [[x, y, 0.0] for x, y in rect1]
    return bbox


def minimum_volume_box(points, return_size=False):
    """Compute the minimum volume box from a convex hull of a set of 3D points.

    Parameters
    ----------
    points : array_like[point]
        XYZ coordinates of the points.
    return_size : bool, optional
        If True, return the size of the box.

    Returns
    -------
    list
        XYZ coordinates of 8 points defining a box.

    """
    hull = ConvexHull(points)
    xyz = points[hull.vertices]
    boxes = []

    for simplex in hull.simplices:
        a, b, c = points[simplex]
        uvw = local_axes(a, b, c)
        if not length_vector(uvw[0]) or not length_vector(uvw[1]):
            continue
        frame = [a, uvw[0], uvw[1]]
        rst = world_to_local_coordinates_numpy(frame, xyz)
        rmin, smin, tmin = amin(rst, axis=0)
        rmax, smax, tmax = amax(rst, axis=0)
        dr = rmax - rmin
        ds = smax - smin
        dt = tmax - tmin
        v = dr * ds * dt

        bbox = [
            [rmin, smin, tmin],
            [rmax, smin, tmin],
            [rmax, smax, tmin],
            [rmin, smax, tmin],
            [rmin, smin, tmax],
            [rmax, smin, tmax],
            [rmax, smax, tmax],
            [rmin, smax, tmax],
        ]

        boxes.append([frame, bbox, v])

    frame, bbox, volume = min(boxes, key=lambda b: b[2])
    bbox = local_to_world_coordinates_numpy(frame, bbox)

    if return_size:
        return bbox, volume

    return bbox


def minimum_area_rectangle_xy(points, return_size=False):
    """Compute the minimum area rectangle from a convex hull of a set of 2D points.

    Parameters
    ----------
    points : array_like[point]
        XY(Z) coordinates of the points.
    return_size : bool, optional
        If True, return the size of the rectangle.

    Returns
    -------
    list
        XYZ coordinates of 4 points defining a rectangle.

    """
    boxes = []

    points = points[:, :2]
    hull = ConvexHull(points)
    xy = points[hull.vertices, :2]
    hull_centroid = sum(xy, axis=0) / len(xy)

    for simplex in hull.simplices:
        p0 = points[simplex[0]]
        p1 = points[simplex[1]]

        vn = xy - p0

        # s direction
        s = p1 - p0
        sl = sum(s**2) ** 0.5
        su = s / sl
        sc = (sum(vn * s, axis=1) / sl).reshape((-1, 1))
        scmax = argmax(sc)
        scmin = argmin(sc)

        # box corners
        b0 = p0 + sc[scmin] * su
        b1 = p0 + sc[scmax] * su

        # t direction
        t = array([-s[1], s[0]])
        tl = sum(t**2) ** 0.5
        tu = t / tl
        tc = (sum(vn * t, axis=1) / tl).reshape((-1, 1))
        tcmax = argmax(tc)
        tcmin = argmin(tc)

        # area
        w = sc[scmax] - sc[scmin]
        h = tc[tcmax] - tc[tcmin]
        a = w * h

        # other box corners
        if dot(t, hull_centroid - p0) < 0:
            b3 = b0 - h * tu
            b2 = b1 - h * tu
        else:
            b3 = b0 + h * tu
            b2 = b1 + h * tu

        # box
        boxes.append([[b0, b1, b2, b3], a[0]])

    # find the box with the smallest area
    bbox, area = min(boxes, key=lambda b: b[1])

    if return_size:
        return bbox, area
    return bbox
