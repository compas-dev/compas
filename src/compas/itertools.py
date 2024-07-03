# recipes with itertools
# see: https://docs.python.org/3.6/library/itertools.html
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import reduce
from itertools import chain
from itertools import islice
from itertools import repeat
from itertools import tee
from operator import mul

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest  # type: ignore

__all__ = [
    "normalize_values",
    "remap_values",
    "meshgrid",
    "linspace",
    "flatten",
    "reshape",
    "pairwise",
    "window",
    "iterable_like",
]


def normalize_values(values, new_min=0.0, new_max=1.0):
    """Normalize a list of numbers to the range between new_min and new_max.

    Parameters
    ----------
    values : sequence[float]
        The data to be normalized.
    new_min : float, optional
        The new minimum of the data.
    new_max : float, optional
        The new maximum of the data.

    Returns
    -------
    list[float]
        A new list of floats mapped to the range `new_min`, `new_max`.

    Examples
    --------
    >>> data = list(range(5, 15))
    >>> data = normalize_values(data)
    >>> min(data)
    0.0
    >>> max(data)
    1.0

    """
    old_max = max(values)
    old_min = min(values)
    old_range = old_max - old_min
    new_range = new_max - new_min
    return [(((value - old_min) * new_range) / old_range) + new_min for value in values]


def remap_values(values, target_min=0.0, target_max=1.0, original_min=None, original_max=None):
    """Maps a list of numbers from one domain to another.

    Parameters
    ----------
    values : sequence[int | float]
        The value to remap
    target_min : int | float, optional
        The minimun value of the target domain.
    target_max : int | float, optional
        The maximum value of the target domain.
    original_min : int | float, optional
        The minimun value of the original domain, other than the actual minimum value.
    original_max : int | float, optional
        The maximum value of the original domain, other than the actual maximum value.

    Returns
    -------
    list[float]
        The remaped list of values.

    """
    if original_min is None:
        original_min = min(values)
    if original_max is None:
        original_max = max(values)
    original_range = original_max - original_min
    target_range = target_max - target_min
    ratio = target_range / original_range
    return [target_min + ((value - original_min) * ratio) for value in values]


def meshgrid(x, y, indexing="xy"):
    """Construct coordinate matrices from two coordinate vectors.

    Parameters
    ----------
    x : list[float]
        The values of the "x axis" of the grid.
    y : list[float]
        The values of the "y axis" of the grid.
    indexing : Literal['xy', 'ij'], optional
        The indexing strategy determines the structure of the output.

    Returns
    -------
    list[list[float]]
        The X values of the coordinate grid.
    list[list[float]]
        The Y values of the coordinate grid.

    Notes
    -----
    The output of this function consists of two "matrices", `X` and `Y`.
    The structure of the matrices is determined by the choice of `indexing`.
    Assuming ``m = len(x)`` and ``n = len(y)``.
    If `indexing` is ``'xy'``,
    the shape of both matrices is ``(n, m)``,
    with `X` containing the elements of `x` in its rows, and `Y` the elements of `y` in its columns.
    If `indexing` is ``'ij'``,
    the shape of both matrices is ``(m, n)``,
    with `X` containing the elements of `x` in its columns, and `Y` the elements of `y` in its rows.

    References
    ----------
    This function mimicks the functionality of ``numpy.meshgrid`` [1]_, but in a simpler form.

    .. [1] `numpy.meshgrid`.
           Available at https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html

    Examples
    --------
    >>> from compas.itertools import linspace, meshgrid
    >>> x = list(linspace(0, 1, 3))
    >>> y = list(linspace(0, 1, 2))

    >>> X, Y = meshgrid(x, y)
    >>> X
    [[0.0, 0.5, 1.0], [0.0, 0.5, 1.0]]
    >>> Y
    [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]

    >>> X, Y = meshgrid(x, y, "ij")
    >>> X
    [[0.0, 0.0], [0.5, 0.5], [1.0, 1.0]]
    >>> Y
    [[0.0, 1.0], [0.0, 1.0], [0.0, 1.0]]

    """
    x = list(x)
    y = list(y)
    if indexing == "xy":
        X = [[x[j] for j in range(len(x))] for i in range(len(y))]
        Y = [[y[i] for j in range(len(x))] for i in range(len(y))]
    else:
        X = [[x[i] for j in range(len(y))] for i in range(len(x))]
        Y = [[y[j] for j in range(len(y))] for i in range(len(x))]
    return X, Y


