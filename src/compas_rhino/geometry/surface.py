from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.datastructures import Mesh
from compas_rhino.geometry._geometry import RhinoGeometry
# from compas.geometry import subtract_vectors
# from compas.geometry import angle_vectors
# from compas.geometry import distance_point_point
from compas.utilities import geometric_key


__all__ = ['RhinoSurface']


class RhinoSurface(RhinoGeometry):
    """"""

    __module__ = 'compas_rhino.geometry'

    def __init__(self):
        super(RhinoSurface, self).__init__()

    @classmethod
    def from_guid(cls, guid):
        obj = compas_rhino.find_object(guid)
        surf = cls()
        surf.guid = guid
        surf.object = obj
        surf.geometry = obj.Geometry
        return surf

    @classmethod
    def from_object(cls, obj):
        surf = cls()
        surf.guid = obj.Id
        surf.object = obj
        surf.geometry = obj.Geometry
        return surf

    @classmethod
    def from_selection(cls):
        guid = compas_rhino.select_surface()
        return cls.from_guid(guid)

    def to_compas(self):
        raise NotImplementedError

    def brep_to_compas(self, cls=None):
        if not self.geometry.HasBrepForm:
            return
        success, brep = self.geometry.TryConvertBrep()
        if not success:
            return

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
        cls = cls or Mesh
        return cls.from_vertices_and_faces(vertices, faces)

    # move to compas.datastructures.Mesh.from_meshgrid(RhinoSurface.to_meshgrid(over_space=True))?
    def uv_to_compas(self, cls=None, density=(10, 10)):
        return self.heightfield_to_compas(cls=cls, density=density, over_space=True)

    # move to compas.datastructures.Mesh.from_meshgrid(RhinoSurface.to_meshgrid(over_space=False))?
    def heightfield_to_compas(self, cls=None, density=(10, 10), over_space=False):
        try:
            u, v = density
        except Exception:
            u, v = density, density
        vertices = self.heightfield(density=(u, v), over_space=over_space)
        faces = []
        for i in range(u - 1):
            for j in range(v - 1):
                face = ((i + 0) * v + j,
                        (i + 0) * v + j + 1,
                        (i + 1) * v + j + 1,
                        (i + 1) * v + j)
                faces.append(face)
        cls = cls or Mesh
        return cls.from_vertices_and_faces(vertices, faces)

    # ==========================================================================
    #
    # ==========================================================================

    def space(self, density=10):
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

    # not taking the heighfield over the space is only possible
    # if the surface is in fact a height field
    # split up and rename!
    def heightfield(self, density=10, over_space=True):
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

    # def descent(self, points=None):
    #     """"""
    #     if not points:
    #         points = self.heightfield()

    #     tol = rs.UnitAbsoluteTolerance()

    #     descent = []

    #     if rs.IsPolysurface(self.guid):
    #         rs.EnableRedraw(False)
    #         faces = {}
    #         for p0 in points:
    #             p = p0[:]
    #             p[2] -= 2 * tol
    #             bcp = rs.BrepClosestPoint(self.guid, p)
    #             uv = bcp[1]
    #             index = bcp[2][1]
    #             try:
    #                 face = faces[index]
    #             except (TypeError, IndexError):
    #                 face = rs.ExtractSurface(self.guid, index, True)
    #                 faces[index] = face
    #             p1 = rs.EvaluateSurface(face, uv[0], uv[1])
    #             vector = [p1[_] - p0[_] for _ in range(3)]
    #             descent.append((p0, vector))
    #         rs.DeleteObjects(faces.values())
    #         rs.EnableRedraw(True)
    #     elif rs.IsSurface(self.guid):
    #         for p0 in points:
    #             p = p0[:]
    #             p[2] -= 2 * tol
    #             bcp = rs.BrepClosestPoint(self.guid, p)
    #             uv = bcp[1]
    #             p1 = rs.EvaluateSurface(self.guid, uv[0], uv[1])
    #             vector = [p1[_] - p0[_] for _ in range(3)]
    #             descent.append((p0, vector))
    #     else:
    #         raise Exception('Object is not a surface.')

    #     return descent

    # def curvature(self, points=None):
    #     """"""
    #     if not points:
    #         points = self.heightfield()

    #     curvature = []

    #     if rs.IsPolysurface(self.guid):
    #         rs.EnableRedraw(False)
    #         faces = {}
    #         for point in points:
    #             bcp = rs.BrepClosestPoint(self.guid, point)
    #             uv = bcp[1]
    #             index = bcp[2][1]
    #             try:
    #                 face = faces[index]
    #             except (TypeError, IndexError):
    #                 face = rs.ExtractSurface(self.guid, index, True)
    #                 faces[index] = face
    #             props = rs.SurfaceCurvature(face, uv)
    #             curvature.append((point, (props[1], props[3], props[5])))
    #         rs.DeleteObjects(faces.values())
    #         rs.EnableRedraw(False)
    #     elif rs.IsSurface(self.guid):
    #         for point in points:
    #             bcp = rs.BrepClosestPoint(self.guid, point)
    #             uv = bcp[1]
    #             props = rs.SurfaceCurvature(self.guid, uv)
    #             curvature.append((point, (props[1], props[3], props[5])))
    #     else:
    #         raise Exception('Object is not a surface.')

    #     return curvature

    # def borders(self, type=1):
    #     """Duplicate the borders of the surface.

    #     Parameters
    #     ----------
    #     type : {0, 1, 2}
    #         The type of border.

    #         * 0: All borders
    #         * 1: The exterior borders.
    #         * 2: The interior borders.

    #     Returns
    #     -------
    #     list
    #         The GUIDs of the extracted border curves.

    #     """
    #     border = rs.DuplicateSurfaceBorder(self.guid, type=type)
    #     curves = rs.ExplodeCurves(border, delete_input=True)
    #     return curves

    # def kinks(self, threshold=1e-3):
    #     """Return the XYZ coordinates of kinks, i.e. tangency discontinuities, along the surface's boundaries.

    #     Returns
    #     -------
    #     list
    #         The list of XYZ coordinates of surface boundary kinks.

    #     """
    #     kinks = []
    #     borders = self.borders(type=0)

    #     for border in borders:
    #         border = RhinoCurve(border)
    #         extremities = map(lambda x: rs.EvaluateCurve(border.guid, rs.CurveParameter(border.guid, x)), [0., 1.])

    #         if border.is_closed():
    #             start_tgt, end_tgt = border.tangents(extremities)
    #             if angle_vectors(start_tgt, end_tgt) > threshold:
    #                 kinks += extremities

    #         else:
    #             kinks += extremities

    #     return list(set(kinks))

    # def project_point(self, point, direction=(0, 0, 1)):
    #     projections = rs.ProjectPointToSurface(point, self.guid, direction)
    #     if not projections:
    #         return self.closest_point(point)
    #     return list(projections[0])

    # def project_points(self, points, direction=(0, 0, 1), include_none=True):
    #     projections = rs.ProjectPointToSurface(points, self.guid, direction)
    #     if not projections:
    #         return self.closest_points(points)
    #     projections[:] = [self.closest_point(point) if not point else point for point in projections]
    #     return map(list, projections)

    # def pull_point(self, point):
    #     pass

    # def pull_points(self, points):
    #     pass

    # def pull_curve(self, curve):
    #     pass

    # def pull_curves(self, curves):
    #     pass

    # def pull_mesh(self, mesh, fixed=None, d=1.0):
    #     if not fixed:
    #         fixed = []
    #     fixed = set(fixed)
    #     for key, attr in mesh.vertices(True):
    #         if key in fixed:
    #             continue
    #         xyz = mesh.vertex_coordinates(key)
    #         point = self.closest_point(xyz)
    #         dx, dy, dz = subtract_vectors(point, xyz)
    #         mesh.vertex[key]['x'] += d * dx
    #         mesh.vertex[key]['y'] += d * dy
    #         mesh.vertex[key]['z'] += d * dz

    # def pull_meshes(self, meshes):
    #     pass

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

        return compas_rhino.rs.EvaluateSurface(self.guid, * compas_rhino.rs.SurfaceClosestPoint(self.guid, xyz))

    def closest_points(self, points):
        return [self.closest_point(point) for point in points]

    # def closest_point_on_boundaries(self, xyz):
    #     """Return the XYZ coordinates of the closest point on the boundaries of the surface from input XYZ-coordinates.

    #     Parameters
    #     ----------
    #     xyz : list
    #         XYZ coordinates.

    #     Returns
    #     -------
    #     list
    #         The XYZ coordinates of the closest point on the boundaries of the surface.

    #     """
    #     borders = self.borders(type=0)
    #     proj_dist = {tuple(proj_xyz): distance_point_point(xyz, proj_xyz) for proj_xyz in [RhinoCurve(border).closest_point(xyz) for border in borders]}
    #     delete_objects(borders)
    #     return min(proj_dist, key=proj_dist.get)

    # def closest_points_on_boundaries(self, points):
    #     return [self.closest_point_on_boundaries(point) for point in points]

    # # --------------------------------------------------------------------------
    # # mapping
    # # --------------------------------------------------------------------------

    # def point_xyz_to_uv(self, xyz):
    #     """Return the UV point from the mapping of a XYZ point based on the UV parameterisation of the surface.

    #     Parameters
    #     ----------
    #     xyz : list
    #         (x, y, z) coordinates.

    #     Returns
    #     -------
    #     list
    #         The (u, v) coordinates of the mapped point.

    #     """
    #     return rs.SurfaceClosestPoint(self.guid, xyz)

    # def point_uv_to_xyz(self, uv):
    #     """Return the XYZ point from the inverse mapping of a UV point based on the UV parameterisation of the surface.

    #     Parameters
    #     ----------
    #     uv : list
    #         (u, v) coordinates.

    #     Returns
    #     -------
    #     list
    #         The (x, y, z) coordinates of the inverse-mapped point.

    #     """
    #     u, v = uv
    #     return tuple(rs.EvaluateSurface(self.guid, *uv))

    # def line_uv_to_xyz(self, line):
    #     """Return the XYZ points from the inverse mapping of a UV line based on the UV parameterisation of the surface.

    #     Parameters
    #     ----------
    #     uv : list
    #         List of (u, v) coordinates.

    #     Returns
    #     -------
    #     list
    #         The list of XYZ coordinates of the inverse-mapped line.

    #     """
    #     return (self.point_uv_to_xyz(line[0]), self.point_uv_to_xyz(line[1]))

    # def polyline_uv_to_xyz(self, polyline):
    #     """Return the XYZ points from the inverse mapping of a UV polyline based on the UV parameterisation of the surface.

    #     Parameters
    #     ----------
    #     uv : list
    #         List of (u, v) coordinates.

    #     Returns
    #     -------
    #     list
    #         The list of (x, y, z) coordinates of the inverse-mapped polyline.

    #     """
    #     return [self.point_uv_to_xyz(vertex) for vertex in polyline]

    # def mesh_uv_to_xyz(self, mesh):
    #     """Return the mesh from the inverse mapping of a UV mesh based on the UV parameterisation of the surface.
    #     The third coordinate of the mesh vertices is discarded.

    #     Parameters
    #     ----------
    #     mesh : Mesh
    #         A mesh.

    #     Returns
    #     -------
    #     mesh : Mesh
    #         The mesh once mapped back to the surface.

    #     """

    #     for vkey in mesh.vertices():
    #         x, y, z = self.point_uv_to_xyz(mesh.vertex_coordinates(vkey)[:2])
    #         mesh.vertex[vkey]['x'] = x
    #         mesh.vertex[vkey]['y'] = y
    #         mesh.vertex[vkey]['z'] = z
    #     return mesh


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    surface = RhinoSurface.from_selection()

    print(surface.guid)
    print(surface.object)
    print(surface.geometry)
    print(surface.type)
    print(surface.name)
