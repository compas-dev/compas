from math import sqrt
from typing import Iterable
from typing import Optional
from typing import Sequence
from typing import overload

from compas._typing import CoordinateType
from compas.tolerance import TOL

_SPEC2TUPLE = {
    "sxyz": (0, 0, 0, 0),
    "sxyx": (0, 0, 1, 0),
    "sxzy": (0, 1, 0, 0),
    "sxzx": (0, 1, 1, 0),
    "syzx": (1, 0, 0, 0),
    "syzy": (1, 0, 1, 0),
    "syxz": (1, 1, 0, 0),
    "syxy": (1, 1, 1, 0),
    "szxy": (2, 0, 0, 0),
    "szxz": (2, 0, 1, 0),
    "szyx": (2, 1, 0, 0),
    "szyz": (2, 1, 1, 0),
    "rzyx": (0, 0, 0, 1),
    "rxyx": (0, 0, 1, 1),
    "ryzx": (0, 1, 0, 1),
    "rxzx": (0, 1, 1, 1),
    "rxzy": (1, 0, 0, 1),
    "ryzy": (1, 0, 1, 1),
    "rzxy": (1, 1, 0, 1),
    "ryxy": (1, 1, 1, 1),
    "ryxz": (2, 0, 0, 1),
    "rzxz": (2, 0, 1, 1),
    "rxyz": (2, 1, 0, 1),
    "rzyz": (2, 1, 1, 1),
}
"""used for Euler angles: to map rotation type and axes to tuples of inner axis, parity, repetition, frame"""

_NEXT_SPEC = [1, 2, 0, 1]


def vector_average(vector: Sequence[float]) -> float:
    """Average of a vector.

    Parameters
    ----------
    vector
        List of values.

    Returns
    -------
    float
        The mean value.

    """
    return sum(vector) / float(len(vector))


def vector_variance(vector: Sequence[float]) -> float:
    """Variance of a vector.

    Parameters
    ----------
    vector
        List of values.

    Returns
    -------
    float
        The variance value.

    """
    m = vector_average(vector)
    return (sum([(i - m) ** 2 for i in vector]) / float(len(vector))) ** 0.5


def vector_standard_deviation(vector: Sequence[float]) -> float:
    """Standard deviation of a vector.

    Parameters
    ----------
    vector
        List of values.

    Returns
    -------
    float
        The standard deviation value.

    """
    return vector_variance(vector) ** 0.5


def argmax(values: Sequence[float]) -> int:
    """Returns the index of the first maximum value within an array.

    Parameters
    ----------
    values
        A list of values.

    Returns
    -------
    int
        The index of the first maximum value within an array.

    Notes
    -----
    NumPy's `argmax` function is different: it returns an array of indices.[^argmax-numpy]

    References
    ----------
    [^argmax-numpy]: [NumPy `argmax`](https://numpy.org/doc/stable/reference/generated/numpy.argmax.html)

    Examples
    --------
    >>> argmax([2, 4, 4, 3])
    1

    """
    return max(range(len(values)), key=lambda i: values[i])


def argmin(values: Sequence[float]) -> int:
    """Returns the index of the first minimum value within an array.

    Parameters
    ----------
    values
        A list of values.

    Returns
    -------
    int
        The index of the first minimum value within an array.

    Notes
    -----
    NumPy's `argmin` function is different: it returns an array of indices.[^argmin-numpy]

    References
    ----------
    [^argmin-numpy]: [NumPy `argmin`](https://numpy.org/doc/stable/reference/generated/numpy.argmin.html)

    Examples
    --------
    >>> argmin([4, 2, 2, 3])
    1

    """
    return min(range(len(values)), key=lambda i: values[i])


# ==============================================================================
# these return something of smaller dimension/length/...
# something_(of)vector/s
# ==============================================================================


def sum_vectors(vectors: Sequence[Sequence[float]], axis: int = 0) -> list[float]:
    """Calculate the sum of a series of vectors along the specified axis.

    Parameters
    ----------
    vectors
        A list of vectors.
    axis
        If `axis == 0`, the sum is taken per column.
        If `axis == 1`, the sum is taken per row.

    Returns
    -------
    list[float]
        The length of the list is `len(vectors[0])`, if `axis == 0`.
        The length is `len(vectors)`, otherwise.

    Examples
    --------
    >>> vectors = [[1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]]
    >>> sum_vectors(vectors)
    [3.0, 6.0, 9.0]
    >>> sum_vectors(vectors, axis=1)
    [6.0, 6.0, 6.0]

    """
    if axis == 0:
        return [sum(vector) for vector in zip(*vectors)]
    return [sum(vector) for vector in vectors]


