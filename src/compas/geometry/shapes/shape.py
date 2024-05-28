from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Rotation
from compas.geometry import Transformation


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
    area : float, read-only
        The surface area of the shape.
    frame : :class:`compas.geometry.Frame`
        The local coordinate system of the shape.
    transformation : :class:`compas.geometry.Transformation`, read-only
        The transformation of the shape to global coordinates.
    volume : float, read-only
        The volume of the shape.

    """

    def __init__(self, frame=None, name=None):
        super(Shape, self).__init__(name=name)
        self._frame = None
        self._transformation = None
        self.frame = frame
        self._resolution_u = 16
        self._resolution_v = 16
        self._vertices = None
        self._edges = None
        self._faces = None
        self._triangles = None

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
            self._transformation = Transformation.from_frame_to_frame(Frame.worldXY(), self.frame)
        return self._transformation

    @property
    def area(self):
        raise NotImplementedError

    @property
    def volume(self):
        raise NotImplementedError

    @property
    def resolution_u(self):
        return self._resolution_u

    @resolution_u.setter
    def resolution_u(self, u):
        if u < 3:
            raise ValueError("The value for u should be u > 3.")
        self._resolution_u = u
        self._vertices = None
        self._edges = None
        self._faces = None
        self._triangles = None

    @property
    def resolution_v(self):
        return self._resolution_v

    @resolution_v.setter
    def resolution_v(self, v):
        if v < 3:
            raise ValueError("The value for v should be v > 3.")
        self._resolution_v = v
        self._vertices = None
        self._edges = None
        self._faces = None
        self._triangles = None

    @property
    def vertices(self):
        self._vertices = self.compute_vertices()
        return self._vertices

    @property
    def edges(self):
        if not self._edges:
            self._edges = self.compute_edges()
        return self._edges

    @property
    def faces(self):
        if not self._faces:
            self._faces = self.compute_faces()
        return self._faces

    @property
    def triangles(self):
        if not self._triangles:
            self._triangles = []
            for face in self.faces:
                if len(face) == 4:
                    a, b, c, d = face
                    self._triangles.append((a, b, c))
                    self._triangles.append((a, c, d))
                else:
                    self._triangles.append(face)
        return self._triangles

    @property
    def points(self):
        vertices = self.compute_vertices()
        return [Point(x, y, z) for x, y, z in vertices]

    @property
    def lines(self):
        vertices = self.compute_vertices()
        return [Line(vertices[u], vertices[v]) for u, v in self.edges]

    @property
    def polygons(self):
        vertices = self.compute_vertices()
        return [[Polygon([vertices[v] for v in face])] for face in self.faces]

    # =============================================================================
    # Discretisation
    # =============================================================================

    def compute_vertices(self):
        raise NotImplementedError

    def compute_edges(self):
        raise NotImplementedError

    def compute_faces(self):
        raise NotImplementedError

    # =============================================================================
    # Constructors
    # =============================================================================

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_vertices_and_faces(self, triangulated=True, u=None, v=None):
        """Convert the shape to a list of vertices and faces.

        Parameters
        ----------
        triangulated : bool, optional
            If True, triangulate the faces.
        u : int, optional
            Number of faces in the "u" direction.
            If no value is provided, the value of `self.resolution_u` will be used.
        v : int, optional
            Number of faces in the "v" direction.
            If no value is provided, the value of `self.resolution_v` will be used.

        Returns
        -------
        list of list of float
            The vertices of the shape.
        list of list of int
            The faces of the shape.

        """
        if u:
            self.resolution_u = u
        if v:
            self.resolution_v = v
        vertices = self.vertices
        if triangulated:
            faces = self.faces
        else:
            faces = self.triangles
        return vertices, faces

    def to_polyhedron(self, triangulated=True, u=None, v=None):
        """Convert the shape to a polyhedron.

        Parameters
        ----------
        triangulated : bool, optional
            If True, triangulate the faces.
        u : int, optional
            Number of faces in the "u" direction.
            If no value is provided, the value of `self.resolution_u` will be used.
        v : int, optional
            Number of faces in the "v" direction.
            If no value is provided, the value of `self.resolution_v` will be used.

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

        vertices, faces = self.to_vertices_and_faces(u=u, v=v, triangulated=triangulated)

        return Polyhedron(vertices, faces)

    def to_mesh(self, triangulated=True, u=None, v=None):
        """Returns a mesh representation of the box.

        Parameters
        ----------
        triangulated: bool, optional
            If True, triangulate the faces.
        u : int, optional
            Number of faces in the "u" direction.
            If no value is provided, the value of `self.resolution_u` will be used.
        v : int, optional
            Number of faces in the "v" direction.
            If no value is provided, the value of `self.resolution_v` will be used.

        Returns
        -------
        :class:`compas.datastructures.Mesh`

        Notes
        -----
        Parameters ``u`` and ``v`` define the resolution of the discretisation of curved geometry.
        If the geometry is not curved in a particular direction, the corresponding parameter will be ignored.
        For example, a cylinder has a resolution in the "u" direction, but not in the "v" direction.
        A sphere has a resolution in both the "u" and the "v" direction.
        A box has no resolution in either direction.

        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces(u=u, v=v, triangulated=triangulated)

        mesh = Mesh.from_vertices_and_faces(vertices, faces)

        return mesh

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

        See Also
        --------
        translate
        rotate
        scale

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

        See Also
        --------
        rotate
        scale
        transform

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

        See Also
        --------
        translate
        scale
        transform

        """
        axis = axis or [0, 0, 1]
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

        See Also
        --------
        translate
        rotate
        transform

        """
        raise NotImplementedError

    # =============================================================================
    # Methods
    # =============================================================================

    def contains_point(self, point):
        """Verify if a point is inside the shape.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
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
        points : list of :class:`compas.geometry.Point`
            The points to test.

        Returns
        -------
        list of bool
            True if the point is inside the shape.
            False otherwise.

        """
        return [self.contains_point(point) for point in points]
