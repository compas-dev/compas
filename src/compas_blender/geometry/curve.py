from compas.cad import CurveGeometryInterface
from compas_blender.utilities import select_curve


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['BlenderCurve']


class BlenderCurve(CurveGeometryInterface):
    """"""

    def __init__(self, object):
        self.guid = object.name
        self.curve = object
        self.geometry = None
        self.attributes = {}
        self.type = self.curve.type

    @classmethod
    def from_selection(cls):
        object = select_curve()
        return cls(object)

    @property
    def xyz(self):
        return list(self.curve.location)

    def hide(self):
        self.curve.hide = True

    def show(self):
        self.curve.hide = False

    def select(self):
        self.curve.select = True

    def unselect(self):
        self.curve.select = False

    def is_line(self):
        pass

    def is_polyline(self):
        pass

    def space(self, density):
        raise NotImplementedError

    def heightfield(self, density):
        raise NotImplementedError

    def curvature(self):
        raise NotImplementedError

    def tangents(self, points):
        raise NotImplementedError

    def descent(self, points):
        raise NotImplementedError

    def divide(self, number_of_segments, over_space=False):
        raise NotImplementedError

    def divide_length(self, length_of_segments):
        raise NotImplementedError

    def closest_point(self, point, maxdist=None):
        raise NotImplementedError

    def closest_points(self, points, maxdist=None):
        raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    curve = BlenderCurve.from_selection()

    print(curve.guid)
    print(curve.curve)
    print(curve.geometry)
    print(curve.attributes)
    print(curve.type)
    curve.unselect()












# from compas_blender.utilities.layers import layer_mask

# try:
#     import bpy
#     from mathutils.geometry import interpolate_bezier
# except ImportError:
#     pass


# __author__     = ['Andrew Liew <liew@arch.ethz.ch>']
# __copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
# __license__    = 'MIT License'
# __email__      = 'liew@arch.ethz.ch'


# __all__ = [
#     'bezier_curve_interpolate',
#     'bezier_curve_points',
#     'curve_to_bmesh',
#     'curve_geometry'
# ]



# def bezier_curve_interpolate(curve, number=3):
#     """Interpolate points along a Bezier curve object.

#     Parameters:
#         curve (obj): Bezier curve object.
#         number (int): Number of interpolation points.

#     Returns:
#         list: Interpolated points [x, y, z.]
#     """
#     co, left, right = bezier_curve_points(curve)
#     vectors = interpolate_bezier(co[0], right[0], left[1], co[1], number)
#     points = [list(point) for point in vectors]
#     return points


# def bezier_curve_points(curve):
#     """Return a Bezier curve's control points.

#     Parameters:
#         curve (obj): Bezier curve object.

#     Returns:
#         list: Control point locations.
#         list: Control point left handles.
#         list: Control point right handles.
#     """
#     points = curve.data.splines[0].bezier_points
#     co = [list(point.co) for point in points]
#     left = [list(point.handle_left) for point in points]
#     right = [list(point.handle_right) for point in points]
#     return co, left, right


# # ==============================================================================
# # General
# # ==============================================================================

# def curve_to_bmesh(curve, name, divisions=10, delete=False):
#     """Convert a Blender curve object into a bmesh of edges.

#     Parameters:
#         curve (obj): Curve object.
#         divisions (int): Number of divisions along curve length.
#         delete (bool): Delete original curve.

#     Returns:
#         obj: Resulting bmesh object.
#     """
#     curve.data.resolution_u = divisions
#     mesh = curve.to_mesh(bpy.context.scene, True, 'PREVIEW')
#     if delete:
#         bpy.ops.object.delete()
#     else:
#         curve.select = False
#     bmesh = bpy.data.objects.new(name, mesh)
#     bmesh.location = [0, 0, 0]
#     bpy.context.scene.objects.link(bmesh)
#     return bmesh


# def curve_geometry(curve, extrude=0, bevel=0, bevel_resolution=1, fill='HALF'):
#     """Alter the geometry of the Blender curve object.

#     Parameters:
#         curve (obj): Curve object.
#         extrude (float): Extrude depth along local z.
#         bevel (float): Bevel depth.
#         bevel_resolution (int): Number of sides for bevel face.
#         fill (str): 'HALF' or 'FULL' solid fill.

#     Returns:
#         None
#     """
#     curve.data.extrude = extrude
#     curve.data.bevel_depth = bevel
#     curve.data.bevel_resolution = bevel_resolution
#     curve.data.fill_mode = fill


# # ==============================================================================
# # Debugging
# # ==============================================================================

# if __name__ == "__main__":

#     curve = add_bezier_curve()
#     print(bezier_curve_points(curve))
#     print(bezier_curve_interpolate(curve, number=4))
#     curve_to_bmesh(curve, name='bmesh', divisions=20)
