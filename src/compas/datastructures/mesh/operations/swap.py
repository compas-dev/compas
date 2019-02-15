from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = ['trimesh_swap_edge']


def trimesh_swap_edge(mesh, u, v, allow_boundary=True):
    """Replace an edge of the mesh by an edge connecting the opposite
    vertices of the adjacent faces.

    Parameters:
        u (str): The key of one of the vertices of the edge.
        v (str): The key of the other vertex of the edge.

    Returns:
        None

    Raises:
        ValueError: If `u` and `v` are not neighbors.
        TriMeshError: If one of the half-edges does not exist.
    """

    # check legality of the swap
    # swapping on the boundary is not allowed
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]

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

    return a, b


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