def norm_vector(vector: Sequence[float]) -> float:
    """Calculate the length of a vector.

    Parameters
    ----------
    vector
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
    return sqrt(sum(axis**2 for axis in vector))


def norm_vectors(vectors: Sequence[Sequence[float]]) -> list[float]:
    """
    Calculate the norm of each vector in a list of vectors.

    Parameters
    ----------
    vectors
        A list of vectors

    Returns
    -------
    list[float]
        A list with the lengths of all vectors.

    Examples
    --------
    >>> norm_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]])
    [1.0, 2.0, 3.0]

    """
    return [norm_vector(vector) for vector in vectors]


def length_vector(vector: CoordinateType) -> float:
    """Calculate the length of the vector.

    Parameters
    ----------
    vector
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


def length_vector_xy(vector: Sequence[float]) -> float:
    """Compute the length of a vector, assuming it lies in the XY plane.

    Parameters
    ----------
    vector
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


def length_vector_sqrd(vector: Sequence[float]) -> float:
    """Compute the squared length of a vector.

    Parameters
    ----------
    vector
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


def length_vector_sqrd_xy(vector: Sequence[float]) -> float:
    """Compute the squared length of a vector, assuming it lies in the XY plane.

    Parameters
    ----------
    vector
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


def scale_vector(vector: Sequence[float], factor: float) -> list[float]:
    """Scale a vector by a given factor.

    Parameters
    ----------
    vector
        XYZ components of the vector.
    factor
        The scaling factor.

    Returns
    -------
    list[float]
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


def scale_vector_xy(vector: Sequence[float], factor: float) -> list[float]:
    """Scale a vector by a given factor, assuming it lies in the XY plane.

    Parameters
    ----------
    vector
        XY(Z) components of the vector.
    factor
        Scale factor.

    Returns
    -------
    list[float]
        The scaled vector in the XY-plane.

    Examples
    --------
    >>> scale_vector_xy([1.0, 2.0, 3.0], 2.0)
    [2.0, 4.0, 0.0]

    """
    return [vector[0] * factor, vector[1] * factor, 0.0]


def scale_vectors(vectors: Sequence[Sequence[float]], factor: float) -> list[list[float]]:
    """Scale multiple vectors by a given factor.

    Parameters
    ----------
    vectors
        A list of vectors.
    factor
        The scaling factor.

    Returns
    -------
    list[list[float]]
        The scaled vectors.

    """
    return [scale_vector(vector, factor) for vector in vectors]


def scale_vectors_xy(vectors: Sequence[Sequence[float]], factor: float) -> list[list[float]]:
    """Scale multiple vectors by a given factor, assuming they lie in the XY plane.

    Parameters
    ----------
    vectors
        A list of vectors.
    factor
        The scaling factor.

    Returns
    -------
    list[list[float]]
        The scaled vectors in the XY plane.

    """
    return [scale_vector_xy(vector, factor) for vector in vectors]


@overload
def normalize_vector(vector: list[float]) -> list[float]: ...


@overload
def normalize_vector(vector: Sequence[float]) -> Sequence[float]: ...


def normalize_vector(vector: Sequence[float]) -> Sequence[float]:
    """Normalise a given vector.

    Parameters
    ----------
    vector
        XYZ components of the vector.

    Returns
    -------
    Sequence[float]
        The normalized vector.

    """
    length = length_vector(vector)
    if not length:
        return vector
    return [vector[0] / length, vector[1] / length, vector[2] / length]


@overload
def normalize_vector_xy(vector: list[float]) -> list[float]: ...


@overload
def normalize_vector_xy(vector: Sequence[float]) -> Sequence[float]: ...


def normalize_vector_xy(vector: Sequence[float]) -> Sequence[float]:
    """Normalize a vector, assuming it lies in the XY-plane.

    Parameters
    ----------
    vector
        XY(Z) components of the vector.

    Returns
    -------
    Sequence[float]
        The normalized vector in the XY-plane.

    """
    length = length_vector_xy(vector)
    if not length:
        return vector
    return [vector[0] / length, vector[1] / length, 0.0]


