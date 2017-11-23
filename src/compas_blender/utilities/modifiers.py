try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
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
        object (obj): The Blender mesh object to bevel.
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
        object (obj): The Blender mesh object to array.
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
        object (obj): The Blender mesh object to subdivide.
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
        object (obj): The Blender mesh object to triangulate.

    Returns:
        None
    """
    object.modifiers.new('triangulate', type='TRIANGULATE')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas_blender.utilities import draw_cuboid
    from compas_blender.utilities import clear_layer

    clear_layer(layer=1)

    cube = draw_cuboid(layer=1)

    subdivide(object=cube, levels=2, type='CATMULL_CLARK')
    triangulate(object=cube)
    linear_array(object=cube, count=3, displace=[2, 1, 1])
    bevel(object=cube, width=0.05, segments=2)
