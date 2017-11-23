try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


def cursor_xyz():
    """ Returns the co-ordinates of the cursor.

    Parameters:
        None

    Returns:
        list: [x, y and z] position.
    """
    return list(bpy.context.scene.cursor_location.copy())


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    print(cursor_xyz())
