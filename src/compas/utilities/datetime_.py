from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time
import datetime


__author__    = 'Tom Van Mele'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'timestamp',
]


def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    print(timestamp())
