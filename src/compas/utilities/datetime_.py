from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time
import datetime


__all__ = [
    'timestamp',
    'now'
]


def timestamp():
    """Generate a timestamp using the current date and time.

    Returns
    -------
    str
        The timestamp.

    Examples
    --------
    >>> type(timestamp()) == type('')
    True
    """
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')


def now():
    """Generate a timestamp using the current date and time.

    Returns
    -------
    str
        The timestamp.

    Examples
    --------
    >>> type(now()) == type('')
    True
    """
    return timestamp()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    doctest.testmod(globs=globals())
