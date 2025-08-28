from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import rhinoscriptsyntax as rs  # type: ignore

import compas_rhino.objects
from compas.datastructures import Mesh
from compas.geometry import Brep
from compas.geometry import BrepError
from compas.geometry import BrepFilletError
from compas.geometry import BrepTrimmingError
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polyline
from compas.tolerance import TOL
from compas_rhino.conversions import box_to_rhino
from compas_rhino.conversions import cone_to_rhino
from compas_rhino.conversions import curve_to_compas
from compas_rhino.conversions import curve_to_rhino
from compas_rhino.conversions import cylinder_to_rhino
from compas_rhino.conversions import frame_to_rhino_plane
from compas_rhino.conversions import line_to_rhino_curve
from compas_rhino.conversions import mesh_to_compas
from compas_rhino.conversions import mesh_to_rhino
from compas_rhino.conversions import plane_to_rhino
from compas_rhino.conversions import point_to_rhino
from compas_rhino.conversions import polyline_to_rhino_curve
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.conversions import torus_to_rhino
from compas_rhino.conversions import transformation_to_rhino
from compas_rhino.conversions import vector_to_rhino
from compas_rhino.geometry import RhinoNurbsCurve
from compas_rhino.geometry import RhinoNurbsSurface

from .builder import _RhinoBrepBuilder
from .edge import RhinoBrepEdge
from .face import RhinoBrepFace
from .loop import RhinoBrepLoop
from .vertex import RhinoBrepVertex


def _export_brep_to_file(brep, filepath):
    objects = Rhino.RhinoDoc.ActiveDoc.Objects
    obj_id = objects.Add(brep)
    obj = objects.Find(obj_id)
    obj.Select(True)
    rs.Command('_-Export "' + filepath + '" _Enter', False)
    objects.Delete(obj_id, True)


def _import_brep_from_file(filepath):
    # TODO: this only seems to work in ScriptEditor (AKA rhino, not GH)
    rs.Command('_-Import "' + filepath + '" _Enter', False)
    guid = rs.LastCreatedObjects()[0]  # this fails, could be Rhino bug
    obj = compas_rhino.objects.find_object(guid)
    geometry = obj.Geometry.Duplicate()
    compas_rhino.objects.delete_object(guid)
    return RhinoBrep.from_native(geometry)


