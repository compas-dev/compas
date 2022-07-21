from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Brep
from compas_rhino.conversions import box_to_rhino
from compas_rhino.conversions import point_to_rhino
from compas_rhino.geometry import RhinoNurbsSurface

import Rhino

from .face import RhinoBrepFace
from .edge import RhinoBrepEdge
from .vertex import RhinoBrepVertex
from .loop import RhinoBrepLoop


TOLERANCE = 1e-6


class RhinoBrep(Brep):
    """
    Rhino Brep backend class.
    Wraps around and allows serialization and de-serialization of a `Rhino.Geometry.Brep`
    """

    def __new__(cls, *args, **kwargs):
        # This breaks the endless recursion when calling `compas.geometry.Brep()` and allows
        # having Brep here as the parent class. Otherwise RhinoBrep() calls Brep.__new__()
        # which calls RhinoBrep() and so on...
        return object.__new__(cls, *args, **kwargs)

    def __init__(self, brep=None):
        super(RhinoBrep, self).__init__()
        self._brep = brep or Rhino.Geometry.Brep()

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_brep(cls, rhino_brep):
        brep = cls(rhino_brep)
        return brep

    @classmethod
    def from_box(cls, box):
        rhino_box = box_to_rhino(box)
        return cls.from_brep(rhino_box.ToBrep())

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def dtype(self):
        # this should make de-serialization backend-agnostic
        # The deserializing type is determined by plugin availability when de-serializing
        # regardless of the context available when serializing.
        return super(RhinoBrep, self).dtype

    @property
    def data(self):
        faces = []
        for face in self.faces:
            faces.append(face.data)
        return {"faces": faces}

    @data.setter
    def data(self, data):
        """
        https://github.com/mcneel/rhino-developer-samples/blob/3179a8386a64602ee670cc832c77c561d1b0944b/rhinocommon/cs/SampleCsCommands/SampleCsTrimmedPlane.cs

        Parameters
        ----------
        data

        Returns
        -------

        """
        faces = []
        for facedata in data["faces"]:
            face = RhinoBrepFace.from_data(facedata)
            faces.append(face)
        self._brep = self._create_rhino_brep(faces)

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def points(self):
        if self._brep:
            return [RhinoBrepVertex(v) for v in self._brep.Vertices]

    @property
    def edges(self):
        if self._brep:
            return [RhinoBrepEdge(e) for e in self._brep.Edges]

    @property
    def loops(self):
        if self._brep:
            return [RhinoBrepLoop(l) for l in self._brep.Loops]

    @property
    def faces(self):
        if self._brep:
            return [RhinoBrepFace(f) for f in self._brep.Faces]

    @property
    def frame(self):
        return Frame.worldXY()

    @property
    def area(self):
        if self._brep:
            return self._brep.GetArea()

    @property
    def volume(self):
        if self._brep:
            return self._brep.GetVolume()

    def _create_rhino_brep(self, faces):
        """
          Things need to be defined in a valid brep:
           1- Vertices
           2- 3D Curves (geometry)
           3- Edges (topology - reference curve geometry)
           4- Surface (geometry)
           5- Faces (topology - reference surface geometry)
           6- Loops (2D parameter space of faces)
           4- Trims and 2D curves (2D parameter space of edges)
        """
        brep = Rhino.Geometry.Brep()
        print("created empty brep: {}".format(brep))
        for face_index, face in enumerate(faces):
            print("reconstructing face with index {}".format(face_index))
            # create face geometry
            surface_index = brep.AddSurface(face.surface.rhino_surface)

            brep_face = brep.Faces.Add(surface_index)
            surface = brep.Surfaces.Item[surface_index]

            # create and add curves
            for loop in face.loops:

                brep_loop = brep.Loops.Add(Rhino.Geometry.BrepLoopType.Outer, brep_face)

                for edge in loop.edges:
                    # add vertuces
                    start_vertex = brep.Vertices.Add(point_to_rhino(edge.start_vertex.point), TOLERANCE)
                    end_vertex = brep.Vertices.Add(point_to_rhino(edge.end_vertex.point), TOLERANCE)

                    curve_3d = edge.to_curve()
                    curve_index = brep.AddEdgeCurve(curve_3d)
                    # create edges
                    brep_edge = brep.Edges.Add(start_vertex, end_vertex, curve_index, TOLERANCE)
                    curve_2d = surface.Pullback(curve_3d, TOLERANCE)
                    curve_2d.Reverse()
                    # curve_2d_index = brep.Curves2D.Add(curve_2d)
                    trim_curve_index = brep.AddTrimCurve(curve_2d)
                    print("added 2d curve with index:{}".format(trim_curve_index))
                    # trim = brep.Trims.Add(False, brep_edge, trim_curve_index)
                    trim = brep.Trims.Add(brep_edge, True, brep_loop, trim_curve_index)
                    trim.IsoStatus = Rhino.Geometry.IsoStatus.None
                    trim.TrimType = Rhino.Geometry.BrepTrimType.Boundary
                    trim.SetTolerances(TOLERANCE, TOLERANCE)
                    trim.SetTolerances(TOLERANCE, TOLERANCE)

                    print("added trim with index:{} with geometry index:{}".format(trim.TrimIndex, trim_curve_index))
                    # trim_index = trim.TrimIndex

                    try:
                        pass
                        # brep_loop.Trims.Add(trim_curve_index)
                    except Exception as ex:
                        print("failed adding trim with curve index:{}".format(trim_curve_index))
                        print("exception is:{}".format(str(ex)))
                brep.Repair(TOLERANCE)

        # if not brep.Repair(TOLERANCE):
        #     raise Exception("Unable to fix Brep!")
        #
        # if not brep.IsValid:
        #     raise Exception("Brep invalid!")
        # create faces
        # check if valid
        # TODO re-construct the Brep from the serialized faces
        return brep


