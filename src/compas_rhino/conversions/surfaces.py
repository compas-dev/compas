from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Mesh
from compas.geometry import NurbsSurface
from compas.geometry import Surface
from compas.utilities import memoize

from .geometry import point_to_compas


def surface_to_rhino(surface):
    """Convert a COMPAS surface to a Rhino surface.

    Parameters
    ----------
    surface : :class:`compas.geometry.Surface`
        A COMPAS surface.

    Returns
    -------
    Rhino.Geometry.Surface

    """
    return surface.native_surface


def surface_to_compas(surface, try_nurbs=True):
    """Convert a Rhino surface to a COMPAS surface.

    Parameters
    ----------
    surface: :rhino:`Rhino.Geometry.Surface`
        A Rhino surface geometry.
    try_nurbs : bool, optional
        Try to convert the surface to a NURBS surface.

    Returns
    -------
    :class:`compas.geometry.Surface` | :class:`compas.geometry.NurbsSurface`
        If `try_nurbs` is `True`, and the geometry of the object has a NURBS representation, return a NURBS surface.
        Otherwise return a general surface.

    """
    if try_nurbs and surface.HasNurbsForm():
        return NurbsSurface.from_native(surface.ToNurbsSurface())
    return Surface.from_native(surface)


# =============================================================================
# To Mesh
# =============================================================================


def surface_to_compas_mesh(surface, nu, nv=None, weld=False, cls=None):
    """Convert the surface to a COMPAS mesh.

    Parameters
    ----------
    surface: :class:`Rhino.Geometry.Surface`
        A Rhino surface.
    nu: int
        The number of faces in the u direction.
    nv: int, optional
        The number of faces in the v direction.
        Default is the same as the u direction.
    weld: bool, optional
        Weld the vertices of the mesh.
        Default is False.
    cls: :class:`compas.datastructures.Mesh`, optional
        The type of COMPAS mesh.

    Returns
    -------
    :class:`compas.datastructures.Mesh`

    """
    nv = nv or nu
    cls = cls or Mesh

    domain_u = surface.Domain(0)
    domain_v = surface.Domain(1)
    du = (domain_u[1] - domain_u[0]) / (nu)
    dv = (domain_v[1] - domain_v[0]) / (nv)

    @memoize
    def point_at(i, j):
        return point_to_compas(surface.PointAt(i, j))

    quads = []
    for i in range(nu):
        for j in range(nv):
            a = point_at(domain_u[0] + (i + 0) * du, domain_v[0] + (j + 0) * dv)
            b = point_at(domain_u[0] + (i + 1) * du, domain_v[0] + (j + 0) * dv)
            c = point_at(domain_u[0] + (i + 1) * du, domain_v[0] + (j + 1) * dv)
            d = point_at(domain_u[0] + (i + 0) * du, domain_v[0] + (j + 1) * dv)
            quads.append([a, b, c, d])

    return cls.from_polygons(quads)
