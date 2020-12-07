from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt
from math import fabs
from random import uniform

__all__ = [
    'close',
    'allclose',
    'argmin',
    'argmax',
    'add_vectors',
    'add_vectors_xy',
    'sum_vectors',
    'cross_vectors',
    'cross_vectors_xy',
    'divide_vectors',
    'divide_vectors_xy',
    'dot_vectors',
    'dot_vectors_xy',
    'length_vector',
    'length_vector_xy',
    'length_vector_sqrd',
    'length_vector_sqrd_xy',
    'multiply_matrices',
    'multiply_matrix_vector',
    'multiply_vectors',
    'multiply_vectors_xy',
    'norm_vector',
    'norm_vectors',
    'normalize_vector',
    'normalize_vector_xy',
    'normalize_vectors',
    'normalize_vectors_xy',
    'homogenize_vectors',
    'dehomogenize_vectors',
    'orthonormalize_vectors',
    'power_vector',
    'power_vectors',
    'scale_vector',
    'scale_vector_xy',
    'scale_vectors',
    'scale_vectors_xy',
    'square_vector',
    'square_vectors',
    'subtract_vectors',
    'subtract_vectors_xy',
    'transpose_matrix',
    'vector_component',
    'vector_component_xy',

    'vector_from_points',
    'vector_from_points_xy',
    'plane_from_points',
    'circle_from_points',
    'circle_from_points_xy',
    'pointcloud',
    'pointcloud_xy'
]


def close(value1, value2, tol=1e-05):
    """Returns True if two values are equal within a tolerance.

    Parameters
    ----------
    value1 : float or int
    value2 : float or int
    tol : float, optional
        The tolerance for comparing values.
        Default is ``1e-05``.

    Examples
    --------
    >>> close(1., 1.001)
    False
    >>> close(1., 1.001, tol=1e-2)
    True
    """
    return fabs(value1 - value2) < tol


def allclose(l1, l2, tol=1e-05):
    """Returns True if two lists are element-wise equal within a tolerance.

    Parameters
    ----------
    l1 : list of float
        The first list of values.
    l2 : list of float
        The second list of values.
    tol : float, optional
        The tolerance for comparing values.
        Default is ``1e-05``.

    Notes
    -----
    The function is similar to NumPy's *allclose* function [1]_.

    Examples
    --------
    >>> allclose([0.1, 0.2, 0.3, 0.4], [0.1, 0.20001, 0.3, 0.4])
    True

    >>> allclose([0.1, 0.2, 0.3, 0.4], [0.1, 0.20001, 0.3, 0.4], tol=1e-6)
    False

    References
    ----------
    .. [1] https://docs.scipy.org/doc/numpy/reference/generated/numpy.allclose.html

    """

    if any(not allclose(a, b, tol) if hasattr(a, '__iter__') else fabs(a - b) > tol for a, b in zip(l1, l2)):
        return False
    return True


def argmax(values):
    """Returns the index of the first maximum value within an array.

    Parameters
    ----------
    values : list of float
        A list of values.

    Notes
    -----
    NumPy's *argmax* function [1]_ is different, it returns an array of indices.

    Examples
    --------
    >>> argmax([2, 4, 4, 3])
    1

    Returns
    -------
    int
        The index of the first maximum value within an array.

    References
    ----------
    .. [1] https://numpy.org/doc/stable/reference/generated/numpy.argmax.html
    """
    return max(range(len(values)), key=lambda i: values[i])


def argmin(values):
    """Returns the index of the first minimum value within an array.

    Parameters
    ----------
    values : list of float
        A list of values.

    Notes
    -----
    NumPy's *argmin* function [1]_ is different, it returns an array of indices.

    Examples
    --------
    >>> argmin([4, 2, 2, 3])
    1

    Returns
    -------
    int
        The index of the first minimum value within an array.

    References
    ----------
    .. [1] https://numpy.org/doc/stable/reference/generated/numpy.argmin.html
    """
    return min(range(len(values)), key=lambda i: values[i])

# ==============================================================================
# these return something of smaller dimension/length/...
# something_(of)vector/s
# ==============================================================================


