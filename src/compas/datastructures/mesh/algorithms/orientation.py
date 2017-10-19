from __future__ import print_function

from compas.datastructures.network.algorithms import network_bfs


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'mesh_unify_cycles',
    'mesh_flip_cycles',
]


def mesh_unify_cycles(mesh, root=None):
    """Unify the cycle directions of all faces.

    Unified cycle directions is a necessary condition for the data structure to
    work properly. When in doubt, run this function on your mesh.

    Parameters:
        root (str): The key of the root face. Defaults to None.

    Raises:
        ValueError: If `direction` is not one of (None, `ccw`, `cw`)

    Dependencies:
        scipy.spatial import cKDTree

    """
    def unify(node, nbr):
        for u, v in mesh.face_halfedges(nbr):
            if u in mesh.face[node]:
                if v in mesh.face[node]:
                    i = mesh.face[node].index(u)
                    j = mesh.face[node].index(v)
                    if i == j - 1:
                        # if the traversal of a neighbouring halfedge
                        # is in the same direction
                        # flip the neighbour
                        mesh.face[nbr][:] = mesh.face[nbr][::-1]
                        return

    if root is None:
        root = mesh.get_any_face()

    network_bfs(mesh.face_adjacency(), root, unify)

    mesh.halfedge = {key: {} for key in mesh.vertices()}
    for fkey in mesh.faces():
        for u, v in mesh.face_halfedges(fkey):
            mesh.halfedge[u][v] = fkey
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None


def mesh_flip_cycles(mesh):
    """Flip the cycle directions of all faces.

    This function does not care about the directions being unified or not. It
    just reverses whatever direction it finds.

    """
    mesh.halfedge = {key: {} for key in mesh.vertices()}
    for fkey in mesh.faces():
        mesh.face[fkey][:] = mesh.face[fkey][::-1]
        for u, v in mesh.face_halfedges(fkey):
            mesh.halfedge[u][v] = fkey
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None


def _mesh_unify_cycles(mesh, root=None):
    """Unify the cycle directions of all faces.

    Unified cycle directions is a necessary condition for the data structure to
    work properly. When in doubt, run this function on your mesh.

    Parameters:
        root: The key of the root face. Defaults to None.

    """

    def is_flipped(face_vertices1, face_vertices2):
        edges = [(face_vertices1[i - 1], face_vertices1[i]) for i in range(len(face_vertices1))]
        for i in range(len(face_vertices2)):
            if (face_vertices2[i - 1], face_vertices2[i]) in edges:
                return True
        return False

    def is_neighbor(face_edges1, face_edges2):
        for u, v in face_edges1:
            if (u, v) in face_edges2 or (v, u) in face_edges2:
                return True
        return False

    # initialize lists and dictionaries
    faces = mesh.faces()
    faces_vertices_dic = {}
    faces_edges = []
    index_key = []
    for fkey in faces:
        face_vertices = mesh.face_vertices(fkey, True)
        faces_vertices_dic[fkey] = face_vertices
        faces_edges.append(set([(face_vertices[i - 1], face_vertices[i]) for i in range(len(face_vertices))]))
        index_key.append(fkey)

    # find neighboring faces
    face_nbr = {key: set() for key in index_key}
    n = len(faces_edges)
    for i in xrange(n):
        keyi = index_key[i]
        fece_edges_i = faces_edges[i]
        for j in xrange(i + 1, n):
            if is_neighbor(fece_edges_i, faces_edges[j]):
                keyj = index_key[j]
                face_nbr[keyi].add(keyj)
                face_nbr[keyj].add(keyi)

    # define root face key
    if root:
        fkeys = [root]
    else:
        fkeys = [mesh.get_any_face()]

    # march over faces and flip if necessary
    seen = set()
    while fkeys:
        fkey = fkeys.pop()
        seen.add(fkey)
        nbrs = face_nbr[fkey]
        for nbr in nbrs:
            if nbr in seen:
                continue
            if is_flipped(faces_vertices_dic[fkey], faces_vertices_dic[nbr]):
                faces_vertices_dic[nbr] = faces_vertices_dic[nbr][::-1]

            seen.add(nbr)
            fkeys += [nbr]

    # reconstruct faces
    for fkey, face in faces_vertices_dic.iteritems():
        del mesh.face[fkey]
        mesh.add_face(face, fkey)

    return mesh


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    import time
    import compas

    from compas.datastructures.mesh import Mesh

    mesh = Mesh.from_obj(compas.get_data('faces_big.obj'))

    # tic = time.time()
    # unify_cycles_mesh(mesh)
    # tac = time.time()
    # print (tac - tic)

    # tic = time.time()
    # _unify_cycles_mesh(mesh)
    # tac = time.time()
    # print (tac - tic)

    mesh_flip_cycles(mesh)

    print(mesh)