def normalize_vectors(vectors: Sequence[Sequence[float]]) -> list[Sequence[float]]:
    """Normalise multiple vectors.

    Parameters
    ----------
    vectors
        A list of vectors.

    Returns
    -------
    list[Sequence[float]]
        The normalized vectors.

    """
    return [normalize_vector(vector) for vector in vectors]


def normalize_vectors_xy(vectors: Sequence[Sequence[float]]) -> list[Sequence[float]]:
    """Normalise multiple vectors, assuming they lie in the XY plane.

    Parameters
    ----------
    vectors
        A list of vectors.

    Returns
    -------
    list[Sequence[float]]
        The normalized vectors in the XY plane.

    """
    return [normalize_vector_xy(vector) for vector in vectors]


def power_vector(vector: Sequence[float], power: float) -> list[float]:
    """Raise a vector to the given power.

    Parameters
    ----------
    vector
        XYZ components of the vector.
    power
        The power to which to raise the vector.

    Returns
    -------
    list[float]
        The raised vector.

    """
    return [axis**power for axis in vector]


def power_vectors(vectors: Sequence[Sequence[float]], power: float) -> list[list[float]]:
    """Raise a list of vectors to the given power.

    Parameters
    ----------
    vectors
        A list of vectors.
    power
        The power to which to raise the vectors.

    Returns
    -------
    list[list[float]]
        The raised vectors.

    """
    return [power_vector(vector, power) for vector in vectors]


def square_vector(vector: Sequence[float]) -> list[float]:
    """Raise a vector to the power 2.

    Parameters
    ----------
    vector
        XYZ components of the vector.

    Returns
    -------
    list[float]
        The squared vector.

    """
    return power_vector(vector, 2)


def square_vectors(vectors: Sequence[Sequence[float]]) -> list[list[float]]:
    """Raise a multiple vectors to the power 2.

    Parameters
    ----------
    vectors
        A list of vectors.

    Returns
    -------
    list[list[float]]
        The squared vectors.

    """
    return [square_vector(vector) for vector in vectors]


# ==============================================================================
# these perform an operation with corresponding elements of the (2) input vectors as operands
# and return a vector with the results
# -> elementwise operations on two vectors
# ==============================================================================


def add_vectors(u: Iterable[float], v: Iterable[float]) -> list[float]:
    """Add two vectors.

    Parameters
    ----------
    u
        XYZ components of the first vector.
    v
        XYZ components of the second vector.

    Returns
    -------
    list[float]
        The resulting vector.

    """
    return [a + b for (a, b) in zip(u, v)]


def add_vectors_xy(u: Sequence[float], v: Sequence[float]) -> list[float]:
    """Add two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u
        XY(Z) components of the first vector.
    v
        XY(Z) components of the second vector.

    Returns
    -------
    list[float]
        Resulting vector in the XY-plane.

    """
    return [u[0] + v[0], u[1] + v[1], 0.0]


def subtract_vectors(u: CoordinateType, v: CoordinateType) -> list[float]:
    """Subtract one vector from another.

    Parameters
    ----------
    u
        XYZ components of the first vector.
    v
        XYZ components of the second vector.

    Returns
    -------
    list[float]
        The resulting vector.

    """
    return [a - b for (a, b) in zip(u, v)]


def subtract_vectors_xy(u: Sequence[float], v: Sequence[float]) -> list[float]:
    """Subtract one vector from another, assuming they lie in the XY plane.

    Parameters
    ----------
    u
        The XY(Z) components of the first vector.
    v
        The XY(Z) components of the second vector.

    Returns
    -------
    list[float]
        Resulting vector in the XY-plane.

    """
    return [u[0] - v[0], u[1] - v[1], 0.0]


def multiply_vectors(u: Sequence[float], v: Sequence[float]) -> list[float]:
    """Element-wise multiplication of two vectors.

    Parameters
    ----------
    u
        The XYZ components of the first vector.
    v
        The XYZ components of the second vector.

    Returns
    -------
    list[float]
        Resulting vector.

    """
    return [a * b for (a, b) in zip(u, v)]


