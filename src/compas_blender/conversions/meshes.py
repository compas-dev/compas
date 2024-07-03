from typing import Optional

import bmesh  # type: ignore
import bpy  # type: ignore

from compas.datastructures import Mesh
from compas.geometry import Translation

# To Do
# -----
# - [ ] Write COMPAS Mesh attributes to Blender
# - [ ] Read Mesh attributes from Blender to COMPAS
# - [ ] Include results of modifiers in VOMPAS Mesh

# =============================================================================
# To Blender
# =============================================================================


def mesh_to_blender(mesh: Mesh) -> bpy.types.Mesh:
    """Convert a COMPAS mesh to a Blender mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    Returns
    -------
    :class:`bpy.types.Mesh`
        A Blender mesh.

    """
    vertices, faces = mesh.to_vertices_and_faces()
    return vertices_and_faces_to_blender_mesh(vertices, faces, name=mesh.name)  # type: ignore


def vertices_and_faces_to_blender_mesh(
    vertices: list[list[float]],
    faces: list[list[int]],
    name: Optional[str] = None,
) -> bpy.types.Mesh:
    """Convert a list of vertices and faces to a Blender mesh.

    Parameters
    ----------
    vertices : list
        A list of vertex coordinates.
    faces : list
        A list of faces, defined as lists of indices into the list of vertices.
    name : str, optional
        The name of the mesh.

    Returns
    -------
    :class:`bpy.types.Mesh`
        A Blender mesh.

    """
    bmesh = bpy.data.meshes.new(name or "Mesh")
    bmesh.from_pydata(vertices, [], faces)
    bmesh.update(calc_edges=True)
    return bmesh


# =============================================================================
# To COMPAS
# =============================================================================


def mesh_to_compas(m: bpy.types.Mesh, name=None) -> Mesh:
    """Convert a Blender mesh to a COMPAS mesh.

    Parameters
    ----------
    m : :class:`bpy.types.Mesh`
        A Blender mesh.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    """
    vertices = [vertex.co for vertex in m.vertices]
    faces = [face.vertices for face in m.polygons]
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    mesh.name = name
    return mesh


def bmesh_to_compas(bm: bmesh.types.BMesh, name=None) -> Mesh:
    """Convert a Blender BMesh to a COMPAS mesh.

    A BMesh is the data structure used by Blender to represent meshes.

    Parameters
    ----------
    bm : :class:`bmesh.types.BMesh`
        A Blender BMesh.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    """
    data = bpy.data.meshes.new(name or "Mesh")
    bm.to_mesh(data)
    bm.free()
    return mesh_to_compas(data, name=name)


def monkey_to_compas():
    """Construct a COMPAS mesh from the Blender monkey.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    """
    bm = bmesh.new()
    bmesh.ops.create_monkey(bm)
    data = bpy.data.meshes.new("Mesh")
    bm.to_mesh(data)
    bm.free()
    return mesh_to_compas(data, name="Suzanne")


def meshobj_to_compas(obj: bpy.types.Object) -> Mesh:
    """Convert a Blender mesh object to a COMPAS mesh.

    Parameters
    ----------
    obj : :class:`bpy.types.Object`
        A Blender mesh object.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    """
    mesh = mesh_to_compas(obj.data)
    T = Translation.from_vector(obj.location)
    mesh.transform(T)
    return mesh
