from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import circle_from_points

__all__ = [
    'trimesh_face_circle'
]


def trimesh_face_circle(mesh, fkey):
    """Get data on circumcentre of triangular face.

    Parameters
    ----------
    fkey : Key
        The face key.

    Returns
    -------
    list, None
        The centre coordinates, the radius value and the normal vector of the circle.
        None if the face is not a triangle

    """

    face_vertices = mesh.face_vertices(fkey)

    # return None if not a triangle (possible improvement with best-fit circle)
    if len(face_vertices) != 3:
        return None
    
    a, b, c = face_vertices

    return circle_from_points(mesh.vertex_coordinates(a), mesh.vertex_coordinates(b), mesh.vertex_coordinates(c))
  

# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas
    from compas.datastructures import Mesh

    vertices = [
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ]

    faces = [
        [0, 1, 2]
    ]

    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    print(trimesh_face_circle(mesh, 0))
