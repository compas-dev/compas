from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'fibonacci',
    'avrg',
    'var',
    'st_dev'
]


def fibonacci(n, memo={}):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 1
    if n not in memo:
        memo[n] = fibonacci(n - 2, memo) + fibonacci(n - 1, memo)
    return memo[n]

def avrg(list):
    """Average of a list.

    Parameters
    ----------
    list : list
        List of values.

    Returns
    -------
    float
        The mean value.

    """

    return sum(list) / float(len(list))

def var(list):
    """Variance of a list.

    Parameters
    ----------
    list : list
        List of values.

    Returns
    -------
    float
        The variance value.

    """

    m = avrg(list)

    return (sum([(i - m) ** 2 for i in list]) / float(len(list))) ** .5

def st_dev(list):
    """Standard deviation of a list.

    Parameters
    ----------
    list : list
        List of values.

    Returns
    -------
    float
        The standard deviation value.

    """

    return var(list) ** .5

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    print(fibonacci(100))
