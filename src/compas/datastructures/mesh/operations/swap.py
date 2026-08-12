from typing import TYPE_CHECKING
from typing import Literal
from typing import Union

from ..types import Edge
from ..types import Face

if TYPE_CHECKING:
    from ..mesh import Mesh


def trimesh_swap_edge(
    mesh: "Mesh", edge: Edge, allow_boundary: bool = True
) -> Union[tuple[Face, Face], Literal[False]]:
    """Replace an edge of the mesh by an edge connecting the opposite
    vertices of the adjacent faces.

    Parameters
    ----------
    mesh
        Instance of mesh.
    edge
        The identifier of the edge to swap.
    allow_boundary
        If False, reject edges incident to boundary vertices.

    Returns
    -------
    tuple[int, int] | False
        The new face identifiers if the swap succeeds, False otherwise.

    """
    u, v = edge

    if not mesh.has_halfedge((u, v)) or not mesh.has_halfedge((v, u)):
        raise ValueError("The edge is not part of the mesh.")

    # check legality of the swap
    # swapping on the boundary is not allowed
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]

    if fkey_uv is None or fkey_vu is None:
        return False

    u_on = mesh.is_vertex_on_boundary(u)
    v_on = mesh.is_vertex_on_boundary(v)

    if u_on and v_on:
        return False

    if not allow_boundary:
        if mesh.is_vertex_on_boundary(u) or mesh.is_vertex_on_boundary(v):
            return False

    # swapping to a half-edge that already exists is not allowed
    uv = mesh.face[fkey_uv]
    vu = mesh.face[fkey_vu]

    o_uv = uv[uv.index(u) - 1]
    o_vu = vu[vu.index(v) - 1]

    if o_uv in mesh.halfedge[o_vu] and o_vu in mesh.halfedge[o_uv]:
        return False

    # swap
    # delete the current half-edge
    del mesh.halfedge[u][v]
    del mesh.halfedge[v][u]

    # delete the adjacent faces
    del mesh.face[fkey_uv]
    del mesh.face[fkey_vu]

    # add the faces created by the swap
    a = mesh.add_face([o_uv, o_vu, v])
    b = mesh.add_face([o_vu, o_uv, u])

    if a is None or b is None:
        raise RuntimeError("Swapping the edge produced an invalid face.")

    return a, b
