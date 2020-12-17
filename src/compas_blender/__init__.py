"""
********************************************************************************
compas_blender
********************************************************************************

.. currentmodule:: compas_blender

.. toctree::
    :maxdepth: 1

    compas_blender.artists
    compas_blender.geometry
    compas_blender.ui
    compas_blender.utilities

"""
try:
    import bpy  # noqa: F401
except ImportError:
    pass
else:
    from .utilities import *  # noqa: F401 F403


def clear():
    # delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True, confirm=False)
    # delete data
    delete_unused_data()  # noqa: F405
    # delete collections
    for collection in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.unlink(collection)
    for block in bpy.data.collections:
        objects = [o for o in block.objects if o.users]
        while objects:
            bpy.data.objects.remove(objects.pop())
        for collection in block.children:
            block.children.unlink(collection)
        if block.users == 0:
            bpy.data.collections.remove(block)


__version__ = '0.19.3'


__all__ = [name for name in dir() if not name.startswith('_')]
__all_plugins__ = [
    # 'compas_blender.geometry.booleans',
]
