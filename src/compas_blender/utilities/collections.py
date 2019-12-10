from compas_blender.utilities import delete_objects

try:
    import bpy
except ImportError:
    pass


__all__ = [
    "create_collection",
    "create_collections",
    "create_collections_from_path",
    "clear_collection",
    "clear_collections"
]


# ==============================================================================
# create
# ==============================================================================


def create_collection(name, parent=None):
    if not name:
        return
    collection = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if not parent:
        if collection.name not in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.link(collection)
    else:
        if collection.name not in parent.children:
            parent.children.link(collection)
    return collection


def create_collections(names):
    collections = [create_collection(name) for name in names]
    return collections


def create_collections_from_path(path, separator='::'):
    names = path.split(separator)
    collections = []
    parent = None
    for name in names:
        collection = create_collection(name, parent=parent)
        parent = collection
        collections.append(collection)
    return collections


# ==============================================================================
# clear
# ==============================================================================

def clear_collection(name):
    objects = list(bpy.data.collections[name].objects)
    if objects:
        delete_objects(objects)


def clear_collections(collections):
    for name in collections:
        clear_collection(name)


# ==============================================================================
# delete
# ==============================================================================

# def delete_collection(name):
#     collection = bpy.data.collections[name]
#     bpy.context.scene.collection.children.unlink(collection)
#     bpy.data.collections.remove(collection)


# def delete_collections(collections):
#     for collection in collections:
#         delete_collection(collection=collection)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