def linspace(start, stop, num=50):
    """Generate a sequence of evenly spaced numbers over a specified interval.

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

    Raises
    ------
    ValueError
        If the number of elements is less than 2.

    References
    ----------
    This function mimicks the functionality of ``numpy.linspace`` [1]_, but in a simpler form.

    .. [1] ``numpy.linspace`` Available at https://numpy.org/doc/stable/reference/generated/numpy.linspace.html

    Examples
    --------
    >>> from compas.itertools import linspace
    >>> list(linspace(0, 1, 3))
    [0.0, 0.5, 1.0]

    """
    if num < 2:
        raise ValueError("ValueError: number of elements must be at least 2, got {:d}".format(num))

    step = (stop - start) / (num - 1)
    for i in range(num - 1):
        yield start + i * step
    yield float(stop)


def flatten(list_of_lists):
    """Flatten one level of nesting.

    Parameters
    ----------
    list_of_lists : iterable[iterable[Any]]
        An iterable object containing other iterable objects.

    Returns
    -------
    iterable
        An iterable containing the elements of the elements of the nested iterables.

    """
    return chain.from_iterable(list_of_lists)


def reshape(lst, shape):
    """Gives a new shape to an array without changing its data.

    This function mimics the functionality of ``numpy.reshape`` [1]_, but in a simpler form.

    Parameters
    ----------
    lst : list
        A list of items.
    shape : int or tuple of ints
        The new shape of the list


    Examples
    --------
    >>> a = [1, 2, 3, 4, 5, 6]
    >>> reshape(a, (2, 3))
    [[1, 2, 3], [4, 5, 6]]
    >>> reshape(a, (3, 2))
    [[1, 2], [3, 4], [5, 6]]
    >>> a = [[1, 2], [3, 4], [5, 6]]
    >>> reshape(a, (2, 3))
    [[1, 2, 3], [4, 5, 6]]


    References
    ----------
    .. [1] ``numpy.reshape`` Available at https://numpy.org/doc/stable/reference/generated/numpy.reshape.html

    """

    def helper(l, shape):  # noqa E741
        if len(shape) == 1:
            if len(l) % shape[0] != 0:
                raise ValueError("ValueError: cannot reshape array of size %d into shape %s" % (len(lst), shape))
            return l
        else:
            n = reduce(mul, shape[1:])
            return [helper(l[i * n : (i + 1) * n], shape[1:]) for i in range(len(l) // n)]

    shape = (shape,) if isinstance(shape, int) else shape
    flattened_list = list(flatten(lst)) if isinstance(lst[0], list) else lst
    if len(list(flattened_list)) != reduce(lambda x, y: x * y, shape):
        raise ValueError("ValueError: cannot reshape array of size %d into shape %s" % (len(lst), shape))
    return helper(flattened_list, shape)


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

    Parameters
    ----------
    target : iterable
        An iterable to be matched in size.
    reference: iterable
        The iterable containing the original data.
    fillvalue : object, optional
        A value to replace missing items.

    Yields
    ------
    object
        The next value in the iterator.

    Notes
    -----
    Values will be yielded one at a time until the reference iterable is exhausted.
    If `target` contains more values than `reference`, `fillvalue` will be used to cover the difference.
    Otherwise, only the same number of items from `reference` will be yielded as there would have been from `target`.

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


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks."""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


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
