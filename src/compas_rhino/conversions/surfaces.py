from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.tolerance import TOL

from compas.geometry import Point
from compas.datastructures import Mesh
from compas.datastructures import meshes_join
from compas.utilities import memoize

from Rhino.Geometry import NurbsSurface as RhinoNurbsSurface  # type: ignore
from Rhino.Geometry import Brep as RhinoBrep  # type: ignore

from .exceptions import ConversionError
from .geometry import point_to_rhino
from .geometry import point_to_compas


# =============================================================================
# To Rhino
# =============================================================================


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
    return surface.rhino_surface


def data_to_rhino_surface(data):
    """Convert a COMPAS surface to a Rhino surface.

    Parameters
    ----------
    data: dict

    Returns
    -------
    :rhino:`Rhino.Geometry.NurbsSurface`

    """
    points = [[Point.from_data(point) for point in row] for row in data["points"]]

    nu = len(points[0])
    nv = len(points)

    nurbs = RhinoNurbsSurface.Create(3, False, data["u_degree"] + 1, data["v_degree"] + 1, nu, nv)
    for i in range(nu):
        for j in range(nv):
            nurbs.Points.SetPoint(i, j, point_to_rhino(points[j][i]))
            nurbs.Points.SetWeight(i, j, data["weights"][j][i])

    u_knotvector = []
    for knot, mult in zip(data["u_knots"], data["u_mults"]):
        for i in range(mult):
            u_knotvector.append(knot)

    for index, knot in enumerate(u_knotvector):
        nurbs.KnotsU.Item[index] = knot

    v_knotvector = []
    for knot, mult in zip(data["v_knots"], data["v_mults"]):
        for i in range(mult):
            v_knotvector.append(knot)

    for index, knot in enumerate(v_knotvector):
        nurbs.KnotsV.Item[index] = knot

    return nurbs


# =============================================================================
# To COMPAS
# =============================================================================


def surface_to_compas_data(surface):
    """Convert a Rhino surface to a COMPAS surface.

    Parameters
    ----------
    surface: :rhino:`Rhino.Geometry.Surface`

    Returns
    -------
    dict

    """
    surface = surface.ToNurbsSurface()

    points = []
    weights = []
    for j in range(surface.Points.VCount):
        _points = []
        _weights = []
        for i in range(surface.Points.UCount):
            point = surface.Points.GetPoint(i, j)
            weight = surface.Points.GetWeight(i, j)
            _points.append(point_to_compas(point))
            _weights.append(weight)
        points.append(_points)
        weights.append(_weights)

    u_knots = []
    u_mults = []
    for index in range(surface.KnotsU.Count):
        u_knots.append(surface.KnotsU.Item[index])
        u_mults.append(surface.KnotsU.KnotMultiplicity(index))

    v_knots = []
    v_mults = []
    for index in range(surface.KnotsV.Count):
        v_knots.append(surface.KnotsV.Item[index])
        v_mults.append(surface.KnotsV.KnotMultiplicity(index))

    u_degree = surface.OrderU - 1
    v_degree = surface.OrderV - 1

    is_u_periodic = False
    is_v_periodic = False

    return {
        "points": [[point.data for point in row] for row in points],
        "weights": weights,
        "u_knots": u_knots,
        "v_knots": v_knots,
        "u_mults": u_mults,
        "v_mults": v_mults,
        "u_degree": u_degree,
        "v_degree": v_degree,
        "is_u_periodic": is_u_periodic,
        "is_v_periodic": is_v_periodic,
    }


def surface_to_compas(surface):
    """Convert a Rhino surface to a COMPAS surface.

    Parameters
    ----------
    surface: :rhino:`Rhino.Geometry.Surface`

    Returns
    -------
    :class:`compas.geometry.Surface`

    """
    from compas_rhino.geometry import RhinoNurbsSurface

    brep = RhinoBrep.TryConvertBrep(surface)

    if brep.Surfaces.Count > 1:  # type: ignore
        raise ConversionError("Conversion of a BRep with multiple underlying surface is currently not supported.")

    return RhinoNurbsSurface.from_rhino(brep.Surfaces[0])


