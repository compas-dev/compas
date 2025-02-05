from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore

from compas.geometry import Brep
from compas.geometry import BrepFace
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Sphere
from compas.geometry import SurfaceType
from compas_rhino.conversions import cylinder_to_compas
from compas_rhino.conversions import cylinder_to_rhino
from compas_rhino.conversions import frame_to_rhino_plane
from compas_rhino.conversions import plane_to_compas_frame
from compas_rhino.conversions import sphere_to_compas
from compas_rhino.conversions import sphere_to_rhino
from compas_rhino.geometry import RhinoNurbsSurface
from compas_rhino.geometry.surfaces import RhinoSurface

from .edge import RhinoBrepEdge
from .loop import RhinoBrepLoop


class RhinoBrepFace(BrepFace):
    """A wrapper for Rhino.Geometry.BrepFace

    Attributes
    ----------
    native_surface : :class:`Rhino.Geometry.Surface`
        The rhino native underlying geometry of this face.
    loops : list[:class:`compas_rhino.geometry.RhinoBrepLoop`], read-only
        The list of loops which comprise this face.
    surface : :class:`compas_rhino.geometry.RhinoNurbsSurface`
        The compas_rhino wrapper of the underlying geometry of this face.
    boundary : :class:`compas_rhino.geometry.RhinoBrepLoop`, read-only
        The loop which defines the outer boundary of this face.
    holes : list[:class:`compas_rhino.geometry.RhinoBrepLoop`], read-only
        The list of loops which comprise the holes of this brep, if any.
    is_plane : float, read-only
        True if the geometry of this face is a plane, False otherwise.
    is_reversed : bool, read-only
        True if the orientation of this face is reversed, False otherwise.
    native_face : :class:`Rhino.Geometry.BrepFace`
        The underlying BrepFace object.

    """

    def __init__(self, rhino_face=None):
        super(RhinoBrepFace, self).__init__()
        self._loops = None
        self._surface = None
        self._face = None
        if rhino_face:
            self.native_face = rhino_face

    # ==============================================================================
    # Data
    # ==============================================================================

    @property
    def __data__(self):
        surface_type, surface, uv_domain, plane = self._get_surface_geometry(self._face.UnderlyingSurface())
        return {
            "surface_type": surface_type,
            "surface": surface.__data__,
            "uv_domain": uv_domain,
            "frame": plane_to_compas_frame(plane).__data__,  # until all shapes have a frame
            "loops": [loop.__data__ for loop in self._loops],
        }

    @classmethod
    def __from_data__(cls, data, builder):
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data : dict
            The data dictionary.
        builder : :class:`compas_rhino.geometry.BrepBuilder`
            The object reconstructing the current Brep.

        Returns
        -------
        :class:`compas.data.Data`
            An instance of this object type if the data contained in the dict has the correct schema.

        """

        instance = cls()
        instance._surface = instance._make_surface__from_data__(data["surface_type"], data["surface"], data["uv_domain"], data["frame"])
        face_builder = builder.add_face(instance._surface)
        for loop_data in data["loops"]:
            RhinoBrepLoop.__from_data__(loop_data, face_builder)
        instance.native_face = face_builder.result
        return instance

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def native_surface(self):
        return self._surface

    @property
    def area(self):
        return self._mass_props.Area

    @property
    def centroid(self):
        return self._mass_props.Centroid

    @property
    def edges(self):
        brep = self._face.Brep
        edge_indices = self._face.AdjacentEdges()
        return [RhinoBrepEdge(brep.Edges[index]) for index in edge_indices]

    @property
    def loops(self):
        return self._loops

    @property
    def surface(self):
        return self._surface

    @property
    def boundary(self):
        return self._loops[0]

    @property
    def holes(self):
        return self._loops[1:]

    @property
    def is_plane(self):
        return self._face.UnderlyingSurface().IsPlanar()

    @property
    def is_cone(self):
        return self._face.UnderlyingSurface().IsCone()

    @property
    def is_cylinder(self):
        return self._face.UnderlyingSurface().IsCylinder()

    @property
    def is_sphere(self):
        return self._face.UnderlyingSurface().IsSphere()

    @property
    def is_torus(self):
        return self._face.UnderlyingSurface().IsTorus()

    @property
    def is_reversed(self):
        return self._face.OrientationIsReversed

    @property
    def native_face(self):
        return self._face

    @native_face.setter
    def native_face(self, rhino_face):
        self._face = rhino_face
        self._mass_props = Rhino.Geometry.AreaMassProperties.Compute(rhino_face.ToBrep())
        self._loops = [RhinoBrepLoop(loop) for loop in rhino_face.Loops]
        self._surface = RhinoNurbsSurface.from_rhino(self._face.UnderlyingSurface().ToNurbsSurface())

    @property
    def nurbssurface(self):
        return self._surface

    @property
    def vertices(self):
        vertices = []
        for edge in self.edges:
            vertices.extend(edge.vertices)
        return vertices

    @property
    def type(self):
        if self.is_cone:
            return SurfaceType.CONE
        elif self.is_cylinder:
            return SurfaceType.CYLINDER
        elif self.is_sphere:
            return SurfaceType.SPHERE
        elif self.is_torus:
            return SurfaceType.TORUS
        elif self.is_plane:
            return SurfaceType.PLANE
        else:
            return SurfaceType.OTHER_SURFACE

    # ==============================================================================
    # Methods
    # ==============================================================================

    @staticmethod
    def _get_surface_geometry(surface):
        uv_domain = [[surface.Domain(0)[0], surface.Domain(0)[1]], [surface.Domain(1)[0], surface.Domain(1)[1]]]
        if isinstance(surface, Rhino.Geometry.PlaneSurface):
            _, plane = surface.FrameAt(0.0, 0.0)
            return "plane", plane_to_compas_frame(plane), uv_domain, plane
        if isinstance(surface, Rhino.Geometry.NurbsSurface):
            _, plane = surface.FrameAt(0.0, 0.0)
            return "nurbs", RhinoNurbsSurface.from_rhino(surface), uv_domain, plane
        if isinstance(surface, Rhino.Geometry.Rhino.Geometry.RevSurface):
            success, cast_surface = surface.TryGetSphere()
            if success:
                return "sphere", sphere_to_compas(cast_surface), uv_domain, cast_surface.EquatorialPlane
            success, cast_surface = surface.TryGetCylinder()
            if success:
                return "cylinder", cylinder_to_compas(cast_surface), uv_domain, cast_surface.BasePlane
            success, cast_surface = surface.TryGetTorus()
        raise NotImplementedError("Support for surface type: {} is not yet implemented.".format(surface.__class__.__name__))

    def _make_surface__from_data__(self, surface_type, surface_data, uv_domain, frame_data):
        u_domain, v_domain = uv_domain
        frame = Frame.__from_data__(frame_data)  # workaround until all shapes have a frame
        if surface_type == "plane":
            frame = Frame.__from_data__(surface_data)  # redundancy in shapes which already have a frame
            surface = RhinoSurface.from_frame(frame, u_domain, v_domain)
        elif surface_type == "sphere":
            sphere = self._make_sphere_surface(surface_data, u_domain, v_domain, frame)
            surface = RhinoSurface.from_rhino(sphere)
        elif surface_type == "cylinder":
            cylinder = self._make_cylinder_surface(surface_data, u_domain, v_domain, frame)
            surface = RhinoSurface.from_rhino(cylinder)
        elif surface_type == "nurbs":
            surface = RhinoNurbsSurface.__from_data__(surface_data)
        elif surface_type == "torus":
            raise NotImplementedError("Support for torus surface is not yet implemented!")
        else:
            raise NotImplementedError("Support for surface type: {} is not yet implemented.".format(surface_type))
        surface.rhino_surface.SetDomain(0, Rhino.Geometry.Interval(*u_domain))
        surface.rhino_surface.SetDomain(1, Rhino.Geometry.Interval(*v_domain))
        return surface

    @staticmethod
    def _make_cylinder_surface(surface_data, u_domain, v_domain, frame):
        cylinder = Cylinder.__from_data__(surface_data)
        cylinder = cylinder_to_rhino(cylinder)
        cylinder.BasePlane = frame_to_rhino_plane(frame)
        surface = Rhino.Geometry.RevSurface.CreateFromCylinder(cylinder)
        surface.SetDomain(0, Rhino.Geometry.Interval(*u_domain))
        surface.SetDomain(1, Rhino.Geometry.Interval(*v_domain))
        return surface

    @staticmethod
    def _make_sphere_surface(surface_data, u_domain, v_domain, frame):
        sphere = Sphere.__from_data__(surface_data)
        sphere = sphere_to_rhino(sphere)
        # seems Sphere => Rhino.Geometry.RevSurface conversion modifies the orientation of the sphere
        # setting the plane here is overriden by this modification and surface ends up oriented differntly than
        # original.
        # sphere.EquatorialPlane = frame_to_rhino_plane(frame)
        surface = Rhino.Geometry.RevSurface.CreateFromSphere(sphere)
        surface.SetDomain(0, Rhino.Geometry.Interval(*u_domain))
        surface.SetDomain(1, Rhino.Geometry.Interval(*v_domain))
        return surface

    # ==============================================================================
    # Methods
    # ==============================================================================

    def adjacent_faces(self):
        """Returns a list of the faces adjacent to this face.

        Returns
        -------
        list[:class:`compas_rhino.geometry.RhinoBrepFace`]
            The list of adjacent faces.

        """
        face_indices = self._face.AdjacentFaces()
        brep = self._face.Brep
        return [RhinoBrepFace(brep.Faces[index]) for index in face_indices]

    def as_brep(self):
        """Returns a Brep representation of this face.

        Returns
        -------
        :class:`~compas_rhino.geometry.RhinoBrep`

        """
        return Brep.from_native(self._face.ToBrep())

    def frame_at(self, u, v):
        """Returns the frame at the given uv parameters.

        Parameters
        ----------
        u : float
            The u parameter.
        v : float
            The v parameter.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The frame at the given uv parameters.

        """
        success, rhino_plane = self._face.FrameAt(u, v)
        if not success:
            raise ValueError("Failed to get frame at uv parameters: ({},{}).".format(u, v))
        return plane_to_compas_frame(rhino_plane)
