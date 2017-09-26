"""Wrapper for the ShapeOp library."""

from __future__ import print_function

try:
    from compas.interop.shapeop._shapeop import *
except ImportError:
    try:
        from compas.interop.shapeop._shapeop_windows import *
    except ImportError:
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'planarize_mesh',
    'circularize_mesh'
]


def planarize_mesh(mesh, fixed=None, kmax=100):
    """"""

    # replace this by explicit closeness values
    fixed = fixed or []
    fixed = set(fixed)

    # create a shapeop solver
    solver = ShapeOpSolver(kmax=kmax)

    # make a key-index map
    # and count the number of vertices in the mesh
    key_index = mesh.key_index()

    # get the vertex coordinates
    xyz = mesh.get_vertices_attributes('xyz')

    # set the coordinates in the solver
    solver.set_points(xyz)

    # add a plane constraint to all faces
    for fkey in mesh.faces():
        vertices = [key_index[key] for key in mesh.face_vertices(fkey)]
        solver.add_plane_constraint(vertices, 1.0)

    # add a closeness constraint to the fixed vertices
    for key in fixed:
        vertex = key_index[key]
        solver.add_closeness_constraint(vertex, 1.0)

    # solve
    solver.solve()

    # update the points array
    points = solver.get_points()

    # clean up
    solver.delete()

    # update
    for index, (key, attr) in enumerate(mesh.vertices(True)):
        index *= 3
        attr['x'] = points[index + 0]
        attr['y'] = points[index + 1]
        attr['z'] = points[index + 2]


def circularize_mesh(mesh, fixed=None, kmax=100):
    """"""

    # replace this by explicit closeness values
    fixed = fixed or []
    fixed = set(fixed)

    # create a shapeop solver
    solver = ShapeOpSolver(kmax=kmax)

    # make a key-index map
    # and count the number of vertices in the mesh
    key_index = mesh.key_index()

    # get the vertex coordinates
    xyz = mesh.get_vertices_attributes('xyz')

    # set the coordinates in the solver
    solver.set_points(xyz)

    # add a plane constraint to all faces
    for fkey in mesh.faces():
        vertices = [key_index[key] for key in mesh.face_vertices(fkey)]
        solver.add_circle_constraint(vertices, 1.0)

    # add a closeness constraint to the fixed vertices
    for key in fixed:
        vertex = key_index[key]
        solver.add_closeness_constraint(vertex, 1.0)

    # solve
    solver.solve()

    # update the points array
    points = solver.get_points()

    # clean up
    solver.delete()

    # update
    for index, (key, attr) in enumerate(mesh.vertices(True)):
        index *= 3
        attr['x'] = points[index + 0]
        attr['y'] = points[index + 1]
        attr['z'] = points[index + 2]


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import compas

    from compas.datastructures.mesh import Mesh
    from compas.datastructures.mesh.viewer import MeshViewer

    mesh = Mesh.from_obj(compas.get_data('hypar.obj'))

    for key, attr in mesh.vertices(True):
        attr['is_fixed'] = mesh.vertex_degree(key) == 2

    circularize_mesh(mesh, fixed=mesh.vertices_where({'is_fixed': True}), kmax=100)

    # ideally:
    # viewer = Viewer()
    # viewer.draw_points(points)
    # viewer.draw_lines(lines)
    # viewer.draw_polygons(polygons)
    # viewer.draw_vectors(vectors)
    # viewer.draw_...
    # viewer.draw_network(network)
    # viewer.draw_mesh(mesh)

    viewer = MeshViewer(mesh)

    viewer.setup()
    viewer.show()
