from typing import Optional

import bpy  # type: ignore

from compas.geometry import Cylinder

# import bmesh  # type: ignore
# import mathutils  # type: ignore
from compas.geometry import Point
from compas.geometry import Pointcloud
from compas.geometry import Sphere

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
    :blender:`bpy.types.Object`
        A Blender sphere object.

    """
    raise NotImplementedError


def pointcloud_to_blender(pointcloud: Pointcloud, radius: float = 0.05, u: int = 16, v: int = 16, name: Optional[str] = None) -> bpy.types.Object:
    """Convert a COMPAS pointcloud to a Blender pointcloud.

    Parameters
    ----------
    pointcloud : list of :class:`compas.geometry.Point`
        A COMPAS pointcloud.
    radius : float, optional
        The radius of the spheres.
    u : int, optional
        Number of faces in the "u" direction.
    v : int, optional
        Number of faces in the "v" direction.
    name : str, optional
        The name of the Blender object.

    Returns
    -------
    :blender:`bpy.types.Mesh`
        A Blender pointcloud mesh.

    """
    vertices = []
    faces = []
    for point in pointcloud:
        sphere = Sphere.from_point_and_radius(point, radius)
        vs, fs = sphere.to_vertices_and_faces(u=u, v=v)
        vertices += vs
        faces += [[f + len(vertices) for f in face] for face in fs]
    mesh = bpy.data.meshes.new(name or pointcloud.name)
    mesh.from_pydata(vertices, [], faces)
    mesh.validate(verbose=False)
    mesh.update(calc_edges=True)
    return mesh

    # mesh = bpy.data.meshes.new(name or pointcloud.name)
    # bm = bmesh.new()
    # for point in pointcloud:
    #     bmesh.ops.create_uvsphere(
    #         bm,
    #         u_segments=u,
    #         v_segments=v,
    #         radius=radius,
    #         matrix=mathutils.Matrix.Translation(point),
    #         calc_uvs=False,
    #     )
    # bm.to_mesh(mesh)
    # bm.free()
    # return mesh


def polygon_to_blender_mesh(
    points: list[list[float]],
    name: Optional[str] = None,
) -> bpy.types.Mesh:
    """Convert a list of vertices and faces to a Blender mesh.

    Parameters
    ----------
    points : list[point]
        A polygon defined as a list of points.

    Returns
    -------
    :blender:`bpy.types.Mesh`
        A Blender mesh.

    """
    bmesh = bpy.data.meshes.new(name or "Polygon")
    bmesh.from_pydata(points, [], [list(range(len(points)))])
    bmesh.update(calc_edges=True)
    return bmesh


def sphere_to_blender_mesh(sphere: Sphere, u: int = 16, v: int = 16, name: Optional[str] = None) -> bpy.types.Mesh:
    """Convert a COMPAS sphere to a Blender mesh.

    Parameters
    ----------
    sphere : :class:`compas.geometry.Sphere`
        A COMPAS sphere.

    Returns
    -------
    :blender:`bpy.types.Mesh`
        A Blender mesh.

    """
    vertices, faces = sphere.to_vertices_and_faces(u=u, v=v)

    mesh = bpy.data.meshes.new(name or "Sphere")
    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)

    return mesh


def cylinder_to_blender_mesh(cylinder: Cylinder, u: int = 16, name: Optional[str] = None) -> bpy.types.Mesh:
    """Convert a COMPAS cylinder to a Blender mesh.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`
        A COMPAS cylinder.
    u : int, optional
        Number of faces in the "u" direction.
    name : str, optional
        The name of the Blender mesh.

    Returns
    -------
    :blender:`bpy.types.Mesh`
        A Blender mesh.

    """
    vertices, faces = cylinder.to_vertices_and_faces(u=u)

    mesh = bpy.data.meshes.new(name or "Cylinder")
    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)

    return mesh


# =============================================================================
# To COMPAS
# =============================================================================
