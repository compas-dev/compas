from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = []


class Descriptor(object):

    def __init__(self, value=None):
        self.value = value

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value


class Float(Descriptor):

    def __init__(self, value, minval=None, maxval=None):
        if minval is not None and maxval is not None:
            if minval > maxval:
                raise Exception('The minimum value cannot be greater than the maximum value.')
        if minval is not None:
            self.minval = float(minval)
            if value < minval:
                raise Exception('The default value is lower than the minimum value.')
        if maxval is not None:
            self.maxval = float(maxval)
            if value > maxval:
                raise Exception('The default value is higher than the maximum value.')
        self.value = float(value)

    def __get__(self, instamce, owner):
        



# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
