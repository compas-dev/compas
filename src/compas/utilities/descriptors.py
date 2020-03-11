from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import color_to_rgb

try:
    basestring
except NameError:
    basestring = str


__all__ = [
    'Float', 'RGBColour',
]


class Float(object):
    """Descriptor for properties of type float.

    Parameters
    ----------
    value : float
        The value of the property.
    minval : float, optional
        The minimum value of the property.
    maxval : float, optional
        The maximum value of the property.
    """

    __slots__ = ('value', 'minval', 'maxval')

    def __init__(self, value, minval=None, maxval=None):
        self.minval = None
        self.maxval = None
        if minval is not None:
            self.minval = float(minval)
        if maxval is not None:
            self.maxval = float(maxval)
        if self.minval is not None and self.maxval is not None:
            if self.minval > self.maxval:
                raise ValueError("The minimum value cannot be greater than the maximum value.")
        value = float(value)
        if self.minval is not None:
            if value < self.minval:
                raise ValueError("The value cannot be smaller than the minimum value.")
        if self.maxval is not None:
            if value > self.maxval:
                raise ValueError("The value cannot be greater than the maximum value.")
        self.value = value

    def __get__(self, obj, objtype):
        return self.value

    def __set__(self, obj, value):
        value = float(value)
        if self.minval is not None:
            if value < self.minval:
                raise ValueError("The value cannot be smaller than the minimum value.")
        if self.maxval is not None:
            if value > self.maxval:
                raise ValueError("The value cannot be greater than the maximum value.")
        self.value = value


class RGBColour(object):
    """Descriptor for RGB color properties.

    Parameters
    ----------
    default : tuple
        The default color.
    normalize : bool, optional
        Normalize the color components, if true.
    description : str, optional
        A description of the purpose of the color property.

    Attributes
    ----------
    value : tuple
        The current value of the color property.
    """

    __slots__ = ('default', 'normalize', 'description', 'value')

    def __init__(self, default, normalize=False, description=""):
        self.default = default
        self.normalize = normalize
        self.description = description
        self.value = None

    def __get__(self, obj, objtype):
        if self.value is None:
            return self.default
        return self.value

    def __set__(self, obj, value):
        self.value = color_to_rgb(value, normalize=self.normalize)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
