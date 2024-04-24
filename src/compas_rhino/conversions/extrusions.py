from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore

from .shapes import box_to_compas
from .shapes import cylinder_to_compas
from .shapes import torus_to_compas

# =============================================================================
# To Rhino
# =============================================================================

# =============================================================================
# To COMPAS
# =============================================================================


def extrusion_to_compas_box(extrusion):
    """Convert a Rhino extrusion to a COMPAS box.

    Parameters
    ----------
    extrusion : :rhino:`Rhino.Geometry.Extrusion`

    Returns
    -------
    :class:`compas.geometry.Box`

    """
    plane = extrusion.GetPathPlane(0)
    bbox = extrusion.GetBoundingBox(plane)
    box = Rhino.Geometry.Box(plane, bbox)
    return box_to_compas(box)


def extrusion_to_compas_cylinder(extrusion, tol=None):
    """Convert a Rhino extrusion to a COMPAS cylinder.

    Parameters
    ----------
    extrusion : :rhino:`Rhino.Geometry.Extrusion`
    tol : float, optional
        The tolerance used to determine if the extrusion is a cylindrical surface.
        Default is the absolute tolerance of the current doc.

    Returns
    -------
    :class:`compas.geometry.Cylinder`

    """
    tol = tol or sc.doc.ModelAbsoluteTolerance
    if extrusion.IsCylinder(tol):
        result, cylinder = extrusion.TryGetFiniteCylinder(tol)
        if result:
            return cylinder_to_compas(cylinder)


def extrusion_to_compas_torus(extrusion, tol=None):
    """Convert a Rhino extrusion to a COMPAS torus.

    Parameters
    ----------
    extrusion : :rhino:`Rhino.Geometry.Extrusion`
    tol : float, optional
        The tolerance used to determine if the extrusion is a toroidal surface.
        Default is the absolute tolerance of the current doc.

    Returns
    -------
    :class:`compas.geometry.Torus`

    """
    tol = tol or sc.doc.ModelAbsoluteTolerance
    if extrusion.IsTorus(tol):
        result, torus = extrusion.TryGetTorus(tol)
        if result:
            return torus_to_compas(torus)
