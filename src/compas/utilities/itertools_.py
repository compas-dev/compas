# recipes with itertools
# see: https://docs.python.org/3.6/library/itertools.html
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import random
# import collections
# import operator

# from operator import itemgetter

from itertools import islice
# from itertools import count
# from itertools import groupby
from itertools import chain
# from itertools import repeat
# from itertools import starmap
from itertools import tee
# from itertools import cycle
# from itertools import filterfalse
# from itertools import combinations

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest


__all__ = [
    'flatten',
    'pairwise',
    'window',
    'iterable_like'
]


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


# def take(n, iterable):
#     """Return the first n items of the iterable as a list.

#     Parameters
#     ----------
#     n : int
#         The number of items.
#     iterable : iterable
#         An iterable object.

#     Returns
#     -------
#     list
#         A list with the first `n` items of `iterable`.

#     Examples
#     --------
#     >>> take(5, range(100))
#     [0, 1, 2, 3, 4]
#     """
#     return list(islice(iterable, n))


# def tabulate(function, start=0):
#     """Return function(0), function(1), ..."""
#     return map(function, count(start))


# def tail(n, iterable):
#     """Return an iterator over the last n items"""
#     # tail(3, 'ABCDEFG') --> E F G
#     return iter(collections.deque(iterable, maxlen=n))


# def consume(iterator, n):
#     """Advance the iterator n-steps ahead. If n is none, consume entirely."""
#     # Use functions that consume iterators at C speed.
#     if n is None:
#         # feed the entire iterator into a zero-length deque
#         collections.deque(iterator, maxlen=0)
#     else:
#         # advance to the empty slice starting at position n
#         next(islice(iterator, n, n), None)


# def nth(iterable, n, default=None):
#     """Returns the nth item or a default value"""
#     return next(islice(iterable, n, None), default)


# def all_equal(iterable):
#     """Returns True if all the elements are equal to each other"""
#     g = groupby(iterable)
#     return next(g, True) and not next(g, False)


# def quantify(iterable, pred=bool):
#     """Count how many times the predicate is true"""
#     return sum(map(pred, iterable))


# def padnone(iterable):
#     """Returns the sequence elements and then returns None indefinitely.

#     Useful for emulating the behavior of the built-in map() function.
#     """
#     return chain(iterable, repeat(None))


# def ncycles(iterable, n):
#     """Returns the sequence elements n times"""
#     return chain.from_iterable(repeat(tuple(iterable), n))


# def dotproduct(vec1, vec2):
#     """Compute the dot product of two vectors of arbitrary but equal length.
#     """
#     return sum(map(operator.mul, vec1, vec2))


# def repeatfunc(func, times=None, *args):
#     """Repeat calls to func with specified arguments."""
#     if times is None:
#         return starmap(func, repeat(args))
#     return starmap(func, repeat(args, times))


# def grouper(iterable, n, fillvalue=None):
#     """Collect data into fixed-length chunks or blocks"""
#     # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"""
#     args = [iter(iterable)] * n
#     return zip_longest(*args, fillvalue=fillvalue)


# def roundrobin(*iterables):
#     """roundrobin('ABC', 'D', 'EF') --> A D E B F C"""
#     # Recipe credited to George Sakkis
#     pending = len(iterables)
#     nexts = cycle(iter(it).__next__ for it in iterables)
#     while pending:
#         try:
#             for next in nexts:
#                 yield next()
#         except StopIteration:
#             pending -= 1
#             nexts = cycle(islice(nexts, pending))


# def partition(pred, iterable):
#     'Use a predicate to partition entries into false entries and true entries'
#     # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
#     t1, t2 = tee(iterable)
#     return filterfalse(pred, t1), filter(pred, t2)


# def powerset(iterable):
#     """powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
#     s = list(iterable)
#     return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


# def unique_everseen(iterable, key=None):
#     """List unique elements, preserving order. Remember all elements ever seen."""
#     # unique_everseen('AAAABBBCCDAABBB') --> A B C D
#     # unique_everseen('ABBCcAD', str.lower) --> A B C D
#     seen = set()
#     seen_add = seen.add
#     if key is None:
#         for element in filterfalse(seen.__contains__, iterable):
#             seen_add(element)
#             yield element
#     else:
#         for element in iterable:
#             k = key(element)
#             if k not in seen:
#                 seen_add(k)
#                 yield element


# def unique_justseen(iterable, key=None):
#     """List unique elements, preserving order. Remember only the element just seen."""
#     # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
#     # unique_justseen('ABBCcAD', str.lower) --> A B C A D
#     return map(next, map(itemgetter(1), groupby(iterable, key)))


# def iter_except(func, exception, first=None):
#     """Call a function repeatedly until an exception is raised.

#     Converts a call-until-exception interface to an iterator interface.
#     Like builtins.iter(func, sentinel) but uses an exception instead
#     of a sentinel to end the loop.

#     Examples:
#         iter_except(functools.partial(heappop, h), IndexError)   # priority queue iterator
#         iter_except(d.popitem, KeyError)                         # non-blocking dict iterator
#         iter_except(d.popleft, IndexError)                       # non-blocking deque iterator
#         iter_except(q.get_nowait, Queue.Empty)                   # loop over a producer Queue
#         iter_except(s.pop, KeyError)                             # non-blocking set iterator

#     """
#     try:
#         if first is not None:
#             yield first()            # For database APIs needing an initial cast to db.first()
#         while True:
#             yield func()
#     except exception:
#         pass


# def first_true(iterable, default=False, pred=None):
#     """Returns the first true value in the iterable.

#     If no true value is found, returns *default*

#     If *pred* is not None, returns the first item
#     for which pred(item) is true.

#     """
#     # first_true([a,b,c], x) --> a or b or c or x
#     # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
#     return next(filter(pred, iterable), default)


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
