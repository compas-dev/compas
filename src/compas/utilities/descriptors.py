from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import color_to_rgb

try:
    basestring
except NameError:
    basestring = str


__all__ = [
    'RGBColour',
]


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
        pass


class Colour(Descriptor):
    pass


class RGBColour(Descriptor):

    def __init__(self, default, normalize=False, description=""):
        self.default = default
        self.normalize = normalize
        self.description = description
        self.value = None

    def __get__(self, instance, owner):
        if self.value is None:
            return self.default
        return self.value

    def __set__(self, instance, value):
        color_to_rgb(value, normalize=self.normalize)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