def sum_vectors(vectors, axis=0):
    """Calculate the sum of a series of vectors along the specified axis.

    Parameters
    ----------
    vectors : list
        A list of vectors.
    axis : int, optional
        If ``axis == 0``, the sum is taken per column.
        If ``axis == 1``, the sum is taken per row.

    Returns
    -------
    list
        The length of the list is ``len(vectors[0])``, if ``axis == 0``.
        The length is ``len(vectors)``, otherwise.

    Examples
    --------
    >>> vectors = [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]]
    >>> sum_vectors(vectors)
    [3.0, 6.0, 9.0]
    >>> sum_vectors(vectors, axis=1)
    [6.0, 6.0, 6.0]

    """
    if axis == 0:
        vectors = zip(*vectors)
    return [sum(vector) for vector in vectors]


def norm_vector(vector):
    """Calculate the length of a vector.

    Parameters
    ----------
    vector : list
        XYZ components of the vector.

    Returns
    -------
    float
        The L2 norm, or *length* of the vector.

    Examples
    --------
    >>> norm_vector([2.0, 0.0, 0.0])
    2.0

    >>> norm_vector([1.0, 1.0, 0.0]) == sqrt(2.0)
    True

    """
    return sqrt(sum(axis ** 2 for axis in vector))


def norm_vectors(vectors):
    """
    Calculate the norm of each vector in a list of vectors.

    Parameters
    ----------
    vectors : list
        A list of vectors

    Returns
    -------
    list
        A list with the lengths of all vectors.

    Examples
    --------
    >>> norm_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]])
    [1.0, 2.0, 3.0]

    """
    return [norm_vector(vector) for vector in vectors]


def length_vector(vector):
    """Calculate the length of the vector.

    Parameters
    ----------
    vector : list
        XYZ components of the vector.

    Returns
    -------
    float
        The length of the vector.

    Examples
    --------
    >>> length_vector([2.0, 0.0, 0.0])
    2.0

    >>> length_vector([1.0, 1.0, 0.0]) == sqrt(2.0)
    True

    """
    return sqrt(length_vector_sqrd(vector))


def length_vector_xy(vector):
    """Compute the length of a vector, assuming it lies in the XY plane.

    Parameters
    ----------
    vector : list
        XY(Z) components of the vector.

    Returns
    -------
    float
        The length of the XY component of the vector.

    Examples
    --------
    >>> length_vector_xy([2.0, 0.0])
    2.0

    >>> length_vector_xy([2.0, 0.0, 0.0])
    2.0

    >>> length_vector_xy([2.0, 0.0, 2.0])
    2.0

    """
    return sqrt(length_vector_sqrd_xy(vector))


def length_vector_sqrd(vector):
    """Compute the squared length of a vector.

    Parameters
    ----------
    vector : list
        XYZ components of the vector.

    Returns
    -------
    float
        The squared length.

    Examples
    --------
    >>> length_vector_sqrd([1.0, 1.0, 0.0])
    2.0

    """
    return vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2


def length_vector_sqrd_xy(vector):
    """Compute the squared length of a vector, assuming it lies in the XY plane.

    Parameters
    ----------
    vector : list
        XY(Z) components of the vector.

    Returns
    -------
    float
        The squared length.

    Examples
    --------
    >>> length_vector_sqrd_xy([1.0, 1.0])
    2.0

    >>> length_vector_sqrd_xy([1.0, 1.0, 0.0])
    2.0

    >>> length_vector_sqrd_xy([1.0, 1.0, 1.0])
    2.0

    """
    return vector[0] ** 2 + vector[1] ** 2


# ==============================================================================
# these perform an operation on a vector and return a modified vector
# -> elementwise operations on 1 vector
# should this not bet ...ed_vector
# ... or else modify the vector in-place
# ==============================================================================


def scale_vector(vector, factor):
    """Scale a vector by a given factor.

    Parameters
    ----------
    vector : list, tuple
        XYZ components of the vector.
    factor : float
        The scaling factor.

    Returns
    -------
    list
        The scaled vector.

    Examples
    --------
    >>> scale_vector([1.0, 2.0, 3.0], 2.0)
    [2.0, 4.0, 6.0]

    >>> v = [2.0, 0.0, 0.0]
    >>> scale_vector(v, 1 / length_vector(v))
    [1.0, 0.0, 0.0]

    """
    return [axis * factor for axis in vector]


