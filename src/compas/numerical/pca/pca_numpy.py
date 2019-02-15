from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

try:
    from numpy import asarray
    from scipy.linalg import svd

except ImportError:
    compas.raise_if_not_ironpython()


__all__ = ['pca_numpy']


def pca_numpy(data):
    """Compute the principle components of a set of data points.

    Parameters
    ----------
    data : list
        A list of `m` observations, measuring `n` variables.
        For example, if the data are points in 2D space, the data parameter
        should contain `m` nested lists of `2` variables, the `x` and `y`
        coordinates.

    Returns
    -------
    tuple
        * The ``mean of the data points``
        * The principle directions.
          The number of principle directions is equal to the dimensionality of the data.
          For example, if the data points are locations in 3D space, three principle components will be returned.
          If the data points are locations in 2D space, only two principle components will be returned.
        * The *spread* of the data along the principle directions.

    Notes
    -----
    PCA of a dataset finds the directions along which the variance of the data
    is largest, i.e. the directions along which the data is most spread out.

    Examples
    --------
    .. plot::
        :include-source:

        from numpy import random

        import matplotlib.pyplot as plt

        from compas.geometry import matrix_from_axis_and_angle
        from compas.geometry import transform_points_numpy

        from compas.plotters import Axes3D
        from compas.plotters import Cloud3D
        from compas.plotters import Bounds
        from compas.plotters import create_axes_3d

        from compas.numerical import pca_numpy

        data = random.rand(300, 3)
        data[:, 0] *= 10.0
        data[:, 1] *= 1.0
        data[:, 2] *= 4.0

        a = 3.14159 * 30.0 / 180
        Ry = matrix_from_axis_and_angle([0, 1.0, 0.0], a, rtype='array')

        a = -3.14159 * 45.0 / 180
        Rz = matrix_from_axis_and_angle([0, 0, 1.0], a, rtype='array')

        R = Rz.dot(Ry)

        data = transform_points_numpy(data, R)

        average, vectors, values = pca_numpy(data)

        axes = create_axes_3d()

        Bounds(data).plot(axes)
        Cloud3D(data).plot(axes)
        Axes3D(average, vectors).plot(axes)

        plt.show()

    """
    X = asarray(data)
    n, dim = X.shape

    assert n >= dim, "The number of observations (n) should be higher than the number of measured variables (dimensions)."

    # the average of the observations for each of the variables
    # for example, if the data are 2D point coordinates,
    # the average is the average of the x-coordinate across all observations
    # and the average of the y-coordinate across all observations
    mean = (X.sum(axis=0) / n).reshape((-1, dim))

    # the spread matrix
    # i.e. the variation of each variable compared to the average of the variable
    # across all observations
    Y = X - mean

    # covariance matrix of spread
    # note: there is a covariance function in NumPy...
    # the shape of the covariance matrix is dim x dim
    # for example, if the data are 2D point coordinates, the shape of C is 2 x 2
    # the diagonal of the covariance matrix contains the variance of each variable
    # the off-diagonal elements of the covariannce matrix contain the covariance
    # of two independent variables
    C = Y.T.dot(Y) / (n - 1)

    assert C.shape[0] == dim, "The shape of the covariance matrix is not correct."

    # SVD of covariance matrix
    u, s, vT = svd(C, full_matrices=False)

    # eigenvectors
    # ------------
    # note: the eigenvectors are normalized
    # note: vT is exactly what it says it will be => the transposed eigenvectors
    # => take the rows of vT, or the columns of v
    # the right-singular vectors of C (the columns of V or the rows of Vt)
    # are the eigenvectors of CtC

    eigenvectors = vT

    # eigenvalues
    # -----------
    # the nonzero singular values of C are the square roots
    # of the nonzero eigenvalues of CtC and CCt

    eigenvalues = s

    # return
    return mean, eigenvectors, eigenvalues


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import random
    from numpy import asarray

    import matplotlib.pyplot as plt

    from compas.geometry import matrix_from_axis_and_angle
    from compas.geometry import transform_points_numpy

    from compas.plotters import Axes3D
    from compas.plotters import Cloud3D
    from compas.plotters import Bounds
    from compas.plotters import create_axes_3d

    data = random.rand(300, 3)
    data[:, 0] *= 10.0
    data[:, 1] *= 1.0
    data[:, 2] *= 4.0

    a = 3.14159 * 30.0 / 180
    Ry = matrix_from_axis_and_angle([0, 1.0, 0.0], a, rtype='array')

    a = -3.14159 * 45.0 / 180
    Rz = matrix_from_axis_and_angle([0, 0, 1.0], a, rtype='array')

    R = Rz.dot(Ry)

    data = transform_points_numpy(data, R)

    average, vectors, values = pca_numpy(data)

    axes = create_axes_3d()

    Bounds(data).plot(axes)
    Cloud3D(data).plot(axes)
    Axes3D(average, vectors).plot(axes)

    plt.show()
