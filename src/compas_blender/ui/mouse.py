
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import bpy
except ImportError:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'cursor_xyz',
]


def cursor_xyz():
    
    """ Returns the spatial co-ordinates of the cursor.

    Parameters
    ----------
    None

    Returns
    -------
    list: 
        [x, y and z] position of the cursor.
    
    """
    
    return list(bpy.context.scene.cursor_location.copy())


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    print(cursor_xyz())
