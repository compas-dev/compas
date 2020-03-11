from compas_blender.utilities import delete_objects
from compas_blender.utilities import get_objects

try:
    import bpy
except ImportError:
    pass


__all__ = [
    'create_layer',
    'create_layers',
    'create_layers_from_path',
    'create_layers_from_paths',
    'create_layers_from_dict',
    'clear_layer',
    'clear_layers',
    'clear_current_layer',
    'delete_layer',
    'delete_layers',
]


# ==============================================================================
# create
# ==============================================================================

def create_layer(layer):
    collection = bpy.data.collections.new(layer)
    bpy.context.scene.collection.children.link(collection)


def create_layers(layers):
    for layer in layers:
        create_layer(layer=layer)


def create_layers_from_path(path, separator='::'):
    raise NotImplementedError


def create_layers_from_paths(paths, separator='::'):
    for path in paths:
        create_layers_from_path(path=path)


def create_layers_from_dict(layers):
    raise NotImplementedError


# ==============================================================================
# clear
# ==============================================================================

def clear_layer(layer):
    objects = get_objects(layer=layer)
    if objects:
        delete_objects(objects=objects)


def clear_layers(layers):
    for layer in layers:
        clear_layer(layer=layer)


def clear_current_layer():
    raise NotImplementedError


# ==============================================================================
# delete
# ==============================================================================

def delete_layer(layer):
    collection = bpy.data.collections[layer]
    bpy.context.scene.collection.children.unlink(collection)
    # redraw()
    collection = bpy.data.collections[layer]
    bpy.data.collections.remove(collection)


def delete_layers(layers):
    for layer in layers:
        delete_layer(layer=layer)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
