from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Curve

# from compas.geometry import Plane

# from compas_rhino.conversions import point_to_rhino
# from compas_rhino.conversions import point_to_compas
# from compas_rhino.conversions import vector_to_compas
# from compas_rhino.conversions import xform_to_rhino
# from compas_rhino.conversions import plane_to_compas_frame
# from compas_rhino.conversions import plane_to_rhino
# from compas_rhino.conversions import box_to_compas


class BlenderCurve(Curve):
    """Class representing a general curve object.

    Parameters
    ----------
    name : str, optional
        Name of the curve.

    Attributes
    ----------
    dimension : int, read-only
        The spatial dimension of the curve.
    domain : tuple[float, float], read-only
        The parameter domain.
    start : :class:`~compas.geometry.Point`, read-only
        The point corresponding to the start of the parameter domain.
    end : :class:`~compas.geometry.Point`, read-only
        The point corresponding to the end of the parameter domain.
    is_closed : bool, read-only
        True if the curve is closed.
    is_periodic : bool, read-only
        True if the curve is periodic.

    Other Attributes
    ----------------
    native_curve : :rhino:`Curve`
        The underlying Rhino curve.

    """

    def __init__(self, name=None):
        super(BlenderCurve, self).__init__(name=name)
        self._native_curve = None

    # def __eq__(self, other):
    #     return self.native_curve.IsEqual(other.native_curve)  # type: ignore

    # ==============================================================================
    # Data
    # ==============================================================================

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def native_curve(self):
        return self._native_curve

    @native_curve.setter
    def native_curve(self, curve):
        self._native_curve = curve

    @property
    def splines(self):
        if self.native_curve:
            return self.native_curve.splines

    @property
    def dimension(self):
        if self.native_curve:
            return self.native_curve.splines[0].dimensions

    @property
    def domain(self):
        if self.native_curve:
            return 0, 1

    @property
    def start(self):
        if self.native_curve:
            return self.native_curve.splines[0].points[0].co

    @property
    def end(self):
        if self.native_curve:
            return self.native_curve.splines[0].points[-1].co

    @property
    def is_closed(self):
        if self.native_curve:
            pass

    @property
    def is_periodic(self):
        if self.native_curve:
            return self.native_curve.splines[0].use_cyclic_u

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_native(cls, native_curve):
        """Construct a curve from an existing Rhino curve.

        Parameters
        ----------
        native_curve : bpy.types.Curve

        Returns
        -------
        :class:`~compas_rhino.geometry.BlenderCurve`

        """
        curve = cls()
        curve.native_curve = native_curve
        return curve

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================

    # def copy(self):
    #     """Make an independent copy of the current curve.

    #     Returns
    #     -------
    #     :class:`~compas_rhino.geometry.RhinoCurve`

    #     """
    #     cls = type(self)
    #     curve = cls()
    #     curve.native_curve = self.native_curve.Duplicate()  # type: ignore
    #     return curve

    # def transform(self, T):
    #     """Transform this curve.

    #     Parameters
    #     ----------
    #     T : :class:`~compas.geometry.Transformation`
    #         A COMPAS transformation.

    #     Returns
    #     -------
    #     None

    #     """
    #     self.native_curve.Transform(xform_to_rhino(T))  # type: ignore

    # def reverse(self):
    #     """Reverse the parametrisation of the curve.

    #     Returns
    #     -------
    #     None

    #     """
    #     self.native_curve.Reverse()  # type: ignore

    # def point_at(self, t):
    #     """Compute a point on the curve.

    #     Parameters
    #     ----------
    #     t : float
    #         The value of the curve parameter. Must be between 0 and 1.

    #     Returns
    #     -------
    #     :class:`~compas.geometry.Point`
    #         the corresponding point on the curve.

    #     """
    #     point = self.native_curve.PointAt(t)  # type: ignore
    #     return point_to_compas(point)

    # def tangent_at(self, t):
    #     """Compute the tangent vector at a point on the curve.

    #     Parameters
    #     ----------
    #     t : float
    #         The value of the curve parameter. Must be between 0 and 1.

    #     Returns
    #     -------
    #     :class:`~compas.geometry.Vector`
    #         The corresponding tangent vector.

    #     """
    #     vector = self.native_curve.TangentAt(t)  # type: ignore
    #     return vector_to_compas(vector)

    # def curvature_at(self, t):
    #     """Compute the curvature at a point on the curve.

    #     Parameters
    #     ----------
    #     t : float
    #         The value of the curve parameter. Must be between 0 and 1.

    #     Returns
    #     -------
    #     :class:`~compas.geometry.Vector`
    #         The corresponding curvature vector.

    #     """
    #     vector = self.native_curve.CurvatureAt(t)  # type: ignore
    #     return vector_to_compas(vector)

    # def frame_at(self, t):
    #     """Compute the local frame at a point on the curve.

    #     Parameters
    #     ----------
    #     t : float
    #         The value of the curve parameter.

    #     Returns
    #     -------
    #     :class:`~compas.geometry.Frame`
    #         The corresponding local frame.

    #     """
    #     t, plane = self.native_curve.FrameAt(t)  # type: ignore
    #     return plane_to_compas_frame(plane)

    # def torsion_at(self, t):
    #     """Compute the torsion of the curve at a parameter.

    #     Parameters
    #     ----------
    #     t : float
    #         The value of the curve parameter.

    #     Returns
    #     -------
    #     float
    #         The torsion value.

    #     """
    #     return self.native_curve.TorsionAt(t)  # type: ignore

    # ==============================================================================
    # Methods continued
    # ==============================================================================
