from compas.geometry import BrepLoop

import Rhino

from .edge import RhinoBrepEdge


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
    edges : list[:class:`~compas_rhino.geometry.RhinoBrepLoop`]
        The list of edges which comprise this loop.
    loop_type : :class:`~compas_rhino.geometry.brep.loop.LoopType`
        The type of this loop.
    is_outer : bool, read-only
        True if this loop is an outer boundary, False otherwise.
    is_inner : bool, read-only
        True if this loop is an inner hole, False otherwise.

    """

    def __init__(self, rhino_loop=None):
        super(RhinoBrepLoop, self).__init__()
        self._loop = None
        self._edges = None
        self._type = LoopType.UNKNOWN
        if rhino_loop:
            self._set_loop(rhino_loop)

    def _set_loop(self, native_loop):
        self._loop = native_loop
        self._type = int(self._loop.LoopType)
        self._edges = [RhinoBrepEdge(t.Edge) for t in self._loop.Trims]

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        return [e.data for e in self._edges]

    @data.setter
    def data(self, value):
        self._edges = [RhinoBrepEdge.from_data(e_data) for e_data in value]

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
