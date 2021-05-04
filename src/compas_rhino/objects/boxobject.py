from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh
from compas_rhino.objects._shapeobject import ShapeObject


class BoxObject(ShapeObject):

    @property
    def mesh(self):
        if not self._mesh:
            self._mesh = Mesh.from_shape(self.shape)
        return self._mesh
