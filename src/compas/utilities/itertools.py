# recipes with itertools
# see: https://docs.python.org/3.6/library/itertools.html
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from itertools import islice
from itertools import chain
from itertools import repeat
from itertools import tee

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest


__all__ = [
    'meshgrid',
    'linspace',
    'flatten',
    'pairwise',
    'window',
    'iterable_like'
]


def meshgrid(x, y, indexing='xy'):
    """Construct coordinate matrices from two coordinate vectors.

    This function mimicks the functionality of ``numpy.meshgrid`` [1], but in a simpler form.

    Parameters
    ----------
    x : list of float
    y : list of float
    indexing : {'xy', 'ij'}, optional
        Default is ``'xy'``.

    Returns
    -------
    (list of list, list of list)
        The X and Y values of the coordinate grid.

    Examples
    --------
    >>> from compas.utilities import linspace, meshgrid
    >>> x = list(linspace(0, 1, 3))
    >>> y = list(linspace(0, 1, 2))

    >>> X, Y = meshgrid(x, y)
    >>> X
    [[0.0, 0.5, 1.0], [0.0, 0.5, 1.0]]
    >>> Y
    [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]

    >>> X, Y = meshgrid(x, y, 'ij')
    >>> X
    [[0.0, 0.0], [0.5, 0.5], [1.0, 1.0]]
    >>> Y
    [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]]

    References
    ----------
    .. [1] ``numpy.meshgrid`` Available at https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html
    """
    if indexing == 'xy':
        X = [[x[j] for j in range(len(x))] for i in range(len(y))]
        Y = [[y[i] for j in range(len(x))] for i in range(len(y))]
        return X, Y
    X = [[x[i] for j in range(len(y))] for i in range(len(x))]
    Y = [[y[j] for j in range(len(y))] for i in range(len(x))]
    return X, Y


def linspace(start, stop, num=50):
    """Generate a sequence of evenly spaced numbers over a specified interval.

    This function mimicks the functionality of ``numpy.linspace`` [1], but in a simpler form.

    Parameters
    ----------
    start : float
        The start value of the sequence.
    stop : float
        The end value of the sequence.
    num : int
        The number of elements in the sequence.

    Yields
    ------
    float
        The next value in the sequence.

    Examples
    --------
    >>> from compas.utilities import linspace
    >>> list(linspace(0, 1, 3))
    [0.0, 0.5, 1.0]

    References
    ----------
    .. [1] ``numpy.linspace`` Available at https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
    """
    step = (stop - start) / (num - 1)
    for i in range(num):
        yield start + i * step


def flatten(listOfLists):
    """Flatten one level of nesting"""
    return chain.from_iterable(listOfLists)


def pairwise(iterable):
    """Returns a sliding window of size 2 over the data of the iterable.

    Parameters
    ----------
    iterable : iterable
        A sequence of items.

    Yields
    ------
    tuple
        Two items per iteration, if there are at least two items in the iterable.

    Examples
    --------
    >>> for a, b in pairwise(range(5)):
    ...     print(a, b)
    ...
    0 1
    1 2
    2 3
    3 4
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def window(seq, n=2):
    """Returns a sliding window (of width n) over the data from the iterable.

    Parameters
    ----------
    seq : iterable
        A sequence of items.
    n : int, optional
        The width of the sliding window.

    Yields
    ------
    tuple
        A tuple of size `n` at every iteration,
        if there are at least `n` items in the sequence.

    Examples
    --------
    >>> for view in window(range(10), 3):
    ...     print(view)
    ...
    (0, 1, 2)
    (1, 2, 3)
    (2, 3, 4)
    (3, 4, 5)
    (4, 5, 6)
    (5, 6, 7)
    (6, 7, 8)
    (7, 8, 9)

    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def iterable_like(target, reference, fillvalue=None):
    """Creates an iterator from a reference object with size equivalent to that of a target iterable.

    Values will be yielded one at a time until the target iterable is exhausted.
    If target and reference are of uneven size, fillvalue will be used to
    substitute the missing values.

    Parameters
    ----------
    target : iterable
        An iterable to be matched in size.
    reference: iterable
        Iterable taken as basis for pairing.
    fillvalue : object, optional
        Defaults to `None`.

    Returns
    -------
    object
        The next value in the iterator

    Notes
    -----
    This function can also produce an iterable capped to the size of target
    whenever the supplied reference is larger.

    Examples
    --------
    >>> keys = [0, 1, 2, 3]
    >>> color = (255, 0, 0)
    >>> list(iterable_like(keys, [color], color))
    [(255, 0, 0), (255, 0, 0), (255, 0, 0), (255, 0, 0)]
    >>> list(iterable_like(color, keys))
    [0, 1, 2]
    """
    target, counter = tee(target)
    zipped = zip_longest(target, reference, fillvalue=fillvalue)
    for _ in counter:
        yield next(zipped)[1]


# ==============================================================================
# Other
# ==============================================================================


def take(n, iterable):
    """Return the first n items of the iterable as a list.

    Parameters
    ----------
    n : int
        The number of items.
    iterable : iterable
        An iterable object.

    Returns
    -------
    list
        A list with the first `n` items of `iterable`.

    Examples
    --------
    >>> take(5, range(100))
    [0, 1, 2, 3, 4]
    """
    return list(islice(iterable, n))


def nth(iterable, n, default=None):
    """Returns the nth item or a default value"""
    return next(islice(iterable, n, None), default)


def padnone(iterable):
    """Returns the sequence elements and then returns None indefinitely.

    Useful for emulating the behavior of the built-in map() function.
    """
    return chain(iterable, repeat(None))


# def grouper(iterable, n, fillvalue=None):
#     """Collect data into fixed-length chunks or blocks"""
#     # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"""
#     args = [iter(iterable)] * n
#     return zip_longest(*args, fillvalue=fillvalue)


# def random_product(*args, repeat=1):
#     """Random selection from itertools.product(*args, **kwds)"""
#     pools = [tuple(pool) for pool in args] * repeat
#     return tuple(random.choice(pool) for pool in pools)


# def random_permutation(iterable, r=None):
#     """Random selection from itertools.permutations(iterable, r)"""
#     pool = tuple(iterable)
#     r = len(pool) if r is None else r
#     return tuple(random.sample(pool, r))


# def random_combination(iterable, r):
#     """Random selection from itertools.combinations(iterable, r)"""
#     pool = tuple(iterable)
#     n = len(pool)
#     indices = sorted(random.sample(range(n), r))
#     return tuple(pool[i] for i in indices)


# def random_combination_with_replacement(iterable, r):
#     """Random selection from itertools.combinations_with_replacement(iterable, r)"""
#     pool = tuple(iterable)
#     n = len(pool)
#     indices = sorted(random.randrange(n) for i in range(r))
#     return tuple(pool[i] for i in indices)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