def scale_vector_xy(vector, factor):
    """Scale a vector by a given factor, assuming it lies in the XY plane.

    Parameters
    ----------
    vector : list
        XY(Z) components of the vector.
    scale : float
        Scale factor.

    Returns
    -------
    list
        The scaled vector in the XY-plane (Z = 0.0).

    Examples
    --------
    >>> scale_vector_xy([1.0, 2.0, 3.0], 2.0)
    [2.0, 4.0, 0.0]

    """
    return [vector[0] * factor, vector[1] * factor, 0.0]


def scale_vectors(vectors, factor):
    """Scale multiple vectors by a given factor.

    Parameters
    ----------
    vectors : list
        A list of vectors.
    factor : float
        The scaling factor.

    Returns
    -------
    vectors : list of list
        The scaled vectors.

    Examples
    --------
    >>>

    """
    return [scale_vector(vector, factor) for vector in vectors]


def scale_vectors_xy(vectors, factor):
    """Scale multiple vectors by a given factor, assuming they lie in the XY plane.

    Parameters
    ----------
    vectors : list of list
        A list of vectors.
    factor : float
        The scaling factor.

    Returns
    -------
    vectors : list of list
        The scaled vectors.

    Examples
    --------
    >>>

    """
    return [scale_vector_xy(vector, factor) for vector in vectors]


def normalize_vector(vector):
    """Normalise a given vector.

    Parameters
    ----------
    vector : list, tuple
        XYZ components of the vector.

    Returns
    -------
    list
        The normalized vector.

    Examples
    --------
    >>>

    """
    length = length_vector(vector)
    if not length:
        return vector
    return [vector[0] / length, vector[1] / length, vector[2] / length]


def normalize_vector_xy(vector):
    """Normalize a vector, assuming it lies in the XY-plane.

    Parameters
    ----------
    vector : sequence of float
        XY(Z) components of the vector.

    Returns
    -------
    list
        The normalized vector in the XY-plane (Z = 0.0)

    Examples
    --------
    >>>

    """
    length = length_vector_xy(vector)
    if not length:
        return vector
    return [vector[0] / length, vector[1] / length, 0.0]


def normalize_vectors(vectors):
    """Normalise multiple vectors.

    Parameters
    ----------
    vectors : list of list
        A list of vectors.

    Returns
    -------
    list
        The normalized vectors.

    Examples
    --------
    >>>

    """
    return [normalize_vector(vector) for vector in vectors]


def normalize_vectors_xy(vectors):
    """Normalise multiple vectors, assuming they lie in the XY plane.

    Parameters
    ----------
    vectors : list of list
        A list of vectors.

    Returns
    -------
    list
        The normalized vectors in the XY plane.

    Examples
    --------
    >>>

    """
    return [normalize_vector_xy(vector) for vector in vectors]


def power_vector(vector, power):
    """Raise a vector to the given power.

    Parameters
    ----------
    vector : list, tuple
        XYZ components of the vector.
    power : int, float
        The power to which to raise the vector.

    Returns
    -------
    vector : list
        The raised vector.

    Examples
    --------
    >>>

    """
    return [axis ** power for axis in vector]


def power_vectors(vectors, power):
    """Raise a list of vectors to the given power.

    Parameters
    ----------
    vectors : list of list
        A list of vectors.
    power : int, float
        The power to which to raise the vectors.

    Returns
    -------
    vector : list
        The raised vectors.

    Examples
    --------
    >>>

    """
    return [power_vector(vector, power) for vector in vectors]


def square_vector(vector):
    """Raise a vector to the power 2.

    Parameters
    ----------
    vector : list, tuple
        XYZ components of the vector.

    Returns
    -------
    vector : list
        The squared vector.

    Examples
    --------
    >>>

    """
    return power_vector(vector, 2)


