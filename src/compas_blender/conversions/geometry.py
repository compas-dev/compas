import bpy  # type: ignore

from compas.geometry import Point
from compas.geometry import Pointcloud


# =============================================================================
# To Blender
# =============================================================================


def point_to_blender_sphere(point: Point) -> bpy.types.Object:
    """Convert a COMPAS point to a Blender sphere.

    Parameters
    ----------
    point : :class:`compas.geometry.Point`
        A COMPAS point.

    Returns
    -------
    :class:`bpy.types.Object`
        A Blender sphere object.

    """
    raise NotImplementedError


def pointcloud_to_blender(pointcloud: Pointcloud) -> bpy.types.Object:
    """Convert a COMPAS pointcloud to a Blender pointcloud.

    Parameters
    ----------
    pointcloud : list of :class:`compas.geometry.Point`
        A COMPAS pointcloud.

    Returns
    -------
    :class:`bpy.types.Object`
        A Blender particle system object.

    """
    raise NotImplementedError


# =============================================================================
# To COMPAS
# =============================================================================
