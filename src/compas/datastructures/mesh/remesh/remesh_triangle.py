from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from triangle import triangulate
except ImportError:
    pass

from compas.utilities import pairwise
from compas.geometry import centroid_points_xy


__all__ = ['trimesh_remesh_triangle']


def trimesh_remesh_triangle(mesh, target, boundary=None, holes=None):
    segments = []
    _holes = []
    if boundary:
        segments += list(pairwise(boundary + boundary[:1]))
    # if holes:
    #     for boundary in holes:
    #         segments += list(pairwise(boundary + boundary[:1]))
    #         _holes.append(centroid_points_xy(boundary))
    tri = {
        'vertices': list(mesh.get_vertices_attributes('xy')),
        'segments': segments,
        'holes'   : _holes,
    }
    print(tri['vertices'])
    result = triangulate(tri, opts='rpa.5'.format(target))
    print(result)
    vertices = result['vertices'].tolist()
    triangles = result['triangles'].tolist()
    cls = type(mesh)
    return cls.from_vertices_and_faces(vertices, triangles)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    vertices = [(0.0, 0.0, 0.0), (10.0, 0.0, 0.0), (6.0, 10.0, 0.0), (0.0, 10.0, 0.0)]
    faces = [[0, 1, 2, 3]]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    key = mesh.insert_vertex(0)

    area = sum(mesh.face_area(fkey) for fkey in mesh.faces()) / mesh.number_of_faces()
    print(area)

    for fkey in mesh.faces():
        print(len(mesh.face_vertices(fkey)))

    finer = trimesh_remesh_triangle(mesh, target=area/10.0)
    print(finer, key)

    plotter = MeshPlotter(finer, figsize=(10, 7))
    plotter.draw_edges()
    plotter.show()