def square_vectors(vectors):
    """Raise a multiple vectors to the power 2.

    Parameters
    ----------
    vectors : list
        A list of vectors.

    Returns
    -------
    vector : list
        The squared vectors.

    Examples
    --------
    >>>

    """
    return [square_vectors(vector) for vector in vectors]


# ==============================================================================
# these perform an operation with corresponding elements of the (2) input vectors as operands
# and return a vector with the results
# -> elementwise operations on two vectors
# ==============================================================================


def add_vectors(u, v):
    """Add two vectors.

    Parameters
    ----------
    u : sequence of float
        XYZ components of the first vector.
    v : sequence of float
        XYZ components of the second vector.

    Returns
    -------
    list
        The resulting vector.

    """
    return [a + b for (a, b) in zip(u, v)]


def add_vectors_xy(u, v):
    """Add two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : sequence of float
        XY(Z) components of the first vector.
    v : sequence of float
        XY(Z) components of the second vector.

    Returns
    -------
    list
        Resulting vector in the XY-plane (Z = 0.0)

    Examples
    --------
    >>>

    """
    return [u[0] + v[0], u[1] + v[1], 0.0]


def subtract_vectors(u, v):
    """Subtract one vector from another.

    Parameters
    ----------
    u : list
        XYZ components of the first vector.
    v : list
        XYZ components of the second vector.

    Returns
    -------
    list
        The resulting vector.

    Examples
    --------
    >>>

    """
    return [a - b for (a, b) in zip(u, v)]


def subtract_vectors_xy(u, v):
    """Subtract one vector from another, assuming they lie in the XY plane.

    Parameters
    ----------
    u : list
        The XY(Z) components of the first vector.
    v : list
        The XY(Z) components of the second vector.

    Returns
    -------
    list
        Resulting vector in the XY-plane (Z = 0.0)

    Examples
    --------
    >>>

    """
    return [u[0] - v[0], u[1] - v[1], 0.0]


def multiply_vectors(u, v):
    """Element-wise multiplication of two vectors.

    Parameters
    ----------
    u : list
        The XYZ components of the first vector.
    v : list
        The XYZ components of the second vector.

    Returns
    -------
    list
        Resulting vector.

    Examples
    --------
    >>>

    """
    return [a * b for (a, b) in zip(u, v)]


def multiply_vectors_xy(u, v):
    """Element-wise multiplication of two vectors assumed to lie in the XY plane.

    Parameters
    ----------
    u : list
        The XY(Z) components of the first vector.
    v : list
        The XY(Z) components of the second vector.

    Returns
    -------
    list
        Resulting vector in the XY plane.

    Examples
    --------
    >>>

    """
    return [u[0] * v[0], u[1] * v[1], 0.0]


def divide_vectors(u, v):
    """Element-wise division of two vectors.

    Parameters
    ----------
    u : list
        The XYZ components of the first vector.
    v : list
        The XYZ components of the second vector.

    Returns
    -------
    list
        Resulting vector.

    Examples
    --------
    >>>

    """
    return [a / b for (a, b) in zip(u, v)]


def divide_vectors_xy(u, v):
    """Element-wise division of two vectors assumed to lie in the XY plane.

    Parameters
    ----------
    u : list
        The XY(Z) components of the first vector.
    v : list
        The XY(Z) components of the second vector.

    Returns
    -------
    list
        Resulting vector in the XY plane.

    Examples
    --------
    >>>

    """
    return [u[0] / v[0], u[1] / v[1], 0.0]


# ==============================================================================
# ...
# ==============================================================================


def cross_vectors(u, v):
    r"""Compute the cross product of two vectors.

    Parameters
    ----------
    u : tuple, list, Vector
        XYZ components of the first vector.
    v : tuple, list, Vector
        XYZ components of the second vector.

    Returns
    -------
    cross : list
        The cross product of the two vectors.

    Notes
    -----
    The xyz components of the cross product of two vectors :math:`\mathbf{u}`
    and :math:`\mathbf{v}` can be computed as the *minors* of the following matrix:

    .. math::
       :nowrap:

        \begin{bmatrix}
        x & y & z \\
        u_{x} & u_{y} & u_{z} \\
        v_{x} & v_{y} & v_{z}
        \end{bmatrix}

    Therefore, the cross product can be written as:

    .. math::
       :nowrap:

        \mathbf{u} \times \mathbf{v}
        =
        \begin{bmatrix}
        u_{y} * v_{z} - u_{z} * v_{y} \\
        u_{z} * v_{x} - u_{x} * v_{z} \\
        u_{x} * v_{y} - u_{y} * v_{x}
        \end{bmatrix}


    Examples
    --------
    >>> cross_vectors([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    [0.0, 0.0, 1.0]

    """
    return [u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]]


