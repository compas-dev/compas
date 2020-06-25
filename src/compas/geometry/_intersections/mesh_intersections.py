from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import length_vector
from compas.geometry import subtract_vectors
from compas.geometry import intersection_line_triangle
from compas.geometry import intersection_segment_plane

__all__ = [
    'intersection_mesh_line',
    'intersection_mesh_plane',
    'mesh_vertices_to_points',
]


def intersection_mesh_line(mesh, line):
    """Compute intersection between mesh faces and line
    First extracts faces from the mesh and computes the intersection between 
    a triangular face and a line, or two triangles of a quad face and a line.
    After one single intersection, stops searching for more.
    Returns one point from line-mesh intersection if intersection occurs.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
    line : compas.geometry.Line

    Returns
    -------
    Point : compas.geometry.Point
    """
    for fkey in list(mesh.faces()):
        vertex_keys = mesh.face_vertices(fkey)
        if not vertex_keys:
            continue
        vertices = [mesh.vertex_attributes(vkey, 'xyz') for vkey in vertex_keys]
        if len(vertex_keys) not in (3, 4):
            continue

        triangle = [vertices[0], vertices[1], vertices[2]]
        intersection = intersection_line_triangle(line, triangle)
        if intersection:
            return Point(intersection[0], intersection[1], intersection[2])

        if len(vertex_keys) == 4:
            triangle_2 = [vertices[2], vertices[3], vertices[0]]
            intersection_2 = intersection_line_triangle(line, triangle_2)
            if intersection_2:
                return Point(intersection_2[0], intersection_2[1], intersection_2[2])
    else:
        return None

def intersection_mesh_plane(mesh, plane, tol=0.0001):
    """Calculate the keys of the points of the intersection of a mesh with a plane

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
    plane : compas.geometry.Plane

    Returns
    -------
    intersections: list of points as keys from mesh
    """
      
    intersections = [] 
    for u, v in list(mesh.edges()):
        a = mesh.vertex_attributes(u,'xyz')
        b = mesh.vertex_attributes(v,'xyz')
        inters = intersection_segment_plane((a,b), plane)
        if not inters:
            continue
        len_a_inters = length_vector(subtract_vectors(inters, a))
        len_a_b = length_vector(subtract_vectors(b, a))
        t = len_a_inters / len_a_b
        if t >= 1.0: 
            t = 1 - tol
        elif t <= 0.0:
            t = tol
        intersection_key = mesh.split_edge(u, v, t=t, allow_boundary=True)
        intersections.append(intersection_key)
    
    return intersections


def mesh_vertices_to_points(mesh, v_keys):
    """Compute compas points from vertex keys from specific mesh
    Returns list of compas points from a list of indexes of the vertexes of a mesh

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
    v_keys : list of vertex indexes of a mesh

    Returns
    -------
    list of compas.geometry.Point 
    """
    return [Point(*mesh.vertex_attributes(v_key, 'xyz')) for v_key in v_keys]
