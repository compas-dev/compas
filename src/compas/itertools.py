# recipes with itertools
# see: https://docs.python.org/3.6/library/itertools.html

from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sequence
from functools import reduce
from itertools import chain
from itertools import islice
from itertools import repeat
from itertools import tee
from itertools import zip_longest
from operator import mul
from typing import Any
from typing import overload


def normalize_values(values: Sequence[float], new_min: float = 0.0, new_max: float = 1.0) -> list[float]:
    """Normalize values to a specified range.

    Parameters
    ----------
    values
        The data to be normalized.
    new_min
        The new minimum of the data.
    new_max
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


def remap_values(
    values: Sequence[float],
    target_min: float = 0.0,
    target_max: float = 1.0,
    original_min: float | None = None,
    original_max: float | None = None,
) -> list[float]:
    """Map values from one domain to another.

    Parameters
    ----------
    values
        The values to remap.
    target_min
        The minimum value of the target domain.
    target_max
        The maximum value of the target domain.
    original_min
        The minimum value of the original domain.
        By default, the minimum of `values` is used.
    original_max
        The maximum value of the original domain, other than the actual maximum value.
        By default, the maximum of `values` is used.

    Returns
    -------
    list[float]
        The remapped values.

    """
    if original_min is None:
        original_min = min(values)
    if original_max is None:
        original_max = max(values)
    original_range = original_max - original_min
    target_range = target_max - target_min
    ratio = target_range / original_range
    return [target_min + ((value - original_min) * ratio) for value in values]


def meshgrid[T, U](
    x: Iterable[T],
    y: Iterable[U],
    indexing: str = "xy",
) -> tuple[list[list[T]], list[list[U]]]:
    """Construct coordinate matrices from two coordinate vectors.

    Parameters
    ----------
    x
        The values of the x-axis of the grid.
    y
        The values of the y-axis of the grid.
    indexing
        The indexing strategy determines the structure of the output.

    Returns
    -------
    tuple[list[list[T]], list[list[U]]]
        The X and Y values of the coordinate grid, in that order.

    Notes
    -----
    The output of this function consists of two "matrices", `X` and `Y`.
    The structure of the matrices is determined by the choice of `indexing`.
    Assuming `m = len(x)` and `n = len(y)`.
    If `indexing` is `"xy"`,
    the shape of both matrices is `(n, m)`,
    with `X` containing the elements of `x` in its rows, and `Y` the elements of `y` in its columns.
    Otherwise, the shape of both matrices is `(m, n)`,
    with `X` containing the elements of `x` in its columns, and `Y` the elements of `y` in its rows.

    References
    ----------
    - [NumPy `meshgrid`](https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html)

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


def linspace(start: float, stop: float, num: int = 50) -> Iterator[float]:
    """Generate a sequence of evenly spaced numbers over a specified interval.

    Parameters
    ----------
    start
        The start value of the sequence.
    stop
        The end value of the sequence.
    num
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
    - [NumPy `linspace`](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html)

    Examples
    --------
    >>> from compas.itertools import linspace
    >>> list(linspace(0, 1, 3))
    [0.0, 0.5, 1.0]

    """
    if num < 2:
        raise ValueError(f"ValueError: number of elements must be at least 2, got {num:d}")

    step = (stop - start) / (num - 1)
    for i in range(num - 1):
        yield start + i * step
    yield float(stop)


def flatten[T](list_of_lists: Iterable[Iterable[T]]) -> Iterator[T]:
    """Flatten one level of nesting.

    Parameters
    ----------
    list_of_lists
        An iterable object containing other iterable objects.

    Returns
    -------
    Iterator[T]
        An iterator over the items of the nested iterables.

    """
    return chain.from_iterable(list_of_lists)


