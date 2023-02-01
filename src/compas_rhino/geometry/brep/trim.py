from compas.geometry import BrepTrim
from compas_rhino.geometry import RhinoNurbsCurve


import Rhino


class RhinoBrepTrim(BrepTrim):
    """An interface for a Brep Trim

    Attributes
    ----------
    curve : :class:`~compas.geometry.NurbsCurve`, read_only
        Returns the geometry for this trim as a 2d curve.
    iso_status : literal(NONE|X|Y|West|South|East|North)
        The isoparametric curve direction on the surface.
    is_reversed : bool
        True if this trim is reversed from its associated edge curve and False otherwise.

    """

    def __init__(self, rhino_trim=None, builder=None):

        super(RhinoBrepTrim, self).__init__()
        self._builder = builder
        self._trim = None
        self._curve = None
        self._is_reversed = None
        self._iso_type = None
        if rhino_trim:
            self._set_trim(rhino_trim)

    def _set_trim(self, rhino_trim):
        self._trim = rhino_trim
        self._curve = RhinoNurbsCurve.from_rhino(rhino_trim.TrimCurve.ToNurbsCurve())
        self._is_reversed = rhino_trim.IsReversed()
        self._iso_type = int(rhino_trim.IsoStatus)

    @property
    def data(self):
        return {
            "vertex": self._trim.StartVertex.VertexIndex,
            "edge": self._trim.Edge.EdgeIndex if self._trim.Edge else -1,  # singular trims have no associated edge
            "curve": RhinoNurbsCurve.from_rhino(self._trim.TrimCurve.ToNurbsCurve()).data,
            "iso": str(self._trim.IsoStatus),
            "is_reversed": "true" if self._trim.IsReversed() else "false",
        }

    @data.setter
    def data(self, value):
        curve = RhinoNurbsCurve.from_data(value["curve"]).rhino_curve
        iso_status = getattr(Rhino.Geometry.IsoStatus, value["iso"])
        is_reversed = True if value["is_reversed"] == "true" else False
        trim = self._builder.add_trim(curve, value["edge"], is_reversed, iso_status, value["vertex"])
        self._set_trim(trim)

    @classmethod
    def from_data(cls, data, builder):
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data : dict
            The data dictionary.
        builder : :class:`~compas_rhino.geometry.BrepLoopBuilder`
            The object reconstructing the current BrepLoop.

        Returns
        -------
        :class:`~compas.data.Data`
            An instance of this object type if the data contained in the dict has the correct schema.

        """
        obj = cls(builder=builder)
        obj.data = data
        return obj

    @property
    def curve(self):
        return self._curve

    @property
    def is_reverse(self):
        return self._curve

    @property
    def iso_status(self):
        return self._iso_type
