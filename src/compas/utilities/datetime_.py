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
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')


def now():
    return timestamp()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    print(timestamp())
