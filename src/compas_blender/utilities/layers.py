from compas_blender.utilities.objects import delete_objects
from compas_blender.utilities.objects import delete_all_objects
from compas_blender.utilities.objects import get_objects

try:
    import bpy
except ImportError:
    pass


__all__ = [
    'clear_layers',
    'layer_mask'
]


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


def clear_layers(layers):
    """ Deletes all objects in given layers.

    Parameters:
        layers (list, str): Layers or 'all'.

    Returns:
        None
    """
    if layers == 'all':
        delete_all_objects()
    elif isinstance(layers, int):
        delete_objects(get_objects(layers))
    elif isinstance(layers, list):
        for layer in layers:
            delete_objects(get_objects(layer))


def layer_mask(layer):
    """ Creates a boolean layer mask.

    Parameters:
        layer (int): Layer number.

    Returns:
        tuple: True at given layer number and False elsewhere.
    """
    return tuple(i == layer for i in range(20))


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    pass
