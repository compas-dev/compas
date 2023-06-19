from compas.geometry import BrepLoop

import Rhino

from .trim import RhinoBrepTrim


class LoopType(object):
    """Represents the type of a brep loop.

    Attributes
    ----------
    UNKNOWN
    OUTER
    INNTER
    SLIT
    CURVE_ON_SURFACE
    POINT_ON_SURFACE

    """

    UNKNOWN = 0
    OUTER = 1
    INNTER = 2
    SLIT = 3
    CURVE_ON_SURFACE = 4
    POINT_ON_SURFACE = 5


class RhinoBrepLoop(BrepLoop):
    """A wrapper for Rhino.Geometry.BrepLoop

    Attributes
    ----------
    edges : list[:class:`~compas_rhino.geometry.RhinoBrepLoop`], read-only
        The list of edges which comprise this loop.
    loop_type : :class:`~compas_rhino.geometry.brep.loop.LoopType`, read-only
        The type of this loop.
    is_outer : bool, read-only
        True if this loop is an outer boundary, False otherwise.
    is_inner : bool, read-only
        True if this loop is an inner hole, False otherwise.

    """

    def __init__(self, rhino_loop=None, builder=None):
        super(RhinoBrepLoop, self).__init__()
        self._builder = builder
        self._loop = None
        self._type = LoopType.UNKNOWN
        self._trims = None
        if rhino_loop:
            self._set_loop(rhino_loop)

    def _set_loop(self, native_loop):
        self._loop = native_loop
        self._type = int(self._loop.LoopType)
        self._trims = [RhinoBrepTrim(trim) for trim in self._loop.Trims]

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        return {"type": str(self._loop.LoopType), "trims": [t.data for t in self._trims]}

    @data.setter
    def data(self, value):
        self._type = (
            Rhino.Geometry.BrepLoopType.Outer if value["type"] == "Outer" else Rhino.Geometry.BrepLoopType.Inner
        )
        loop_builder = self._builder.add_loop(self._type)
        for trim_data in value["trims"]:
            RhinoBrepTrim.from_data(trim_data, loop_builder)
        self._set_loop(loop_builder.result)

    @classmethod
    def from_data(cls, data, builder):
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data : dict
            The data dictionary.
        builder : :class:`~compas_rhino.geometry.BrepFaceBuilder`
            The object reconstructing the current BrepFace.

        Returns
        -------
        :class:`~compas.data.Data`
            An instance of this object type if the data contained in the dict has the correct schema.

        """
        obj = cls(builder=builder)
        obj.data = data
        return obj

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def edges(self):
        return self._edges

    @property
    def is_outer(self):
        return self._type == LoopType.OUTER

    @property
    def is_inner(self):
        return self._type == LoopType.INNTER

    @property
    def loop_type(self):
        return Rhino.Geometry.BrepLoopType(self._type)
