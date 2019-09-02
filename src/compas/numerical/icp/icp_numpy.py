from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from numpy import asarray
from scipy.linalg import svd

from compas.numerical.pca import pca_numpy
from compas.geometry import Transformation
from compas.geometry import Frame
from compas.geometry import transform_points_numpy

__all__ = ['icp_numpy']


def icp_numpy(d1, d2, tol=1e-3):
    """Align two point clouds using the Iterative Closest Point (ICP) method.

    Parameters
    ----------
    d1 : list of point
        Point cloud 1.
    d2 : list of point
        Point cloud 2.
    tol : float, optional
        Tolerance for finding matches.
        Default is ``1e-3``.

    Returns
    -------

    Notes
    -----

    Examples
    --------

    References
    ----------

    """
    d1 = asarray(d1)
    d2 = asarray(d2)

    point, axes, spread =  pca_numpy(d1)
    frame1 = Frame(point, axes[0], axes[1])

    point, axes, spread =  pca_numpy(d2)
    frame2 = Frame(point, axes[0], axes[1])

    T = Transformation.from_frame_to_frame(frame1, frame2)
    transform_points_numpy(d1, T)

    y = cdist(d1, d2 , 'eucledian')
    closest = argmin(y, axes=1)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
