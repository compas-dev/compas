from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import atan2
from math import pi
from math import sqrt

import clr  # type: ignore
import Rhino  # type: ignore
import scriptcontext  # type: ignore
import System  # type: ignore

from compas.plugins import plugin


@plugin(category="trimesh", requires=["Rhino"])
def trimesh_gaussian_curvature(M):
    r"""Compute the discrete Gaussian curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The discrete Gaussian curvature per vertex.

    Notes
    -----
    Description: The angle defect at a vertex is used to describe the Gaussian curvature in a neighborhood around a vertex.

    Notation Convention:
        * :math:`K_{i}` - discrete Gaussian curvature at vertex i
        * :math:`j,k` - the vertices from the Star of vertex i
        * :math:`e_{ij},\, e_{ik}` - the vectors from vertex i to j and i to k
        * :math:`\\theta_{i}^{jk}` - interior angle at vertex i of triangle ijk

    Formula:

    .. math::

        K_{i} = 2\pi-\sum\\theta_{i}^{jk}

    References
    ----------
    .. [1] Formula of Discrete Gaussian Curvature available at Keenan Crane's lecture, 03:16-07:11, at https://youtu.be/sokeN5VxBB8

    Examples
    --------
    Make a mesh from scratch
    >>> from compas.geometry import Sphere
    >>> sphere = Sphere([1, 1, 1], 1)
    >>> sphere = Mesh.from_shape(sphere, u=30, v=30)
    >>> sphere.quads_to_triangles()
    >>> M = sphere.to_vertices_and_faces()

    Compute the discrete Gaussian curvature
    >>> K = trimesh_gaussian_curvature(M)

    """
    # (0) see if input is already Rhino.Geometry.Mesh
    mesh = Rhino.Geometry.Mesh()
    if not isinstance(M, Rhino.Geometry.Mesh):
        for x, y, z in M[0]:
            mesh.Vertices.Add(x, y, z)
        for face in M[1]:
            mesh.Faces.AddFace(*face)
    else:
        mesh = M

    # (1) check if it is a trimesh
    if mesh.Faces.QuadCount > 0:
        raise ValueError("Mesh is not trimesh.")

    # (2) Prepare ingredient and return list
    pi_2 = 2 * pi
    K = []

    # (3) Main - loop every vertex for angle defect
    for i in range(mesh.Vertices.Count):
        vert_neighbors_topo = mesh.TopologyVertices.ConnectedTopologyVertices(mesh.TopologyVertices.TopologyVertexIndex(i), True)
        vert_neighbors = []
        if vert_neighbors_topo is None:
            K.append(None)
            continue
        for vert in vert_neighbors_topo:
            vert_neighbors.extend(mesh.TopologyVertices.MeshVertexIndices(vert))
        angles = []
        valence = len(vert_neighbors)
        v_i = mesh.Vertices[i]
        # loop every neighbor
        for j in range(valence):
            v_j = mesh.Vertices[vert_neighbors[j]]
            v_k = mesh.Vertices[vert_neighbors[(j + 1) % valence]]
            e_ij = v_j - v_i
            e_ik = v_k - v_i
            angles.append(Rhino.Geometry.Vector3d.VectorAngle(e_ij, e_ik))
        K.append(pi_2 - sum(angles))
    # (4) Output
    return K


trimesh_gaussian_curvature.__plugin__ = True


@plugin(category="trimesh", requires=["Rhino"])
def trimesh_mean_curvature(M):
    r"""Compute the discrete mean curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The discrete mean curvature per vertex.

    Notes
    -----
    Description: The discrete mean curvature is computed by edge length and its dihedral angle.

    Notation Convention:
        * :math:`H_{i}` - discrete mean curvature at vertex i
        * :math:`E` - all the edges connected to vertex i
        * :math:`j` - a vertex connected to vertex i
        * :math:`l_{ij}` - the length of edge ij
        * :math:`\phi_{ij}` - the dihedral angle of edge ij

    Formula:

    .. math::

        H_{i} = \frac{1}{4}\sum_{ij\in E}l_{ij}\phi_{ij}

    References
    ----------
    .. [1] Formula of Discrete Mean Curvature available at Keenan Crane's lecture, 03:16-07:11, at https://youtu.be/sokeN5VxBB8
    .. [2] Formula of dihedral angle available at Keenan Crane's lecture, 04:20-05:43, at https://youtu.be/NlU1m-OfumE

    Examples
    --------
    Make a mesh from scratch
    >>> from compas.geometry import Sphere
    >>> sphere = Sphere([1, 1, 1], 1)
    >>> sphere = Mesh.from_shape(sphere, u=30, v=30)
    >>> sphere.quads_to_triangles()
    >>> M = sphere.to_vertices_and_faces()

    Compute the discrete mean curvature
    >>> H = trimesh_mean_curvature(M)

    """
    # (0) see if input is already Rhino.Geometry.Mesh
    mesh = Rhino.Geometry.Mesh()
    if not isinstance(M, Rhino.Geometry.Mesh):
        for x, y, z in M[0]:
            mesh.Vertices.Add(x, y, z)
        for face in M[1]:
            mesh.Faces.AddFace(*face)
    else:
        mesh = M

    # (1) check if it is a trimesh
    if mesh.Faces.QuadCount > 0:
        raise ValueError("Mesh is not trimesh.")

    # (2) Prepare ingredient and return list
    H = []
    mesh.FaceNormals.ComputeFaceNormals()
    faces_normal = mesh.FaceNormals

    # (3) Main - loop over all vertices
    for i in range(mesh.Vertices.Count):
        edges = mesh.TopologyVertices.ConnectedEdges(mesh.TopologyVertices.TopologyVertexIndex(i))
        vertex = Rhino.Geometry.Point3d.FromPoint3f(mesh.Vertices[i])
        if edges is None:
            H.append(None)
            continue
        x = []
        # (3.1) loop topology edges of such vertex
        for edge in edges:
            l_ij = mesh.TopologyEdges.EdgeLine(edge).Length
            orientation = clr.StrongBox[System.Array[bool]]()
            faces = mesh.TopologyEdges.GetConnectedFaces(edge, orientation)
            if len(faces) != 2:
                x.append(0)
                continue
            # (3.2) to know which face is on left or right
            orientation = list(orientation.Value)
            start_pt = mesh.TopologyEdges.EdgeLine(edge).From
            direction = start_pt.EpsilonEquals(vertex, scriptcontext.doc.ModelAbsoluteTolerance)
            normals = dict(zip(orientation, [faces_normal[faces[0]], faces_normal[faces[1]]]))
            e = mesh.TopologyEdges.EdgeLine(edge).Direction
            e.Unitize()
            n1 = normals[True]
            n2 = normals[False]
            if not direction:
                e.Reverse()
                n1, n2 = n2, n1
            # (3.3) calculate dihedral angle
            angle = dihedral_angle(e, n1, n2)
            x.append(l_ij * angle)
        H.append(1 / 4 * sum(x))

    # (4) Output
    return H


