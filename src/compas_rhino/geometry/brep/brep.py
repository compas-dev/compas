from compas.geometry import Geometry
from compas_rhino.conversions import box_to_rhino


class RhinoBRep(Geometry):
    def __init__(self):
        self.rhino_brep = None

    @property
    def points(self):
        if self.rhino_brep:
            return [v for v in self.rhino_brep.Vertices]

    @property
    def edges(self):
        if self.rhino_brep:
            return [e for e in self.rhino_brep.Edges]

    @property
    def loops(self):
        if self.rhino_brep:
            return [l for l in self.rhino_brep.Loops]

    @property
    def faces(self):
        if self.rhino_brep:
            return [f for f in self.rhino_brep.Faces]

    @property
    def frame(self):
        """TODO: what to do here? Brep has no Frame/plane information"""
        # if self.rhino_brep:
        #     return self.rhino_brep.Frame
        pass

    @property
    def area(self):
        if self.rhino_brep:
            return self.rhino_brep.GetArea()

    @property
    def volume(self):
        if self.rhino_brep:
            return self.rhino_brep.GetVolume()

    @classmethod
    def from_shape(cls, shape):
        brep = cls()
        brep.rhino_brep = shape
        return brep

    @classmethod
    def from_box(cls, box):
        rhino_box = box_to_rhino(box)
        return cls.from_shape(rhino_box.ToBrep())





