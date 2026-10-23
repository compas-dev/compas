from collections.abc import Collection
from typing import TYPE_CHECKING

from .matrices import trimesh_cotangent_laplacian_matrix

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.datastructures.mesh.types import Vertex


def trimesh_smooth_laplacian_cotangent(trimesh: "Mesh", fixed: Collection["Vertex"], kmax: int = 10) -> None:
    """Smooth a triangle mesh with cotangent Laplacian weights.

    Parameters
    ----------
    trimesh : Mesh
        The triangle mesh to modify.
    fixed
        Vertex identifiers whose coordinates should remain unchanged.
    kmax
        Number of smoothing iterations.

    Notes
    -----
    The mesh is modified in place. During each iteration, every non-fixed
    vertex is displaced by its cotangent Laplacian vector.

    """
    from numpy import array

    vertex_index = trimesh.vertex_index()
    for _ in range(kmax):
        V = array(trimesh.vertices_attributes("xyz"))
        L = trimesh_cotangent_laplacian_matrix(trimesh)
        d = L.dot(V)
        V = V + d
        for key, attr in trimesh.vertices(True):
            if key in fixed:
                continue
            index = vertex_index[key]
            attr["x"] = V[index][0]
            attr["y"] = V[index][1]
            attr["z"] = V[index][2]
