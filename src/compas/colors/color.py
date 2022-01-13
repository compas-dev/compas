from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data


class Color(Data):

    def __init__(self, r, g, b, alpha=1.0, space='rgb1', **kwargs):
        super(Color, self).__init__(**kwargs)
        self.r = r
        self.g = g
        self.b = b
        self.alpha = alpha
        self.space = space

    @property
    def data(self):
        return {'red': self.red, 'green': self.green, 'blue': self.blue, 'alpha': self.alpha}

    @data.setter
    def data(self, data):
        self.red = data['red']
        self.green = data['green']
        self.blue = data['blue']
        self.alpha = data['alpha']

    @property
    def rgba255(self):
        r = int(self.r * 255)
        g = int(self.g * 255)
        b = int(self.b * 255)
        a = int(self.alpha * 255)
        return r, g, b, a

    @property
    def rgb255(self):
        r = int(self.r * 255)
        g = int(self.g * 255)
        b = int(self.b * 255)
        return r, g, b

    @property
    def rgba1(self):
        r = self.r
        g = self.g
        b = self.b
        a = self.alpha
        return r, g, b, a

    @property
    def rgb1(self):
        r = self.r
        g = self.g
        b = self.b
        return r, g, b

    def __len__(self):
        return 3

    def __iter__(self):
        return iter(self.rgb1)

    @classmethod
    def white(cls):
        return cls(1, 1, 1)

    @classmethod
    def black(cls):
        return cls(0, 0, 0)

    @classmethod
    def grey(cls):
        return cls(0.5, 0.5, 0.5)

    @classmethod
    def red(cls):
        return cls(1.0, 0, 0)

    @classmethod
    def orange(cls):
        return cls(1.0, 0.5, 0)

    @classmethod
    def yellow(cls):
        return cls(1.0, 1.0, 0)

    # chartreuse
    @classmethod
    def lime(cls):
        return cls(0.5, 1.0, 0)

    @classmethod
    def green(cls):
        return cls(0, 1.0, 0)

    # spring
    @classmethod
    def mint(cls):
        return cls(0, 1.0, 0.5)

    @classmethod
    def cyan(cls):
        return cls(0, 1.0, 1.0)

    @classmethod
    def azure(cls):
        return cls(0, 0.5, 1.0)

    @classmethod
    def blue(cls):
        return cls(0, 0, 1.0)

    @classmethod
    def violet(cls):
        return cls(0.5, 0, 1.0)

    @classmethod
    def magenta(cls):
        return cls(1.0, 0, 1.0)

    # rose
    @classmethod
    def pink(cls):
        return cls(1.0, 0, 0.5)

    # other

    @classmethod
    def maroon(cls):
        return cls(0.5, 0, 0)

    @classmethod
    def brown(cls):
        return cls(0.5, 0.25, 0)

    @classmethod
    def olive(cls):
        return cls(0.5, 0.5, 0.0)

    @classmethod
    def teal(cls):
        return cls(0, 0.5, 0.5)

    @classmethod
    def navy(cls):
        return cls(0, 0, 0.5)

    @classmethod
    def purple(cls):
        return cls(0.5, 0, 0.5)

    @classmethod
    def silver(cls):
        return cls(0.75, 0.75, 0.75)

    # @classmethod
    # def dark(cls):
    #     return cls(0.25, 0.25, 0.25)

    # ochre
    # beige
    # bordeaux
    # hotpink
    # steel
    # midnight
    # salmon
