from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import functools
import pstats

from functools import wraps

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

try:
    import cProfile as Profile
except ImportError:
    import profile as Profile


__all__ = [
    'abstractstaticmethod',
    'abstractclassmethod',
    'memoize',
    'print_profile'
]


class abstractstaticmethod(staticmethod):
    """Decorator for declaring a static method abstract.

    Parameters
    ----------
    function : callable
        The method to declare abstract static.
    """

    __slots__ = ()

    __isabstractmethod__ = True

    def __init__(self, function):
        function.__isabstractmethod__ = True
        super(abstractstaticmethod, self).__init__(function)


class abstractclassmethod(classmethod):
    """Decorator for declaring a class method abstract.

    Parameters
    ----------
    function : callable
        The class method to declare abstract.
    """

    __slots__ = ()

    __isabstractmethod__ = True

    def __init__(self, function):
        function.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(function)


def memoize(func, *args, **kwargs):
    """Decorator to wrap a function with a memoizing callable.

    Parameters
    ----------
    func : callable
        The function that should be memoized.

    Returns
    -------
    memoized_func : callable
        A wrapper for the original function that returns a previously
        computed and cached result when possible.
    """
    cache = func.cache = {}

    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return memoized_func


def print_profile(func):
    """Decorate a function with automatic profile printing.

    Parameters
    ----------
    func : callable
        The function to decorate.

    Returns
    -------
    callable
        The decorated function.

    Examples
    --------
    .. code-block:: python

        @print_profile
        def f(n):
            return sum(for i in range(n))

        print(f(100))
        print(f.__doc__)
        print(f.__name__)

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        profile = Profile.Profile()
        profile.enable()
        #
        res = func(*args, **kwargs)
        #
        profile.disable()
        stream = StringIO()
        stats = pstats.Stats(profile, stream=stream)
        stats.strip_dirs()
        stats.sort_stats(1)
        stats.print_stats(20)
        print(stream.getvalue())
        #
        return res
    return wrapper


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
