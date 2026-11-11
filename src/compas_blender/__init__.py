# type: ignore

try:
    import bpy
    import compas_blender.data

except ImportError:
    pass


__version__ = "2.15.0"


__all__ = [
    "clear",
    "redraw",
]

__all_plugins__ = [
    "compas_blender.geometry.booleans",
    "compas_blender.scene",
]

# =============================================================================
# =============================================================================
# =============================================================================
# General helpers
# =============================================================================
# =============================================================================
# =============================================================================


def clear(guids=None):
    """Clear all scene objects."""
    if guids is None:
        # delete all objects
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=True, confirm=False)
        # delete data
        compas_blender.data.delete_unused_data()
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
    else:
        for obj in guids:
            bpy.data.objects.remove(obj, do_unlink=True)


def redraw():
    """Trigger a redraw."""
    # There is no window to redraw when Blender runs in background mode.
    if bpy.ops.wm.redraw_timer.poll():
        bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)
