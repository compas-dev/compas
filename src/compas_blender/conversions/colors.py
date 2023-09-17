import bpy  # type: ignore

from compas.colors import Color


def color_to_blender_material(color: Color) -> bpy.types.Material:
    """Convert a COMPAS color to a Blender material.

    Parameters
    ----------
    color : :class:`compas.colors.Color`
        A COMPAS color.

    Returns
    -------
    :blender:`bpy.types.Material`
        A Blender material.

    """
    name = "-".join(["{0:.3f}".format(i) for i in color.rgba])
    material = bpy.data.materials.get(name, bpy.data.materials.new(name))
    material.diffuse_color = color.rgba
    return material
