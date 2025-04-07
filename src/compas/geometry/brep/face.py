from compas.data import Data
from compas.geometry import Polygon


class SurfaceType(object):
    """Enumaration of surface types."""

    PLANE = 0
    CYLINDER = 1
    CONE = 2
    SPHERE = 3
    TORUS = 4
    BEZIER_SURFACE = 5
    BSPLINE_SURFACE = 6
    SURFACE_OF_REVOLUTION = 7
    SURFACE_OF_EXTRUSTION = 8
    OFFSET_SURFACE = 9
    OTHER_SURFACE = 10


class BrepFace(Data):
    """An interface for a Brep Face.

    Attributes
    ----------
    area : float, read-only
        Returns the area of this face's geometry.
    centroid : :class:`compas.geometry.Point`, read-only
        Returns the centroid of this face's geometry.
    edges : list[:class:`compas.geometry.BrepEdge`], read-only
        Returns a list of the edges comprising this face.
    is_bspline : bool, read-only
        Returns True if this face is a bspline, False otherwise.
    is_cone : bool, read-only
        Returns True if this face is a cone, False otherwise.
    is_cylinder : bool, read-only
        Returns True if this face is a cylinder, False otherwise.
    is_plane : bool, read-only
        Returns True if this face is a plane, False otherwise.
    is_sphere : bool, read-only
        Returns True if this face is a sphere, False otherwise.
    is_torus : bool, read-only
        Returns True if this face is a torus, False otherwise.
    is_reversed : bool, read-only
        True if the orientation of this face is reversed, False otherwise.
    is_valid : bool, read-only
        Return True if this face is valid, False otherwise.
    loops : list[:class:`compas.geometry.BrepLoop`], read-only
        Returns a list of the loops comprising this face.
    native_face : Any
        The underlying face object. Type is backend-dependent.
    nurbssurface : :class:`compas.geometry.NurbsSurface`, read-only
        Returns the geometry of this face as a NURBS surface.
    surface : :class:`compas.geometry.Surface`, read-only
        Returns the geometry of this face as a surface.
    type : literal(SurfaceType), read-only
        Returns the surface type of this face. One of: PLANE, CYLINDER, CONE, SPHERE, TORUS, BEZIER_SURFACE,
        BSPLINE_SURFACE, SURFACE_OF_REVOLUTION, SURFACE_OF_EXTRUSTION, OFFSET_SURFACE, OTHER_SURFACE.
    vertices : list[:class:`compas.geometry.BrepVertex`], read-only
        Returns a list of the vertices comprising this face.

    """

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def is_plane(self):
        raise NotImplementedError

    @property
    def is_cylinder(self):
        raise NotImplementedError

    @property
    def is_sphere(self):
        raise NotImplementedError

    @property
    def is_torus(self):
        raise NotImplementedError

    @property
    def is_cone(self):
        raise NotImplementedError

    @property
    def is_bspline(self):
        raise NotImplementedError

    @property
    def vertices(self):
        raise NotImplementedError

    @property
    def edges(self):
        raise NotImplementedError

    @property
    def loops(self):
        raise NotImplementedError

    @property
    def surface(self):
        raise NotImplementedError

    @property
    def native_face(self):
        raise NotImplementedError

    @property
    def nurbssurface(self):
        raise NotImplementedError

    @property
    def area(self):
        raise NotImplementedError

    @property
    def centroid(self):
        raise NotImplementedError

    @property
    def is_reversed(self):
        raise NotImplementedError

    @property
    def is_valid(self):
        raise NotImplementedError

    @property
    def type(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_plane(cls, plane):
        """Construct a face from a plane geometry.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`

        Returns
        -------
        :class:`compas.geometry.BrepFace`

        """
        raise NotImplementedError

    @classmethod
    def from_cylinder(cls):
        """Construct a face from a cylinder geometry.

        Parameters
        ----------
        cylinder : :class:`compas.geometry.Cylinder`

        Returns
        -------
        :class:`compas.geometry.BrepFace`

        """
        raise NotImplementedError

    @classmethod
    def from_cone(cls, cone):
        """Construct a face from a cone geometry.

        Parameters
        ----------
        cone : :class:`compas.geometry.Cone`

        Returns
        -------
        :class:`compas.geometry.BrepFace`

        """
        raise NotImplementedError

    @classmethod
    def from_sphere(cls, sphere):
        """Construct a face from a sphere geometry.

        Parameters
        ----------
        sphere : :class:`compas.geometry.Sphere`

        Returns
        -------
        :class:`compas.geometry.BrepFace`

        """
        raise NotImplementedError

    @classmethod
    def from_torus(cls, torus):
        """Construct a face from a torus geometry.

        Parameters
        ----------
        torus : :class:`compas.geometry.Torus`

        Returns
        -------
        :class:`compas.geometry.BrepFace`

        """
        raise NotImplementedError

    @classmethod
    def from_surface(cls, surface):
        """Construct a face from a surfaces geometry.

        Parameters
        ----------
        surface : :class:`compas.geometry.Surface`

        Returns
        -------
        :class:`compas.geometry.BrepFace`

        """
        raise NotImplementedError

    # ==============================================================================
    # Conversions
    # ==============================================================================

    def to_polygon(self):
        """Convert the face to a polygon without underlying geometry.

        Returns
        -------
        :class:`~compas.geometry.Polygon`

        """
        points = []
        for vertex in self.loops[0].vertices:
            points.append(vertex.point)
        return Polygon(points)

    # ==============================================================================
    # Methods
    # ==============================================================================

    def adjacent_faces(self):
        """Returns a list of the faces adjacent to this face.

        Returns
        -------
        list[:class:`compas.geometry.BrepFace`]

        """
        raise NotImplementedError

    def as_brep(self):
        """Returns a Brep representation of this face.

        Returns
        -------
        :class:`compas.geometry.Brep`

        """
        raise NotImplementedError

    def add_loop(self, loop, *args, **kwargs):
        """Adds an inner loop to this face.

        Parameters
        ----------
        loop : :class:`compas.geometry.BrepLoop`
            The loop to add

        Notes
        -----
        Any additional arguments may be backend specific.

        """
        raise NotImplementedError

    def add_loops(self, loops, *args, **kwargs):
        """Adds several inner loops to this face.

        Parameters
        ----------
        loops : list[:class:`compas.geometry.BrepLoop`]
            The loops to add.

        Notes
        -----
        Any additional arguments may be backend specific.

        """
        raise NotImplementedError

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
        raise NotImplementedError

    def try_get_nurbssurface(
        self,
        precision,
        continuity_u,
        continuity_v,
        maxdegree_u,
        maxdegree_v,
        maxsegments_u,
        maxsegments_v,
    ):
        """Returns the NURBS surface representation of this face. Or None if this cannot be done.

        Parameters
        ----------
        precision : float
            The precision of the conversion.
        continuity_u : int
            The continuity of the surface in the u direction.
        continuity_v : int
            The continuity of the surface in the v direction.
        maxdegree_u : int
            The maximum degree of the surface in the u direction.
        maxdegree_v : int
            The maximum degree of the surface in the v direction.
        maxsegments_u : int
            The maximum number of segments in the u direction.
        maxsegments_v : int
            The maximum number of segments in the v direction.

        Returns
        -------
        :class:`~compas.geometry.NurbsSurface` or None

        """
        raise NotImplementedError
