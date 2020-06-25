from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise

from compas.datastructures import Mesh
from compas.geometry import Polyline
from compas.geometry import intersection_segment_plane
from compas.geometry._intersections.mesh_intersections import intersection_mesh_plane
from compas.geometry import subtract_vectors
from compas.geometry import dot_vectors

__all__ = [
    'split_polyline_plane',
    'split_mesh_plane',
]


def split_polyline_plane(polyline, plane):
    """Split a polyline by a plane, returns a list of polylines, if there has been intersections
    Returns list of the splitted polylines

    Parameters
    ----------
    polyline : compas.geometry.Polyline
    plane : compas.geometry.Plane

    Returns
    -------
    list of :class: 'compas.geometry.Polyline'
    """
    points_from_split_polylines = []
    sublist = []
    for i, segment in enumerate(pairwise(polyline)):
        sublist.append(segment.start)
        intersection = intersection_segment_plane(segment, plane)
        if intersection:
            sublist.append(intersection)
            points_from_split_polylines.append(sublist)
            sublist = []
            sublist.append(intersection)
        if i == len(pairwise(polyline)) - 1:
            sublist.append(segment.end)
            points_from_split_polylines.append(sublist)

    return [Polyline(sublist) for sublist in points_from_split_polylines]


def _mesh_from_split(mesh, v_keys, f_keys, intersections, open=True):
    """ Return a mesh from the positive or negative verts, faces and the intersection verts of a splitted mesh
    open = true for open splits, open= False for closed splits
    """
    vertices = {key: mesh.vertex_coordinates(key) for key in v_keys + intersections}
    faces = [mesh.face_vertices(f_key) for f_key in f_keys]
    final_mesh = Mesh.from_vertices_and_faces(vertices, faces)
    if not open:
        final_mesh.add_face(final_mesh.vertices_on_boundary(True))
    return final_mesh


def split_mesh_plane(mesh, plane, open=True):
    """ Calculate all the intersections between edges of the mesh and cutting plane,
    and splits every mesh edge at the intersection point, if it exists.
    Returns a list of the resulting splitted meshes.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
    plane : compas.geometry.Plane

    Returns
    -------
    splitted_meshes : list of compas.datastructures.Mesh
    """

    intersections = intersection_mesh_plane(mesh, plane)

    if len(intersections) < 3:
        return None

    for f_key in list(mesh.faces()):
        split = [v_key for v_key in mesh.face_vertices(f_key) if v_key in intersections]
        if len(split) == 2:
            mesh.split_face(f_key, split[0], split[1])

    positive_vertices = []
    negative_vertices = []
    for v_key in mesh.vertices():
        if v_key in intersections:
            continue
        vert_a = mesh.vertex_attributes(v_key, 'xyz')
        ori_vert_a = subtract_vectors(vert_a, plane.point)
        similarity = dot_vectors(plane.normal, ori_vert_a)
        if similarity > 0.0:
            positive_vertices.append(v_key)
        elif similarity < 0.0:
            negative_vertices.append(v_key)

    positive_faces = []
    for key in positive_vertices:
        positive_faces += mesh.vertex_faces(key)
    positive_faces = list(set(positive_faces))

    negative_faces = []
    for key in negative_vertices:
        negative_faces += mesh.vertex_faces(key)
    negative_faces = list(set(negative_faces))

    positive_mesh = _mesh_from_split(mesh, positive_vertices, positive_faces, intersections, open)
    negative_mesh = _mesh_from_split(mesh, negative_vertices, negative_faces, intersections, open)

    splitted_meshes = [positive_mesh, negative_mesh]
    return splitted_meshes
    