def surface_to_compas_mesh(surface, cls=None, facefilter=None, cleanup=False):
    """Convert the surface b-rep loops to a COMPAS mesh.

    Parameters
    ----------
    cls : :class:`compas.datastructures.Mesh`, optional
        The type of COMPAS mesh.
    facefilter : callable, optional
        A filter for selection which Brep faces to include.
        If provided, the filter should return True or False per face.
        A very simple filter that includes all faces is ``def facefilter(face): return True``.
        Default parameter value is None in which case all faces are included.
    cleanup : bool, optional
        Flag indicating to clean up the result.
        Cleaning up means to remove isolated faces and unused vertices.
        Default is False.

    Returns
    -------
    :class:`compas.datastructures.Mesh`
        The resulting mesh.

    Examples
    --------
    >>> import compas_rhino
    >>> from compas_rhino.geometry import RhinoSurface
    >>> from compas.scene import Scene

    >>> def facefilter(face):
    ...     success, w, h = face.GetSurfaceSize()
    ...     if success:
    ...         if w > 10 and h > 10:
    ...             return True
    ...     return False
    ...

    >>> guid = compas_rhino.select_surface()
    >>> surf = RhinoSurface.from_guid(guid)
    >>> mesh = surf.to_compas(facefilter=facefilter)

    >>> scene = Scene()
    >>> scene.add(mesh, layer="Blocks")
    >>> scene.redraw()

    """
    if not surface.HasBrepForm:
        return

    brep = RhinoBrep.TryConvertBrep(surface)

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
        segments = curve.Explode()
        a = segments[0].PointAtStart
        b = segments[0].PointAtEnd
        a_gkey = TOL.geometric_key(a)
        b_gkey = TOL.geometric_key(b)
        gkey_xyz[a_gkey] = a
        gkey_xyz[b_gkey] = b
        face = [a_gkey, b_gkey]
        for segment in segments[1:-1]:
            b = segment.PointAtEnd
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


def surface_to_compas_quadmesh(surface, nu, nv=None, weld=False, facefilter=None, cls=None):
    """Convert the surface to a COMPAS mesh.

    Parameters
    ----------
    nu: int
        The number of faces in the u direction.
    nv: int, optional
        The number of faces in the v direction.
        Default is the same as the u direction.
    weld: bool, optional
        Weld the vertices of the mesh.
        Default is False.
    facefilter: callable, optional
        A filter for selection which Brep faces to include.
        If provided, the filter should return True or False per face.
        A very simple filter that includes all faces is ``def facefilter(face): return True``.
        Default parameter value is None in which case all faces are included.
    cls: :class:`compas.geometry.Mesh`, optional
        The type of COMPAS mesh.

    Returns
    -------
    :class:`compas.geometry.Mesh`

    """
    nv = nv or nu
    cls = cls or Mesh

    if not surface.HasBrepForm:
        return

    brep = RhinoBrep.TryConvertBrep(surface)

    if facefilter and callable(facefilter):
        faces = [face for face in brep.Faces if facefilter(face)]
    else:
        faces = brep.Faces

    meshes = []
    for face in faces:
        domain_u = face.Domain(0)
        domain_v = face.Domain(1)
        du = (domain_u[1] - domain_u[0]) / (nu)
        dv = (domain_v[1] - domain_v[0]) / (nv)

        @memoize
        def point_at(i, j):
            return point_to_compas(face.PointAt(i, j))

        quads = []
        for i in range(nu):
            for j in range(nv):
                a = point_at(domain_u[0] + (i + 0) * du, domain_v[0] + (j + 0) * dv)
                b = point_at(domain_u[0] + (i + 1) * du, domain_v[0] + (j + 0) * dv)
                c = point_at(domain_u[0] + (i + 1) * du, domain_v[0] + (j + 1) * dv)
                d = point_at(domain_u[0] + (i + 0) * du, domain_v[0] + (j + 1) * dv)
                quads.append([a, b, c, d])

        meshes.append(cls.from_polygons(quads))

    return meshes_join(meshes, cls=cls)