def cross_vectors_xy(u, v):
    """Compute the cross product of two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : sequence of float
        XY(Z) coordinates of the first vector.
    v : sequence of float
        XY(Z) coordinates of the second vector.

    Returns
    -------
    list
        The cross product of the two vectors.
        This vector will be perpendicular to the XY plane.

    Examples
    --------
    >>> cross_vectors_xy([1.0, 0.0], [0.0, 1.0])
    [0.0, 0.0, 1.0]

    >>> cross_vectors_xy([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    [0.0, 0.0, 1.0]

    >>> cross_vectors_xy([1.0, 0.0, 1.0], [0.0, 1.0, 1.0])
    [0.0, 0.0, 1.0]

    """
    return [0.0, 0.0, u[0] * v[1] - u[1] * v[0]]


def dot_vectors(u, v):
    """Compute the dot product of two vectors.

    Parameters
    ----------
    u : tuple, list, Vector
        XYZ components of the first vector.
    v : tuple, list, Vector
        XYZ components of the second vector.

    Returns
    -------
    dot : float
        The dot product of the two vectors.

    Examples
    --------
    >>> dot_vectors([1.0, 0, 0], [2.0, 0, 0])
    2.0

    """
    return sum(a * b for a, b in zip(u, v))


def dot_vectors_xy(u, v):
    """Compute the dot product of two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : sequence of float
        XY(Z) coordinates of the first vector.
    v : sequence of float
        XY(Z) coordinates of the second vector.

    Returns
    -------
    float
        The dot product of the XY components of the two vectors.

    Examples
    --------
    >>> dot_vectors_xy([1.0, 0], [2.0, 0])
    2.0

    >>> dot_vectors_xy([1.0, 0, 0], [2.0, 0, 0])
    2.0

    >>> dot_vectors_xy([1.0, 0, 1], [2.0, 0, 1])
    2.0

    """
    return u[0] * v[0] + u[1] * v[1]


def vector_component(u, v):
    """Compute the component of u in the direction of v.

    Parameters
    ----------
    u : sequence of float
        XYZ components of the vector.
    v : sequence of float
        XYZ components of the direction.

    Returns
    -------
    proj_v(u) : list
        The component of u in the direction of v.

    Notes
    -----
    This is similar to computing direction cosines, or to the projection of
    a vector onto another vector. See the respective Wikipedia pages ([1]_, [2]_)
    for more info.

    References
    ----------
    .. [1] *Direction cosine*. Available at https://en.wikipedia.org/wiki/Direction_cosine.
    .. [2] *Vector projection*. Available at https://en.wikipedia.org/wiki/Vector_projection.

    Examples
    --------
    >>> vector_component([1.0, 2.0, 3.0], [1.0, 0.0, 0.0])
    [1.0, 0.0, 0.0]

    """
    l2 = length_vector_sqrd(v)
    if not l2:
        return [0, 0, 0]
    x = dot_vectors(u, v) / l2
    return scale_vector(v, x)


def vector_component_xy(u, v):
    """Compute the component of u in the direction of v, assuming they lie in the XY-plane.

    Parameters
    ----------
    u : sequence of float
        XYZ components of the vector.
    v : sequence of float
        XYZ components of the direction.

    Returns
    -------
    proj_v(u) : list
        The component of u in the direction of v.

    Notes
    -----
    This is similar to computing direction cosines, or to the projection of
    a vector onto another vector. See the respective Wikipedia pages ([1]_, [2]_)
    for more info.

    References
    ----------
    .. [1] *Direction cosine*. Available at https://en.wikipedia.org/wiki/Direction_cosine.
    .. [2] *Vector projection*. Available at https://en.wikipedia.org/wiki/Vector_projection.

    Examples
    --------
    >>> vector_component_xy([1, 2, 0], [1, 0, 0])
    [1.0, 0.0, 0.0]

    """
    l2 = length_vector_sqrd_xy(v)
    if not l2:
        return [0, 0, 0]
    x = dot_vectors_xy(u, v) / l2
    return scale_vector_xy(v, x)


