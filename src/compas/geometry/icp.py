from typing import TYPE_CHECKING

from compas._typing import CoordinatesType

if TYPE_CHECKING:
    from numpy.typing import NDArray


def _bestfit_transform(source: "NDArray", target: "NDArray") -> "NDArray":
    from numpy import dot
    from numpy import identity
    from numpy import mean
    from numpy.linalg import det
    from scipy.linalg import svd

    _, dimension = source.shape
    source_mean = mean(source, axis=0)
    target_mean = mean(target, axis=0)
    source_centered = source - source_mean
    target_centered = target - target_mean
    covariance = dot(source_centered.T, target_centered)
    left, _, vectors = svd(covariance)
    rotation = dot(vectors.T, left.T)
    if det(rotation) < 0:
        vectors[dimension - 1, :] *= -1
        rotation = dot(vectors.T, left.T)
    translation = target_mean.T - dot(rotation, source_mean.T)
    transformation = identity(dimension + 1)
    transformation[:dimension, :dimension] = rotation
    transformation[:dimension, dimension] = translation
    return transformation


def icp(source: CoordinatesType, target: CoordinatesType, tol: float | None = None, maxiter: int = 100) -> "tuple[NDArray, NDArray]":
    """Align two point clouds using the iterative closest point method.

    Parameters
    ----------
    source
        Coordinates of the source point cloud.
    target
        Coordinates of the target point cloud.
    tol
        Convergence tolerance. By default, `TOL.approximation` is used.
    maxiter
        Maximum number of refinement iterations.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray]
        The transformed source points and accumulated transformation matrix.

    Notes
    -----
    The source and target are initially aligned using their PCA frames. The
    alignment is then refined through closest-point correspondence and
    singular-value decomposition of the cross-covariance matrix.

    """
    from numpy import argmin
    from numpy import asarray
    from numpy.linalg import multi_dot
    from scipy.linalg import norm
    from scipy.spatial.distance import cdist

    from compas.geometry import Frame
    from compas.geometry import Transformation
    from compas.geometry import pca
    from compas.geometry import transform_points_numpy
    from compas.linalg.decompositions import normrow
    from compas.tolerance import TOL

    tolerance = TOL.approximation if tol is None else tol
    source_points = asarray(source)
    target_points = asarray(target)

    origin, axes, _ = pca(source_points)
    # NumPy rows satisfy the coordinate protocol at runtime, but NumPy's
    # overloaded indexing stubs cannot express that structural compatibility.
    source_frame = Frame(origin, axes[0], axes[1])  # pyright: ignore[reportArgumentType]
    origin, axes, _ = pca(target_points)
    target_frame = Frame(origin, axes[0], axes[1])  # pyright: ignore[reportArgumentType]

    initial = Transformation.from_frame_to_frame(source_frame, target_frame)
    source_points = transform_points_numpy(source_points, initial.matrix)
    transformations = [asarray(initial.matrix)]

    for _ in range(maxiter):
        distances = cdist(source_points, target_points, "euclidean")
        closest = argmin(distances, axis=1)
        residual = norm(normrow(source_points - target_points[closest]))
        if TOL.is_zero(residual, tol=tolerance):
            break

        transformation = _bestfit_transform(source_points, target_points[closest])
        source_points = transform_points_numpy(source_points, transformation)
        transformations.append(transformation)

    if len(transformations) == 1:
        return source_points, transformations[0]
    return source_points, multi_dot(transformations[::-1])
