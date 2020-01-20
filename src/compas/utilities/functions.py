from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import factorial


__all__ = [
    'fibonacci',
    'binomial_coefficient'
]


def fibonacci(n, memo={}):
    """Memoized function for generating fibonacci numbers.

    Parameters
    ----------
    n : int
        The position of the number in the sequence.
    memo : dict
        The memoization dict.

    Returns
    -------
    int
        The nth fibonacci number.

    Examples
    --------
    >>> fibonacci(0)
    0
    >>> fibonacci(1)
    1
    >>> fibonacci(2)
    1
    >>> fibonacci(3)
    2
    >>> fibonacci(4)
    3
    """
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 1
    if n not in memo:
        memo[n] = fibonacci(n - 2, memo) + fibonacci(n - 1, memo)
    return memo[n]


def binomial_coefficient(n, k):
    """Returns the binomial coefficient of the :math:`x^k` term in the
    polynomial expansion of the binomial power :math:`(1 + x)^n`.

    Notes
    -----
    Arranging binomial coefficients into rows for successive values of `n`,
    and in which `k` ranges from 0 to `n`, gives a triangular array known as
    Pascal's triangle.

    Parameters
    ----------
    n : int
        The number of terms.
    k : int
        The index of the coefficient.

    Returns
    -------
    int
        The coefficient.
    """
    return int(factorial(n) / float(factorial(k) * factorial(n - k)))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    doctest.testmod(globs=globals())
