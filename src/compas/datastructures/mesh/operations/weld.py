from typing import TYPE_CHECKING
from typing import Collection
from typing import Iterable
from typing import Optional

from compas.topology import connected_components
from compas.topology import vertex_adjacency_from_edges

from ..types import Edge
from ..types import Face
from ..types import Vertex
from .substitute import mesh_substitute_vertex_in_faces

if TYPE_CHECKING:
    from ..mesh import Mesh


def mesh_unweld_vertices(
    mesh: "Mesh", fkey: Face, where: Optional[Collection[Vertex]] = None
) -> list[Vertex]:
    """Unweld a face of the mesh.

    Parameters
    ----------
    mesh
        A mesh object.
    fkey
        The identifier of a face.
    where
        A list of vertices to unweld.
        Default is to unweld all vertices of the face.

    Returns
    -------
    list[int]
        The vertices of the unwelded face.

    """
    vertices = mesh.face_vertices(fkey)
    face_attributes = dict(mesh.face_attributes(fkey))

    if not where:
        where = vertices
    selected = set(where)

    face = []
    for vertex in vertices:
        if vertex in selected:
            vertex = mesh.add_vertex(attr_dict=dict(mesh.vertex_attributes(vertex)))
        face.append(vertex)

    mesh.delete_face(fkey)
    mesh.add_face(face, fkey=fkey, attr_dict=face_attributes)

    return face


def mesh_unweld_edges(mesh: "Mesh", edges: Iterable[Edge]) -> None:
    """Unwelds a mesh along edges.

    Parameters
    ----------
    mesh
        A mesh.
    edges
        List of edges as tuples of vertex keys.

    Returns
    -------
    None

    """
    edges = set(edges)

    # set of vertices in edges to unweld
    vertices = set([i for edge in edges for i in edge])

    # to store changes to do all at once
    vertex_changes = {}

    for vkey in vertices:
        # maps between old mesh face index and new network vertex index
        old_to_new = {nbr: i for i, nbr in enumerate(mesh.vertex_faces(vkey))}
        new_to_old = {i: nbr for i, nbr in enumerate(mesh.vertex_faces(vkey))}

        # get adjacency network of faces around the vertex excluding adjacency
        # through the edges to unweld
        network_edges = []
        for nbr in mesh.vertex_neighbors(vkey):
            if not mesh.is_edge_on_boundary((vkey, nbr)) and (vkey, nbr) not in edges and (nbr, vkey) not in edges:
                face_vkey_nbr = mesh.halfedge[vkey][nbr]
                face_nbr_vkey = mesh.halfedge[nbr][vkey]
                if face_vkey_nbr is None or face_nbr_vkey is None:
                    continue
                network_edges.append(
                    (
                        old_to_new[face_vkey_nbr],
                        old_to_new[face_nbr_vkey],
                    )
                )

        adjacency = vertex_adjacency_from_edges(network_edges)
        for key, values in adjacency.items():
            adjacency[key] = {value: None for value in values}
        # include non connected vertices
        edge_vertices = list(set([i for edge in network_edges for i in edge]))
        for i in range(len(mesh.vertex_faces(vkey))):
            if i not in edge_vertices:
                adjacency[i] = {}

        # collect the disconnected parts around the vertex due to unwelding
        vertex_changes[vkey] = [[new_to_old[key] for key in part] for part in connected_components(adjacency)]

    for vkey, changes in vertex_changes.items():
        # for each disconnected part replace the vertex by a new vertex in the
        # faces of the part
        for change in changes:
            mesh_substitute_vertex_in_faces(mesh, vkey, mesh.add_vertex(attr_dict=mesh.vertex[vkey]), change)

        # delete old vertices
        mesh.delete_vertex(vkey)
