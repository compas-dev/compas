from typing import TYPE_CHECKING

from compas._typing import CoordinatesType

if TYPE_CHECKING:
    from numpy.typing import NDArray


def bestfit_line(points: CoordinatesType) -> "tuple[NDArray, NDArray]":
    """Fit a line to points using principal component analysis.

    Parameters
    ----------
    points
        XYZ coordinates of the points.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        The line origin and direction vector.

    Raises
    ------
    ValueError
        If there are fewer points than coordinate dimensions.

    """
    from compas.geometry import pca

    origin, axes, _ = pca(points)
    return origin, axes[0]


def bestfit_plane(points: CoordinatesType) -> "tuple[NDArray, NDArray]":
    """Fit a plane to points using principal component analysis.

    Parameters
    ----------
    points
        XYZ coordinates of the points.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        A point on the plane and its normal vector.

    Raises
    ------
    ValueError
        If there are fewer points than coordinate dimensions.

    """
    from compas.geometry import pca

    origin, axes, _ = pca(points)
    return origin, axes[2]


def bestfit_frame(points: CoordinatesType) -> "tuple[NDArray, NDArray, NDArray]":
    """Fit a frame to points using principal component analysis.

    Parameters
    ----------
    points
        XYZ coordinates of the points.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]
        The frame origin, X axis, and Y axis.

    Raises
    ------
    ValueError
        If there are fewer points than coordinate dimensions.

    """
    from compas.geometry import pca

    origin, axes, _ = pca(points)
    return origin, axes[0], axes[1]


def bestfit_circle(points: CoordinatesType) -> "tuple[NDArray, NDArray, float]":
    """Fit a circle to points using nonlinear least squares.

    Parameters
    ----------
    points
        XYZ coordinates of the points.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray, float]
        The circle center, normal vector, and radius.

    Raises
    ------
    ValueError
        If there are fewer points than coordinate dimensions.

    Notes
    -----
    The points are first transformed to their best-fit frame. The circle is
    then fitted in that frame by minimizing the deviation of the individual
    point radii from their average.[^bestfit-circle-scipy-cookbook]

    References
    ----------
    [^bestfit-circle-scipy-cookbook]: [Least squares circle](https://scipy-cookbook.readthedocs.io/items/Least_Squares_Circle.html)

    """
    from numpy import asarray
    from numpy import sqrt
    from scipy.optimize import leastsq

    from compas.geometry import local_to_world_coordinates_numpy
    from compas.geometry import pca
    from compas.geometry import world_to_local_coordinates_numpy

    xyz = asarray(points)
    origin, axes, _ = pca(xyz)
    frame = [origin, axes[0], axes[1]]
    local = world_to_local_coordinates_numpy(frame, xyz)
    x = local[:, 0]
    y = local[:, 1]

    def distances(xc: float, yc: float) -> "NDArray":
        return sqrt((x - xc) ** 2 + (y - yc) ** 2)

    def residuals(center: "NDArray") -> "NDArray":
        radii = distances(*center)
        return radii - radii.mean()

    center, _ = leastsq(residuals, (0.00001, 0.00001))
    radius = float(distances(*center).mean())
    xyz = local_to_world_coordinates_numpy(frame, [[center[0], center[1], 0.0]])[0]
    return xyz, axes[2], radius


def bestfit_sphere(points: CoordinatesType) -> tuple[list[float], float]:
    """Fit a sphere to points using linear least squares.

    Parameters
    ----------
    points
        XYZ coordinates of the points.

    Returns
    -------
    tuple[list[float], float]
        The sphere center and radius.

    Notes
    -----
    The implementation follows a linear least-squares sphere fit.[^bestfit-sphere-jekel]

    References
    ----------
    [^bestfit-sphere-jekel]: [Least Squares Sphere Fit](https://jekel.me/2015/Least-Squares-Sphere-Fit/)

    """
    from numpy import asarray
    from numpy import sqrt
    from numpy import zeros
    from numpy.linalg import lstsq

    x = asarray([point[0] for point in points])
    y = asarray([point[1] for point in points])
    z = asarray([point[2] for point in points])
    matrix = zeros((len(x), 4))
    matrix[:, 0] = x * 2
    matrix[:, 1] = y * 2
    matrix[:, 2] = z * 2
    matrix[:, 3] = 1

    values = zeros((len(x), 1))
    values[:, 0] = x * x + y * y + z * z
    coefficients, _, _, _ = lstsq(matrix, values)
    squared_radius = coefficients[0] ** 2 + coefficients[1] ** 2 + coefficients[2] ** 2 + coefficients[3]
    radius = float(sqrt(squared_radius)[0])
    center = [float(coefficients[0][0]), float(coefficients[1][0]), float(coefficients[2][0])]
    return center, radius
