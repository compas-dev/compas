from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import scriptcontext as sc  # type: ignore

from .exceptions import ConversionError
from .shapes import cone_to_compas
from .shapes import cylinder_to_compas
from .shapes import sphere_to_compas

# =============================================================================
# To Rhino
# =============================================================================


def brep_to_rhino(brep):
    """Convert a COMPAS brep to a Rhino brep.

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
