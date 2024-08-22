from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino.Geometry  # type: ignore  # noqa: F401
import scriptcontext as sc  # type: ignore

import compas
import compas.geometry  # noqa: F401
from compas.datastructures import Mesh
from compas.geometry import Brep
from compas.tolerance import TOL

from .exceptions import ConversionError
from .extrusions import extrusion_to_compas_box
from .geometry import point_to_compas
from .shapes import cone_to_compas
from .shapes import cylinder_to_compas
from .shapes import sphere_to_compas
from .surfaces import surface_to_compas

if not compas.IPY:
    from typing import Callable  # noqa: F401
    from typing import Type  # noqa: F401

# =============================================================================
# To Rhino
# =============================================================================


def brep_to_rhino(brep):
    # type: (Brep) -> Rhino.Geometry.Brep
    """Convert a COMPAS Brep to a Rhino Brep.

    Parameters
    ----------
    brep : :class:`compas.geometry.Brep`

    Returns
    -------
    :rhino:`Rhino.Geometry.Brep`

    """
    return brep.native_brep


# =============================================================================
# To COMPAS
# =============================================================================


def brep_to_compas(brep):
    # type: (Rhino.Geometry.Brep) -> Brep
    """Convert a Rhino Brep to a COMPAS Brep.

    Parameters
    ----------
    brep : :rhino:`Rhino.Geometry.Brep`

    Returns
    -------
    :class:`compas.geometry.Brep`

    """
    return Brep.from_native(brep)


# =============================================================================
# To COMPAS Shapes
# =============================================================================


def brep_to_compas_box(brep):
    # type: (Rhino.Geometry.Brep) -> compas.geometry.Box
    """Convert a Rhino brep to a COMPAS box.

    Parameters
    ----------
    brep : :rhino:`Rhino.Geometry.Brep`

    Returns
    -------
    :class:`compas.geometry.Box`

    """
    return extrusion_to_compas_box(brep.Geometry)


def brep_to_compas_cone(brep):
    # type: (Rhino.Geometry.Brep) -> compas.geometry.Cone
    """Convert a Rhino brep to a COMPAS cone.

    Parameters
    ----------
    brep : :rhino:`Rhino.Geometry.Brep`

    Returns
    -------
    :class:`compas.geometry.Cone`

    Raises
    ------
    ConversionError

    """
    if brep.Faces.Count > 2:
        raise ConversionError("Brep cannot be converted to a cone.")

    for face in brep.Faces:
        if face.IsCone():
            result, cone = face.TryGetCone()
            if result:
                return cone_to_compas(cone)

    raise ConversionError("Brep cannot be converted to a cone.")


def brep_to_compas_cylinder(brep, tol=None):
    # type: (Rhino.Geometry.Brep, float | None) -> compas.geometry.Cylinder
    """Convert a Rhino brep to a COMPAS cylinder.

    Parameters
    ----------
    brep : :rhino:`Rhino.Geometry.Brep`

    Returns
    -------
    :class:`compas.geometry.Cylinder`

    Raises
    ------
    ConversionError

    """
    tol = tol or sc.doc.ModelAbsoluteTolerance

    if brep.Faces.Count > 3:
        raise ConversionError("Brep cannot be converted to a cylinder.")

    for face in brep.Faces:
        # being too strict about what is considered a cylinder
        # results in cylinders created by Rhino itself
        # to not be recognized...
        if face.IsCylinder(tol):
            result, cylinder = face.TryGetFiniteCylinder(tol)
            if result:
                return cylinder_to_compas(cylinder)

    raise ConversionError("Brep cannot be converted to a cylinder.")


def brep_to_compas_sphere(brep):
    # type: (Rhino.Geometry.Brep) -> compas.geometry.Sphere
    """Convert a Rhino brep to a COMPAS sphere.

    Parameters
    ----------
    brep : :rhino:`Rhino.Geometry.Brep`

    Returns
    -------
    :class:`compas.geometry.Sphere`

    Raises
    ------
    ConversionError

    """
    if brep.Faces.Count != 1:
        raise ConversionError("Brep cannot be converted to a sphere.")

    face = brep.Faces.Item[0]
    if not face.IsSphere():
        raise ConversionError("Brep cannot be converted to a sphere.")

    result, sphere = face.TryGetSphere()
    if result:
        return sphere_to_compas(sphere)

    raise ConversionError("Brep cannot be converted to a sphere.")


