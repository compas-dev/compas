from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from numpy import array
from numpy.random import choice
from numpy.random import rand
from numpy import sqrt




__all__ = [
    'mesh_to_points',
]

def mesh_to_points(mesh, num_points: int = 10000):
    """Convert a mesh to points

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        The mesh data structure.
    num_points : (int) 
        How many points sampled
    return_normals : (bool)  (TODO)
        Return normals for the points, if True

    Returns
    -------
    list
        A numpy array with dim = [num_points, 3].

    Examples
    --------


    """
    if mesh.is_empty():
    raise ValueError("Mesh is empty.")
    if mesh.is_quadmesh():
        mesh.quads_to_triangles()
    if not mesh.is_valid():
        raise ValueError("Mesh is invalid.")
        
    # (1)  acquire the list of area
    first_idx = list(mesh.face.keys())[0]
    add_idx = 0
    area_list=[]
    if first_idx != 0:
        add_idx = first_idx
    for i in range(len(mesh.face)):
        area_list.append(mesh.face_area(i+add_idx))
    area_list = array(area_list)
    area_list_norm = area_list / area_list.sum()

    # (2) sample num_points on a mesh face regarding its weight of area
    mesh_face_idx = list(mesh.face.keys())
    sample_face_idxs = choice(mesh_face_idx, num_points, p=area_list_norm) - add_idx

    # (3) create a ndarray of vertices regarding the faces
    vertices = mesh.to_vertices_and_faces()[0]
    vertices = array(vertices)
    faces = mesh.to_vertices_and_faces()[1]
    faces = array(faces)
    faces_vertices = vertices[faces]

    # (4) Barycentric Coordinate for Surface Sampling
    v0, v1, v2 = faces_vertices[:, 0], faces_vertices[:, 1], faces_vertices[:, 2]
    r1_r2 = rand(2, num_points)
    r1, r2 = r1_r2[0], r1_r2[1] #r1, r2 uniformly distributed from 0 to 1
    r1_sqrt = sqrt(r1)
    w0 = 1.0 - r1_sqrt
    w1 = r1_sqrt * (1.0 - r2)
    w2 = r1_sqrt * r2
    a = v0[sample_face_idxs]
    b = v1[sample_face_idxs]
    c = v2[sample_face_idxs]

    # (5) Finally vertices of points
    samples_points = w0[ :, None] * a + w1[ :, None] * b + w2[ :, None] * c
    return samples_points

if __name__ == '__main__':

    import doctest
    import compas
    from compas.datastructures import Mesh

    hypar = Mesh.from_obj(compas.get('hypar.obj'))
    mesh = Mesh.from_obj(compas.get('faces.obj'))

    doctest.testmod()