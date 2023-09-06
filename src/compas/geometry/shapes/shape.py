from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Geometry
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Rotation
from compas.geometry import Plane


class Shape(Geometry):
    """Base class for geometric shapes.

    Shapes are parametrically defined with repsect to a local coordinate system.
    The local coordinate system of a shape is defined by a frame.
    The default frame is the word coordinate system, i.e. the origin and the axes of the world XY plane.

    Shapes are finite, closed objects, with a boundary that separates the interior from the exterior.
    They have a well-defined surface area and volume.

    An explicit representation of a shape is obtained by discretising its boundary into a set of vertices and faces with a chosen resolution (:meth:`to_vertices_and_faces`).
    The vertices and faces can be used to construct a :class:`compas.geometry.Polyhedron` object (:meth:`to_polyhedron`).
    A shape can also be converted to a :class:`compas.geometry.Brep` object (:meth:`to_brep`).

    Breps and polyhedrons support boolean operations.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`, optional
        The local coordinate system of the shape.
        Default is ``None``, in which case the world coordinate system is used.

    Attributes
    ----------
    frame : :class:`compas.geometry.Frame`
        The local coordinate system of the shape.
    transformation : :class:`compas.geometry.Transformation`, read-only
        The transformation of the shape to global coordinates.
    normal : :class:`compas.geometry.Vector`, read-only
        The normal of the shape.
    plane : :class:`compas.geometry.Plane`, read-only
        The plane of the shape.
    area : float, read-only
        The surface area of the shape.
    volume : float, read-only
        The volume of the shape.

    """

    def __init__(self, frame=None, **kwargs):
        super(Shape, self).__init__(**kwargs)
        self._frame = None
        self._transformation = None
        self.frame = frame

    # =============================================================================
    # Data
    # =============================================================================

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def frame(self):
        if not self._frame:
            self._frame = Frame.worldXY()
        return self._frame

    @frame.setter
    def frame(self, frame):
        if not frame:
            self._frame = None
        else:
            self._frame = Frame(frame[0], frame[1], frame[2])
        self._transformation = None

    @property
    def transformation(self):
        if not self._transformation:
            self._transformation = Transformation.from_frame_to_frame(self.frame, Frame.worldXY())
        return self._transformation

    @property
    def point(self):
        return self.frame.point

    @point.setter
    def point(self, point):
        self.frame.point = point

    @property
    def plane(self):
        return Plane(self.frame.point, self.frame.zaxis)

    @property
    def area(self):
        raise NotImplementedError

    @property
    def volume(self):
        raise NotImplementedError

    # =============================================================================
    # Constructors
    # =============================================================================

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_vertices_and_faces(self, **kwargs):
        """Convert the shape to a list of vertices and faces.

        Returns
        -------
        list of list of float
            The vertices of the shape.
        list of list of int
            The faces of the shape.

        """
        raise NotImplementedError

    def to_polyhedron(self, triangulated=True, u=16, v=None):
        """Convert the shape to a polyhedron.

        Parameters
        ----------
        triangulated : bool, optional
            If True, triangulate the faces.
        u : int, optional
            Number of faces in the "u" direction.
        v : int, optional
            Number of faces in the "v" direction.
            If no value is provided, and the shape has two parameter directions, the value of ``u`` will be used.

        Returns
        -------
        :class:`compas.geometry.Polyhedron`
            The polyhedron representation of the shape.

        Notes
        -----
        Parameters ``u`` and ``v`` define the resolution of the discretisation of curved geometry.
        If the geometry is not curved in a particular direction, the corresponding parameter will be ignored.
        For example, a cylinder has a resolution in the "u" direction, but not in the "v" direction.
        A sphere has a resolution in both the "u" and the "v" direction.
        A box has no resolution in either direction.

        """
        from compas.geometry import Polyhedron

        v = v or u

        vertices, faces = self.to_vertices_and_faces(u=u, v=v)

        if triangulated:
            triangles = []
            for face in faces:
                if len(face) == 4:
                    triangles.append(face[0:3])
                    triangles.append([face[0], face[2], face[3]])
                else:
                    triangles.append(face)
            faces = triangles

        return Polyhedron(vertices, faces)

    def to_brep(self):
        """Convert the shape to a Brep.

        Returns
        -------
        :class:`compas.geometry.Brep`
            The Brep representation of the shape.

        """
        raise NotImplementedError

    # =============================================================================
    # Transformation
    # =============================================================================

    def transform(self, transformation):
        """Transform the shape.

        Transformations of a shape are performed by applying the transformation to the frame of the shape.
        Transformations of the shape with respect to its local coordinate system are not supported.
        For this reason, only (combinations of) translations and rotations are supported.
        To scale a shape, use the :meth:`Shape.scale` method.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the shape.

        Returns
        -------
        None

        """
        self.frame.transform(transformation)

    def translate(self, vector):
        """Translate the shape.

        Parameters
        ----------
        vector : :class:`Vector`
            The translation vector.

        Returns
        -------
        None

        """
        self.frame.point += vector

    def rotate(self, angle, axis=None, point=None):
        """Rotate the shape.

        Parameters
        ----------
        vector : :class:`Vector`
            The translation vector.

        Returns
        -------
        None

        """
        point = point or [0, 0, 0]
        matrix = Rotation.from_axis_and_angle(axis=axis, angle=angle, point=point)
        self.transform(matrix)

    def scale(self, scale):
        """Scale the shape.

        Scale transformations are applied to the parameters of a shape rahter than to its frame.
        Only uniform scaling is supported.

        Parameters
        ----------
        scale : float
            The scaling factor.

        Returns
        -------
        None

        """
        raise NotImplementedError

    # =============================================================================
    # Methods
    # =============================================================================

    def contains_point(self, point):
        """Verify if a point is inside the shape.

        Parameters
        ----------
        point : :class:`Point`
            The point to test.

        Returns
        -------
        bool
            True if the point is inside the shape.
            False otherwise.

        """
        raise NotImplementedError

    def contains_points(self, points):
        """Verify if a list of points are inside the shape.

        Parameters
        ----------
        points : list of :class:`Point`
            The points to test.

        Returns
        -------
        list of bool
            True if the point is inside the shape.
            False otherwise.

        """
        return [self.contains_point(point) for point in points]
