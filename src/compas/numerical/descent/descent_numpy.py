
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

try:
    from numpy import array
    from numpy import eye
    from numpy import finfo
    from numpy import float64
    from numpy import maximum
    from numpy import mean
    from numpy import newaxis
    from numpy import ones
    from numpy import reshape
    from numpy import sqrt
    from numpy import sum
    from numpy import zeros

except ImportError:
    compas.raise_if_not_ironpython()

else:
    eps = finfo(float64).eps
    e = sqrt(eps)


__all__ = ['descent_numpy']


def descent_numpy(x0, fn, iterations=1000, gtol=10**(-6), bounds=None, limit=0, args=()):

    """A gradient descent optimisation solver.

    Parameters
    ----------
    x0 : array-like
        n x 1 starting guess of x.
    fn : obj
        The objective function to minimize.
    iterations : int
        Maximum number of iterations.
    gtol : float
        Mean residual of the gradient for convergence.
    bounds : list
        List of lower and upper bound pairs [[lb, ub], ...], None=unconstrained.
    limit : float
        Value of the objective function for which to terminate optimisation.
    args : tuple
        Additional parameters needed for fn.

    Returns
    -------
    float
        Final value of the objective function.
    array
        Values of x at the found local minimum.

    """

    r  = 0.5
    c  = 0.0001
    n  = len(x0)
    x0 = reshape(array(x0), (n, 1))

    if bounds:
        bounds = array(bounds)
        lb = bounds[:, 0][:, newaxis]
        ub = bounds[:, 1][:, newaxis]
    else:
        lb = ones((n, 1)) * -10**20
        ub = ones((n, 1)) * +10**20

    zn = zeros((n, 1))
    g  = zeros((n, 1))
    v  = eye(n) * e

    def phi(x, mu, *args):
        p = mu * (sum(maximum(lb - x, zn)) + sum(maximum(x - ub, zn)))**2
        return fn(x, *args) + p

    i  = 0
    mu = 1

    while i < iterations:

        p0 = phi(x0, mu, *args)

        for j in range(n):
            vj = v[:, j][:, newaxis]
            g[j, 0] = (phi(x0 + vj, mu, *args) - p0) / e

        D = sum(-g * g)

        a  = 1
        x1 = x0 - a * g

        while phi(x1, mu, *args) > p0 + c * a * D:
            a *= r
            x1 = x0 - a * g

        x0 -= a * g

        mu  *= 10
        res = mean(abs(g))
        i   += 1
        f1  = phi(x0, mu, *args)

        if f1 < limit:
            break

        if res < gtol:
            break

        print('Iteration: {0}  fopt: {1:.3g}  gres: {2:.3g}  step: {3}'.format(i, f1, res, a))

    return f1, x0


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    def fn(u, *args):

        # Booth's function, fopt=0, uopt=(1, 3)

        x = u[0]
        y = u[1]
        z = (x + 2 * y - 7)**2 + (2 * x + y - 5)**2

        return float(z)

    x0 = [-6., -6.]
    bounds = [[0, 2], [2, 4]]
    fopt, uopt = descent_numpy(x0, fn, gtol=10**(-4), bounds=bounds)

    print(uopt)
