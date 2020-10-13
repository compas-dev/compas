import bpy

from compas.geometry import add_vectors
from compas.plugins import plugin


__all__ = [
    'boolean_union_mesh_mesh',
    'boolean_difference_mesh_mesh',
    'boolean_intersection_mesh_mesh',
]


@plugin(category='booleans', requires=['bpy'])
def boolean_union_mesh_mesh(A, B, remesh=False):
    """Compute the boolean union of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean union.
    """
    return _boolean_operation(A, B, 'UNION')


@plugin(category='booleans', requires=['bpy'])
def boolean_difference_mesh_mesh(A, B, remesh=False):
    """Compute the boolean difference of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean difference.
    """
    return _boolean_operation(A, B, 'DIFFERENCE')


@plugin(category='booleans', requires=['bpy'])
def boolean_intersection_mesh_mesh(A, B, remesh=False):
    """Compute the boolean intersection of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean intersection.
    """
    return _boolean_operation(A, B, 'INTERSECT')


def _boolean_operation(A, B, method):
    boolean = A.modifiers.new(type="BOOLEAN", name="A {} B".format(method))
    boolean.object = B
    boolean.operation = method
    bpy.ops.object.modifier_apply({"object": A}, modifier=boolean.name)
    vertices = [add_vectors(A.location, vertex.co) for vertex in A.data.vertices]
    faces = [list(A.data.polygons[face].vertices) for face in range(len(A.data.polygons))]
    return vertices, faces
