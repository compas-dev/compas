from compas.cad import SurfaceGeometryInterface
from compas.geometry import subtract_vectors
from builtins import range

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

    from Rhino.Geometry import Point3d

    find_object = sc.doc.Objects.Find

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['RhinoSurface', ]


class RhinoSurface(SurfaceGeometryInterface):
    """"""

    def __init__(self, guid=None):
        self.guid = guid
        self.surface = RhinoSurface.find(guid)
        self.geometry = self.surface.Geometry
        self.attributes = self.surface.Attributes
        self.otype = self.geometry.ObjectType

    @staticmethod
    def find(guid):
        return find_object(guid)

    def space(self, density=10):
        """"""
        try:
            du, dv = density
        except TypeError:
            du = density
            dv = density

        density_u = int(du)
        density_v = int(dv)

        uv = []

        rs.EnableRedraw(False)

        if rs.IsPolysurface(self.guid):
            faces = rs.ExplodePolysurfaces(self.guid)
        elif rs.IsSurface(self.guid):
            faces = [self.guid]
        else:
            raise Exception('Object is not a surface.')

        for face in faces:
            domain_u = rs.SurfaceDomain(face, 0)
            domain_v = rs.SurfaceDomain(face, 1)
            du = (domain_u[1] - domain_u[0]) / (density_u - 1)
            dv = (domain_v[1] - domain_v[0]) / (density_v - 1)

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
        """"""
        try:
            du, dv = density
        except TypeError:
            du = density
            dv = density

        du = int(du)
        dv = int(dv)

        xyz = []

        rs.EnableRedraw(False)

        if rs.IsPolysurface(self.guid):
            faces = rs.ExplodePolysurfaces(self.guid)
        elif rs.IsSurface(self.guid):
            faces = [self.guid]
        else:
            raise Exception('Object is not a surface.')

        if over_space:
            for guid in faces:
                face = RhinoSurface(guid)
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

    def borders(self):
        """"""
        border = rs.DuplicateSurfaceBorder(self.guid, type=1)
        curves = rs.ExplodeCurves(border, delete_input=True)
        return curves

    # def project_point(self, point, direction=(0, 0, 1)):
    #     ppoints = rs.ProjectPointToSurface(point, self.guid, direction)
    #     if not ppoints:
    #         raise Exception('Could not project point to surface.')
    #     ppoint = ppoints[0]

    # def project_points(self, points, direction=(0, 0, 1), include_none=True):
    #     projections = rs.ProjectPointToSurface(points, self.guid, direction)
    #     print projections
    #     return map(list, projections)
    #     # projections = []
    #     # for point in points:
    #     #     ppoints = rs.ProjectPointToSurface(point, self.guid, direction)
    #     #     if not ppoints:
    #     #         print ppoints
    #     #         raise Exception('Could not project point to surface.')
    #     #     ppoint = ppoints[0]
    #     #     projections.append(list(ppoint))
    #     # return projections

    def closest_point(self, point, maxdist=None):
        point = self.geometry.ClosestPoint(Point3d(*point))
        return list(point)

    def closest_points(self, points, maxdist=None):
        return [self.closest_point(point) for point in points]

    def pull_point(self, point):
        pass

    def pull_points(self, points):
        pass

    def pull_curve(self, curve):
        pass

    def pull_curves(self, curves):
        pass

    def pull_mesh(self, mesh, fixed=None, d=1.0):
        if not fixed:
            fixed = []
        fixed = set(fixed)
        for key, attr in mesh.vertices(True):
            if key in fixed:
                continue
            xyz = mesh.vertex_coordinates(key)
            point = self.closest_point(xyz)
            dx, dy, dz = subtract_vectors(point, xyz)
            mesh.vertex[key]['x'] += d * dx
            mesh.vertex[key]['y'] += d * dy
            mesh.vertex[key]['z'] += d * dz

    def pull_meshes(self, meshes):
        pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    import compas_rhino

    guid = compas_rhino.select_surface()

    surface = RhinoSurface(guid)

    points = []
    for xyz in surface.heightfield():
        points.append({
            'pos'   : xyz,
            'name'  : 'heightfield',
            'color' : (0, 255, 0),
        })

    compas_rhino.xdraw_points(points, layer='Layer 01', clear=True, redraw=True)