def _join_meshes(meshes):
    result = Mesh()
    for mesh in meshes:
        result.join(mesh)
    return result


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
    centroid : :class:`compas.geometry.Point`, read-only
        The calculated centroid of this brep.
    curves : list[:class:`compas_rhino.geometry.RhinoNurbsCurve`], read-only
        The list of curves which comprise this brep.
    is_closed : bool, read-only
        True if this brep is closed, False otherwise.
    is_compound : bool, read-only
        True if this brep is compound, False otherwise.
    is_compoundsolid : bool, read-only
        True if this brep is compound solid, False otherwise.
    is_convex : bool, read-only
        True if this brep is convex, False otherwise.
    is_infinite : bool, read-only
        True if this brep is infinite, False otherwise.
    is_orientable : bool, read-only
        True if this brep is orientable, False otherwise.
    is_shell : bool, read-only
        True if this brep is a shell, False otherwise.
    is_surface : bool, read-only
        True if this brep is a surface, False otherwise.
    is_valid : bool, read-only
        True if this brep is valid, False otherwise.
    orientation : literal(:class:`~compas.geometry.BrepOrientation`), read-only
        The orientation of this brep. One of: FORWARD, REVERSED, INTERNAL, EXTERNAL.
    shells : list[:class:`compas_rhino.geometry.RhinoBrep`], read-only
        The list of shells which comprise this brep.
    solids : list[:class:`compas_rhino.geometry.RhinoBrep`], read-only
        The list of solids which comprise this brep.
    surfaces : list[:class:`compas_rhino.geometry.RhinoNurbsSurface`], read-only
        The list of surfaces which comprise this brep.

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

    @property
    def centroid(self):
        assert self._brep
        centroid = Rhino.Geometry.AreaMassProperties.Compute(self._brep).Centroid
        return Point(*centroid)

    @property
    def curves(self):
        assert self._brep
        return [RhinoNurbsCurve.from_native(c.ToNurbsCurve()) for c in self._brep.Curves3D]

    @property
    def is_closed(self):
        assert self._brep
        return self._brep.IsSolid

    @property
    def is_convex(self):
        raise NotImplementedError("Convexity check is not implemented for Rhino Breps.")

    @property
    def is_infinite(self):
        # TODO: what does this exactly mean? couldn't find in the Rhino API
        raise NotImplementedError

    @property
    def is_orientable(self):
        assert self._brep
        return self._brep.SolidOrientation in (Rhino.Geometry.BrepSolidOrientation.Inward, Rhino.Geometry.BrepSolidOrientation.Outward)

    @property
    def is_shell(self):
        # not sure how to get this one
        raise NotImplementedError

    @property
    def is_surface(self):
        assert self._brep
        return self._brep.IsSurface

    @property
    def is_valid(self):
        assert self._brep
        return self.IsValid

    @property
    def orientation(self):
        assert self._brep
        # TODO: align this with compas.geometry.BrepOrientation
        return self._brep.SolidOrientation

    @property
    def surfaces(self):
        assert self._brep
        return [[RhinoNurbsSurface.from_native(s.ToNurbsSurface()) for s in self._brep.Surfaces]]

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
    def from_brepfaces(cls, faces):
        """Create a Brep from a list of Brep faces forming an open or closed shell.

        Parameters
        ----------
        faces : list[:class:`compas.geometry.BrepFace`]

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        brep = Rhino.Geometry.Brep()
        for face in faces:
            brep.Faces.Add(face.native_face.UnderlyingSurface())
        return cls.from_native(brep)

    @classmethod
    def from_breps(cls, breps, tolerance=None):
        """Joins the breps at any overlapping edges to form as few as possible resulting breps. There may be more than one brep in the result array.

        Parameters
        ----------
        breps : list of :class:`compas.geometry.Brep`

        Returns
        -------
        list of :class:`compas.geometry.Brep`

        """
        tolerance = tolerance or TOL
        rhino_breps = [b.native_brep for b in breps]
        resulting_breps = Rhino.Geometry.Brep.JoinBreps(rhino_breps, tolerance.absolute, tolerance.angular)
        return [cls.from_native(brep) for brep in resulting_breps]

    @classmethod
    def from_cone(cls, cone, cap_bottom=True):
        """Create a RhinoBrep from a cone.

        Parameters
        ----------
        cone : :class:`compas.geometry.Cone`
            The cone geometry of the brep.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        rhino_cone = cone_to_rhino(cone)
        return cls.from_native(rhino_cone.ToBrep(cap_bottom))

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
    def from_curves(cls, curves, tolerance=None):
        """Create a RhinoBreps from a list of planar face boundary curves.

        Parameters
        ----------
        curves : list of :class:`~compas.geometry.Curve` or :class:`~compas.geometry.Polyline`
            The planar curves that make up the face borders of brep faces.

        Returns
        -------
        list of :class:`~compas_rhino.geometry.RhinoBrep`

        """
        tolerance = tolerance or TOL.absolute
        if not isinstance(curves, list):
            curves = [curves]
        faces = []
        for curve in curves:
            if isinstance(curve, Polyline):
                rhino_curve = polyline_to_rhino_curve(curve)
            else:
                rhino_curve = curve_to_rhino(curve)
            face = Rhino.Geometry.Brep.CreatePlanarBreps(rhino_curve, tolerance)
            if face is None:
                raise BrepError("Failed to create face from curve: {} ".format(curve))
            if len(face) > 1:
                raise BrepError("Failed to create single face from curve: {} ".format(curve))
            faces.append(face[0])
        rhino_brep = Rhino.Geometry.Brep.JoinBreps(faces, tolerance)
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
    def from_iges(cls, filepath):
        """Construct a RhinoBrep from a IGES file.

        Parameters
        ----------
        filepath : str
            The path to the step file.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        if not filepath.endswith(".igs"):
            raise ValueError("Expected file with .igs extension")
        return _import_brep_from_file(filepath)

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
    def from_pipe(cls, path, radius, cap_mode="none", tolerance=None, *args, **kwargs):
        """Construct a Brep by extruding a circle curve along the path curve.

        Parameters
        ----------
        curve : :class:`compas.geometry.Curve`
            The curve to extrude
        radius : float
            The radius of the pipe.
        cap_mode : literal('none', 'flat', 'round'), optional
            The type of end caps to create. Defaults to 'none'.
        tolerance : :class:`~compas.tolerance.Tolerance`, optional
            A Tolerance instance to use for the operation. Defaults to `TOL`.

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        tolerance = tolerance or TOL

        if cap_mode == "none":
            cap_mode = Rhino.Geometry.PipeCapMode.NONE
        elif cap_mode == "flat":
            cap_mode = Rhino.Geometry.PipeCapMode.Flat
        elif cap_mode == "round":
            cap_mode = Rhino.Geometry.PipeCapMode.Round
        else:
            raise ValueError("Invalid cap_ends value. Must be 'none', 'flat' or 'round'.")

        if hasattr(path, "native_curve"):
            path = curve_to_rhino(path)
        elif isinstance(path, Polyline):
            path = polyline_to_rhino_curve(path)
        elif isinstance(path, Line):
            path = line_to_rhino_curve(path)
        else:
            raise TypeError("Unsupported path curve type: {}".format(type(path)))

        result = Rhino.Geometry.Brep.CreatePipe(path, radius, False, cap_mode, True, tolerance.absolute, tolerance.angular)
        if result is None:
            raise BrepError("Failed to create pipe from curve: {} and radius: {}".format(path, radius))

        return [cls.from_native(brep) for brep in result]

    @classmethod
    def from_plane(cls, plane, domain_u=(-1, +1), domain_v=(-1, +1)):
        """Create a RhinoBrep from a plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane` or :class:`compas.geometry.Frame`
            The source plane.
        domain_u : tuple of float, optional
            The U domain of the plane. Defaults to (-1, +1).
        domain_v : tuple of float, optional
            The V domain of the plane. Defaults to (-1, +1).

        Notes
        -----
        When using a Rhino Plane, to maintain the original orientation data
        use :meth:`~compas_rhino.conversions.plane_to_compas_frame` and :meth:`~compas_rhino.conversions.frame_to_rhino_plane`.

        Returns
        -------
        :class:`compas_rhino.geometry.RhinoBrep`

        """
        if isinstance(plane, Frame):
            rhino_plane = frame_to_rhino_plane(plane)
        else:
            rhino_plane = plane_to_rhino(plane)
        u = Rhino.Geometry.Interval(domain_u[0], domain_u[1])
        v = Rhino.Geometry.Interval(domain_v[0], domain_v[1])
        surface = Rhino.Geometry.PlaneSurface(rhino_plane, u, v)
        return cls.from_native(surface.ToBrep())

    @classmethod
    def from_polygons(cls, polygons, tolerance=None, *args, **kwargs):
        """Create a RhinoBrep from a list of polygons.

        Parameters
        ----------
        polygons : list of :class:`compas.geometry.Polygon`
            The source polygons.

        Returns
        -------
        list of :class:`compas_rhino.geometry.RhinoBrep`

        """
        tolerance = tolerance or TOL.absolute
        polylines = []
        for polygon in polygons:
            points = polygon.points + [polygon.points[0]]  # make a closed polyline from the polygon
            polylines.append(Polyline(points=[*points]))
        return cls.from_curves(polylines, tolerance)

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
        if not filepath.endswith(".step"):
            raise ValueError("Expected file with .step extension")
        return _import_brep_from_file(filepath)

    @classmethod
    def from_sweep(cls, profile, path, is_closed=False, tolerance=None):
        """Construct one or more RhinoBrep(s) from a sweep operation.

        Parameters
        ----------
        profile : :class:`compas.geometry.Curve`
            Curve describing the cross-section of the surface created by the sweep operation.
        path : :class:`compas.geometry.Curve`
            Curve describing the edge of the sweep surface. The profile curve is sweeped along this curve.
        is_closed : bool, optional
            If True, the resulting surface will be closed, if possible. Defaults to False.
        tolerance : float, optional
            The precision to use for the operation. Defaults to `TOL.absolute`.

        Returns
        -------
        list of :class:`compas_rhino.geometry.RhinoBrep`

        """
        tolerance = tolerance or TOL.absolute
        if hasattr(profile, "native_curve"):
            profile = curve_to_rhino(profile)
        elif isinstance(profile, Polyline):
            profile = polyline_to_rhino_curve(profile)
        elif isinstance(profile, Line):
            profile = line_to_rhino_curve(profile)
        else:
            raise TypeError("Unsupported profile type: {}".format(type(profile)))

        if hasattr(path, "native_curve"):
            path = curve_to_rhino(path)
        elif isinstance(path, Polyline):
            path = polyline_to_rhino_curve(path)
        elif isinstance(path, Line):
            path = line_to_rhino_curve(path)
        else:
            raise TypeError("Unsupported path type: {}".format(type(path)))

        results = Rhino.Geometry.Brep.CreateFromSweep(path, profile, is_closed, tolerance)
        if not results:
            raise BrepError("Sweep operation ended with no result")

        return [cls.from_native(result) for result in results]

    @classmethod
    def from_torus(cls, torus):
        """Construct a RhinoBrep from a COMPAS torus.

        Parameters
        ----------
        torus : :class:`compas.geometry.Torus`

        Returns
        -------
        :class:`compas.geometry.BRep`

        """
        rhino_torus = torus_to_rhino(torus)
        return cls.from_native(rhino_torus.ToBrep())

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

    def to_viewmesh(self, linear_deflection: float = 0.001):
        """
        Convert the Brep to a single view mesh.

        Note
        ----
        Edges as polylines is not currently implemented for RhinoBrep. Therefore, an empty list will be returned.

        Parameters
        ----------
        linear_deflection : float, optional
            The maximum linear deflection between the geometry and its discrete representation.

        Returns
        -------
        tuple[:class:`compas.datastructures.Mesh`, list[:class:`compas.geometry.Polyline`]]

        """
        return _join_meshes(self.to_meshes()), []

    def to_step(self, filepath):
        if not filepath.endswith(".step"):
            raise ValueError("Attempted to export STEP but file ends with {} extension".format(filepath.split(".")[-1]))
        _export_brep_to_file(self._brep, filepath)

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
