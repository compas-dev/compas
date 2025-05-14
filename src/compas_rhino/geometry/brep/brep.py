from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino.objects
from compas.geometry import Brep
from compas.geometry import BrepError
from compas.geometry import BrepFilletError
from compas.geometry import BrepTrimmingError
from compas.geometry import Frame
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polyline
from compas.tolerance import TOL
from compas_rhino.conversions import box_to_rhino
from compas_rhino.conversions import curve_to_compas
from compas_rhino.conversions import curve_to_rhino
from compas_rhino.conversions import cylinder_to_rhino
from compas_rhino.conversions import mesh_to_compas
from compas_rhino.conversions import mesh_to_rhino
from compas_rhino.conversions import plane_to_rhino
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import polyline_to_rhino_curve
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import vector_to_rhino

from .builder import _RhinoBrepBuilder
from .edge import RhinoBrepEdge
from .face import RhinoBrepFace
from .loop import RhinoBrepLoop
from .vertex import RhinoBrepVertex


class RhinoBrep(Brep):
    """Rhino Brep backend class.

    Wraps around and allows serialization and de-serialization of a :class:`Rhino.Geometry.Brep`.

    Attributes
    ----------
    native_brep : :class:`Rhino.Geometry.Brep`
        The underlying Rhino Brep instance.
    vertices : list[:class:`compas_rhino.geometry.RhinoBrepVertex`], read-only
        The list of vertices which comprise this Brep.
    points : list[:class:`compas.geometry.Point`], read-only
        The list of vertex geometries as points in 3D space.
    edges : list[:class:`compas_rhino.geometry.RhinoBrepEdge`], read-only
        The list of edges which comprise this brep.
    trims : list[:class:`compas_rhino.geometry.RhinoBrepTrim`], read-only
        The list of trims which comprise this brep.
    loops : list[:class:`compas_rhino.geometry.RhinoBrepLoop`], read-only
        The list of loops which comprise this brep.
    faces : list[:class:`compas_rhino.geometry.RhinoBrepFace`], read-only
        The list of faces which comprise this brep.
    frame : :class:`compas.geometry.Frame`, read-only
        The brep's origin (Frame.worldXY()).
    area : float, read-only
        The calculated area of this brep.
    volume : float, read-only
        The calculated volume of this brep.

    """

    def __init__(self):
        super(RhinoBrep, self).__init__()
        self._brep = Rhino.Geometry.Brep()

    def __deepcopy__(self, *args, **kwargs):
        return self.copy()

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def __data__(self):
        return {
            "vertices": [v.__data__ for v in self.vertices],  # type: ignore
            "edges": [e.__data__ for e in self.edges],  # type: ignore
            "faces": [f.__data__ for f in self.faces],  # type: ignore
        }

    @classmethod
    def __from_data__(cls, data):
        """Construct a RhinoBrep from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        instance = cls()
        builder = _RhinoBrepBuilder()
        for v_data in data["vertices"]:
            RhinoBrepVertex.__from_data__(v_data, builder)
        for e_data in data["edges"]:
            RhinoBrepEdge.__from_data__(e_data, builder)
        for f_data in data["faces"]:
            RhinoBrepFace.__from_data__(f_data, builder)
        instance.native_brep = builder.result
        return instance

    def copy(self, cls=None):
        """Creates a deep-copy of this Brep using the native Rhino.Geometry.Brep copying mechanism.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        # Avoid reconstruction when just copying. for sake of efficiency and stability
        return RhinoBrep.from_native(self._brep.DuplicateBrep())

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def is_manifold(self):
        return self._brep.IsManifold

    @property
    def is_solid(self):
        return self._brep.IsSolid

    @property
    def native_brep(self):
        return self._brep

    @native_brep.setter
    def native_brep(self, rhino_brep):
        self._brep = rhino_brep

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
    def trims(self):
        if self._brep:
            return [RhinoBrepEdge(trim) for trim in self._brep.Trims]

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
    def from_boolean_difference(cls, breps_a, breps_b):
        """Construct a Brep from the boolean difference of two groups of Breps.

        Parameters
        ----------
        breps_a : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            One or more Breps from which to substract.
        breps_b : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            One or more Breps to substract.

        Returns
        -------
        list(:class:`compas_rhino.geometry.RhinoBrep`)
            list of one or more resulting Breps.

        """
        if not isinstance(breps_a, list):
            breps_a = [breps_a]
        if not isinstance(breps_b, list):
            breps_b = [breps_b]
        resulting_breps = Rhino.Geometry.Brep.CreateBooleanDifference(
            [b.native_brep for b in breps_a],
            [b.native_brep for b in breps_b],
            TOL.absolute,
        )
        return [RhinoBrep.from_native(brep) for brep in resulting_breps]

    @classmethod
    def from_boolean_union(cls, breps_a, breps_b):
        """Construct a Brep from the boolean union of two groups of Breps.

        Parameters
        ----------
        breps_a : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            One of more breps to join.
        breps_b : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            Another one of more breps to join.

        Returns
        -------
        list(:class:`compas_rhino.geometry.RhinoBrep`)
            list of one or more resulting Breps.

        """
        if not isinstance(breps_a, list):
            breps_a = [breps_a]
        if not isinstance(breps_b, list):
            breps_b = [breps_b]

        resulting_breps = Rhino.Geometry.Brep.CreateBooleanUnion([b.native_brep for b in breps_a + breps_b], TOL.absolute)
        return [RhinoBrep.from_native(brep) for brep in resulting_breps]

    @classmethod
    def from_boolean_intersection(cls, breps_a, breps_b):
        """Construct a Brep from the boolean intersection of two groups of Breps.

        Parameters
        ----------
        breps_a : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            One or more Breps to instrsect.
        breps_b : :class:`compas_rhino.geometry.RhinoBrep` or list(:class:`compas_rhino.geometry.RhinoBrep`)
            Another one or more Breps to intersect.

        Returns
        -------
        list(:class:`compas_rhino.geometry.RhinoBrep`)
            list of one or more resulting Breps.

        """
        if not isinstance(breps_a, list):
            breps_a = [breps_a]
        if not isinstance(breps_b, list):
            breps_b = [breps_b]
        resulting_breps = Rhino.Geometry.Brep.CreateBooleanIntersection(
            [b.native_brep for b in breps_a],
            [b.native_brep for b in breps_b],
            TOL.absolute,
        )
        return [RhinoBrep.from_native(brep) for brep in resulting_breps]

    @classmethod
    def from_box(cls, box):
        """Create a RhinoBrep from a box.

        Parameters
        ----------
        box : :class:`compas.geometry.Box`
            The box geometry of the brep.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        rhino_box = box_to_rhino(box)
        return cls.from_native(rhino_box.ToBrep())

    @classmethod
    def from_cylinder(cls, cylinder):
        """Create a RhinoBrep from a box.

        Parameters
        ----------
        box : :class:`compas.geometry.Box`
            The box geometry of the brep.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        rhino_cylinder = cylinder_to_rhino(cylinder)
        return cls.from_native(rhino_cylinder.ToBrep(True, True))

    @classmethod
    def from_curves(cls, curves):
        """Create a RhinoBreps from a list of planar face boundary curves.

        Parameters
        ----------
        curves : list of :class:`~compas.geometry.Curve` or :class:`~compas.geometry.Polyline`
            The planar curves that make up the face borders of brep faces.

        Returns
        -------
        list of :class:`~compas_rhino.geometry.RhinoBrep`

        """
        if not isinstance(curves, list):
            curves = [curves]
        faces = []
        for curve in curves:
            if isinstance(curve, Polyline):
                rhino_curve = polyline_to_rhino_curve(curve)
            else:
                rhino_curve = curve_to_rhino(curve)
            face = Rhino.Geometry.Brep.CreatePlanarBreps(rhino_curve, TOL.absolute)
            if face is None:
                raise BrepError("Failed to create face from curve: {} ".format(curve))
            if len(face) > 1:
                raise BrepError("Failed to create single face from curve: {} ".format(curve))
            faces.append(face[0])
        rhino_brep = Rhino.Geometry.Brep.JoinBreps(faces, TOL.absolute)
        if rhino_brep is None:
            raise BrepError("Failed to create Brep from faces: {} ".format(faces))
        return [cls.from_native(brep) for brep in rhino_brep]

    @classmethod
    def from_extrusion(cls, curve, vector, cap_ends=True):
        """Create a RhinoBrep from an extrusion.

        Parameters
        ----------
        curve : :class:`~compas.geometry.Curve` or :class:`~compas.geometry.Polyline`
            The curve to extrude.
        vector : :class:`~compas.geometry.Vector`
            The vector to extrude the curve along.
        cap_ends : bool, optional
            If True, the plannar ends of the extrusion will be capped, if possible.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoBrep`

        """
        if isinstance(curve, Polyline):
            rhino_curve = polyline_to_rhino_curve(curve)
        else:
            rhino_curve = curve_to_rhino(curve)
        extrusion = Rhino.Geometry.Surface.CreateExtrusion(rhino_curve, vector_to_rhino(vector))
        if extrusion is None:
            raise BrepError("Failed to create extrusion from curve: {} and vector: {}".format(curve, vector))
        rhino_brep = extrusion.ToBrep()
        if cap_ends:
            capped = rhino_brep.CapPlanarHoles(TOL.absolute)
            if capped:
                rhino_brep = capped
        return cls.from_native(rhino_brep)

    @classmethod
    def from_loft(cls, curves):
        """Construct a Brep by lofting a set of curves.

        Parameters
        ----------
        curves : list[:class:`compas.geometry.Curve`]

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        rhino_curves = [curve_to_rhino(curve) for curve in curves]
        start = Rhino.Geometry.Point3d.Unset
        end = Rhino.Geometry.Point3d.Unset
        loft_type = Rhino.Geometry.LoftType.Normal

        results = Rhino.Geometry.Brep.CreateFromLoft(rhino_curves, start, end, loft_type, closed=False)
        if not results:
            raise BrepTrimmingError("Loft operation ended with no result")
        result = results[0]

        return cls.from_native(result)

    @classmethod
    def from_mesh(cls, mesh):
        """Create a RhinoBrep from a mesh.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            The source mesh.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        rhino_mesh = mesh_to_rhino(mesh)
        return cls.from_native(Rhino.Geometry.Brep.CreateFromMesh(rhino_mesh, True))

    @classmethod
    def from_native(cls, rhino_brep):
        """Constructs a RhinoBrep from an instance of a Rhino.Geometry.Brep.

        Parameters
        ----------
        rhino_brep : :class:`Rhino.Geometry.Brep`
            The instance of Rhino brep to wrap.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        brep = cls()
        brep._brep = rhino_brep
        return brep

    @classmethod
    def from_sphere(cls, sphere):
        """Create a RhinoBrep from a sphere.

        Parameters
        ----------
        sphere : :class:`compas.geometry.Sphere`
            The source sphere.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        rhino_sphere = sphere_to_rhino(sphere)
        return cls.from_native(rhino_sphere.ToBrep())

    @classmethod
    def from_step(cls, filepath):
        """Construct a RhinoBrep from a STEP file.

        Parameters
        ----------
        filepath : str
            The path to the step file.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        rs.Command('_-Import "' + filepath + '" _Enter', False)
        guid = rs.LastCreatedObjects()[0]
        obj = compas_rhino.objects.find_object(guid)
        geometry = obj.Geometry.Duplicate()
        compas_rhino.objects.delete_object(guid)
        return cls.from_native(geometry)

    # ==============================================================================
    # Conversions
    # ==============================================================================

    # ==============================================================================
    # Methods
    # ==============================================================================

    def contains(self, object):
        """Check if the Brep contains a given geometric primitive.

        Only closed and manifold breps can be checked for containment.

        Parameters
        ----------
        object : :class:`~compas.geometry.Point`, :class:`~compas.geometry.Curve`, :class:`~compas.geometry.Surface`
            The object to check for containment.

        Raises
        ------
        BrepError
            If the Brep is not solid.

        Returns
        -------
        bool
            True if the object is contained in the Brep, False otherwise.

        """
        if not self.is_solid:
            raise BrepError("Cannot check for containment if brep is not manifold or is not closed")

        if isinstance(object, Point):
            return self._brep.IsPointInside(point_to_rhino(object), TOL.absolute, False)
        else:
            raise NotImplementedError

    def to_meshes(self, u=16, v=16):
        """Convert the faces of this Brep shape to meshes.

        Parameters
        ----------
        u : int, optional
            The number of mesh faces in the U direction of the underlying surface geometry of every face of the Brep.
        v : int, optional
            The number of mesh faces in the V direction of the underlying surface geometry of every face of the Brep.

        Returns
        -------
        list[:class:`~compas.datastructures.Mesh`]

        """
        rg_meshes = Rhino.Geometry.Mesh.CreateFromBrep(self._brep, Rhino.Geometry.MeshingParameters.Default)
        meshes = [mesh_to_compas(m) for m in rg_meshes]
        return meshes

    def transform(self, matrix):
        """Transform this Brep by given transformation matrix

        Parameters
        ----------
        matrix: :class:`compas.geometry.Transformation`
            The transformation matrix by which to transform this Brep.

        Returns
        -------
        None

        """
        self._brep.Transform(transformation_to_rhino(matrix))

    def trim(self, plane, tolerance=None):
        """Trim this brep by the given trimming plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Frame` or :class:`compas.geometry.Plane`
            The frame or plane to use when trimming. The discarded bit is in the direction of the frame's normal.
        tolerance : float, optional
            The precision to use for the trimming operation. Defaults to `TOL.absolute`.

        Notes
        -----
        Trimming operation may result in multiple results (breps). When trimming, only one is used.
        The used bit is the one on the opposite side of the cutting plane's normal.

        Returns
        -------
        None

        Raises
        ------
        BrepTrimmingError
            If the trimming operation ended with no result.

        See Also
        --------
        :meth:`compas_rhino.geometry.RhinoBrep.trimmed`

        """
        result = self.trimmed(plane, tolerance)
        self._brep = result.native_brep

    def trimmed(self, plane, tolerance=None):
        """Returns a trimmed copy of this brep by the given trimming plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Frame` or :class:`compas.geometry.Plane`
            The frame or plane to use when trimming. The discarded bit is in the direction of the plane's normal.
        tolerance : float, optional
            The precision to use for the trimming operation. Defaults to `TOL.absolute`.

        Notes
        -----
        Trimming operation may result in multiple results (breps). When trimming, only one is used.
        The used bit is the one on the opposite side of the cutting plane's normal.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoBrep`

        Raises
        ------
        BrepTrimmingError
            If the trimming operation ended with no result.

        See Also
        --------
        :meth:`compas_rhino.geometry.RhinoBrep.trim`

        """
        tolerance = tolerance or TOL.absolute
        if isinstance(plane, Frame):
            plane = Plane.from_frame(plane)
        results = self._brep.Trim(plane_to_rhino(plane), tolerance)
        if not results:
            raise BrepTrimmingError("Trim operation ended with no result")
        result = results[0]
        capped = result.CapPlanarHoles(tolerance)
        if capped:
            result = capped
        return RhinoBrep.from_native(result)

    def slice(self, plane):
        """Slice through the Brep with a plane.

        Parameters
        ----------
        plane : :class:`~compas.geometry.Plane` or :class:`~compas.geometry.Frame`
            The plane to slice through the brep.

        Returns
        -------
        list(:class:`~compas.geometry.Curve`)
            Zero or more curves which represent the intersection(s) between the brep and the plane.

        """
        if isinstance(plane, Frame):
            plane = Plane.from_frame(plane)
        curves = Rhino.Geometry.Brep.CreateContourCurves(self._brep, plane_to_rhino(plane))
        return [curve_to_compas(curve) for curve in curves]

    def split(self, cutter):
        """Splits a Brep into pieces using a Brep as a cutter.

        Parameters
        ----------
        cutter : :class:`compas_rhino.geometry.RhinoBrep`
            Another Brep to use as a cutter.

        Returns
        -------
        list(:class:`compas_rhino.geometry.RhinoBrep`)
            list of zero or more resulting Breps.

        """
        resulting_breps = self._brep.Split(cutter.native_brep, TOL.absolute)
        return [RhinoBrep.from_native(brep) for brep in resulting_breps]

    def fillet(self, radius, edges=None):
        """Fillet edges of the Brep.

        Parameters
        ----------
        radius : float
            The radius of the fillet.
        edges : list(:class:`compas_rhino.geometry.RhinoBrepEdge`)
            The edges to fillet.

        Raises
        -------
        BrepFilletingError
            If the fillet operation fails.

        """
        resulting_breps = self.filleted(radius, edges)
        self._brep = resulting_breps.native_brep

    def filleted(self, radius, edges=None):
        """Returns a filleted copy of the Brep.

        Parameters
        ----------
        radius : float
            The radius of the fillet.
        edges : list(:class:`compas_rhino.geometry.RhinoBrepEdge`)
            List of edges to exclude from the operation. When None all edges are included.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`
            The resulting Brep.

        Raises
        -------
        BrepFilletingError
            If the fillet operation fails.

        """
        all_edge_indices = set(edge.native_edge.EdgeIndex for edge in self.edges)  # type: ignore
        excluded_indices = set(edge.native_edge.EdgeIndex for edge in edges or [])

        edge_indices = all_edge_indices - excluded_indices
        radii = [radius] * len(edge_indices)
        blend = Rhino.Geometry.BlendType.Fillet
        rail = Rhino.Geometry.RailType.DistanceFromEdge

        resulting_breps = Rhino.Geometry.Brep.CreateFilletEdges(self._brep, edge_indices, radii, radii, blend, rail, TOL.absolute)
        if not resulting_breps:
            raise BrepFilletError("Fillet operation ended with no result")
        return RhinoBrep.from_native(resulting_breps[0])

    def flip(self):
        """Flip the orientation of all faces of the Brep.

        Returns
        -------
        None

        """
        self._brep.Flip()

    def cap_planar_holes(self, tolerance=None):
        """Cap all planar holes in the Brep.

        Parameters
        ----------
        tolerance : float, optional
            The precision to use for the operation. Defaults to `TOL.absolute`.

        Returns
        -------
        None

        Raises
        ------
        BrepError
            If the operation fails.

        """
        tolerance = tolerance or TOL.absolute
        result = self._brep.CapPlanarHoles(tolerance)
        if result:
            self._brep = result
        else:
            raise BrepError("Failed to cap planar holes")
