"""compas.cad.blender.utilities.modifiers : Blender modifier functions."""

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'bevel',
    'linear_array',
    'subdivide',
    'triangulate'
]


def bevel(object, width=0.2, segments=1, only_vertices=False):
    """ Bevel a Blender mesh object.

    Parameters:
        object (obj): The bmesh object to bevel.
        width (float): Width of the bevel.
        segments (int): Number of bevel segments.
        only_vertices (bool): Bevel only vertices.

    Returns:
        None
    """
    object.modifiers.new('bevel', type='BEVEL')
    object.modifiers['bevel'].width = width
    object.modifiers['bevel'].segments = segments
    object.modifiers['bevel'].use_only_vertices = only_vertices


def linear_array(object, count=2, displace=[1, 0, 0]):
    """ Create a linear array from a Blender mesh object.

    Parameters:
        object (obj): The bmesh object to array.
        count (int): Number of array objects.
        displace (list): [dx, dy, dz] displacements.

    Returns:
        None
    """
    object.modifiers.new('linear_array', type='ARRAY')
    object.modifiers['linear_array'].count = count
    object.modifiers['linear_array'].relative_offset_displace = displace


def subdivide(object, levels=1, type='SIMPLE'):
    """ Subdivides a Blender mesh object.

    Parameters:
        object (obj): The bmesh object to subdivide.
        levels (int): Number of subdivision levels.
        type (str): Subdivision type 'CATMULL_CLARK', 'SIMPLE'.

    Returns:
        None
    """
    object.modifiers.new('subdivision', type='SUBSURF')
    object.modifiers['subdivision'].levels = levels
    object.modifiers['subdivision'].subdivision_type = type


def triangulate(object):
    """ Triangulate a Blender mesh object.

    Parameters:
        object (obj): The bmesh object to triangulate.

    Returns:
        None
    """
    object.modifiers.new('triangulate', type='TRIANGULATE')


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas_blender.utilities import draw_cubes
    from compas_blender.utilities import clear_layers

    clear_layers([0])

    cube = draw_cubes()[0]
    subdivide(cube, levels=2, type='CATMULL_CLARK')
    linear_array(cube, count=3, displace=[2, 1, 1])
    bevel(cube)
    triangulate(cube)
