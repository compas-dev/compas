from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


def is_int3(items):
    return len(items) == 3 and all(isinstance(item, int) for item in items)


def is_float3(items):
    return len(items) == 3 and all(isinstance(item, float) for item in items)
