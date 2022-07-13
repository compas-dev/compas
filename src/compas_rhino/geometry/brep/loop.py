from compas.data import Data

from .edge import RhinoBRepEdge


class RhinoBRepLoop(Data):
    def __init__(self, rhino_loop=None):
        super(RhinoBRepLoop, self).__init__()
        self._rhino_loop = None
        if rhino_loop:
            self.rhino_loop = rhino_loop

    @property
    def rhino_loop(self):
        return self._rhino_loop

    @rhino_loop.setter
    def rhino_loop(self, value):
        self._rhino_loop = value
        self.edges = [RhinoBRepEdge(t.Edge) for t in self._rhino_loop.Trims]

    @property
    def data(self):
        return [e.data for e in self.edges]

    @data.setter
    def data(self, value):
        self.edges = [RhinoBRepEdge.from_data(e_data) for e_data in value]