# ==============================================================================
# these involve vectors interpreted as matrices (lists of lists)
# -> matrix multiplication
# ==============================================================================


def transpose_matrix(M):
    """Transpose a matrix.

    Parameters
    ----------
    M : sequence of sequence of float
        The matrix to be transposed.

    Returns
    -------
    list of list of float
        The result matrix.

    """
    return list(map(list, zip(* list(M))))


def multiply_matrices(A, B):
    r"""Mutliply a matrix with a matrix.

    Parameters
    ----------
    A : sequence of sequence of float
        The first matrix.
    B : sequence of sequence of float
        The second matrix.

    Returns
    -------
    C : list of list of float
        The result matrix.

    Raises
    ------
    Exception
        If the shapes of the matrices are not compatible.
        If the row length of B is inconsistent.

    Notes
    -----
    This is a pure Python version of the following linear algebra procedure:

    .. math::

        \mathbf{A} \cdot \mathbf{B} = \mathbf{C}

    with :math:`\mathbf{A}` a *m* by *n* matrix, :math:`\mathbf{B}` a *n* by *o*
    matrix, and :math:`\mathbf{C}` a *m* by *o* matrix.

    Examples
    --------
    >>> A = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    >>> B = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    >>> multiply_matrices(A, B)
    [[4.0, 0.0, 0.0], [0.0, 4.0, 0.0], [0.0, 0.0, 4.0]]

    """
    A = list(A)
    B = list(B)
    n = len(B)     # number of rows in B
    o = len(B[0])  # number of cols in B
    if not all(len(row) == o for row in B):
        raise Exception('Row length in matrix B is inconsistent.')
    if not all([len(row) == n for row in A]):
        raise Exception('Matrix shapes are not compatible.')
    B = list(zip(* list(B)))
    return [[dot_vectors(row, col) for col in B] for row in A]


def multiply_matrix_vector(A, b):
    r"""Multiply a matrix with a vector.

    Parameters
    ----------
    A : list of list
        The matrix.
    b : list
        The vector.

    Returns
    -------
    c : list
        The resulting vector.

    Raises
    ------
    Exception
        If not all rows of the matrix have the same length as the vector.

    Notes
    -----
    This is a Python version of the following linear algebra procedure:

    .. math::

        \mathbf{A} \cdot \mathbf{x} = \mathbf{b}

    with :math:`\mathbf{A}` a *m* by *n* matrix, :math:`\mathbf{x}` a vector of
    length *n*, and :math:`\mathbf{b}` a vector of length *m*.

    Examples
    --------
    >>> matrix = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
    >>> vector = [1.0, 2.0, 3.0]
    >>> multiply_matrix_vector(matrix, vector)
    [2.0, 4.0, 6.0]

    """
    n = len(b)
    if not all([len(row) == n for row in A]):
        raise Exception('Matrix shape is not compatible with vector length.')
    return [dot_vectors(row, b) for row in A]


# ==============================================================================
# linalg
# ==============================================================================


def homogenize_vectors(vectors, w=1.0):
    """Homogenise a list of vectors.

    Parameters
    ----------
    vectors : list
        A list of vectors.
    w : float, optional
        Homogenisation parameter.
        Defaults to ``1.0``.

    Returns
    -------
    list
        Homogenised vectors.

    Examples
    --------
    >>> vectors = [[1.0, 0.0, 0.0]]
    >>> homogenize_vectors(vectors)
    [[1.0, 0.0, 0.0, 1.0]]

    Notes
    -----
    Vectors described by XYZ components are homogenised by appending a homogenisation
    parameter to the components, and by dividing each component by that parameter.
    Homogenisatioon of vectors is often used in relation to transformations.

    """
    return [[x / w, y / w, z / w, w] for x, y, z in vectors]


