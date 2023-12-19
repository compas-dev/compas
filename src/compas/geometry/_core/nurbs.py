from itertools import groupby


def construct_knotvector(degree, pointcount):
    """Construct a nonperiodic (clamped), uniform knot vector for a curve with given degree and number of control points.

    This function will generate a knotvector of the form
    ``[0] * (order) + [i / d for i in range(1, d)] + [1] * (order)``, with ``order = degree + 1`` and ``d = pointcount - degree``.
    Therefore the length of the knotvector will be ``pointcount + degree + 1``.

    For example, if degree is 3 and the number of control points is 7, the knot vector will be ``[0, 0, 0, 0, 1/4, 2/4, 3/4, 1, 1, 1, 1]``.

    Parameters
    ----------
    degree : int
        Degree of the curve.
    pointcount : int
        The number of control points of the curve.

    Returns
    -------
    list[float]
        Knot vector.

    Raises
    ------
    ValueError
        If the number of control points is less than degree + 1.

    See Also
    --------
    knotvector_to_knots_and_mults
    knots_and_mults_to_knotvector
    find_span
    compute_basisfuncs
    compute_basisfuncsderivs

    References
    ----------
    The NURBS Book. Chapter 2. Page 66.

    """
    order = degree + 1

    if order > pointcount:
        raise ValueError("The order of the curve (degree + 1) cannot be larger than the number of control points.")

    d = pointcount - degree
    return [0] * (order) + [i / d for i in range(1, d)] + [1] * (order)


def knotvector_to_knots_and_mults(knotvector):
    """Convert a knot vector to a list of knots and multiplicities.

    Parameters
    ----------
    knotvector : list[int | float]
        Knot vector.

    Returns
    -------
    tuple[list[int | float], list[int]]
        Knots and multiplicities.

    See Also
    --------
    construct_knotvector
    knots_and_mults_to_knotvector
    find_span
    compute_basisfuncs
    compute_basisfuncsderivs

    Notes
    -----
    The "standard" representation of a knot vector is a list of the form
    ``[0] * (degree + 1) + [i / d for i in range(1, d)] + [1] * (degree + 1)``, with ``d = pointcount - degree``.
    This representation is used, for example, in the NURBS Book and OpenCASCADe.

    Rhino uses a knot vector of the form ``[0] * (degree) + [i / d for i in range(1, d)] + [1] * (degree)``.

    """
    knots = []
    mults = []

    for knot, multiplicity in groupby(knotvector):
        knots.append(knot)
        mults.append(len(list(multiplicity)))

    return knots, mults


def knots_and_mults_to_knotvector(knots, mults):
    """Convert a list of knots and multiplicities to a knot vector.

    Parameters
    ----------
    knots : list[int | float]
        Knots.
    mults : list[int]
        Multiplicities.

    Returns
    -------
    list[int | float]
        Knot vector.

    See Also
    --------
    construct_knotvector
    knotvector_to_knots_and_mults
    find_span
    compute_basisfuncs
    compute_basisfuncsderivs

    Notes
    -----
    The "standard" representation of a knot vector is a list of the form
    ``[0] * (degree + 1) + [i / d for i in range(1, d)] + [1] * (degree + 1)``, with ``d = pointcount - degree``.
    This representation is used, for example, in the NURBS Book and OpenCASCADe.

    Rhino uses a knot vector of the form ``[0] * (degree) + [i / d for i in range(1, d)] + [1] * (degree)``.

    """
    knotvector = []

    for knot, multiplicity in zip(knots, mults):
        knotvector.extend([knot] * multiplicity)

    return knotvector


def find_span(n, degree, knotvector, u):
    """Find the knot span index for a given knot value.

    Parameters
    ----------
    n : int
        Number of control points minus 1.
    degree : int
        Degree of the curve.
    knotvector : list[int | float]
        Knot vector of the curve.
    u : float
        Parameter value.

    Returns
    -------
    int
        Knot span index.

    Raises
    ------
    ValueError
        If the parameter value is greater than the maximum knot or less than the minimum knot.

    See Also
    --------
    construct_knotvector
    knotvector_to_knots_and_mults
    knots_and_mults_to_knotvector
    compute_basisfuncs
    compute_basisfuncsderivs

    References
    ----------
    The NURBS Book. Chapter 2. Page 68. Algorithm A2.1.

    """
    if u > knotvector[-1]:
        raise ValueError("Parameter value is greater than the maximum knot.")

    if u < knotvector[0]:
        raise ValueError("Parameter value is less than the minimum knot.")

    if u == knotvector[n + 1]:
        return n

    low = degree
    high = n + 1
    mid = (low + high) // 2

    while u < knotvector[mid] or u >= knotvector[mid + 1]:
        if u < knotvector[mid]:
            high = mid
        else:
            low = mid
        mid = (low + high) // 2

    return mid