def multiply_vectors_xy(u: Sequence[float], v: Sequence[float]) -> list[float]:
    """Element-wise multiplication of two vectors assumed to lie in the XY plane.

    Parameters
    ----------
    u
        The XY(Z) components of the first vector.
    v
        The XY(Z) components of the second vector.

    Returns
    -------
    list[float]
        Resulting vector in the XY plane.

    """
    return [u[0] * v[0], u[1] * v[1], 0.0]


def divide_vectors(u: Sequence[float], v: Sequence[float]) -> list[float]:
    """Element-wise division of two vectors.

    Parameters
    ----------
    u
        The XYZ components of the first vector.
    v
        The XYZ components of the second vector.

    Returns
    -------
    list[float]
        Resulting vector.

    """
    return [a / b for (a, b) in zip(u, v)]


def divide_vectors_xy(u: Sequence[float], v: Sequence[float]) -> list[float]:
    """Element-wise division of two vectors assumed to lie in the XY plane.

    Parameters
    ----------
    u
        The XY(Z) components of the first vector.
    v
        The XY(Z) components of the second vector.

    Returns
    -------
    list[float]
        Resulting vector in the XY plane.

    """
    return [u[0] / v[0], u[1] / v[1], 0.0]


# ==============================================================================
# ...
# ==============================================================================


def cross_vectors(u: CoordinateType, v: CoordinateType) -> list[float]:
    r"""Compute the cross product of two vectors.

    Parameters
    ----------
    u
        XYZ components of the first vector.
    v
        XYZ components of the second vector.

    Returns
    -------
    list[float]
        The cross product of the two vectors.

    Notes
    -----
    The xyz components of the cross product of two vectors $\mathbf{u}$
    and $\mathbf{v}$ can be computed as the *minors* of the following matrix:

    $$
        \begin{bmatrix}
        x & y & z \\
        u_{x} & u_{y} & u_{z} \\
        v_{x} & v_{y} & v_{z}
        \end{bmatrix}
    $$

    Therefore, the cross product can be written as:

    $$
        \begin{aligned}
            \mathbf{u} \times \mathbf{v}
            & =
            \begin{bmatrix}
            u_{y} * v_{z} - u_{z} * v_{y} \\
            u_{z} * v_{x} - u_{x} * v_{z} \\
            u_{x} * v_{y} - u_{y} * v_{x}
            \end{bmatrix}
        \end{aligned}
    $$

    Examples
    --------
    >>> cross_vectors([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    [0.0, 0.0, 1.0]

    """
    return [
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    ]


def cross_vectors_xy(u: Sequence[float], v: Sequence[float]) -> list[float]:
    """Compute the cross product of two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u
        XY(Z) coordinates of the first vector.
    v
        XY(Z) coordinates of the second vector.

    Returns
    -------
    list[float]
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


def dot_vectors(u: CoordinateType, v: CoordinateType) -> float:
    """Compute the dot product of two vectors.

    Parameters
    ----------
    u
        XYZ components of the first vector.
    v
        XYZ components of the second vector.

    Returns
    -------
    float
        The dot product of the two vectors.

    Examples
    --------
    >>> dot_vectors([1.0, 0, 0], [2.0, 0, 0])
    2.0

    """
    return sum(a * b for a, b in zip(u, v))


def dot_vectors_xy(u: Sequence[float], v: Sequence[float]) -> float:
    """Compute the dot product of two vectors, assuming they lie in the XY-plane.

    Parameters
    ----------
    u
        XY(Z) coordinates of the first vector.
    v
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


