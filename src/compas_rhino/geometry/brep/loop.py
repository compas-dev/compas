from compas.data import Data

from .edge import RhinoBrepEdge


class RhinoBrepLoop(Data):
    def __init__(self, rhino_loop=None):
        super(RhinoBrepLoop, self).__init__()
        self._loop = None
        self.edges = None
        if rhino_loop:
            self._set_loop(rhino_loop)

    def _set_loop(self, native_loop):
        self._loop = native_loop
        self.edges = [RhinoBrepEdge(t.Edge) for t in self._loop.Trims]

    @property
    def data(self):
        return [e.data for e in self.edges]

    @data.setter
    def data(self, value):
        self.edges = [RhinoBrepEdge.from_data(e_data) for e_data in value]
