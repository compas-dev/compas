from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from numpy.typing import ArrayLike
    from numpy.typing import NDArray

    from compas._typing import CoordinatesType


def pca(data: "CoordinatesType | ArrayLike") -> "tuple[NDArray, NDArray, NDArray]":
    """Compute the principal components of a dataset.

    Parameters
    ----------
    data
        An array containing $m$ observations of $n$ variables.

    Returns
    -------
    tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]
        The mean of the observations, the principal directions, and the
        variance along each principal direction. Directions and variances are
        ordered from largest to smallest variance.

    Raises
    ------
    ValueError
        If there are fewer observations than variables.

    Notes
    -----
    Principal component analysis identifies the orthogonal directions along
    which the variance of the observations is largest.

    """
    from numpy import asarray
    from scipy.linalg import svd

    observations = asarray(data)
    count, dimension = observations.shape
    if count < dimension:
        raise ValueError("The number of observations should be at least the number of measured variables.")

    mean = (observations.sum(axis=0) / count).reshape((-1, dimension))
    centered = observations - mean
    covariance = centered.T.dot(centered) / (count - 1)
    _, variances, directions = svd(covariance, full_matrices=False)
    return mean[0], directions, variances
