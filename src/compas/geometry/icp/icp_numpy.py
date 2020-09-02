from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import numpy as np
from numpy import asarray
from numpy import argmin
from numpy.linalg import det
from scipy.spatial.distance import cdist
from scipy.linalg import svd
from scipy.linalg import norm

from compas.numerical import pca_numpy
from compas.numerical import normrow
from compas.geometry import Transformation
from compas.geometry import Frame
from compas.geometry import transform_points_numpy


__all__ = ['icp_numpy']


def bestfit_transform(A, B):
    n, m = A.shape
    Am = np.mean(A, axis=0)
    Bm = np.mean(B, axis=0)
    AA = A - Am
    BB = B - Bm
    # cross-covariance matrix
    C = np.dot(AA.T, BB)
    U, S, Vt = svd(C)
    # rigid rotation of the data frames
    R = np.dot(Vt.T, U.T)
    # check for RotoReflection
    if det(R) < 0:
        Vt[m-1, :] *= -1
        R = np.dot(Vt.T, U.T)
    # translation that moves data set means to same location
    # this can be done differently (by applying three transformations (T1, R, T2))
    T = Bm.T - np.dot(R, Am.T)
    X = np.identity(m+1)
    X[:m, :m] = R
    X[:m, m] = T
    return X


def icp_numpy(source, target, tol=1e-3):
    """Align two point clouds using the Iterative Closest Point (ICP) method.

    Parameters
    ----------
    source : list of point
        The source data.
    target : list of point
        The target data.
    tol : float, optional
        Tolerance for finding matches.
        Default is ``1e-3``.

    Returns
    -------

        The transformed points

    Notes
    -----
    First we align the source with the target cloud using the frames resulting
    from a PCA of each of the clouds, simply by calculating a frame-to-frame transformation.

    This initial alignment is used to establish an initial correspondence between
    the points of the two clouds.

    Then we iteratively improve the alignment by computing successive "best-fit"
    transformations using SVD of the cross-covariance matrix of the two data sets.
    During this iterative process, we continuously update the correspondence
    between the point clouds by finding the closest point in the target to each
    of the source points.

    The algorithm terminates when the alignment error is below a specified tolerance.

    Examples
    --------
    >>>

    """
    A = asarray(source)
    B = asarray(target)

    origin, axes, _ = pca_numpy(A)
    A_frame = Frame(origin, axes[0], axes[1])

    origin, axes, _ = pca_numpy(B)
    B_frame = Frame(origin, axes[0], axes[1])

    X = Transformation.from_frame_to_frame(A_frame, B_frame)
    A = transform_points_numpy(A, X)

    for i in range(20):
        D = cdist(A, B, 'euclidean')
        closest = argmin(D, axis=1)
        if norm(normrow(A - B[closest])) < tol:
            break
        X = bestfit_transform(A, B[closest])
        A = transform_points_numpy(A, X)

    return A, X


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
