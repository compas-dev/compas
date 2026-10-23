from collections.abc import Iterable
from itertools import islice
from typing import TYPE_CHECKING
from typing import Literal
from typing import overload

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.plugins import pluggable

if TYPE_CHECKING:
    from numpy.typing import NDArray


def bounding_box(points: Iterable[CoordinateType]) -> list[list[float]]:
    """Compute the axis-aligned bounding box of a collection of points.

    Parameters
    ----------
    points
        XYZ coordinates of the points.

    Returns
    -------
    list[list[float]]
        XYZ coordinates of 8 points defining a box.

    See Also
    --------
    [`oriented_bounding_box`][compas.geometry.oriented_bounding_box]
    [`bounding_box_xy`][compas.geometry.bounding_box_xy]

    """
    x, y, z = zip(*points)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    min_z = min(z)
    max_z = max(z)
    return [
        [min_x, min_y, min_z],
        [max_x, min_y, min_z],
        [max_x, max_y, min_z],
        [min_x, max_y, min_z],
        [min_x, min_y, max_z],
        [max_x, min_y, max_z],
        [max_x, max_y, max_z],
        [min_x, max_y, max_z],
    ]


def bounding_box_xy(points: Iterable[CoordinateType]) -> list[list[float]]:
    """Compute the axis-aligned bounding box of points in the XY plane.

    Parameters
    ----------
    points
        XY(Z) coordinates of the points.

    Returns
    -------
    list[list[float]]
        XYZ coordinates of four points defining a rectangle in the XY plane.

    See Also
    --------
    [`oriented_bounding_box_xy`][compas.geometry.oriented_bounding_box_xy]
    [`bounding_box`][compas.geometry.bounding_box]

    Notes
    -----
    Z coordinates, when present, are ignored.

    """
    x, y = islice(zip(*points), 2)
    min_x = min(x)
    max_x = max(x)
    min_y = min(y)
    max_y = max(y)
    return [
        [min_x, min_y, 0.0],
        [max_x, min_y, 0.0],
        [max_x, max_y, 0.0],
        [min_x, max_y, 0.0],
    ]


@pluggable(category="geometry")
def oriented_bounding_box(points: CoordinatesType, tol: float | None = None) -> list[list[float]]:
    """Compute the minimum-volume oriented bounding box of a collection of points.

    Parameters
    ----------
    points
        XYZ coordinates of the points.
    tol
        Tolerance for deciding if the points are essentially two-dimensional.
        By default, `TOL.absolute` is used.

    Returns
    -------
    list[list[float]]
        XYZ coordinates of 8 points defining a box.

    See Also
    --------
    [`oriented_bounding_box_xy`][compas.geometry.oriented_bounding_box_xy]
    [`bounding_box`][compas.geometry.bounding_box]

    Notes
    -----
    This function is pluggable. Its default implementation uses NumPy and
    SciPy, which are imported only when the function is called.

    """
    from numpy import asarray
    from numpy import vstack

    from compas.geometry import local_to_world_coordinates_numpy
    from compas.geometry import pca
    from compas.geometry import world_to_local_coordinates_numpy
    from compas.tolerance import TOL

    xyz = asarray(points)
    _, dim = xyz.shape

    if dim != 3:
        raise ValueError("The point coordinates should be 3D: %i" % dim)

    xyz = xyz[:, :3]
    mean, vectors, values = pca(xyz)
    frame = mean, vectors[0], vectors[1]

    if TOL.is_zero(values[2], tol):
        local = world_to_local_coordinates_numpy(frame, xyz)
        rectangle, area = _minimum_area_rectangle_xy(local, return_size=True)
        aligned = bounding_box(local)[:4]
        aligned_area = (aligned[1][0] - aligned[0][0]) * (aligned[3][1] - aligned[0][1])
        corners = rectangle if area < aligned_area else aligned
        flat = [[point[0], point[1], 0.0] for point in corners]
        box = local_to_world_coordinates_numpy(frame, flat)
        return vstack((box, box)).tolist()

    box, volume = _minimum_volume_box(xyz, return_size=True)
    local = world_to_local_coordinates_numpy(frame, xyz)
    aligned = bounding_box(local)
    aligned_volume = (aligned[1][0] - aligned[0][0]) * (aligned[3][1] - aligned[0][1]) * (aligned[4][2] - aligned[0][2])

    if volume < aligned_volume:
        return box.tolist()
    return local_to_world_coordinates_numpy(frame, aligned).tolist()


