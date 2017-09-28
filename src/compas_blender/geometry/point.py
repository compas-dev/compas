from compas_blender.utilities.layers import layer_mask
from compas_blender.utilities.objects import deselect_all_objects

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'add_empty'
]


def add_empty(type='PLAIN_AXES', location=[0, 0, 0], layer=0, radius=1):
    """ Creates an Empty object.

    Parameters:
        type (str): Display type: 'PLAIN_AXES', 'ARROWS', 'SINGLE_ARROW', 'CIRCLE', 'CUBE', 'SPHERE', 'CONE'.
        location (list): Co-ordinates for Empty.
        layer (int): Layer number.
        radius (float): Size of the Empty.

    Returns:
        obj: Created Empty object.
    """
    bpy.ops.object.empty_add(type=type, radius=radius, view_align=False, location=location, layers=layer_mask(layer))
    deselect_all_objects()
    return bpy.context.object


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    add_empty(type='PLAIN_AXES', location=[0, 0, 1])
    add_empty(type='ARROWS', location=[2, 0, 1])
    add_empty(type='SINGLE_ARROW', location=[4, 0, 1])
    add_empty(type='CUBE', location=[6, 0, 1])
    add_empty(type='SPHERE', location=[8, 0, 1])