trimesh_mean_curvature.__plugin__ = True


@plugin(category="trimesh", requires=["Rhino"])
def trimesh_principal_curvature(M):
    r"""Compute the principal curvature of a triangle mesh.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.

    Returns
    -------
    list[float]
        The max curvature per vertex.
    list[float]
        The min curvature per vertex.

    Notes
    -----
    Description: The discrete principal curvature is computed by mean curvature, Gaussian curvature, and vertex area.

    Notation Convention:
        * :math:`\kappa^1_i, \kappa^2_i` - The max principal curvature and the min principal curvature at the vertex i
        * :math:`H_i` - the discrete mean curvature at vertex i
        * :math:`K_i` - the discrete Gaussian curvature at vertex i
        * :math:`A_i` - the area of the dual cell centered at vertex i

    Formula:

    .. math::

        \kappa^1_i, \kappa^2_i =  \frac{H_i}{A_i}\pm\sqrt{\left( \,\frac{H_i}{A_i}\right)\,^2-\frac{K_i}{A_i}}

    References
    ----------
    .. [1] Formula of Discrete Principal Curvature available at Keenan Crane's lecture, 03:16-07:11, at https://youtu.be/sokeN5VxBB8

    Examples
    --------
    Make a mesh from scratch
    >>> from compas.geometry import Sphere
    >>> sphere = Sphere([1, 1, 1], 1)
    >>> sphere = Mesh.from_shape(sphere, u=30, v=30)
    >>> sphere.quads_to_triangles()
    >>> M = sphere.to_vertices_and_faces()

    Compute the discrete principal curvature
    >>> H = trimesh_principal_curvature(M)

    """
    # (0) see if input is already Rhino.Geometry.Mesh
    mesh = Rhino.Geometry.Mesh()
    if not isinstance(M, Rhino.Geometry.Mesh):
        for x, y, z in M[0]:
            mesh.Vertices.Add(x, y, z)
        for face in M[1]:
            mesh.Faces.AddFace(*face)
    else:
        mesh = M

    # (1) check if it is a trimesh
    if mesh.Faces.QuadCount > 0:
        raise ValueError("Mesh is not trimesh.")

    # (2) Prepare ingredient and return list
    k1 = []
    k2 = []
    A = trimesh_barycentric_area(mesh)
    H = trimesh_mean_curvature(mesh)
    K = trimesh_gaussian_curvature(mesh)

    # (3) Main - loop over all vertices
    for i in range(mesh.Vertices.Count):
        if A[i] == 0:
            k1.append(None)
            k2.append(None)
            continue
        H_ = H[i] / A[i]
        K_ = K[i] / A[i]

        discriminant = sqrt(max(0, H_ * H_ - K_))
        k1.append(H_ + discriminant)
        k2.append(H_ - discriminant)

    # (4) Output
    return k1, k2


trimesh_principal_curvature.__plugin__ = True


def trimesh_barycentric_area(mesh):
    # (1) prepare return list
    areas = [0] * mesh.Vertices.Count

    # (2) Main - loop over mesh faces rather than vertices
    for i in range(mesh.Faces.Count):
        # Heron's Formula
        ptA = mesh.Faces.GetFaceVertices(i)[1]
        ptB = mesh.Faces.GetFaceVertices(i)[2]
        ptC = mesh.Faces.GetFaceVertices(i)[3]
        dA = ptB.DistanceTo(ptC)
        dB = ptA.DistanceTo(ptC)
        dC = ptA.DistanceTo(ptB)
        p = (dA + dB + dC) / 2
        area = sqrt(p * (p - dA) * (p - dB) * (p - dC)) / 3

        # topology vertices
        verts_topo = mesh.Faces.GetTopologicalVertices(i)
        # vertices
        verts = []
        for vert_topo in verts_topo:
            verts.extend(mesh.TopologyVertices.MeshVertexIndices(vert_topo))
        for vert in verts:
            areas[vert] += area

    # (3) output
    return areas


def dihedral_angle(e, n1, n2):
    # Compute the dihedral angle of an edge
    # e: the vector from vertex i to j
    # n1: the normal vector of MeshFace on LEFT side
    # n2: the normal vector of MeshFace on RIGHT side

    cos_theta = Rhino.Geometry.Vector3d.Multiply(n1, n2)
    sin_theta = Rhino.Geometry.Vector3d.Multiply(Rhino.Geometry.Vector3d.CrossProduct(n1, n2), e)
    return atan2(sin_theta, cos_theta)
