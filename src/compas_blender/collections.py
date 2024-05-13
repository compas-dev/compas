from typing import List
from typing import Text

import bpy  # type: ignore

from compas_blender.objects import delete_objects


def collection_path(collection, names=[]):
    for parent in bpy.data.collections:
        if collection.name in parent.children:
            names.append(parent.name)
            collection_path(parent, names)
    return names


def create_collection(name: Text, parent: bpy.types.Collection = None) -> bpy.types.Collection:
    """Create a collection with the given name.

    Parameters
    ----------
    name : str
        The name of the collection.
    parent : bpy.types.Collection, optional
        A parent collection.

    Returns
    -------
    :blender:`bpy.types.Collection`

    """
    if not name:
        return

    if not parent:
        if name in bpy.data.collections:
            count = 1
            newname = f"{name}.{count:04}"
            while newname in bpy.data.collections:
                count += 1
                newname = f"{name}.{count:04}"
            name = newname
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    else:
        path = collection_path(parent)[::-1] + [parent.name]
        name = "::".join(path) + "::" + name
        if name not in parent.children:
            collection = bpy.data.collections.new(name)
            parent.children.link(collection)
        else:
            collection = bpy.data.collections.get(name)
    return collection


def create_collections(names: List[Text]) -> List[bpy.types.Collection]:
    """Create multiple collections at once.

    Parameters
    ----------
    names : list[str]
        Collection names.

    Returns
    -------
    list[:blender:`bpy.types.Collection`]

    """
    collections = [create_collection(name) for name in names]
    return collections


def create_collections_from_path(path: Text, separator: Text = "::") -> List[bpy.types.Collection]:
    """Create nested collections from a collection path string.

    Parameters
    ----------
    path : str
        The collection path with collection names separated by the specified separator.
    separator : str, optional
        The separator between components of the path.

    Returns
    -------
    list[:blender:`bpy.types.Collection`]

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
    """Clear the objects from a collection.

    Parameters
    ----------
    name : str
        The name of the collection.

    Returns
    -------
    None

    """
    objects = list(bpy.data.collections[name].objects)
    if objects:
        delete_objects(objects)


def clear_collections(collections: List[bpy.types.Collection]):
    """Clear the objects from multiple collections.

    Parameters
    ----------
    collections : list[:blender:`bpy.types.Collection`]
        A list of collections.

    Returns
    -------
    None

    """
    for name in collections:
        clear_collection(name)
