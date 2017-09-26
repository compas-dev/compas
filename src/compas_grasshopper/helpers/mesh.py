import rhinoscriptsyntax as rs
from compas.datastructures.mesh import Mesh
from compas.utilities import geometric_key

__author__    = 'Tomas Mendez Echenagucia'
__copyright__ = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__   = 'MIT license'
__email__     = 'mendez@arch.ethz.ch'


__all__ = []

# 'draw_mesh_as_faces',
# 'update_mesh_edge_attributes',
# 'update_mesh_face_attributes',
# 'display_mesh_vertex_labels',
# 'display_mesh_edge_labels',
# 'display_mesh_face_labels',


def make_gkdict(mesh, precision='3f'):
    gkdict = {}
    for key in mesh.vertex:
        xyz = mesh.get_vertex_attributes(key, ['x', 'y', 'z'])
        gk = geometric_key(xyz=xyz, precision=precision)
        gkdict[gk] = key
    return gkdict


def draw_mesh(mesh):
    vkeys = sorted(mesh.vertex.keys(), key=int)
    v = mesh.vertex
    vertices = [[v[k]['x'], v[k]['y'], v[k]['z']] for k in vkeys]
    faces = [mesh.face_vertices(fk, ordered=True) for fk in mesh.faces()]
    rs.AddMesh(vertices, faces)


def mesh_from_guid(guid):
    vertices = rs.MeshVertices(guid)
    faces = [list(face) for face in rs.MeshFaceVertices(guid)]
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    return mesh


# def update_mesh_edge_attributes(mesh, lines, name, values):
#     gkdict = make_gkdict(mesh, precision='3f')
#     if len(values) == 1:
#         values = [values[0]] * len(lines)
#     for i, line in enumerate(lines):
#         value = values[i]
#         u = gkdict[geometric_key(rs.CurveStartPoint(line), precision='3f')]
#         v = gkdict[geometric_key(rs.CurveEndPoint(line), precision='3f')]
#         mesh.set_edge_attribute(u, v, name, value)


def update_mesh_vertex_attributes(mesh, points, name, values):
    gkdict = make_gkdict(mesh, precision='3f')
    if len(values) == 1:
        values = [values[0]] * len(points)
    for i, point in enumerate(points):
        value = values[i]
        u = gkdict[geometric_key(point, precision='3f')]
        mesh.set_vertex_attribute(u, name, value)


def move_mesh(mesh, vector):
    """Move the entire mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): A mesh object.
        vector (list, tupple): The displacement vector.

    """

    for key, attr in mesh.vertices(True):
        attr['x'] += vector[0]
        attr['y'] += vector[1]
        attr['z'] += vector[2]


def move_mesh_vertex(mesh, points, vectors):
    """Move the entire mesh.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): A mesh object.
        vector (list, tupple): The displacement vector.

    """
    gkdict = make_gkdict(mesh, precision='3f')
    if len(vectors) == 1:
        vectors = [vectors[0]] * len(points)
    for i, point in enumerate(points):
        u = gkdict[geometric_key(point, precision='3f')]
        vector = vectors[i]
        mesh.vertex[u]['x'] += vector[0]
        mesh.vertex[u]['y'] += vector[1]
        mesh.vertex[u]['z'] += vector[2]
