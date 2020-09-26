from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino

from compas.datastructures import Mesh
from compas.geometry import angle_vectors
from compas.geometry import distance_point_point
from compas.utilities import geometric_key

from ._geometry import BaseRhinoGeometry


__all__ = ['RhinoSurface']


class RhinoSurface(BaseRhinoGeometry):
    """Wrapper for Rhino surface objects."""

    def __init__(self):
        super(RhinoSurface, self).__init__()

    @classmethod
    def from_geometry(cls):
        raise NotImplementedError

    @classmethod
    def from_selection(cls):
        guid = compas_rhino.select_surface()
        return cls.from_guid(guid)

    def to_compas(self, cls=None):
        """Convert the surface b-rep loops to a COMPAS mesh.

        Parameters
        ----------
        cls : :class:`compas.datastructures.Mesh`, optional
            The type of COMPAS mesh.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            The resulting mesh.

        """
        if not self.geometry.HasBrepForm:
            return
        brep = Rhino.Geometry.Brep.TryConvertBrep(self.geometry)
        gkey_xyz = {}
        faces = []
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
        polygons = []
        for temp in faces:
            face = []
            for vertex in temp:
                if vertex not in face:
                    face.append(vertex)
            polygons.append(face)
        cls = cls or Mesh
        return cls.from_vertices_and_faces(vertices, polygons)

    # def uv_to_compas(self, cls=None, density=(10, 10)):
    #     """Convert the surface UV space to a COMPAS mesh.

    #     Parameters
    #     ----------
    #     cls : :class:`compas.datastructures.Mesh`, optional
    #         The type of mesh.
    #     density : tuple of int, optional
    #         The density in the U and V directions.
    #         Default is ``u = 10`` and ``v = 10``.

    #     Returns
    #     -------
    #     :class:`compas.datastructures.Mesh`
    #         The COMPAS mesh.
    #     """
    #     return self.heightfield_to_compas(cls=cls, density=density, over_space=True)

    # def heightfield_to_compas(self, cls=None, density=(10, 10), over_space=False):
    #     """Convert a heightfiled of the surface to a COMPAS mesh.

    #     Parameters
    #     ----------
    #     cls : :class:`compas.datastructures.Mesh`, optional
    #         The type of mesh.
    #     density : tuple of int, optional
    #         The density in the two grid directions.
    #         Default is ``u = 10`` and ``v = 10``.
    #     over_space : bool, optional
    #         Construct teh grid over the surface UV space instead of the XY axes.
    #         Default is ``False``.

    #     Returns
    #     -------
    #     :class:`compas.datastructures.Mesh`
    #         The COMPAS mesh.
    #     """
    #     try:
    #         u, v = density
    #     except Exception:
    #         u, v = density, density
    #     vertices = self.heightfield(density=(u, v), over_space=over_space)
    #     faces = []
    #     for i in range(u - 1):
    #         for j in range(v - 1):
    #             face = [(i + 0) * v + j,
    #                     (i + 1) * v + j,
    #                     (i + 1) * v + j + 1,
    #                     (i + 0) * v + j + 1]
    #             faces.append(face)
    #     cls = cls or Mesh
    #     return cls.from_vertices_and_faces(vertices, faces)

    # ==========================================================================
    #
    # ==========================================================================

    def space(self, density=(10, 10)):
        """Construct a parameter grid overt the UV space of the surface.

        Parameters
        ----------
        density : tuple, optional
            The density in the U and V directions of the parameter space.
            Default is ``10`` in both directions.

        Returns
        -------
        list
            A list of UV parameter tuples.
        """
        rs = compas_rhino.rs
        rs.EnableRedraw(False)
        try:
            du, dv = density
        except TypeError:
            du = density
            dv = density
        density_u = int(du)
        density_v = int(dv)
        if rs.IsPolysurface(self.guid):
            faces = rs.ExplodePolysurfaces(self.guid)
        elif rs.IsSurface(self.guid):
            faces = [self.guid]
        else:
            raise Exception('Object is not a surface.')
        uv = []
        for face in faces:
            domain_u = rs.SurfaceDomain(face, 0)
            domain_v = rs.SurfaceDomain(face, 1)
            du = (domain_u[1] - domain_u[0]) / (density_u - 1)
            dv = (domain_v[1] - domain_v[0]) / (density_v - 1)
            # move to meshgrid function
            for i in range(density_u):
                for j in range(density_v):
                    uv.append((domain_u[0] + i * du, domain_v[0] + j * dv))
        if len(faces) > 1:
            rs.DeleteObjects(faces)
        rs.EnableRedraw(True)
        return uv

    def heightfield(self, density=(10, 10), over_space=True):
        """Construct a point grid over the surface.

        Parameters
        ----------
        density : tuple, optional
            The density in the U and V directions of the grid.
            Default is ``10`` in both directions.
        over_space : bool, optional
            Construct the grid over the UV space of the surface.
            Default is ``True``.

        Returns
        -------
        list
            List of grid points.

        """
        rs = compas_rhino.rs
        rs.EnableRedraw(False)
        try:
            du, dv = density
        except TypeError:
            du = density
            dv = density
        du = int(du)
        dv = int(dv)
        if rs.IsPolysurface(self.guid):
            faces = rs.ExplodePolysurfaces(self.guid)
        elif rs.IsSurface(self.guid):
            faces = [self.guid]
        else:
            raise Exception('Object is not a surface.')
        xyz = []
        if over_space:
            for guid in faces:
                face = RhinoSurface.from_guid(guid)
                uv = face.space(density)
                for u, v in uv:
                    xyz.append(list(rs.EvaluateSurface(face.guid, u, v)))
        else:
            for guid in faces:
                bbox = rs.BoundingBox(guid)
                xmin = bbox[0][0]
                xmax = bbox[1][0]
                ymin = bbox[0][1]
                ymax = bbox[3][1]
                xstep = 1.0 * (xmax - xmin) / (du - 1)
                ystep = 1.0 * (ymax - ymin) / (dv - 1)
                seeds = []
                for i in range(du):
                    for j in range(dv):
                        seed = xmin + i * xstep, ymin + j * ystep, 0
                        seeds.append(seed)
                points = map(list, rs.ProjectPointToSurface(seeds, guid, [0, 0, 1]))
                xyz += points
        if len(faces) > 1:
            rs.DeleteObjects(faces)
        rs.EnableRedraw(True)
        return xyz

    def descent(self, points=None):
        """"""
        rs = compas_rhino.rs
        if not points:
            points = self.heightfield()
        tol = rs.UnitAbsoluteTolerance()
        descent = []
        if rs.IsPolysurface(self.guid):
            rs.EnableRedraw(False)
            faces = {}
            for p0 in points:
                p = p0[:]
                p[2] -= 2 * tol
                bcp = rs.BrepClosestPoint(self.guid, p)
                uv = bcp[1]
                index = bcp[2][1]
                try:
                    face = faces[index]
                except (TypeError, IndexError):
                    face = rs.ExtractSurface(self.guid, index, True)
                    faces[index] = face
                p1 = rs.EvaluateSurface(face, uv[0], uv[1])
                vector = [p1[_] - p0[_] for _ in range(3)]
                descent.append((p0, vector))
            rs.DeleteObjects(faces.values())
            rs.EnableRedraw(True)
        elif rs.IsSurface(self.guid):
            for p0 in points:
                p = p0[:]
                p[2] -= 2 * tol
                bcp = rs.BrepClosestPoint(self.guid, p)
                uv = bcp[1]
                p1 = rs.EvaluateSurface(self.guid, uv[0], uv[1])
                vector = [p1[_] - p0[_] for _ in range(3)]
                descent.append((p0, vector))
        else:
            raise Exception('Object is not a surface.')
        return descent

    def curvature(self, points=None):
        """"""
        rs = compas_rhino.rs
        if not points:
            points = self.heightfield()
        curvature = []
        if rs.IsPolysurface(self.guid):
            rs.EnableRedraw(False)
            faces = {}
            for point in points:
                bcp = rs.BrepClosestPoint(self.guid, point)
                uv = bcp[1]
                index = bcp[2][1]
                try:
                    face = faces[index]
                except (TypeError, IndexError):
                    face = rs.ExtractSurface(self.guid, index, True)
                    faces[index] = face
                props = rs.SurfaceCurvature(face, uv)
                curvature.append((point, (props[1], props[3], props[5])))
            rs.DeleteObjects(faces.values())
            rs.EnableRedraw(False)
        elif rs.IsSurface(self.guid):
            for point in points:
                bcp = rs.BrepClosestPoint(self.guid, point)
                uv = bcp[1]
                props = rs.SurfaceCurvature(self.guid, uv)
                curvature.append((point, (props[1], props[3], props[5])))
        else:
            raise Exception('Object is not a surface.')
        return curvature

    def borders(self, border_type=1):
        """Duplicate the borders of the surface.

        Parameters
        ----------
        border_type : {0, 1, 2}
            The type of border.

            * 0: All borders
            * 1: The exterior borders.
            * 2: The interior borders.

        Returns
        -------
        list
            The GUIDs of the extracted border curves.
        """
        rs = compas_rhino.rs
        border = rs.DuplicateSurfaceBorder(self.guid, type=border_type)
        curves = rs.ExplodeCurves(border, delete_input=True)
        return curves

    def kinks(self, threshold=1e-3):
        """Return the XYZ coordinates of kinks, i.e. tangency discontinuities, along the surface's boundaries.

        Returns
        -------
        list
            The list of XYZ coordinates of surface boundary kinks.
        """
        from .curve import RhinoCurve
        rs = compas_rhino.rs
        kinks = []
        borders = self.borders(border_type=0)
        for border in borders:
            border = RhinoCurve(border)
            extremities = map(lambda x: rs.EvaluateCurve(border.guid, rs.CurveParameter(border.guid, x)), [0., 1.])
            if border.is_closed():
                start_tgt, end_tgt = border.tangents(extremities)
                if angle_vectors(start_tgt, end_tgt) > threshold:
                    kinks += extremities
            else:
                kinks += extremities
        return list(set(kinks))

    def closest_point(self, xyz):
        """Return the XYZ coordinates of the closest point on the surface from input XYZ-coordinates.

        Parameters
        ----------
        xyz : list
            XYZ coordinates.

        Returns
        -------
        list
            The XYZ coordinates of the closest point on the surface.

        """
        rs = compas_rhino.rs
        return rs.EvaluateSurface(self.guid, * rs.SurfaceClosestPoint(self.guid, xyz))

    def closest_points(self, points):
        return [self.closest_point(point) for point in points]

    def closest_point_on_boundaries(self, xyz):
        """Return the XYZ coordinates of the closest point on the boundaries of the surface from input XYZ-coordinates.

        Parameters
        ----------
        xyz : list
            XYZ coordinates.

        Returns
        -------
        list
            The XYZ coordinates of the closest point on the boundaries of the surface.

        """
        from .curve import RhinoCurve
        borders = self.borders(type=0)
        proj_dist = {tuple(proj_xyz): distance_point_point(xyz, proj_xyz) for proj_xyz in [RhinoCurve(border).closest_point(xyz) for border in borders]}
        compas_rhino.delete_objects(borders)
        return min(proj_dist, key=proj_dist.get)

    def closest_points_on_boundaries(self, points):
        return [self.closest_point_on_boundaries(point) for point in points]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
