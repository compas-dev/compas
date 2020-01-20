from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import abc
import functools


__all__ = ['memoize']


class abstractstatic(staticmethod):
    """Decorator for declaring a static method abstract.

    Parameters
    ----------
    function : callable
        The method to declare abstract static.
    """

    __slots__ = ()

    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True

    __isabstractmethod__ = True


def memoize(func, *args, **kwargs):
    """Decorator to wrap a function with a memoizing callable.

    Parameters
    ----------
    func : callable
        The function that should be memoized.
    """
    cache = func.cache = {}
    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
