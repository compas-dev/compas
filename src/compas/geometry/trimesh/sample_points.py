from typing import TYPE_CHECKING
from typing import Literal
from typing import overload

from compas._typing import MeshType

if TYPE_CHECKING:
    from numpy.typing import NDArray


@overload
def trimesh_sample_points(mesh: MeshType, num_points: int = 1000, return_normals: Literal[False] = False) -> "NDArray": ...


@overload
def trimesh_sample_points(mesh: MeshType, num_points: int, return_normals: Literal[True]) -> "tuple[NDArray, NDArray]": ...


@overload
def trimesh_sample_points(mesh: MeshType, num_points: int, return_normals: bool) -> "NDArray | tuple[NDArray, NDArray]": ...


def trimesh_sample_points(
    mesh: MeshType,
    num_points: int = 1000,
    return_normals: bool = False,
) -> "NDArray | tuple[NDArray, NDArray]":
    """Sample points uniformly by area on a triangle mesh.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.
    num_points
        Number of points to sample.
    return_normals
        If `True`, also return the unit normal of the sampled face for every
        point.

    Returns
    -------
    numpy.ndarray
        An array of sampled XYZ coordinates when `return_normals` is `False`.
    tuple[numpy.ndarray, numpy.ndarray]
        The sampled coordinates and corresponding face normals when
        `return_normals` is `True`.

    Raises
    ------
    ValueError
        If the mesh contains no triangle with positive area.

    Notes
    -----
    Faces are selected with probability proportional to their area. Points on
    each selected face are generated from uniformly distributed barycentric
    coordinates.[^trimesh-sampling-barycentric]

    References
    ----------
    [^trimesh-sampling-barycentric]: [Efficient barycentric point sampling on meshes](https://arxiv.org/abs/1708.07559)

    """
    from numpy import asarray
    from numpy import cross
    from numpy import sqrt
    from numpy.linalg import norm
    from numpy.random import choice
    from numpy.random import random

    vertices, faces = mesh
    xyz = asarray(vertices, dtype=float)
    triangles = asarray(faces, dtype=int)

    face_vertices = xyz[triangles]
    edge01 = face_vertices[:, 1] - face_vertices[:, 0]
    edge02 = face_vertices[:, 2] - face_vertices[:, 0]
    face_normals = cross(edge01, edge02)
    double_areas = norm(face_normals, axis=1)
    if not double_areas.size or double_areas.sum() == 0:
        raise ValueError("The mesh must contain at least one nondegenerate triangle.")
    probabilities = double_areas / double_areas.sum()
    face_indices = choice(len(triangles), num_points, p=probabilities)

    random_values = random((2, num_points))
    root = sqrt(random_values[0])
    weights = (1.0 - root, root * (1.0 - random_values[1]), root * random_values[1])
    selected = face_vertices[face_indices]
    samples = weights[0][:, None] * selected[:, 0] + weights[1][:, None] * selected[:, 1] + weights[2][:, None] * selected[:, 2]

    if not return_normals:
        return samples

    unit_normals = face_normals / double_areas[:, None]
    return samples, unit_normals[face_indices]
