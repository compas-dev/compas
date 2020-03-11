try:
    import bpy
except ImportError:
    pass


__all__ = [
    "delete_all_data",
]


def delete_all_data():
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
