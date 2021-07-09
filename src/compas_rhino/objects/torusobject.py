from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.objects._shapeobject import ShapeObject


class TorusObject(ShapeObject):

    def __init__(self, shape, u=None, v=None, **kwargs):
        super(TorusObject, self).__init__(shape, **kwargs)
        self.artist.u = u
        self.artist.v = v
