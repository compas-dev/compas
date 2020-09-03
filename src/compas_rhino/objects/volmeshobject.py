from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino
from compas_rhino.objects._object import BaseObject


__all__ = ['VolMeshObject']


class VolMeshObject(BaseObject):

    def __init__(self, volmesh, scene=None, name=None, layer=None, visible=True, settings=None):
        super(VolMeshObject, self).__init__(volmesh, scene, name, layer, visible, settings)

    @property
    def volmesh(self):
        return self.item

    @volmesh.setter
    def volmesh(self, volmesh):
        self.item = volmesh

    def clear(self):
        self.artist.clear()

    def draw(self):
        """Draw the object representing the volmesh.
        """
        if not self.visible:
            return
        self.artist.draw()

    def select(self):
        raise NotImplementedError

    def modify(self):
        raise NotImplementedError

    def move(self):
        raise NotImplementedError


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pass
