from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = ['trimesh_swap_edge']


def trimesh_swap_edge(self, u, v, allow_boundary=True):
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
    fkey_uv = self.halfedge[u][v]
    fkey_vu = self.halfedge[v][u]

    if fkey_uv is None or fkey_vu is None:
        return

    if not allow_boundary:
        if self.is_vertex_on_boundary(u) or self.is_vertex_on_boundary(v):
            return

    # swapping to a half-edge that already exists is not allowed
    uv = self.face[fkey_uv]
    vu = self.face[fkey_vu]

    o_uv = uv[uv.index(u) - 1]
    o_vu = vu[vu.index(v) - 1]

    if o_uv in self.halfedge[o_vu] and o_vu in self.halfedge[o_uv]:
        return

    # swap
    # delete the current half-edge
    del self.halfedge[u][v]
    del self.halfedge[v][u]

    # delete the adjacent faces
    del self.face[fkey_uv]
    del self.face[fkey_vu]

    # add the faces created by the swap
    a = self.add_face([o_uv, o_vu, v])
    b = self.add_face([o_vu, o_uv, u])

    return a, b


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