def oriented_bounding_box_xy(points: CoordinatesType) -> list[list[float]]:
    """Compute the minimum-area oriented bounding box of points in the XY plane.

    Parameters
    ----------
    points
        XY(Z) coordinates of the points.

    Returns
    -------
    list[list[float]]
        XYZ coordinates of 4 points defining a rectangle.

    Raises
    ------
    ValueError
        If the point coordinates have fewer than two components.

    See Also
    --------
    [`bounding_box_xy`][compas.geometry.bounding_box_xy]
    [`oriented_bounding_box`][compas.geometry.oriented_bounding_box]

    """
    from numpy import asarray
    from numpy import zeros

    xyz = asarray(points)
    count, dim = xyz.shape

    if dim < 2:
        raise ValueError("The point coordinates should be at least 2D: %i" % dim)

    if dim == 2:
        temp = zeros((count, 3))
        temp[:, :2] = xyz
        xyz = temp
    elif dim == 3:
        xyz[:, 2] = 0

    rectangle = _minimum_area_rectangle_xy(xyz)
    return [[x, y, 0.0] for x, y in rectangle]


@overload
def _minimum_volume_box(points: "NDArray", return_size: Literal[False] = False) -> "NDArray": ...


@overload
def _minimum_volume_box(points: "NDArray", return_size: Literal[True]) -> "tuple[NDArray, float]": ...


@overload
def _minimum_volume_box(points: "NDArray", return_size: bool) -> "NDArray | tuple[NDArray, float]": ...


def _minimum_volume_box(points: "NDArray", return_size: bool = False) -> "NDArray | tuple[NDArray, float]":
    from numpy import amax
    from numpy import amin
    from scipy.spatial import ConvexHull

    from compas.geometry import local_axes
    from compas.geometry import local_to_world_coordinates_numpy
    from compas.geometry import world_to_local_coordinates_numpy
    from compas.linalg.vectors import length_vector

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
        volume = dr * ds * dt
        box = [
            [rmin, smin, tmin],
            [rmax, smin, tmin],
            [rmax, smax, tmin],
            [rmin, smax, tmin],
            [rmin, smin, tmax],
            [rmax, smin, tmax],
            [rmax, smax, tmax],
            [rmin, smax, tmax],
        ]
        boxes.append([frame, box, volume])

    frame, box, volume = min(boxes, key=lambda candidate: candidate[2])
    box = local_to_world_coordinates_numpy(frame, box)
    if return_size:
        return box, volume
    return box


@overload
def _minimum_area_rectangle_xy(points: "NDArray", return_size: Literal[False] = False) -> "list[NDArray]": ...


@overload
def _minimum_area_rectangle_xy(points: "NDArray", return_size: Literal[True]) -> "tuple[list[NDArray], float]": ...


@overload
def _minimum_area_rectangle_xy(points: "NDArray", return_size: bool) -> "list[NDArray] | tuple[list[NDArray], float]": ...


def _minimum_area_rectangle_xy(points: "NDArray", return_size: bool = False) -> "list[NDArray] | tuple[list[NDArray], float]":
    from numpy import argmax
    from numpy import argmin
    from numpy import array
    from numpy import dot
    from numpy import sum
    from scipy.spatial import ConvexHull

    boxes = []
    xy = points[:, :2]
    hull = ConvexHull(xy)
    vertices = xy[hull.vertices, :2]
    hull_centroid = sum(vertices, axis=0) / len(vertices)

    for simplex in hull.simplices:
        p0 = xy[simplex[0]]
        p1 = xy[simplex[1]]
        vectors = vertices - p0

        s = p1 - p0
        sl = sum(s**2) ** 0.5
        su = s / sl
        sc = (sum(vectors * s, axis=1) / sl).reshape((-1, 1))
        scmax = argmax(sc)
        scmin = argmin(sc)
        b0 = p0 + sc[scmin] * su
        b1 = p0 + sc[scmax] * su

        t = array([-s[1], s[0]])
        tl = sum(t**2) ** 0.5
        tu = t / tl
        tc = (sum(vectors * t, axis=1) / tl).reshape((-1, 1))
        tcmax = argmax(tc)
        tcmin = argmin(tc)
        width = sc[scmax] - sc[scmin]
        height = tc[tcmax] - tc[tcmin]
        area = width * height

        if dot(t, hull_centroid - p0) < 0:
            b3 = b0 - height * tu
            b2 = b1 - height * tu
        else:
            b3 = b0 + height * tu
            b2 = b1 + height * tu
        boxes.append([[b0, b1, b2, b3], area[0]])

    rectangle, area = min(boxes, key=lambda candidate: candidate[1])
    if return_size:
        return rectangle, area
    return rectangle