def compute_basisfuncs(degree, knotvector, i, u):
    """Compute the nonzero basis functions for a given parameter value.

    Parameters
    ----------
    degree : int
        Degree of the curve.
    knotvector : list
        Knot vector of the curve.
    i : int
        Knot span index.
    u : float
        Parameter value.

    Returns
    -------
    list[float]
        Basis functions.

    See Also
    --------
    construct_knotvector
    knotvector_to_knots_and_mults
    knots_and_mults_to_knotvector
    find_span
    compute_basisfuncsderivs

    Notes
    -----
    In any given knot span, :math:`\\[u_{j}, u_{j+1}\\)` at most degree + 1 of the :math:`N_{i,degree}` basis functions are nonzero,
    namely the functions :math:`N_{j-degree,degree}, \\dots, N_{j,degree}`.

    References
    ----------
    The NURBS Book. Chapter 2. Page 56.
    The NURBS Book. Chapter 2. Page 70. Algorithm A2.2.

    """
    N = [0.0 for _ in range(degree + 1)]
    left = [0.0 for _ in range(degree + 1)]
    right = [0.0 for _ in range(degree + 1)]

    N[0] = 1.0

    for j in range(1, degree + 1):
        left[j] = u - knotvector[i + 1 - j]
        right[j] = knotvector[i + j] - u

        saved = 0.0

        for r in range(j):
            temp = N[r] / (right[r + 1] + left[j - r])
            N[r] = saved + right[r + 1] * temp
            saved = left[j - r] * temp

        N[j] = saved

    return N


def compute_basisfuncsderivs(degree, knotvector, i, u, n):
    """Compute the derivatives of the basis functions for a given parameter value.

    Parameters
    ----------
    degree : int
        Degree of the curve.
    knotvector : list[int | float]
        Knot vector of the curve.
    i : int
        Knot span index.
    u : float
        Parameter value.
    n : int
        Number of derivatives to compute.

    Returns
    -------
    list[float]
        Derivatives of the basis functions.

    See Also
    --------
    construct_knotvector
    knotvector_to_knots_and_mults
    knots_and_mults_to_knotvector
    find_span
    compute_basisfuncs

    References
    ----------
    The NURBS Book. Chapter 2. Page 72. Algorithm A2.3.

    """
    # output
    derivs = [[0.0 for _ in range(degree + 1)] for _ in range(n + 1)]

    # Algorithm A2.2 modified to store the basis functions and knot differences
    ndu = [[0.0 for _ in range(degree + 1)] for _ in range(degree + 1)]
    ndu[0][0] = 1.0

    left = [0.0 for _ in range(degree + 1)]
    right = [0.0 for _ in range(degree + 1)]

    for j in range(1, degree + 1):
        left[j] = u - knotvector[i + 1 - j]
        right[j] = knotvector[i + j] - u

        saved = 0.0

        for r in range(j):
            # Lower triangle
            ndu[j][r] = right[r + 1] + left[j - r]

            temp = ndu[r][j - 1] / ndu[j][r]

            # Upper triangle
            ndu[r][j] = saved + right[r + 1] * temp

            saved = left[j - r] * temp

        ndu[j][j] = saved

    # load the basis functions
    for j in range(degree + 1):
        derivs[0][j] = ndu[j][degree]

    # compute the derivatives
    a = [[0.0 for _ in range(degree + 1)] for _ in range(2)]

    for r in range(degree + 1):
        s1 = 0
        s2 = 1
        a[0][0] = 1.0

        for k in range(1, n + 1):
            d = 0.0
            rk = r - k
            pk = degree - k

            if r >= k:
                a[s2][0] = a[s1][0] / ndu[pk + 1][rk]
                d = a[s2][0] * ndu[rk][pk]

            if rk >= -1:
                j1 = 1
            else:
                j1 = -rk

            if r - 1 <= pk:
                j2 = k - 1
            else:
                j2 = degree - r

            for j in range(j1, j2 + 1):
                a[s2][j] = (a[s1][j] - a[s1][j - 1]) / ndu[pk + 1][rk + j]
                d += a[s2][j] * ndu[rk + j][pk]

            if r <= pk:
                a[s2][k] = -a[s1][k - 1] / ndu[pk + 1][r]
                d += a[s2][k] * ndu[r][pk]

            derivs[k][r] = d

            j = s1
            s1 = s2
            s2 = j

    # Multiply through by the correct factors
    r = degree
    for k in range(1, n + 1):
        for j in range(degree + 1):
            derivs[k][j] *= r
        r *= degree - k

    return derivs
