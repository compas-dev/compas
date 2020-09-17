from numpy import array

from compas.datastructures.mesh.core import trimesh_cotangent_laplacian_matrix


__all__ = ['trimesh_smooth_laplacian_cotangent']


def trimesh_smooth_laplacian_cotangent(trimesh, fixed, kmax=10):
    """Smooth a triangle mesh using a laplacian matrix with cotangent weights.

    Parameters
    ----------
    trimesh : :class:`compas.datastructures.Mesh`
        A triangle mesh.
    fixed : list
        A list of fixed vertices.
    kmax : int (optional, default is 10)
        The maximum number of smoothing rounds.

    """
    for k in range(kmax):
        V = array(trimesh.vertices_attributes('xyz'))
        L = trimesh_cotangent_laplacian_matrix(trimesh)
        d = L.dot(V)
        V = V + d
        for key, attr in trimesh.vertices(True):
            if key in fixed:
                continue
            attr['x'] = V[key][0]
            attr['y'] = V[key][1]
            attr['z'] = V[key][2]


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
