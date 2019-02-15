from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'average',
    'variance',
    'standard_deviation'
]


def average(list):
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

def variance(list):
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

    m = average(list)

    return (sum([(i - m) ** 2 for i in list]) / float(len(list))) ** .5

def standard_deviation(list):
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

    return variance(list) ** .5

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    print(standard_deviation(range(5)))
