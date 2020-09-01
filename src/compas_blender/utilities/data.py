import bpy


__all__ = [
    "delete_all_data",
]


def delete_all_data():
    """Delete all collections, mesh and curve objects, meshes, curves, materials."""
    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            bpy.data.objects.remove(obj)
        elif obj.type == 'CURVE':
            bpy.data.objects.remove(obj)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for curve in bpy.data.curves:
        bpy.data.curves.remove(curve)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
