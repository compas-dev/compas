from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from compas.datastructures import Mesh
from compas.geometry import Brep
from compas.tolerance import TOL

from .exceptions import ConversionError
from .geometry import point_to_compas
from .shapes import cone_to_compas
from .shapes import cylinder_to_compas
from .shapes import sphere_to_compas

# =============================================================================
# To Rhino
# =============================================================================


def brep_to_rhino(brep):
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
    """Convert a Rhino brep to a COMPAS box.

    Parameters
    ----------
    brep : :rhino:`Rhino.Geometry.Brep`

    Returns
    -------
    :class:`compas.geometry.Box`

    """
    raise NotImplementedError


def brep_to_compas_cone(brep):
    """Convert a Rhino brep to a COMPAS cone.

    Parameters
    ----------
    brep : :rhino:`Rhino.Geometry.Brep`

    Returns
    -------
    :class:`compas.geometry.Cone`

    """
    if brep.Faces.Count > 2:
        raise ConversionError("Object brep cannot be converted to a cone.")

    for face in brep.Faces:
        if face.IsCone():
            result, cone = face.TryGetCone()
            if result:
                return cone_to_compas(cone)


def brep_to_compas_cylinder(brep, tol=None):
    """Convert a Rhino brep to a COMPAS cylinder.

    Parameters
    ----------
    brep : :rhino:`Rhino.Geometry.Brep`

    Returns
    -------
    :class:`compas.geometry.Cylinder`

    """
    tol = tol or sc.doc.ModelAbsoluteTolerance

    if brep.Faces.Count > 3:
        raise ConversionError("Object brep cannot be converted to a cylinder.")

    for face in brep.Faces:
        # being too strict about what is considered a cylinder
        # results in cylinders created by Rhino itself
        # to not be recognized...
        if face.IsCylinder(tol):
            result, cylinder = face.TryGetFiniteCylinder(tol)
            if result:
                return cylinder_to_compas(cylinder)


def brep_to_compas_sphere(brep):
    """Convert a Rhino brep to a COMPAS sphere.

    Parameters
    ----------
    brep : :rhino:`Rhino.Geometry.Brep`

    Returns
    -------
    :class:`compas.geometry.Sphere`

    """
    if brep.Faces.Count != 1:
        raise ConversionError("Brep cannot be converted to a sphere.")

    face = brep.Faces.Item[0]
    if not face.IsSphere():
        raise ConversionError("Brep cannot be converted to a sphere.")

    result, sphere = face.TryGetSphere()
    if result:
        return sphere_to_compas(sphere)


# =============================================================================
# To COMPAS Mesh
# =============================================================================


def brep_to_compas_mesh(brep, facefilter=None, cleanup=False, cls=None):
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
