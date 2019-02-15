from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import random

from compas.datastructures.mesh.smoothing import mesh_smooth_area

from compas.datastructures.mesh.operations import trimesh_collapse_edge
from compas.datastructures.mesh.operations import trimesh_swap_edge
from compas.datastructures.mesh.operations import trimesh_split_edge


__all__ = [
    'trimesh_remesh',
]


def trimesh_remesh(mesh,
                   target,
                   kmax=100,
                   tol=0.1,
                   divergence=0.01,
                   verbose=False,
                   allow_boundary_split=False,
                   allow_boundary_swap=False,
                   allow_boundary_collapse=False,
                   smooth=True,
                   fixed=None,
                   callback=None,
                   callback_args=None):
    """Remesh until all edges have a specified target length.

    Parameters
    ----------
    mesh : Mesh
        A triangle mesh.
    target : float
        The target length for the mesh edges.
    kmax : int, optional [100]
        The number of iterations.
    tol : float, optional [0.1]
        Length deviation tolerance.
    divergence : float, optional [0.01]
        ??
    verbose : bool, optional [False]
        Print feedback messages.
    allow_boundary_split : bool, optional [False]
        Allow boundary edges to be split.
    allow_boundary_swap : bool, optional [False]
        Allow boundary edges or edges connected to the boundary to be swapped.
    allow_boundary_collapse : bool, optional [False]
        Allow boundary edges or edges connected to the boundary to be collapsed.
    smooth : bool, optional [True]
        Apply smoothing at every iteration.
    fixed : list, optional [None]
        A list of vertices that have to stay fixed.
    callback : callable, optional [None]
        A user-defined function that is called after every iteration.
    callback_args : list, optional [None]
        A list of additional parameters to be passed to the callback function.

    Returns
    -------
    None

    Notes
    -----
    This algorithm not only changes the geometry of the mesh, but also its
    topology as needed to achieve the specified target lengths.
    Topological changes are made such that vertex valencies are well-balanced
    and close to six. This involves three operations:

        * split edges that are longer than a maximum length,
        * collapse edges that are shorter than a minimum length,
        * swap edges if this improves the valency error.

    The minimum and maximum lengths are calculated based on a desired target
    length.

    For more info, see [1]_.

    References
    ----------
    .. [1] Botsch, M. & Kobbelt, L., 2004. *A remeshing approach to multiresolution modeling*.
           Proceedings of the 2004 Eurographics/ACM SIGGRAPH symposium on Geometry processing - SGP '04, p.185.
           Available at: http://portal.acm.org/citation.cfm?doid=1057432.1057457.

    Examples
    --------
    .. plot::
        :include-source:

        from compas.datastructures import Mesh
        from compas.datastructures import trimesh_remesh
        from compas.plotters import MeshPlotter

        vertices = [
            (0.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            (6.0, 10.0, 0.0),
            (0.0, 10.0, 0.0),
            (5.0, 5.0, 0.0)
        ]
        faces = [
            (0, 1, 4),
            (1, 2, 4),
            (2, 3, 4),
            (3, 0, 4)
        ]

        mesh = Mesh.from_vertices_and_faces(vertices, faces)

        trimesh_remesh(
            mesh,
            target=0.5,
            tol=0.05,
            kmax=300,
            allow_boundary_split=True,
            allow_boundary_swap=True,
            allow_boundary_collapse=True,
            verbose=False
        )

        plotter = MeshPlotter(mesh)

        plotter.draw_vertices(radius=0.03)
        plotter.draw_faces()
        plotter.draw_edges()

        plotter.show()

    See Also
    --------
    * :func:`compas.geometry.smooth_area`

    """
    if verbose:
        print(target)

    lmin = (1 - tol) * (4.0 / 5.0) * target
    lmax = (1 + tol) * (4.0 / 3.0) * target

    edge_lengths = [mesh.edge_length(u, v) for u, v in mesh.edges()]
    target_start = max(edge_lengths) / 2.0

    fac = target_start / target

    boundary = set(mesh.vertices_on_boundary())

    fixed = fixed or []
    fixed = set(fixed)

    count = 0

    kmax_start = kmax / 2.0

    for k in range(kmax):

        if k <= kmax_start:
            scale = fac * (1.0 - k / kmax_start)
            dlmin = lmin * scale
            dlmax = lmax * scale
        else:
            dlmin = 0
            dlmax = 0

        if verbose:
            print(k)

        count += 1

        if k % 20 == 0:
            num_vertices_1 = mesh.number_of_vertices()

        # split
        if count == 1:
            visited = set()

            for u, v in list(mesh.edges()):
                if u in visited or v in visited:
                    continue
                if mesh.edge_length(u, v) <= lmax + dlmax:
                    continue

                if verbose:
                    print('split edge: {0} - {1}'.format(u, v))

                trimesh_split_edge(mesh, u, v, allow_boundary=allow_boundary_split)

                visited.add(u)
                visited.add(v)

        # collapse
        elif count == 2:
            visited = set()

            for u, v in list(mesh.edges()):
                if u in visited or v in visited:
                    continue
                if mesh.edge_length(u, v) >= lmin - dlmin:
                    continue
                if verbose:
                    print('collapse edge: {0} - {1}'.format(u, v))

                trimesh_collapse_edge(mesh, u, v, allow_boundary=allow_boundary_collapse, fixed=fixed)

                visited.add(u)
                visited.add(v)

                visited.update(mesh.halfedge[u])

        # swap
        elif count == 3:
            visited = set()

            for u, v in list(mesh.edges()):
                if u in visited or v in visited:
                    continue

                f1 = mesh.halfedge[u][v]
                f2 = mesh.halfedge[v][u]

                if f1 is None or f2 is None:
                    continue

                face1 = mesh.face[f1]
                face2 = mesh.face[f2]

                v1 = face1[face1.index(u) - 1]
                v2 = face2[face2.index(v) - 1]

                valency1 = mesh.vertex_degree(u)
                valency2 = mesh.vertex_degree(v)
                valency3 = mesh.vertex_degree(v1)
                valency4 = mesh.vertex_degree(v2)

                if u in boundary:
                    valency1 += 2
                if v in boundary:
                    valency2 += 2
                if v1 in boundary:
                    valency3 += 2
                if v2 in boundary:
                    valency4 += 2

                current_error = abs(valency1 - 6) + abs(valency2 - 6) + abs(valency3 - 6) + abs(valency4 - 6)
                flipped_error = abs(valency1 - 7) + abs(valency2 - 7) + abs(valency3 - 5) + abs(valency4 - 5)

                if current_error <= flipped_error:
                    continue

                if verbose:
                    print('swap edge: {0} - {1}'.format(u, v))

                trimesh_swap_edge(mesh, u, v, allow_boundary=allow_boundary_swap)

                visited.add(u)
                visited.add(v)
        # count
        else:
            count = 0

        if (k - 10) % 20 == 0:
            num_vertices_2 = mesh.number_of_vertices()

            if abs(1 - num_vertices_1 / num_vertices_2) < divergence and k > kmax_start:
                break

        # smoothen
        if smooth:
            if allow_boundary_split:
                boundary = set(mesh.vertices_on_boundary())

            mesh_smooth_area(mesh, fixed=fixed.union(boundary), kmax=1)

        # callback
        if callback:
            callback(mesh, k, callback_args)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures import Mesh
    from compas.datastructures import mesh_smooth_area

    from compas.plotters import MeshPlotter


    vertices = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (6.0, 10.0, 0.0), (0.0, 10.0, 0.0)]
    faces = [[0, 1, 2, 3]]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)

    key = mesh.insert_vertex(0)
    fixed = [key]

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_edges(width=0.5)

    def callback(mesh, k, args):
        print(k)
        plotter.update_edges()
        plotter.update()

    trimesh_remesh(
        mesh,
        0.5,
        kmax=200,
        allow_boundary_split=True,
        allow_boundary_swap=True,
        allow_boundary_collapse=True,
        fixed=fixed,
        callback=callback)

    mesh_smooth_area(mesh, fixed=mesh.vertices_on_boundary())

    plotter.update_edges()
    plotter.update(pause=2.0)
    plotter.show()
