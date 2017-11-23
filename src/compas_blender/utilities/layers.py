from compas_blender.utilities import delete_objects
from compas_blender.utilities import delete_all_objects
from compas_blender.utilities import get_objects

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'clear_layer',
    'clear_layers',
    'layer_mask'
]


def clear_layer(layer):
    """ Deletes objects in given layer.

    Parameters:
        layer (int): Layer number.

    Returns:
        None
    """
    delete_objects(get_objects(layer=layer))


def clear_layers(layers):
    """ Deletes objects in given layers.

    Parameters:
        layers (list, str): Layers or 'all'.

    Returns:
        None
    """
    if layers == 'all':
        delete_all_objects()
    elif isinstance(layers, list):
        for layer in layers:
            delete_objects(get_objects(layer=layer))


def clear_current_layer():
    raise NotImplementedError


def layer_mask(layer):
    """ Creates a boolean layer mask.

    Parameters:
        layer (int): Layer number.

    Returns:
        tuple: True at given layer number and False elsewhere.
    """
    return tuple(i == layer for i in range(20))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    print(layer_mask(layer=0))
    clear_layers(layers=[0, 1])
