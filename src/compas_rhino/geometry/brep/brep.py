from compas.geometry import Frame
from compas.geometry import Brep
from compas.geometry import BrepInvalidError
from compas.geometry import BrepTrimmingError
from compas.geometry import Plane

from compas_rhino.conversions import box_to_rhino
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import xform_to_rhino
from compas_rhino.conversions import frame_to_rhino
from compas_rhino.conversions import cylinder_to_rhino

import Rhino

from .face import RhinoBrepFace
from .edge import RhinoBrepEdge
from .vertex import RhinoBrepVertex
from .loop import RhinoBrepLoop


TOLERANCE = 1e-6


class RhinoBrep(Brep):
    """Rhino Brep backend class.

    Wraps around and allows serialization and de-serialization of a :class:`Rhino.Geometry.Brep`.

    Attributes
    ----------
    native_brep : :class:`Rhino.Geometry.Brep`
        The underlying Rhino Brep instance.
    vertices : list[:class:`~compas_rhino.geometry.RhinoBrepVertex`], read-only
        The list of vertices which comprise this Brep.
    points : list[:class:`~compas.geometry.Point`], read-only
        The list of vertex geometries as points in 3D space.
    edges : list[:class:`~compas_rhino.geometry.RhinoBrepEdge`], read-only
        The list of edges which comprise this brep.
    loops : list[:class:`~compas_rhino.geometry.RhinoBrepLoop`], read-only
        The list of loops which comprise this brep.
    faces : list[:class:`~compas_rhino.geometry.RhinoBrepFace`], read-only
        The list of faces which comprise this brep.
    frame : :class:`~compas.geometry.Frame`, read-only
        The brep's origin (Frame.worldXY()).
    area : float, read-only
        The calculated area of this brep.
    volume : float, read-only
        The calculated volume of this brep.

    """

    # this makes de-serialization backend-agnostic.
    # The deserializing type is determined by plugin availability when de-serializing
    # regardless of the context available when serializing.
    __class__ = Brep

    def __new__(cls, *args, **kwargs):
        # This breaks the endless recursion when calling `compas.geometry.Brep()` and allows
        # having Brep here as the parent class. Otherwise RhinoBrep() calls Brep.__new__()
        # which calls RhinoBrep() and so on...
        return object.__new__(cls, *args, **kwargs)

    def __init__(self, brep=None):
        super(RhinoBrep, self).__init__()
        self._brep = brep or Rhino.Geometry.Brep()

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def data(self):
        faces = []
        for face in self.faces:
            faces.append(face.data)
        return {"faces": faces}

    @data.setter
    def data(self, data):
        faces = []
        for facedata in data["faces"]:
            face = RhinoBrepFace.from_data(facedata)
            faces.append(face)
        self._create_native_brep(faces)

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def native_brep(self):
        return self._brep

    @property
    def vertices(self):
        return self.points

    @property
    def points(self):
        if self._brep:
            return [RhinoBrepVertex(vertex) for vertex in self._brep.Vertices]

    @property
    def edges(self):
        if self._brep:
            return [RhinoBrepEdge(edge) for edge in self._brep.Edges]

    @property
    def loops(self):
        if self._brep:
            return [RhinoBrepLoop(loop) for loop in self._brep.Loops]

    @property
    def faces(self):
        if self._brep:
            return [RhinoBrepFace(face) for face in self._brep.Faces]

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

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_brep(cls, rhino_brep):
        """Constructs a RhinoBrep from an instance of a Rhino brep

        Parameters
        ----------
        rhino_brep : :class:`Rhino.Geometry.Brep`
            The instance of Rhino brep to wrap.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        brep = cls(rhino_brep)
        return brep

    @classmethod
    def from_box(cls, box):
        """Create a RhinoBrep from a box.

        Parameters
        ----------
        box : :class:`~compas.geometry.Box`
            The box geometry of the brep.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoBrep`

        """
        rhino_box = box_to_rhino(box)
        return cls.from_brep(rhino_box.ToBrep())

    @classmethod
    def from_cylinder(cls, cylinder):
        """Create a RhinoBrep from a box.

        Parameters
        ----------
        box : :class:`~compas.geometry.Box`
            The box geometry of the brep.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoBrep`

        """
        rhino_cylinder = cylinder_to_rhino(cylinder)
        return cls.from_brep(rhino_cylinder.ToBrep(True, True))

    # ==============================================================================
    # Methods
    # ==============================================================================

    def transform(self, matrix):
        """Transform this Brep by given transformation matrix

        Parameters
        ----------
        matrix: :class:`~compas.geometry.Transformation`
            The transformation matrix by which to transform this Brep.

        Returns
        -------
        None

        """
        self._brep.Transform(xform_to_rhino(matrix))

    def trim(self, trimming_plane, tolerance=TOLERANCE):
        """Trim this brep by the given trimming plane

        Parameters
        ----------
        trimming_plane : :class:`~compas.geometry.Frame` or :class:`~compas.geometry.Plane`
            The frame or plane to use when trimming.

        tolerance : float
            The precision to use for the trimming operation.

        Returns
        -------
        None

        """
        if isinstance(trimming_plane, Plane):
            trimming_plane = Frame.from_plane(trimming_plane)
        rhino_frame = frame_to_rhino(trimming_plane)
        rhino_frame.Flip()
        results = self._brep.Trim(rhino_frame, tolerance)
        if not results:
            raise BrepTrimmingError("Trim operation ended with no result")

        self._brep = results[0]

    @classmethod
    def from_boolean_difference(cls, breps_a, breps_b):
        """Construct a Brep from the boolean difference of two groups of Breps.

        Parameters
        ----------
        brep_a : :class:`~compas_rhino.geometry.RhinoBrep` or list(:class:`~compas_rhino.geometry.RhinoBrep`)
            One or more Breps from which to substract.
        brep_b : :class:`~compas_rhino.geometry.RhinoBrep` or list(:class:`~compas_rhino.geometry.RhinoBrep`)
            One or more Breps to substract.

        Returns
        -------
        list(:class:`~compas_rhino.geometry.RhinoBrep`)
            list of one or more resulting Breps.

        """
        if not isinstance(breps_a, list):
            breps_a = [breps_a]
        if not isinstance(breps_b, list):
            breps_b = [breps_b]
        resulting_breps = Rhino.Geometry.Brep.CreateBooleanDifference(
            [b.native_brep for b in breps_a],
            [b.native_brep for b in breps_b],
            TOLERANCE
        )
        return [RhinoBrep.from_brep(brep) for brep in resulting_breps]

    @classmethod
    def from_boolean_union(cls, breps_a, breps_b):
        """Construct a Brep from the boolean union of two groups of Breps.

        Parameters
        ----------
        breps_a : :class:`~compas_rhino.geometry.RhinoBrep` or list(:class:`~compas_rhino.geometry.RhinoBrep`)
            One of more breps to join.
        breps_b : :class:`~compas_rhino.geometry.RhinoBrep` or list(:class:`~compas_rhino.geometry.RhinoBrep`)
            Another one of more breps to join.

        Returns
        -------
        list(:class:`~compas_rhino.geometry.RhinoBrep`)
            list of one or more resulting Breps.

        """
        if not isinstance(breps_a, list):
            breps_a = [breps_a]
        if not isinstance(breps_b, list):
            breps_b = [breps_b]

        resulting_breps = Rhino.Geometry.Brep.CreateBooleanUnion([b.native_brep for b in breps_a + breps_b], TOLERANCE)
        return [RhinoBrep.from_brep(brep) for brep in resulting_breps]

    @classmethod
    def from_boolean_intersection(cls, breps_a, breps_b):
        """Construct a Brep from the boolean intersection of two groups of Breps.

        Parameters
        ----------
        brep_a : :class:`~compas_rhino.geometry.RhinoBrep` or list(:class:`~compas_rhino.geometry.RhinoBrep`)
            One or more Breps to instrsect.
        brep_b : :class:`~compas_rhino.geometry.RhinoBrep` or list(:class:`~compas_rhino.geometry.RhinoBrep`)
            Another one or more Breps to intersect.

        Returns
        -------
        list(:class:`~compas_rhino.geometry.RhinoBrep`)
            list of one or more resulting Breps.

        """
        if not isinstance(breps_a, list):
            breps_a = [breps_a]
        if not isinstance(breps_b, list):
            breps_b = [breps_b]
        resulting_breps = Rhino.Geometry.Brep.CreateBooleanIntersection(
            [b.native_brep for b in breps_a],
            [b.native_brep for b in breps_b],
            TOLERANCE
        )
        return [RhinoBrep.from_brep(brep) for brep in resulting_breps]

    # ==============================================================================
    # Other Methods
    # ==============================================================================

    def _create_native_brep(self, faces):
        # Source: https://github.com/mcneel/rhino-developer-samples/blob/3179a8386a64602ee670cc832c77c561d1b0944b/rhinocommon/cs/SampleCsCommands/SampleCsTrimmedPlane.cs
        # Things need to be defined in a valid brep:
        #  1- Vertices
        #  2- 3D Curves (geometry)
        #  3- Edges (topology - reference curve geometry)
        #  4- Surfaces (geometry)
        #  5- Faces (topology - reference surface geometry)
        #  6- Loops (2D parameter space of faces)
        #  4- Trims and 2D curves (2D parameter space of edges)
        self._brep = Rhino.Geometry.Brep()
        for face in faces:
            rhino_face, rhino_surface = self._create_brep_face(face)
            for loop in face.loops:
                rhino_loop = self._brep.Loops.Add(Rhino.Geometry.BrepLoopType.Outer, rhino_face)
                for edge in loop.edges:
                    start_vertex, end_vertex = self._add_edge_vertices(edge)
                    rhino_edge = self._add_edge(edge, start_vertex, end_vertex)
                    rhino_2d_curve = self._create_trim_curve(rhino_edge, rhino_surface)
                    self._add_trim(rhino_2d_curve, rhino_edge, rhino_loop)

        self._brep.Repair(TOLERANCE)
        self._brep.JoinNakedEdges(
            TOLERANCE
        )  # without this, Brep.Trim() led to some weird results on de-serialized Breps
        self._validate_brep()

    def _validate_brep(self):
        if self._brep.IsValid:
            return

        error_message = ""
        valid_topo, log_topo = self._brep.IsValidTopology()
        valid_tol, log_tol = self._brep.IsValidTolerancesAndFlags()
        valid_geo, log_geo = self._brep.IsValidGeometry()
        if not valid_geo:
            error_message += "Invalid geometry:\n{}\n".format(log_geo)
        if not valid_topo:
            error_message += "Invalid topology:\n{}\n".format(log_topo)
        if not valid_tol:
            error_message += "Invalid tolerances:\n{}\n".format(log_tol)

        raise BrepInvalidError(error_message)

    def _create_brep_face(self, face):
        # Geometry
        surface_index = self._brep.AddSurface(face.native_surface)
        brep_surface = self._brep.Surfaces.Item[surface_index]
        # Topology
        brep_face = self._brep.Faces.Add(surface_index)
        return brep_face, brep_surface

    def _add_edge_vertices(self, edge):
        start_vertex = self._brep.Vertices.Add(point_to_rhino(edge.start_vertex.point), TOLERANCE)
        end_vertex = self._brep.Vertices.Add(point_to_rhino(edge.end_vertex.point), TOLERANCE)
        return start_vertex, end_vertex

    def _add_edge(self, edge, start_vertex, end_vertex):
        # Geometry
        curve_index = self._brep.AddEdgeCurve(edge.curve)
        # Topology
        rhino_edge = self._brep.Edges.Add(start_vertex, end_vertex, curve_index, TOLERANCE)
        return rhino_edge

    def _add_trim(self, rhino_trim_curve, rhino_edge, rhino_loop):
        # Geometry
        trim_curve_index = self._brep.AddTrimCurve(rhino_trim_curve)
        # Topology
        trim = self._brep.Trims.Add(rhino_edge, True, rhino_loop, trim_curve_index)
        trim.IsoStatus = getattr(
            Rhino.Geometry.IsoStatus, "None"
        )  # IsoStatus.None makes lint, IDE and even Python angry
        trim.TrimType = Rhino.Geometry.BrepTrimType.Boundary
        trim.SetTolerances(TOLERANCE, TOLERANCE)

    @staticmethod
    def _create_trim_curve(rhino_edge, rhino_surface):
        curve_2d = rhino_surface.Pullback(rhino_edge.EdgeCurve, TOLERANCE)
        curve_2d.Reverse()
        return curve_2d
