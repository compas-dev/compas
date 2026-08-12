from typing import TYPE_CHECKING
from typing import Iterable
from typing import Optional

from ..types import Face
from ..types import Vertex

if TYPE_CHECKING:
    from ..mesh import Mesh


def mesh_substitute_vertex_in_faces(
    mesh: "Mesh",
    old_vkey: Vertex,
    new_vkey: Vertex,
    fkeys: Optional[Iterable[Face]] = None,
) -> list[Face]:
    """Substitute in a mesh a vertex by another one.
    In all faces by default or in a given set of faces.

    Parameters
    ----------
    mesh
        The mesh data structure.
    old_vkey
        The old vertex key.
    new_vkey
        The new vertex key.
    fkeys
        Face keys in which to substitute the old vertex with the new one.
        Default is to substitute it in all faces.

    Returns
    -------
    list[int]
        The list of modified faces.

    """

    # apply to all faces if there is none chosen
    faces = list(mesh.faces()) if fkeys is None else list(fkeys)

    # substitute vertices
    for fkey in faces:
        face_vertices = [new_vkey if key == old_vkey else key for key in mesh.face_vertices(fkey)]
        mesh.delete_face(fkey)
        mesh.add_face(face_vertices, fkey)

    return faces
