import bpy
from typing import List, Text

from compas_blender.utilities import delete_objects


__all__ = [
    "create_collection",
    "create_collections",
    "create_collections_from_path",
    "clear_collection",
    "clear_collections"
]


def create_collection(name: Text, parent: bpy.types.Collection = None) -> bpy.types.Collection:
    """Create a collection with the given name.

    Parameters
    ----------
    name : str
    parent : :class:`bpy.types.Collection`, optional

    Returns
    -------
    :class:`bpy.types.Collection`

    """
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


def create_collections(names: List[Text]) -> List[bpy.types.Collection]:
    """Create multiple collections at once.

    Parameters
    ----------
    names : list of str

    Returns
    -------
    list of :class:`bpy.types.Collection`
    """
    collections = [create_collection(name) for name in names]
    return collections


def create_collections_from_path(path: Text, separator: Text = '::') -> List[bpy.types.Collection]:
    """Create nested collections from a collection path string.

    Parameters
    ----------
    path : str
        The collection path with collection names separated by the specified separator.
    separator : str, optional

    Returns
    -------
    list of :class:`bpy.types.Collection`
    """
    names = path.split(separator)
    collections = []
    parent = None
    for name in names:
        collection = create_collection(name, parent=parent)
        parent = collection
        collections.append(collection)
    return collections


def clear_collection(name: Text):
    """Clear the objects from a collection."""
    objects = list(bpy.data.collections[name].objects)
    if objects:
        delete_objects(objects)


def clear_collections(collections: List[bpy.types.Collection]):
    """Clear the objects from multiple collections."""
    for name in collections:
        clear_collection(name)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
