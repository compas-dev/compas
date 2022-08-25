from compas.data import Data


class BrepFace(Data):
    """An interface for a Brep Face.

    Attributes
    ----------
    is_plane : bool, read-only
        Returns True if this face is a plane, False otherwise.
    is_cylinder : bool, read-only
        Returns True if this face is a cylinder, False otherwise.
    is_sphere : bool, read-only
        Returns True if this face is a sphere, False otherwise.
    is_torus : bool, read-only
        Returns True if this face is a torus, False otherwise.
    is_cone : bool, read-only
        Returns True if this face is a cone, False otherwise.
    is_bspline : bool, read-only
        Returns True if this face is a bspline, False otherwise.
    vertices : list[:class:`~compas.geometry.BrepVertex`], read-only
        Returns a list of the vertices comprising this face.
    edges : list[:class:`~compas.geometry.BrepEdge`], read-only
        Returns a list of the edges comprising this face.
    loops : list[:class:`~compas.geometry.BrepLoop`], read-only
        Returns a list of the loops comprising this face.
    surface : :class:`~compas.geometry.Surface`, read-only
        Returns the geometry of this face as a surface.
    nurbssurface : :class:`~compas.geometry.NurbsSurface`, read-only
        Returns the geometry of this face as a NURBS surface.
    area : float, read-only
        Returns the area of this face's geometry.
    centroid : :class:`~compas.geometry.Point`, read-only
        Returns the centroid of this face's geometry.
    is_valid : bool, read-only
        Return True if this face is valid, False otherwise.

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
    def nurbssurface(self):
        raise NotImplementedError

    @property
    def area(self):
        raise NotImplementedError

    @property
    def centroid(self):
        raise NotImplementedError

    @property
    def is_valid(self):
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_plane(cls, plane):
        """Construct a face from a plane geometry.

        Parameters
        ----------
        plane : :class:`~compas.geometry.Plane`

        Returns
        -------
        :class:`~compas.geometry.BrepFace`

        """
        raise NotImplementedError

    @classmethod
    def from_cylinder(cls):
        """Construct a face from a cylinder geometry.

        Parameters
        ----------
        cylinder : :class:`~compas.geometry.Cylinder`

        Returns
        -------
        :class:`~compas.geometry.BrepFace`

        """
        raise NotImplementedError

    @classmethod
    def from_cone(cls, cone):
        """Construct a face from a cone geometry.

        Parameters
        ----------
        cone : :class:`~compas.geometry.Cone`

        Returns
        -------
        :class:`~compas.geometry.BrepFace`

        """
        raise NotImplementedError

    @classmethod
    def from_sphere(cls, sphere):
        """Construct a face from a sphere geometry.

        Parameters
        ----------
        sphere : :class:`~compas.geometry.Sphere`

        Returns
        -------
        :class:`~compas.geometry.BrepFace`

        """
        raise NotImplementedError

    @classmethod
    def from_torus(cls, torus):
        """Construct a face from a torus geometry.

        Parameters
        ----------
        torus : :class:`~compas.geometry.Torus`

        Returns
        -------
        :class:`~compas.geometry.BrepFace`

        """
        raise NotImplementedError

    @classmethod
    def from_surface(cls, surface):
        """Construct a face from a surfaces geometry.

        Parameters
        ----------
        surface : :class:`~compas.geometry.Surface`

        Returns
        -------
        :class:`~compas.geometry.BrepFace`

        """
        raise NotImplementedError
