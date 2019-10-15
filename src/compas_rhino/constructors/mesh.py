from __future__ import print_function

import compas
import compas_rhino

from compas.utilities import geometric_key

from compas_rhino.geometry import RhinoSurface

try:
    import Rhino
    import scriptcontext as sc

except ImportError:
    compas.raise_if_ironpython()


__all__ = [
    'mesh_from_guid',
    'mesh_from_surface',
    'mesh_from_surface_uv',
    'mesh_from_surface_heightfield'
]


# ==============================================================================
# constructors
# ==============================================================================


def mesh_from_guid(cls, guid):
    """Construct a mesh from a Rhino mesh.

    Parameters
    ----------
    cls : Mesh
        A mesh type.
    guid : str
        The GUID of the Rhino mesh.

    Returns
    -------
    Mesh
        A mesh object.

    """
    vertices, faces = compas_rhino.get_mesh_vertices_and_faces(guid)
    faces = [face[:-1] if face[-2] == face[-1] else face for face in faces]
    mesh = cls.from_vertices_and_faces(vertices, faces)
    return mesh


def mesh_from_surface(cls, guid):
    """Construct a mesh from a Rhino surface.

    Parameters
    ----------
    cls : Mesh
        A mesh type.
    guid : str
        The GUID of the Rhino surface.

    Returns
    -------
    Mesh
        A mesh object.

    """
    gkey_xyz = {}
    faces = []
    obj = sc.doc.Objects.Find(guid)

    if not obj.Geometry.HasBrepForm:
        return

    brep = Rhino.Geometry.Brep.TryConvertBrep(obj.Geometry)

    for loop in brep.Loops:
        curve = loop.To3dCurve()
        segments = curve.Explode()
        face = []
        sp = segments[0].PointAtStart
        ep = segments[0].PointAtEnd
        sp_gkey = geometric_key(sp)
        ep_gkey = geometric_key(ep)
        gkey_xyz[sp_gkey] = sp
        gkey_xyz[ep_gkey] = ep
        face.append(sp_gkey)
        face.append(ep_gkey)

        for segment in segments[1:-1]:
            ep = segment.PointAtEnd
            ep_gkey = geometric_key(ep)
            face.append(ep_gkey)
            gkey_xyz[ep_gkey] = ep

        faces.append(face)

    gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz)}
    vertices = [list(xyz) for gkey, xyz in gkey_xyz.items()]
    faces = [[gkey_index[gkey] for gkey in f] for f in faces]
    mesh = cls.from_vertices_and_faces(vertices, faces)

    return mesh


def mesh_from_surface_uv(cls, guid, density=(10, 10)):
    """Construct a mesh from a point cloud aligned with the uv space of a Rhino NURBS surface.

    Parameters
    ----------
    cls : Mesh
        The mesh type.
    guid : str
        The GUID of the surface.
    density : tuple
        The density of the point grid in the u and v directions.

    Returns
    -------
    Mesh
        A mesh object.

    See Also
    --------
    * :class:`compas_rhino.geometry.RhinoSurface`

    Examples
    --------
    >>>

    """
    return mesh_from_surface_heightfield(cls, guid, density=density)


def mesh_from_surface_heightfield(cls, guid, density=(10, 10)):
    """Create a mesh data structure from a point grid aligned with the uv space of a Rhino NURBS surface.

    Parameters
    ----------
    cls : Mesh
        The mesh type.
    guid : str
        The GUID of the surface.
    density : tuple
        The density of the point grid in the u and v directions.

    Returns
    -------
    Mesh
        A mesh object.

    See Also
    --------
    * :class:`compas_rhino.geometry.RhinoSurface`

    Examples
    --------
    >>>

    """
    try:
        u, v = density
    except Exception:
        u, v = density, density

    surface = RhinoSurface(guid)

    mesh = cls()

    vertices = surface.heightfield(density=(u, v), over_space=True)

    for x, y, z in vertices:
        mesh.add_vertex(x=x, y=y, z=z)

    for i in range(u - 1):
        for j in range(v - 1):
            face = ((i + 0) * v + j,
                    (i + 0) * v + j + 1,
                    (i + 1) * v + j + 1,
                    (i + 1) * v + j)
            mesh.add_face(face)

    return mesh


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