def dehomogenize_vectors(vectors):
    """Dehomogenise a list of vectors.

    Parameters
    ----------
    vectors : list
        A list of vectors.

    Returns
    -------
    list
        Dehomogenised vectors.

    Examples
    --------
    >>>

    """
    return [[x * w, y * w, z * w] for x, y, z, w in vectors]


def orthonormalize_vectors(vectors):
    """Orthonormalize a set of vectors.

    Parameters
    ----------
    vectors : list of list
        The set of vectors to othonormalize.

    Returns
    -------
    basis : list of list
        An othonormal basis for the input vectors.

    Notes
    -----
    This creates a basis for the range (column space) of the matrix A.T,
    with A = vectors.

    Orthonormalisation is according to the Gram-Schmidt process.

    Examples
    --------
    >>> orthonormalize_vectors([[1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]

    """
    basis = []
    for v in vectors:
        if basis:
            e = subtract_vectors(v, sum_vectors([vector_component(v, b) for b in basis]))
        else:
            e = v
        if any(axis > 1e-10 for axis in e):
            basis.append(normalize_vector(e))
    return basis


# ==============================================================================
# constructors
# ==============================================================================


def vector_from_points(a, b):
    """Construct a vector from two points.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates of first point.
    b : sequence of float
        XYZ coordinates of second point.

    Returns
    -------
    ab : sequence of float
        The vector from ``a`` to ``b``.

    Examples
    --------
    >>>

    """
    return b[0] - a[0], b[1] - a[1], b[2] - a[2]


def vector_from_points_xy(a, b):
    """
    Create a vector based on a start point a and end point b in the XY-plane.

    Parameters
    ----------
    a : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    b : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).

    Returns
    -------
    ab : tuple
        Resulting 3D vector in the XY-plane (Z = 0.0).

    Notes
    -----
    The result of this function is equal to ``subtract_vectors(b, a)``

    """
    return b[0] - a[0], b[1] - a[1], 0.0


def plane_from_points(a, b, c):
    """Construct a plane from three points.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates.
    b : sequence of float
        XYZ coordinates.
    c : sequence of float
        XYZ coordinates.

    Returns
    -------
    plane : tuple
        Base point and normal vector (normalized).

    Examples
    --------
    >>>

    """
    ab = subtract_vectors(b, a)
    ac = subtract_vectors(c, a)
    n = normalize_vector(cross_vectors(ab, ac))
    return a, n


def circle_from_points(a, b, c):
    """Construct a circle from three points.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates.
    b : sequence of float
        XYZ coordinates.
    c : sequence of float
        XYZ coordinates.

    Returns
    -------
    circle : tuple
        Center, radius, normal  of the circle.

    Notes
    -----
    For more information, see [1]_.

    References
    ----------
    .. [1] Wikipedia. *Circumscribed circle*.
           Available at: https://en.wikipedia.org/wiki/Circumscribed_circle.

    Examples
    --------
    >>>

    """
    ab = subtract_vectors(b, a)
    cb = subtract_vectors(b, c)
    ba = subtract_vectors(a, b)
    ca = subtract_vectors(a, c)
    ac = subtract_vectors(c, a)
    bc = subtract_vectors(c, b)
    normal = normalize_vector(cross_vectors(ab, ac))
    d = 2 * length_vector_sqrd(cross_vectors(ba, cb))
    A = length_vector_sqrd(cb) * dot_vectors(ba, ca) / d
    B = length_vector_sqrd(ca) * dot_vectors(ab, cb) / d
    C = length_vector_sqrd(ba) * dot_vectors(ac, bc) / d
    Aa = scale_vector(a, A)
    Bb = scale_vector(b, B)
    Cc = scale_vector(c, C)
    center = sum_vectors([Aa, Bb, Cc])
    radius = length_vector(subtract_vectors(a, center))
    return center, radius, normal


