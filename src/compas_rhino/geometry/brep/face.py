from compas.data import Data
from compas_rhino.geometry import RhinoNurbsSurface

from .loop import RhinoBRepLoop


class RhinoBRepFace(Data):

    TOLERANCE = 1e-6

    def __init__(self, rhino_face=None):
        super(RhinoBRepFace, self).__init__()
        self.loops = None
        self.surface = None
        if rhino_face:
            self.rhino_face = rhino_face

    @property
    def rhino_face(self):
        return self._rhino_face

    @rhino_face.setter
    def rhino_face(self, value):
        self._rhino_face = value
        self.loops = [RhinoBRepLoop(l) for l in self._rhino_face.Brep.Loops]
        self.surface = RhinoNurbsSurface.from_rhino(self._rhino_face.ToNurbsSurface())

    @property
    def data(self):
        boundary = self.loops[0].data
        holes = None
        if len(self.loops) > 1:
            holes = [loop.data for loop in self.loops[1:]]
        return {"boundary": boundary, "surface": self.surface, "holes": holes}

    @data.setter
    def data(self, value):
        boundary = RhinoBRepLoop.from_data(value["boundary"])
        holes = [RhinoBRepLoop.from_data(l) for l in value["holes"]]
        self.loops = boundary + holes
        self.surface = RhinoNurbsSurface.from_data(value["surface"])
