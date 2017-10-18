from __future__ import print_function
from __future__ import absolute_import

from .smoothing import mesh_smooth_centroid

from ..operations.split import trimesh_split_edge
from ..operations.collapse import trimesh_collapse_edge
from ..operations.swap import trimesh_swap_edge


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'trimesh_optimise_topology',
]


def trimesh_optimise_topology(mesh,
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

    This involves three operations:

        * split edges that are longer than a maximum length,
        * collapse edges that are shorter than a minimum length,
        * swap edges if this improves the valency error.

    The minimum and maximum lengths are calculated based on a desired target
    length:

    Parameters:
        mesh (Mesh) : A triangle mesh.
        target (float) : The target length.
        tol (float) : Length deviation tolerance. Defaults to `0.1`
        kmax (int) : The number of iterations.
        verbose (bool) : Print feedback messages, if True.

    Returns:
        None

    Note:
        This algorithm not only changes the geometry of the mesh, but also its
        topology as needed to achieve the specified target lengths.
        Topological changes are made such that vertex valencies are well-balanced
        and close to six.

    Examples:

        .. plot::
            :include-source:

            from compas.datastructures import Mesh
            from compas.visualization import MeshPlotter
            from compas.datastructures import trimesh_optimise_topology

            vertices = [
                (0.0, 0.0, 0.0),
                (10.0, 0.0, 0.0),
                (10.0, 10.0, 0.0),
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

            trimesh_optimise_topology(
                mesh,
                target=0.5,
                tol=0.05,
                kmax=300,
                allow_boundary_split=True,
                allow_boundary_swap=True,
                verbose=False
            )

            plotter = MeshPlotter(mesh)

            plotter.draw_vertices(radius=0.05)
            plotter.draw_faces()

            plotter.show()

    """
    if verbose:
        print(target)

    lmin = (1 - tol) * (4.0 / 5.0) * target
    lmax = (1 + tol) * (4.0 / 3.0) * target

    edge_lengths = [mesh.edge_length(u, v) for u, v in mesh.wireframe()]
    target_start = max(edge_lengths) / 2.0

    fac = float(target_start / target)

    boundary = set(mesh.vertices_on_boundary())
    count = 0

    kmax_start = kmax / 2.0

    for k in xrange(kmax):

        if k <= kmax_start:
            scale_val = fac * (1.0 - k / kmax_start)
            dlmin = lmin * scale_val
            dlmax = lmax * scale_val
        else:
            dlmin = 0
            dlmax = 0

        if verbose:
            print(k)

        count += 1

        if k % 20 == 0:
            num_vertices_1 = len(mesh.vertex)

        # split
        if count == 1:
            visited = set()

            for u, v in mesh.wireframe():
                # is this correct?
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

            for u, v in mesh.wireframe():
                # is this correct?
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

            for u, v in mesh.wireframe():
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
            num_vertices_2 = len(mesh.vertex)

            if abs(1 - num_vertices_1 / float(num_vertices_2)) < divergence and k > kmax_start:
                break

        # smoothen
        if smooth:
            boundary = set(mesh.vertices_on_boundary())
            mesh_smooth_centroid(mesh, fixed=boundary, kmax=1)

        if callback:
            callback(mesh, k, callback_args)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import time

    from compas.datastructures.mesh import Mesh

    from compas.visualization.plotters.meshplotter import MeshPlotter

    vertices = [
        (0.0, 0.0, 0.0),
        (10.0, 0.0, 0.0),
        (10.0, 10.0, 0.0),
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

    t0 = time.time()

    trimesh_optimise_topology(
        mesh,
        0.5,
        tol=0.05,
        kmax=300,
        allow_boundary_split=True,
        allow_boundary_swap=True,
        fixed=mesh.vertices_on_boundary()
    )

    t1 = time.time()

    print(t1 - t0)

    plotter = MeshPlotter(mesh)

    plotter.defaults['vertex.edgewidth'] = 0.1

    plotter.defaults['face.facecolor'] = '#eeeeee'
    plotter.defaults['face.edgecolor'] = '#222222'
    plotter.defaults['face.edgewidth'] = 0.1

    plotter.draw_vertices(radius=0.05)
    plotter.draw_faces()

    plotter.show()
