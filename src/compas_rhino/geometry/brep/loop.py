from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore

from compas.geometry import BrepLoop

from .edge import RhinoBrepEdge
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
    edges : list[:class:`compas_rhino.geometry.RhinoBrepEdge`], read-only
        The list of edges which comprise this loop.
    trims : list[:class:`compas_rhino.geometry.RhinoBrepTrim`], read-only
        The list of trims which comprise this loop.
    loop_type : :class:`compas_rhino.geometry.brep.loop.LoopType`, read-only
        The type of this loop.
    is_outer : bool, read-only
        True if this loop is an outer boundary, False otherwise.
    is_inner : bool, read-only
        True if this loop is an inner hole, False otherwise.
    native_loop : :class:`Rhino.Geometry.BrepLoop`
        The underlying Rhino BrepLoop object.

    """

    def __init__(self, rhino_loop=None):
        super(RhinoBrepLoop, self).__init__()
        self._loop = None
        self._type = LoopType.UNKNOWN
        self._trims = None
        self._type = None
        if rhino_loop:
            self.native_loop = rhino_loop

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def __data__(self):
        return {"type": str(self._loop.LoopType), "trims": [t.__data__ for t in self._trims]}

    @classmethod
    def __from_data__(cls, data, builder):
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data : dict
            The data dictionary.
        builder : :class:`compas_rhino.geometry.BrepFaceBuilder`
            The object reconstructing the current BrepFace.

        Returns
        -------
        :class:`compas.data.Data`
            An instance of this object type if the data contained in the dict has the correct schema.

        """
        instance = cls()
        instance._type = Rhino.Geometry.BrepLoopType.Outer if data["type"] == "Outer" else Rhino.Geometry.BrepLoopType.Inner
        loop_builder = builder.add_loop(instance._type)
        for trim_data in data["trims"]:
            RhinoBrepTrim.__from_data__(trim_data, loop_builder)
        instance.native_loop = loop_builder.result
        return instance

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def edges(self):
        return [RhinoBrepEdge(trim.Edge) for trim in self._loop.Trims]

    @property
    def trims(self):
        return self._trims

    @property
    def is_outer(self):
        return self._type == LoopType.OUTER

    @property
    def is_inner(self):
        return self._type == LoopType.INNTER

    @property
    def loop_type(self):
        return Rhino.Geometry.BrepLoopType(self._type)

    @property
    def native_loop(self):
        return self._loop

    @native_loop.setter
    def native_loop(self, rhino_loop):
        self._loop = rhino_loop
        self._type = int(self._loop.LoopType)
        self._trims = [RhinoBrepTrim(trim) for trim in self._loop.Trims]
