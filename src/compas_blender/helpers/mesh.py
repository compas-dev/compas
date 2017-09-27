from compas.datastructures.mesh import Mesh

from compas.geometry import centroid_points

from compas_blender.utilities import draw_bmesh
from compas_blender.utilities import deselect_all_objects
from compas_blender.utilities import xdraw_cubes
from compas_blender.utilities import xdraw_labels
from compas_blender.utilities import xdraw_lines

from compas_blender.geometry import bmesh_data

import json

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'draw_mesh',
    'mesh_from_bmesh',
    'display_mesh_vertex_labels',
    'display_mesh_edge_labels',
    'display_mesh_face_labels'
]


# ==============================================================================
# drawing
# ==============================================================================

def draw_mesh(mesh, type='mesh', layer=0, show_vertices=0.01, show_edges=0.005, show_faces=True,
              vertex_name_attr=[], edge_name_attr=[], face_name_attr=[]):
    """ Draw a representation of a Mesh datastructure.

    Parameters:
        mesh (obj): Mesh datastructure.
        type (str): Draw as 'mesh' or 'faces'.
        layer (int): Layer to draw Mesh on.
        show_vertices (float): Size of vertex cubes when type is 'faces'.
        show_edges (float): Size of lines when type is 'faces'.
        show_faces (bool): Draw Mesh faces.
        vertex_name_attr (list): Attributes to show in vertex names.
        edge_name_attr (list): Attributes to show in edge names.
        face_name_attr (list): Attributes to show in face names.

    Returns:
        obj: Created Blender mesh or None.
    """
    keys = list(mesh.vertices())
    vertices = [mesh.vertex_coordinates(key) for key in keys]

    k_i = mesh.key_index()
    uv_i = {(u, v): index for index, (u, v) in enumerate(mesh.edges())}
    u_v = list(mesh.edges())
    edges = [(k_i[u], k_i[v]) for u, v in u_v]

    fkeys = list(mesh.faces())
    faces = [mesh.face[fkey] for fkey in fkeys]

    if type == 'mesh':

        return draw_bmesh('mesh', vertices=vertices, edges=edges, faces=faces)

    elif type == 'faces':

        if show_vertices:
            cubes_vertices = []
            for key in keys:
                vertex = mesh.vertex[key]
                xyz = mesh.vertex_coordinates(key)
                color = 'black' if vertex.get('is_fixed', None) else 'white'
                name_dic = {}
                for attr in vertex_name_attr:
                    name_dic[attr] = vertex.get(attr, 'None')
                name = json.dumps(name_dic)
                cubes_vertices.append({'radius': show_vertices, 'pos': xyz, 'color': color, 'name': name})
            xdraw_cubes(cubes_vertices)

        if show_edges:
            lines_edges = []
            for u, v in u_v:
                sp = mesh.vertex_coordinates(u)
                ep = mesh.vertex_coordinates(v)
                i = uv_i[(u, v)]
                color = mesh.edge[u][v].get('color', 'grey')
                name_dic = {}
                for attr in edge_name_attr:
                    name_dic[attr] = mesh.edge[u][v].get(attr, 'None')
                name = json.dumps(name_dic)
                lines_edges.append({'name': name, 'start': sp, 'end': ep, 'layer': layer, 'color': color, 'width': show_edges})
            xdraw_lines(lines_edges)

        if show_faces:
            for fkey in fkeys:
                facedata = mesh.facedata[fkey]
                color = facedata.get('color', 'grey')
                pts = [vertices[i] for i in mesh.face[fkey]]
                name_dic = {}
                for attr in face_name_attr:
                    name_dic[attr] = facedata.get(attr, 'None')
                name = json.dumps(name_dic)
                draw_bmesh(name=name, vertices=pts, faces=[list(range(len(pts)))], layer=layer, color=color)

    deselect_all_objects()


def draw_mesh_as_faces():
    raise NotImplementedError


def display_mesh_vertex_labels(mesh, layer=0):
    """ Draw Mesh vertex labels.

    Parameters:
        mesh (obj): Mesh datastructure.
        layer (int): Layer to draw labels on.

    Returns:
        None
    """
    keys = list(mesh.vertices())
    vertices = [mesh.vertex_coordinates(key) for key in keys]
    labels = []
    for i, xyz in enumerate(vertices):
        labels.append({'name': 'V{0}'.format(i), 'pos': xyz, 'layer': layer})
    xdraw_labels(labels)


def display_mesh_edge_labels(mesh, layer=0):
    """ Draw Mesh edge labels.

    Parameters:
        mesh (obj): Mesh datastructure.
        layer (int): Layer to draw labels on.

    Returns:
        None
    """
    uv_i = {(u, v): index for index, (u, v) in enumerate(mesh.edges())}
    u_v = list(mesh.edges())
    labels = []
    for u, v in u_v:
        sp = mesh.vertex_coordinates(u)
        ep = mesh.vertex_coordinates(v)
        xyz = centroid_points([sp, ep])
        i = uv_i[(u, v)]
        labels.append({'name': 'E{0}'.format(i), 'pos': xyz, 'layer': layer})
    xdraw_labels(labels)


def display_mesh_face_labels(mesh, layer=0):
    """ Draw Mesh face labels.

    Parameters:
        mesh (obj): Mesh datastructure.
        layer (int): Layer to draw labels on.

    Returns:
        None
    """
    fkeys = list(mesh.faces())
    labels = []
    for fkey in fkeys:
        xyz = centroid_points([mesh.vertex_coordinates(i) for i in mesh.face[fkey]])
        labels.append({'name': 'F{0}'.format(fkey), 'pos': xyz, 'layer': layer})
    xdraw_labels(labels)


# ==============================================================================
# constructors
# ==============================================================================

def mesh_from_bmesh(bmesh):
    """ Create a Mesh datastructure from a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        obj: Mesh object.
    """
    vertices, _, faces = bmesh_data(bmesh)
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    mesh.add_edges_from_faces()
    return mesh


def mesh_from_surface():
    raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas_blender.utilities import delete_all_objects
    from compas_blender.utilities import draw_plane

    mesh = mesh_from_bmesh(draw_plane(dx=1, dy=1, bracing='cross'))

    delete_all_objects()

    draw_mesh(mesh, type='mesh')
    display_mesh_vertex_labels(mesh)
    display_mesh_edge_labels(mesh)
    display_mesh_face_labels(mesh)
