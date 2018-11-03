
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

#from compas_blender.utilities import delete_objects
#from compas_blender.utilities import delete_all_objects
#from compas_blender.utilities import get_objects

try:
    import bpy
except ImportError:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'create_layers_from_paths',
    'create_layers_from_dict',
    'create_layers',
#    'clear_layer',
#    'clear_layers',
#    'clear_current_layer',
#    'delete_layers',
#    'layer_mask'
]


def create_layers_from_paths():
    raise NotImplementedError
    

def create_layers_from_dict():
    raise NotImplementedError
    
    
def create_layers():
    raise NotImplementedError
    
    
#def clear_layer(layer):
#    """ Deletes objects in given layer.

#    Parameters:
#        layer (int): Layer number.

#    Returns:
#        None
#    """
#    delete_objects(get_objects(layer=layer))


#def clear_layers(layers):
#    """ Deletes objects in given layers.

#    Parameters:
#        layers (list, str): Layers or 'all'.

#    Returns:
#        None
#    """
#    if layers == 'all':
#        delete_all_objects()
#    elif isinstance(layers, list):
#        for layer in layers:
#            delete_objects(get_objects(layer=layer))


#def clear_current_layer():
#    raise NotImplementedError


#def layer_mask(layer):
#    """ Creates a boolean layer mask.

#    Parameters:
#        layer (int): Layer number.

#    Returns:
#        tuple: True at given layer number and False elsewhere.
#    """
#    return tuple(i == layer for i in range(20))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass

    #create_layers()
    
    #for i in dir(bpy.context): 
        #print(i)
    #print(bpy.data.collections[0].objects[1])
        #print(i)
        #print(dir(bpy.context.layer_collection))
#    print(layer_mask(layer=0))
#    clear_layers(layers=[0, 1])
    #bpy.ops.object.move_to_collection(collection_index=2)
    #
    
    #area = bpy.context.area.type
    #bpy.context.area.type = 'OUTLINER'
    #bpy.ops.outliner.collection_new(nested=True)
    #bpy.context.area.type = area
    #print(a)
    #print(dir(bpy.context))

    #print(bpy.data.collections)
