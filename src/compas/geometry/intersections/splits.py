from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh
from compas.geometry import Polyline
from compas.geometry import intersection_segment_plane
from compas.geometry.intersections import intersection_mesh_plane
from compas.geometry import subtract_vectors
from compas.geometry import dot_vectors

__all__ = [
    'split_polyline_plane',
    'split_mesh_plane',
]

def split_polyline_plane(polyline, plane):
    """Splits a polyline by a plane, returns a list of polylines, if there has been intersections
    Returns list of the splitted polylines

    Parameters
    ----------
    polyline : compas.datastructures.Polyline
    plane : compas.geometry.Plane

    Returns
    -------
    polylines : list of compas.geometry.Polyline
    """
    splitted_polylines_points=[]
    sublist=[]
    for i, segment in enumerate(polyline.lines):
        sublist.append(segment.start) 
        temp_intersection = intersection_segment_plane(segment, plane)
        if temp_intersection:
            sublist.append(temp_intersection)
            splitted_polylines_points.append(sublist) 
            sublist=[] 
            sublist.append(temp_intersection) 
        if i == len(polyline.lines)-1: 
            sublist.append(segment.end) 
            splitted_polylines_points.append(sublist)

    return [Polyline(sublist) for sublist in splitted_polylines_points] 

def split_mesh_plane(mesh, plane, open=True): #compas
    """ Calculates all the intersections between edges of the mesh and cutting plane,
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
    def mesh_from_split(self, mesh, v_keys, f_keys, intersections, open=True): # compas
        """ Returns a mesh from the positive or negative verts, faces and the intersection verts of a splitted mesh
        open = true for open splits, open= False for closed splits
        """
        vertices = {key: mesh.vertex_coordinates(key) for key in v_keys + intersections}
        faces = [mesh.face_vertices(f_key) for f_key in f_keys]
        final_mesh = Mesh.from_vertices_and_faces(vertices, faces)
        if not open: 
            final_mesh.add_face(final_mesh.vertices_on_boundary(True))
        return final_mesh

    intersections = intersection_mesh_plane(mesh, plane)

    if len(intersections)> 2:
        for f_key in list(mesh.faces()):
            split = [v_key for v_key in mesh.face_vertices(f_key) if v_key in intersections]
            if len(split)== 2:
                mesh.split_face(f_key, split[0], split[1])

        pos_verts =[]
        neg_verts = []
        for v_key in mesh.vertices():
            if v_key in intersections: 
                continue
            vert_a = mesh.vertex_attributes(v_key,'xyz')
            ori_vert_a = subtract_vectors(vert_a, plane.point)
            similarity = dot_vectors(plane.normal, ori_vert_a)
            if similarity > 0.0:
                pos_verts.append(v_key)
            elif similarity < 0.0:
                neg_verts.append(v_key)
        
        pos_faces=[]
        for key in pos_verts:
            pos_faces += mesh.vertex_faces(key)
        pos_faces = list(set(pos_faces))

        neg_faces=[]
        for key in neg_verts:
            neg_faces += mesh.vertex_faces(key)
        neg_faces = list(set(neg_faces))

        pos_mesh = mesh_from_split(mesh, pos_verts, pos_faces, intersections, open)
        neg_mesh = mesh_from_split(mesh, neg_verts, neg_faces, intersections, open)

        splitted_meshes = [pos_mesh, neg_mesh]
        return splitted_meshes
    else:
        return None