def reshape(lst: Sequence[Any], shape: int | tuple[int, ...]) -> Sequence[Any]:
    """Give a new shape to an array without changing its data.

    This function mimics the functionality of `numpy.reshape`, but in a simpler form.

    Parameters
    ----------
    lst
        A list of items.
    shape
        The new shape of the list.

    Returns
    -------
    Sequence[Any]
        The reshaped values.

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
    - [NumPy `reshape`](https://numpy.org/doc/stable/reference/generated/numpy.reshape.html)

    """

    def helper(values: Sequence[Any], dimensions: tuple[int, ...]) -> Sequence[Any]:
        if len(dimensions) == 1:
            if len(values) % dimensions[0] != 0:
                raise ValueError("ValueError: cannot reshape array of size %d into shape %s" % (len(lst), shape))
            return values
        else:
            n = reduce(mul, dimensions[1:])
            return [helper(values[i * n : (i + 1) * n], dimensions[1:]) for i in range(len(values) // n)]

    shape = (shape,) if isinstance(shape, int) else shape
    flattened_list = list(flatten(lst)) if isinstance(lst[0], list) else lst
    if len(list(flattened_list)) != reduce(lambda x, y: x * y, shape):
        raise ValueError("ValueError: cannot reshape array of size %d into shape %s" % (len(lst), shape))
    return helper(flattened_list, shape)


def pairwise[T](iterable: Iterable[T]) -> Iterator[tuple[T, T]]:
    """Return a sliding window of size two over an iterable.

    Parameters
    ----------
    iterable
        A sequence of items.

    Yields
    ------
    tuple[T, T]
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


def window[T](seq: Iterable[T], n: int = 2) -> Iterator[tuple[T, ...]]:
    """Return a sliding window over an iterable.

    Parameters
    ----------
    seq
        A sequence of items.
    n
        The width of the sliding window.

    Yields
    ------
    tuple[T, ...]
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


@overload
def iterable_like[T, U](target: Iterable[T], reference: Iterable[U], fillvalue: U) -> Iterator[U]: ...


@overload
def iterable_like[T, U](target: Iterable[T], reference: Iterable[U], fillvalue: None = None) -> Iterator[U | None]: ...


def iterable_like[T, U](
    target: Iterable[T],
    reference: Iterable[U],
    fillvalue: U | None = None,
) -> Iterator[U | None]:
    """Create an iterator matching the length of a target iterable.

    Parameters
    ----------
    target
        The iterable whose length should be matched.
    reference
        The iterable containing the values to yield.
    fillvalue
        A value to replace missing items.

    Yields
    ------
    U
        The next value when `fillvalue` is provided.
    U | None
        The next value when `fillvalue` is omitted.

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


def take[T](n: int, iterable: Iterable[T]) -> list[T]:
    """Return the first n items of the iterable as a list.

    Parameters
    ----------
    n
        The number of items.
    iterable
        An iterable object.

    Returns
    -------
    list[T]
        A list with the first `n` items of `iterable`.

    Examples
    --------
    >>> take(5, range(100))
    [0, 1, 2, 3, 4]

    """
    return list(islice(iterable, n))


@overload
def nth[T](iterable: Iterable[T], n: int) -> T | None: ...


@overload
def nth[T, U](iterable: Iterable[T], n: int, default: U) -> T | U: ...


def nth[T, U](iterable: Iterable[T], n: int, default: U | None = None) -> T | U | None:
    """Return the item at an index, or a default value.

    Parameters
    ----------
    iterable
        The iterable containing the item.
    n
        The zero-based item index.
    default
        The value returned when the index is not present.

    Returns
    -------
    T | None
        The item, or `None` when `default` is omitted and the index is not present.
    T | U
        The item, or `default` when a default value is provided and the index is not present.

    """
    return next(islice(iterable, n, None), default)


def padnone[T](iterable: Iterable[T]) -> Iterator[T | None]:
    """Return the items of an iterable followed by `None` indefinitely.

    Parameters
    ----------
    iterable
        The iterable to pad.

    Yields
    ------
    T | None
        The original items followed by `None` values.

    """
    return chain(iterable, repeat(None))


def grouper[T, U](iterable: Iterable[T], n: int, fillvalue: U | None = None) -> Iterator[tuple[T | U | None, ...]]:
    """Collect data into fixed-length groups.

    Parameters
    ----------
    iterable
        The iterable to group.
    n
        The number of items per group.
    fillvalue
        The value used to complete the final group.

    Yields
    ------
    tuple[T | U | None, ...]
        A fixed-length group of items.

    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
