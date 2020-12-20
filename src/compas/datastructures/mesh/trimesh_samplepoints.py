from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from numpy import array
from numpy.random import choice
from numpy.random import rand
from numpy import sqrt
from numpy import float64
from numpy import cross
from numpy.linalg import norm
from numpy import clip
from numpy import finfo


__all__ = [
    'trimesh_samplepoints',
]


def trimesh_samplepoints(mesh, num_points: int = 1000, return_normals: bool = False):
    """Compute sample points on a triangle mesh surface

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        Mesh is limited to triangle mesh
    num_points : (int)
        How many points sampled
    return_normals : (bool)
        if True, return the normals vector of sampled points

    Returns
    -------
    samples_points(numpy.ndarray)
        A numpy array representing sampled points with dim = [num_points, 3]
    (if True) samples_points_normals(numpy.ndarray)
        A numpy array representing the normal vector of sampled points  with dim = [num_points, 3]

    Examples
    --------
    >>> hypar = Mesh.from_obj(compas.get('hypar.obj'))
    >>> hypar.is_trimesh() # First check if the input mesh is triangle mesh
    False
    >>> hypar.quads_to_triangles()
    >>> samples_pts, pts_normals = trimesh_samplepoints(hypar, 1000, True)
    >>> # the x,y,z of sample points would be the following
    >>> x, y, z = samples_pts[:,0], samples_pts[:,1], samples_pts[:,2]
    >>> # the sample points added normal vector would be the following
    >>> X, Y, Z = x + pts_normals[:,0] , y + pts_normals[:,1] , z + pts_normals[:,2]
    >>> # You can import matplotlib for visualization
    >>> import matplotlib.pyplot as plt
    >>> from mpl_toolkits.mplot3d import Axes3D
    >>> fig = plt.figure(figsize=(5, 5))
    >>> ax = Axes3D(fig)
    >>> ax.scatter3D(x, y, z, label="Points")
    <mpl_toolkits.mplot3d.art3d.Path3DCollection object at ...
    >>> ax.scatter3D(X, Y, Z, label="Points Added Normal")
    <mpl_toolkits.mplot3d.art3d.Path3DCollection object at ...
    >>> ax.legend(fontsize="16")
    <matplotlib.legend.Legend object at ...
    >>> ax.set_xlabel('x')
    Text(0.5, 0, 'x')
    >>> ax.set_ylabel('y')
    Text(0.5, 0, 'y')
    >>> ax.set_zlabel('z')
    Text(0.5, 0, 'z')
    >>> ax.view_init(190, 30)
    >>> plt.show()

    References
    ----------
    .. [1] Barycentric coordinate system, Available at https://en.wikipedia.org/wiki/Barycentric_coordinate_system
    .. [2] Efficient barycentric point sampling on meshes, arXiv:1708.07559

    """
    if mesh.is_empty():
        raise ValueError("Mesh is empty.")
    if not mesh.is_trimesh():
        raise ValueError("Mesh is not trimesh.")
    if not mesh.is_valid():
        raise ValueError("Mesh is invalid.")

    # (1)  acquire the area of all mesh faces
    area_list = array([mesh.face_area(face) for face in mesh.faces()])
    area_list_norm = area_list / area_list.sum()

    # (2) sample num_points on a mesh face regarding its weight of area
    faces = list(range(mesh.number_of_faces()))
    samples_faces = choice(faces, num_points, p=area_list_norm)

    # (3) create a ndarray of vertices regarding the faces
    vertices, faces = mesh.to_vertices_and_faces()
    vertices = array(vertices, dtype=float64)
    faces = array(faces)
    faces_vertices = vertices[faces]

    # (4) Barycentric Coordinate for Surface Sampling
    v0, v1, v2 = faces_vertices[:, 0], faces_vertices[:, 1], faces_vertices[:, 2]
    r1_r2 = rand(2, num_points)
    r1, r2 = r1_r2[0], r1_r2[1]  # r1, r2 uniformly distributed from 0 to 1
    r1_sqrt = sqrt(r1)
    w0 = 1.0 - r1_sqrt
    w1 = r1_sqrt * (1.0 - r2)
    w2 = r1_sqrt * r2
    a = v0[samples_faces]
    b = v1[samples_faces]
    c = v2[samples_faces]

    # (5) return vertices of points in the format of ndarray
    samples_points = w0[:, None] * a + w1[:, None] * b + w2[:, None] * c

    # (6) (if True) Return the normal vector of the sampled points
    if return_normals:

        samples_points_normals = cross((v1 - v0), (v2 - v1), axis=1)
        samples_points_normals_norm = norm(samples_points_normals, ord=2, axis=1, keepdims=True)
        samples_points_normals = samples_points_normals / samples_points_normals_norm
        samples_points_normals = clip(samples_points_normals, a_min=finfo(float64).eps, a_max=None)
        samples_points_normals = samples_points_normals[samples_faces]

        return samples_points, samples_points_normals
    else:
        return samples_points


if __name__ == '__main__':

    import doctest
    import compas
    from compas.datastructures import Mesh

    hypar = Mesh.from_obj(compas.get('hypar.obj'))

    doctest.testmod(optionflags=doctest.ELLIPSIS)
