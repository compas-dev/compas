from compas.data import Data
from compas_rhino.geometry import RhinoNurbsCurve


import Rhino


class RhinoBrepTrim(Data):
    def __init__(self, rhino_trim=None, builder=None):
        super(RhinoBrepTrim, self).__init__()
        self._builder = builder
        self._trim = None
        self._curve = None
        self._is_reversed = None
        if rhino_trim:
            self._set_trim(rhino_trim)

    def _set_trim(self, rhino_trim):
        self._trim = rhino_trim

    @property
    def data(self):
        return {
            "edge": self._trim.Edge.EdgeIndex,
            "curve": RhinoNurbsCurve.from_rhino(self._trim.TrimCurve.ToNurbsCurve()).data,
            "iso": str(self._trim.IsoStatus),
            "is_reversed": "true" if self._trim.IsReversed() else "false"
        }

    @data.setter
    def data(self, value):
        curve = RhinoNurbsCurve.from_data(value["curve"]).rhino_curve
        iso_status = getattr(Rhino.Geometry.IsoStatus, value["iso"])
        is_reversed = True if value["is_reversed"] == "true" else False
        trim = self._builder.add_trim(curve, value["edge"], is_reversed, iso_status)
        self._set_trim(trim)

    @classmethod
    def from_data(cls, data, builder):
        obj = cls(builder=builder)
        obj.data = data
        return obj
