from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = ['SceneObject']


class SceneObject(object):
    """Base class for all objects in a ``Scene``."""

    def __init__(self, scene=None, name=None, layer=None):
        self.scene = scene
        self.name = name
        self.layer = layer
        self.xform = []

    def draw(self):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