def vector_component(u: Sequence[float], v: Sequence[float]) -> list[float]:
    """Compute the component of u in the direction of v.

    Parameters
    ----------
    u
        XYZ components of the vector.
    v
        XYZ components of the direction.

    Returns
    -------
    list[float]
        The component of u in the direction of v.

    Notes
    -----
    This is similar to computing direction cosines, or to the projection of
    a vector onto another vector.[^vector-component-direction-cosine] [^vector-component-projection]

    References
    ----------
    [^vector-component-direction-cosine]: [Direction cosine](https://en.wikipedia.org/wiki/Direction_cosine)
    [^vector-component-projection]: [Vector projection](https://en.wikipedia.org/wiki/Vector_projection)

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


def vector_component_xy(u: Sequence[float], v: Sequence[float]) -> list[float]:
    """Compute the component of u in the direction of v, assuming they lie in the XY-plane.

    Parameters
    ----------
    u
        XYZ components of the vector.
    v
        XYZ components of the direction.

    Returns
    -------
    list[float]
        The component of u in the XY plane, in the direction of v.

    Notes
    -----
    This is similar to computing direction cosines, or to the projection of
    a vector onto another vector.[^vector-component-xy-direction-cosine] [^vector-component-xy-projection]

    References
    ----------
    [^vector-component-xy-direction-cosine]: [Direction cosine](https://en.wikipedia.org/wiki/Direction_cosine)
    [^vector-component-xy-projection]: [Vector projection](https://en.wikipedia.org/wiki/Vector_projection)

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
# linalg
# ==============================================================================


def homogenize_vectors(vectors: Sequence[Sequence[float]], w: float = 1.0) -> list[list[float]]:
    """Homogenise a list of vectors.

    Parameters
    ----------
    vectors
        A list of vectors.
    w
        Homogenisation parameter.

    Returns
    -------
    list[list[float]]
        Homogenised vectors.

    Notes
    -----
    Vectors described by XYZ components are homogenised by appending a homogenisation
    parameter to the components, and by dividing each component by that parameter.
    Homogenisatioon of vectors is often used in relation to transformations.

    Examples
    --------
    >>> vectors = [[1.0, 0.0, 0.0]]
    >>> homogenize_vectors(vectors)
    [[1.0, 0.0, 0.0, 1.0]]

    """
    return [[x / w, y / w, z / w, w] for x, y, z in vectors]


def dehomogenize_vectors(vectors: Sequence[Sequence[float]]) -> list[list[float]]:
    """Dehomogenise a list of vectors.

    Parameters
    ----------
    vectors
        A list of vectors.

    Returns
    -------
    list[list[float]]
        Dehomogenised vectors.

    """
    return [[x * w, y * w, z * w] for x, y, z, w in vectors]


def orthonormalize_vectors(vectors: Sequence[Sequence[float]]) -> list[Sequence[float]]:
    """Orthonormalize a set of vectors.

    Parameters
    ----------
    vectors
        The set of vectors to othonormalize.

    Returns
    -------
    list[Sequence[float]]
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


# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# Deprecated
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================


def close(value1: float, value2: float, tol: float = 1e-05) -> bool:
    """Returns True if two values are equal within a tolerance.

    Parameters
    ----------
    value1
    value2
    tol
        The absolute tolerance for comparing values.
        Default is `TOL.absolute`.

    Returns
    -------
    bool
        True if the values are closer than the tolerance.
        False otherwise.

    Warnings
    --------
    Deprecated since version 2.0. This function will be removed in version 2.1.
    Use [`TOL.is_close`][compas.tolerance.Tolerance.is_close] instead.

    The tolerance value used by this function is an absolute tolerance.
    It is more accurate to use a combination of absolute and relative tolerance.
    Therefore, use [`TOL.is_close`][compas.tolerance.Tolerance.is_close] instead.

    """
    return TOL.is_close(value1, value2, rtol=0.0, atol=tol)


def allclose(l1: Sequence[float], l2: Sequence[float], tol: Optional[float] = None) -> bool:
    """Returns True if two lists are element-wise equal within a tolerance.

    Parameters
    ----------
    l1
        The first list of values.
    l2
        The second list of values.
    tol
        The absolute tolerance for comparing values.
        Default is `TOL.absolute`.

    Returns
    -------
    bool
        True if all corresponding values of the two lists are closer than the tolerance.
        False otherwise.

    Warnings
    --------
    Deprecated since version 2.0. This function will be removed in version 2.1.
    Use [`TOL.is_allclose`][compas.tolerance.Tolerance.is_allclose] instead.

    The tolerance value used by this function is an absolute tolerance.
    It is more accurate to use a combination of absolute and relative tolerance.
    Therefore, use [`TOL.is_allclose`][compas.tolerance.Tolerance.is_allclose] instead.

    Notes
    -----
    The function is similar to NumPy's `allclose` function.[^allclose-numpy]

    References
    ----------
    [^allclose-numpy]: [NumPy `allclose`](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html)

    """
    return TOL.is_allclose(l1, l2, atol=tol)
