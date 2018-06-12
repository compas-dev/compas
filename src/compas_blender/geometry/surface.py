from compas_blender.geometry import BlenderGeometry


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['BlenderSurface']


class BlenderSurface(BlenderGeometry):
    """"""

    def __init__(self, object):
        self.guid = object.name
        self.mesh = object
        self.geometry = None
        self.attributes = {}
        self.type = self.mesh.type


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