def circle_from_points_xy(a, b, c):
    """Create a circle from three points lying in the XY-plane

    Parameters
    ----------
    a : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    b : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    c : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).

    Returns
    -------
    tuple
        XYZ coordinates of center in the XY-plane (Z = 0.0) and radius of the circle.

    Notes
    -----
    For more info, see [1]_.

    References
    ----------
    .. [1] Wikipedia. *Circumscribed circle*.
           Available at: https://en.wikipedia.org/wiki/Circumscribed_circle.

    Examples
    --------
    >>>

    """
    ax, ay = a[0], a[1]
    bx, by = b[0], b[1]
    cx, cy = c[0], c[1]
    a = bx - ax
    b = by - ay
    c = cx - ax
    d = cy - ay
    e = a * (ax + bx) + b * (ay + by)
    f = c * (ax + cx) + d * (ay + cy)
    g = 2 * (a * (cy - by) - b * (cx - bx))
    if g == 0:
        return None
    centerx = (d * e - b * f) / g
    centery = (a * f - c * e) / g
    radius = sqrt((ax - centerx) ** 2 + (ay - centery) ** 2)
    return [centerx, centery, 0.0], radius, [0, 0, 1]


def pointcloud(n, xbounds, ybounds=None, zbounds=None):
    """Construct a point cloud.

    Parameters
    ----------
    n : int
        The number of points in the cloud.
    xbounds : 2-tuple of float
        The min/max values for the x-coordinates of the points in the cloud.
    ybounds : 2-tuple of float, optional
        The min/max values for the y-coordinates of the points in the cloud.
        If ``None``, defaults to the value of the ``xbounds``.
    zbounds : 2-tuple of float, optional
        The min/max values for the z-coordinates of the points in the cloud.
        If ``None``, defaults to the value of the ``xbounds``.

    Returns
    -------
    list of list:
        A list of points forming the cloud.

    Examples
    --------
    >>> cloud = pointcloud(10, (0.0, 1.0))
    >>> all((0.0 < x < 1.0) and (0.0 < y < 1.0) and (0.0 < z < 1.0) for x, y, z in cloud)
    True

    >>> cloud = pointcloud(10, (5.0, 10.0), (0.0, 1.0), (-2.0, 3.0))
    >>> all((5.0 < x < 10.0) and (0.0 < y < 1.0) and (-2.0 < z < 3.0) for x, y, z in cloud)
    True

    """
    if ybounds is None:
        ybounds = xbounds
    if zbounds is None:
        zbounds = xbounds
    xmin, xmax = map(float, xbounds)
    ymin, ymax = map(float, ybounds)
    zmin, zmax = map(float, zbounds)
    x = [uniform(xmin, xmax) for i in range(n)]
    y = [uniform(ymin, ymax) for i in range(n)]
    z = [uniform(zmin, zmax) for i in range(n)]
    return list(map(list, zip(x, y, z)))


def pointcloud_xy(n, xbounds, ybounds=None):
    """Construct a point cloud in the XY plane.

    Parameters
    ----------
    n : int
        The number of points in the cloud.
    xbounds : 2-tuple of float
        The min/max values for the x-coordinates of the points in the cloud.
    ybounds : 2-tuple of float, optional
        The min/max values for the y-coordinates of the points in the cloud.
        If ``None``, defaults to the value of the ``xbounds``.

    Returns
    -------
    list:
        A list of points in the XY plane (Z = 0).

    Examples
    --------
    >>> cloud = pointcloud_xy(10, (0.0, 1.0))
    >>> all((0.0 < x < 1.0) and (0.0 < y < 1.0) and z == 0.0 for x, y, z in cloud)
    True

    >>> cloud = pointcloud_xy(10, (5.0, 10.0), (0.0, 1.0))
    >>> all((5.0 < x < 10.0) and (0.0 < y < 1.0) and z == 0.0 for x, y, z in cloud)
    True

    """
    if ybounds is None:
        ybounds = xbounds
    xmin, xmax = map(float, xbounds)
    ymin, ymax = map(float, ybounds)
    x = [uniform(xmin, xmax) for i in range(n)]
    y = [uniform(ymin, ymax) for i in range(n)]
    z = [0.0 for i in range(n)]
    return list(map(list, zip(x, y, z)))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod()
