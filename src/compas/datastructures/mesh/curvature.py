from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi

from compas.geometry import angle_points


__all__ = [
    'trimesh_mean_curvature',
    'trimesh_gaussian_curvature'
]


def trimesh_mean_curvature(mesh):
    pass


def trimesh_gaussian_curvature(mesh):
    r"""Compute the gaussian curvature at the vertices of a triangle mesh using the angular deficit.

    The angular deficit at a vertex is defined as the difference between a full
    circle angle (:math:`2\pi`) and the sum of the angles in the adjacent trianlges.

    .. math::

        k_{G}(v_{i}) = 2\pi - \sum_{j \in N(i)} \teta_{ij}

    where :math:`N(i)` are the triangles incident on vertex :math:`i` and :math:`\teta_{ij}`
    is the angle at vertex :math:`i` in triangle :math:`j`.

    Parameters
    ----------
    mesh : compas.oatastructures.Mesh
        The triangle mesh data structure.

    Returns
    -------
    list of float
        Per vertex curvature values.

    Warning
    -------
    This function will not check if the provided mesh is actually a triangle mesh.
    It will just treat as such...

    Examples
    --------
    .. code-block:: python

        pass

    """
    pi2 = 2 * pi
    key_xyz = {key: mesh.get_vertex_attributes(key, 'xyz') for key in mesh.vertices()}
    curvature = []
    for key in mesh.vertices():
        angles = []
        o = key_xyz[key]
        for u in mesh.vertex_neighbors(key):
            fkey = mesh.halfedge[key][u]
            if fkey is not None:
                vertices = mesh.face_vertices(fkey)
                v = vertices[vertices.index(key) - 1]
                a = key_xyz[u]
                b = key_xyz[v]
                print(o, a, b)
                angles.append(angle_points(o, a, b))
        curvature.append(pi2 - sum(angles))
    return curvature


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from numpy import array

    import compas

    from compas.utilities import i_to_rgb

    from compas.datastructures import Mesh
    from compas.datastructures import trimesh_cotangent_laplacian_matrix
    from compas.datastructures import mesh_laplacian_matrix
    from compas.datastructures import mesh_quads_to_triangles
    from compas.datastructures import mesh_flip_cycles

    from compas.geometry import add_vectors
    from compas.geometry import subtract_vectors
    from compas.numerical import normrow

    from compas.plotters import MeshPlotter


    # mesh = Mesh.from_polyhedron(8)
    mesh = Mesh.from_obj(compas.get('mesh.obj'))

    mesh_quads_to_triangles(mesh)
    # mesh_flip_cycles(mesh)

    # xyz = array(mesh.get_vertices_attributes('xyz'))

    # L = mesh_laplacian_matrix(mesh)

    # d = L.dot(xyz).tolist()

    # curvature = normrow(d).ravel().tolist()
    # print(curvature)

    curvature = trimesh_gaussian_curvature(mesh)

    plotter = MeshPlotter(mesh, figsize=(12, 8), tight=True)

    # lines = []
    # for index, key in enumerate(mesh.vertices()):
    #     vector = d[index]
    #     start = xyz[index]
    #     end = subtract_vectors(start, vector)
    #     lines.append({
    #         'start' : end,
    #         'end'   : start,
    #         'arrow' : 'start',
    #         'color' : '#ff0000'
    #     })

    c_min = min(curvature)
    c_max = max(curvature)
    c_spn = c_max - c_min

    plotter.draw_vertices(
        radius=0.1,
        facecolor={key: i_to_rgb((curvature[key] - c_min) / c_spn) for key in mesh.vertices()}
    )
    plotter.draw_faces()

    # plotter.draw_arrows(lines)

    plotter.show()
