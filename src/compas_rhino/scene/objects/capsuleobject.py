from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ._shapeobject import ShapeObject


class CapsuleObject(ShapeObject):

    def __init__(self, shape, u=None, v=None, **kwargs):
        super(CapsuleObject, self).__init__(shape, **kwargs)
        self.artist.u = u
        self.artist.v = v
