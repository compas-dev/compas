from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

try:
    from numpy import set_printoptions

except ImportError:
    if 'ironpython' not in sys.version.lower():
        raise


__author__    = ['Tom Van Mele <vanmelet@ethz.ch>', 'Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'float_formatter',
    'set_array_print_precision',
    'unset_array_print_precision'
]


float_precision = '2f'


def float_formatter(x):
    """Formats float to truncated string.

    Parameters
    ----------
    x : float
        Input float.

    Returns
    -------
    str
        Truncated string with default precision .2f.

    Notes
    -----
    stackoverflow.com/questions/21008858/formatting-floats-in-a-numpy-array
    float_formatter = lambda x: '%.2f' % x

    Examples
    --------
    >>> float_formatter(3.14159265359)
    '+3.14'

    """
    return '{0:+.{1}}'.format(x, float_precision)


def set_array_print_precision(precision='2f'):
    """Changes float precision of float_formatter.

    Parameters
    ----------
    precision : str
        Precision e.g. '3f'.

    Returns
    -------
    None

    Notes
    -----
    stackoverflow.com/questions/21008858/formatting-floats-in-a-numpy-array
    set_printoptions(formatter={'float_kind': float_formatter})

    Examples
    --------
    >>> set_array_print_precision(precision='4f')
    >>> float_formatter(3.14159265359)
    '+3.1416'
    """
    global float_precision
    float_precision = precision
    set_printoptions(formatter={'float_kind': float_formatter})


def unset_array_print_precision():
    """Unchanges float precision of float_formatter back to default.

    Parameters
    ----------
    None

    Returns
    -------
    None

    """
    set_printoptions(formatter=None)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
