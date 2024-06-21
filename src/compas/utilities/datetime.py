from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import time


def timestamp():
    """Generate a timestamp using the current date and time.

    Returns
    -------
    str
        The timestamp.

    Examples
    --------
    >>> type(timestamp()) == type("")
    True

    """
    return datetime.datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")


def now():
    """Generate a timestamp using the current date and time.

    Returns
    -------
    str
        The timestamp.

    Examples
    --------
    >>> type(now()) == type("")
    True

    """
    return timestamp()
