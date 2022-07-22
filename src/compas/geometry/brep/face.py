from compas.data import Data


class BrepFace(Data):
    """
    An interface for a Brep Face
    """

    # ==============================================================================
    # Properties
    # ==============================================================================

    @property
    def is_plane(self):
        """
        Returns True if this face is a plane, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_cylinder(self):
        """
        Returns True if this face is a cylinder, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_sphere(self):
        """
        Returns True if this face is a sphere, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_torus(self):
        """
        Returns True if this face is a torus, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_cone(self):
        """
        Returns True if this face is a cone, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def is_bspline(self):
        """
        Returns True if this face is a bspline, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    @property
    def vertices(self):
        """
        Returns a list of the vertices comprising this face.

        Returns
        -------
        list[:class:`compas.geometry.BrepVertex`]
        """
        raise NotImplementedError

    @property
    def edges(self):
        """
        Returns a list of the edges comprising this face.

        Returns
        -------
        list[:class:`compas.geometry.BrepEdge`]
        """
        raise NotImplementedError

    @property
    def loops(self):
        """
        Returns a list of the loops comprising this face.

        Returns
        -------
        list[:class:`compas.geometry.BrepLoop`]
        """
        raise NotImplementedError

    @property
    def surface(self):
        raise NotImplementedError

    @property
    def nurbssurface(self):
        raise NotImplementedError

    @property
    def area(self):
        """
        Returns the calculated area of this face.

        Returns
        -------
        float
        """
        raise NotImplementedError

    @property
    def centroid(self):
        raise NotImplementedError

    @property
    def is_valid(self):
        """
        Returns True if this face is valid, False otherwise.

        Returns
        -------
        bool
        """
        raise NotImplementedError

    # ==============================================================================
    # Constructors
    # ==============================================================================

    @classmethod
    def from_plane(cls):
        raise NotImplementedError

    @classmethod
    def from_cylinder(cls):
        raise NotImplementedError

    @classmethod
    def from_cone(cls):
        raise NotImplementedError

    @classmethod
    def from_sphere(cls):
        raise NotImplementedError

    @classmethod
    def from_torus(cls):
        raise NotImplementedError

    @classmethod
    def from_surface(cls):
        raise NotImplementedError
