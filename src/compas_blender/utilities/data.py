import bpy


__all__ = [
    "delete_unused_data",
]


def delete_unused_data():
    """Delete all collections, mesh and curve objects, meshes, curves, materials."""
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.curves:
        if block.users == 0:
            bpy.data.curves.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