# =============================================================================
# To COMPAS Surface
# =============================================================================


def brep_to_compas_surface(brep, tol=None):
    # type: (Rhino.Geometry.Brep, float | None) -> compas.geometry.NurbsSurface
    """Convert a Rhino brep to a COMPAS surface.

    Parameters
    ----------
    brep : :rhino:`Rhino.Geometry.Brep`

    Returns
    -------
    :class:`compas.geometry.NurbsSurface`

    Raises
    ------
    ConversionError

    """
    tol = tol or sc.doc.ModelAbsoluteTolerance

    if brep.Faces.Count != 1:
        raise ConversionError("Brep cannot be converted to a surface.")

    face = brep.Faces.Item[0]

    if not face.HasNurbsForm():
        raise ConversionError("Brep cannot be converted to a surface.")

    result, surface = face.ToNurbsSurface(tol)
    if result:
        return surface_to_compas(surface)

    raise ConversionError("Brep cannot be converted to a surface.")


# =============================================================================
# To COMPAS Mesh
# =============================================================================


def brep_to_compas_mesh(brep, facefilter=None, cleanup=False, cls=None):
    # type: (Rhino.Geometry.Brep, Callable | None, bool, Type[Mesh] | None) -> Mesh
    """Convert the face loops of a Rhino brep to a COMPAS mesh.

    Parameters
    ----------
    brep : :class:`Rhino.Geometry.Brep`
        A Rhino brep.
    facefilter : callable, optional
        A filter for selection which Brep faces to include.
        If provided, the filter should return True or False per face.
        A very simple filter that includes all faces is ``def facefilter(face): return True``.
        Default parameter value is None in which case all faces are included.
    cleanup : bool, optional
        Flag indicating to clean up the result.
        Cleaning up means to remove isolated faces and unused vertices.
        Default is False.
    cls : :class:`compas.datastructures.Mesh`, optional
        The type of COMPAS mesh.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        The resulting mesh.

    """
    if facefilter and callable(facefilter):
        brepfaces = [face for face in brep.Faces if facefilter(face)]
    else:
        brepfaces = brep.Faces

    # vertex maps and face lists
    gkey_xyz = {}
    faces = []
    for face in brepfaces:
        loop = face.OuterLoop
        curve = loop.To3dCurve()
        segments = list(curve.Explode())
        a = point_to_compas(segments[0].PointAtStart)
        b = point_to_compas(segments[0].PointAtEnd)
        a_gkey = TOL.geometric_key(a)
        b_gkey = TOL.geometric_key(b)
        gkey_xyz[a_gkey] = a
        gkey_xyz[b_gkey] = b
        face = [a_gkey, b_gkey]
        for segment in segments[1:-1]:
            b = point_to_compas(segment.PointAtEnd)
            b_gkey = TOL.geometric_key(b)
            face.append(b_gkey)
            gkey_xyz[b_gkey] = b
        faces.append(face)

    # vertices and faces
    gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz)}
    vertices = [list(xyz) for gkey, xyz in gkey_xyz.items()]
    faces = [[gkey_index[gkey] for gkey in face] for face in faces]

    # remove duplicates from vertexlist
    polygons = []
    for temp in faces:
        face = []
        for vertex in temp:
            if vertex not in face:
                face.append(vertex)
        polygons.append(face)

    # define mesh type
    cls = cls or Mesh
    # create mesh
    mesh = cls.from_vertices_and_faces(vertices, polygons)

    # remove isolated faces
    if cleanup:
        if mesh.number_of_faces() > 1:
            for face in list(mesh.faces()):
                if not mesh.face_neighbors(face):
                    mesh.delete_face(face)
        mesh.remove_unused_vertices()

    return mesh
