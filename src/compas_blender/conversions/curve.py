# from mathutils.geometry import interpolate_bezier

# from compas.geometry import add_vectors
from ._geometry import BlenderGeometry


class BlenderCurve(BlenderGeometry):
    """Wrapper for Blender curves.

    Examples
    --------
    .. code-block:: python

        pass
    """

    @property
    def geometry(self):
        """:blender:`bpy.types.Curve` - The curve geometry data block."""
        return self._geometry

    @geometry.setter
    def geometry(self, datablock):
        self._object = None
        self._geometry = datablock

    def to_compas(self):
        """Convert the curve to a COMPAS curve.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoNurbsCurve`
        """
        from compas.geometry import NurbsCurve

        curve = NurbsCurve()
        curve.rhino_curve = self.geometry
        return curve

    # def control_points(self):
    #     return self.geometry.splines[0].bezier_points

    # def control_point_coordinates(self):
    #     points = self.control_points()
    #     middle = [list(i.co) for i in points]
    #     left = [list(i.handle_left) for i in points]
    #     right = [list(i.handle_right) for i in points]
    #     return middle, left, right

    # def divide(self, number_of_segments):
    #     m, l, r = self.control_point_coordinates()
    #     points = [list(i) for i in interpolate_bezier(m[0], r[0], l[1], m[1], number_of_segments + 1)]
    #     return [add_vectors(self.location, point) for point in points]
