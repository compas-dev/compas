from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

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

import pstats

from functools import wraps


__all__ = [
    'print_profile',
]


def print_profile(func):
    """Decorate a function with automatic profile printing.

    Parameters:
        func (function) : The function to decorate.

    Returns:
        function : The decorated function.

    Examples:

        .. code-block:: python

            @print_profile
            def f(n):
                \"\"\"Sum up all integers below n.\"\"\"
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
        stats  = pstats.Stats(profile, stream=stream)
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

    @print_profile
    def f(n):
        """sum all integers below n"""
        s = 0
        for i in range(n):
            s += i
        return s

    print(f(100))

    print(f.__doc__)
    print(f.__name__)
