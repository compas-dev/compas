from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import allclose
from compas.geometry import argmax
from compas.geometry import axis_angle_vector_from_matrix
from compas.geometry import basis_vectors_from_matrix
from compas.geometry import cross_vectors
from compas.geometry import decompose_matrix
from compas.geometry import euler_angles_from_matrix
from compas.geometry import matrix_from_axis_angle_vector
from compas.geometry import matrix_from_basis_vectors
from compas.geometry import matrix_from_euler_angles
from compas.geometry import matrix_from_quaternion
from compas.geometry import quaternion_from_matrix
from compas.geometry import subtract_vectors
from compas.geometry import Transformation

from compas.geometry.primitives import Point
from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Quaternion
from compas.geometry.primitives import Vector


class Frame(Primitive):
    """A frame is defined by a base point and two orthonormal base vectors.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        The origin of the frame.
    xaxis : [float, float, float] | :class:`~compas.geometry.Vector`
        The x-axis of the frame.
    yaxis : [float, float, float] | :class:`~compas.geometry.Vector`
        The y-axis of the frame.

    Attributes
    ----------
    point : :class:`~compas.geometry.Point`
        The base point of the frame.
    xaxis : :class:`~compas.geometry.Vector`
        The local X axis of the frame.
    yaxis : :class:`~compas.geometry.Vector`
        The local Y axis of the frame.
    zaxis : :class:`~compas.geometry.Vector`, read-only
        The Z axis of the frame.
    normal : :class:`~compas.geometry.Vector`, read-only
        The normal of the base plane of the frame.
    quaternion : :class:`~compas.geometry.Quaternion`, read-only
        The quaternion from the rotation given by the frame.
    axis_angle_vector : :class:`~compas.geometry.Vector`, read-only
        The axis-angle vector representing the rotation of the frame.

    Notes
    -----
    All input vectors are orthonormalized when creating a frame, with the first
    vector as starting point.

    Examples
    --------
    >>> from compas.geometry import Point
    >>> from compas.geometry import Vector
    >>> f = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    >>> f = Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0))

    """

    def __init__(self, point, xaxis, yaxis, **kwargs):
        super(Frame, self).__init__(**kwargs)
        self._point = None
        self._xaxis = None
        self._yaxis = None
        self.point = point
        self.xaxis = xaxis
        self.yaxis = yaxis

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        from schema import Schema

        return Schema(
            {
                "point": Point.DATASCHEMA.fget(None),
                "xaxis": Vector.DATASCHEMA.fget(None),
                "yaxis": Vector.DATASCHEMA.fget(None),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "frame"

    @property
    def data(self):
        """dict : The data dictionary that represents the frame."""
        return {
            "point": self.point.data,
            "xaxis": self.xaxis.data,
            "yaxis": self.yaxis.data,
        }

    @data.setter
    def data(self, data):
        self.point = Point.from_data(data["point"])
        self.xaxis = Vector.from_data(data["xaxis"])
        self.yaxis = Vector.from_data(data["yaxis"])

    @classmethod
    def from_data(cls, data):
        """Construct a frame from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> data = {'point': [0.0, 0.0, 0.0], 'xaxis': [1.0, 0.0, 0.0], 'yaxis': [0.0, 1.0, 0.0]}
        >>> frame = Frame.from_data(data)
        >>> frame.point
        Point(0.000, 0.000, 0.000)
        >>> frame.xaxis
        Vector(1.000, 0.000, 0.000)
        >>> frame.yaxis
        Vector(0.000, 1.000, 0.000)

        """
        frame = cls(
            Point.from_data(data["point"]),
            Vector.from_data(data["xaxis"]),
            Vector.from_data(data["yaxis"]),
        )
        return frame

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def xaxis(self):
        return self._xaxis

    @xaxis.setter
    def xaxis(self, vector):
        xaxis = Vector(*vector)
        xaxis.unitize()
        self._xaxis = xaxis

    @property
    def yaxis(self):
        return self._yaxis

    @yaxis.setter
    def yaxis(self, vector):
        yaxis = Vector(*vector)
        yaxis.unitize()
        zaxis = Vector.cross(self.xaxis, yaxis)
        zaxis.unitize()
        self._yaxis = Vector.cross(zaxis, self.xaxis)

    @property
    def normal(self):
        return Vector(*cross_vectors(self.xaxis, self.yaxis))

    @property
    def zaxis(self):
        return self.normal

    @property
    def quaternion(self):
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return Quaternion(*quaternion_from_matrix(R))

    @property
    def axis_angle_vector(self):
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return Vector(*axis_angle_vector_from_matrix(R))

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Frame({0!r}, {1!r}, {2!r})".format(self.point, self.xaxis, self.yaxis)

    def __len__(self):
        return 3

    def __getitem__(self, key):
        if key == 0:
            return self.point
        if key == 1:
            return self.xaxis
        if key == 2:
            return self.yaxis
        raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.point = value
            return
        if key == 1:
            self.xaxis = value
            return
        if key == 2:
            self.yaxis = value
        raise KeyError

    def __iter__(self):
        return iter([self.point, self.xaxis, self.yaxis])

    def __eq__(self, other, tol=1e-05):
        if not hasattr(other, "__iter__") or not hasattr(other, "__len__") or len(self) != len(other):
            return False
        return allclose(self, other)

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def worldXY(cls):
        """Construct the world XY frame.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The world XY frame.

        Examples
        --------
        >>> frame = Frame.worldXY()
        >>> frame.point
        Point(0.000, 0.000, 0.000)
        >>> frame.xaxis
        Vector(1.000, 0.000, 0.000)
        >>> frame.yaxis
        Vector(0.000, 1.000, 0.000)

        """
        return cls([0, 0, 0], [1, 0, 0], [0, 1, 0])

    @classmethod
    def worldZX(cls):
        """Construct the world ZX frame.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The world ZX frame.

        Examples
        --------
        >>> frame = Frame.worldZX()
        >>> frame.point
        Point(0.000, 0.000, 0.000)
        >>> frame.xaxis
        Vector(0.000, 0.000, 1.000)
        >>> frame.yaxis
        Vector(1.000, 0.000, 0.000)

        """
        return cls([0, 0, 0], [0, 0, 1], [1, 0, 0])

    @classmethod
    def worldYZ(cls):
        """Construct the world YZ frame.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The world YZ frame.

        Examples
        --------
        >>> frame = Frame.worldYZ()
        >>> frame.point
        Point(0.000, 0.000, 0.000)
        >>> frame.xaxis
        Vector(0.000, 1.000, 0.000)
        >>> frame.yaxis
        Vector(0.000, 0.000, 1.000)

        """
        return cls([0, 0, 0], [0, 1, 0], [0, 0, 1])

    @classmethod
    def from_points(cls, point, point_xaxis, point_xyplane):
        """Constructs a frame from 3 points.

        Parameters
        ----------
        point : [float, float, float] | :class:`~compas.geometry.Point`
            The origin of the frame.
        point_xaxis : [float, float, float] | :class:`~compas.geometry.Point`
            A point on the x-axis of the frame.
        point_xyplane : [float, float, float] | :class:`~compas.geometry.Point`
            A point within the xy-plane of the frame.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> frame = Frame.from_points([0, 0, 0], [1, 0, 0], [0, 1, 0])
        >>> frame.point
        Point(0.000, 0.000, 0.000)
        >>> frame.xaxis
        Vector(1.000, 0.000, 0.000)
        >>> frame.yaxis
        Vector(0.000, 1.000, 0.000)

        """
        xaxis = subtract_vectors(point_xaxis, point)
        xyvec = subtract_vectors(point_xyplane, point)
        yaxis = cross_vectors(cross_vectors(xaxis, xyvec), xaxis)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_rotation(cls, rotation, point=[0, 0, 0]):
        """Constructs a frame from a Rotation.

        Parameters
        ----------
        rotation : :class:`~compas.geometry.Rotation`
            The rotation defines the orientation of the frame.
        point : [float, float, float] | :class:`~compas.geometry.Point`, optional
            The origin of the frame.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.geometry import Rotation
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> R = Rotation.from_frame(f1)
        >>> f2 = Frame.from_rotation(R, point=f1.point)
        >>> f1 == f2
        True

        """
        xaxis, yaxis = rotation.basis_vectors
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_transformation(cls, transformation):
        """Constructs a frame from a Transformation.

        Parameters
        ----------
        transformation : :class:`~compas.geometry.Transformation`
            The transformation defines the orientation of the frame through the
            rotation and the origin through the translation.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.geometry import Transformation
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> f2 = Frame.from_transformation(T)
        >>> f1 == f2
        True

        """
        xaxis, yaxis = transformation.basis_vectors
        point = transformation.translation_vector
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_matrix(cls, matrix):
        """Construct a frame from a matrix.

        Parameters
        ----------
        matrix : list[list[float]]
            The 4x4 transformation matrix in row-major order.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.geometry import matrix_from_euler_angles
        >>> ea1 = [0.5, 0.4, 0.8]
        >>> M = matrix_from_euler_angles(ea1)
        >>> f = Frame.from_matrix(M)
        >>> ea2 = f.euler_angles()
        >>> allclose(ea1, ea2)
        True

        """
        _, _, angles, point, _ = decompose_matrix(matrix)
        R = matrix_from_euler_angles(angles, static=True, axes="xyz")
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_list(cls, values):
        """Construct a frame from a list of 12 or 16 float values.

        Parameters
        ----------
        values : list[float]
            The list of 12 or 16 values representing a 4x4 matrix.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The constructed frame.

        Raises
        ------
        ValueError
            If the length of the list is neither 12 nor 16.

        Notes
        -----
        Since the transformation matrix follows the row-major order, the
        translational components must be at the list's indices 3, 7, 11.

        Examples
        --------
        >>> l = [-1.0,  0.0,  0.0, 8110, 0.0,  0.0, -1.0, 7020, 0.0, -1.0,  0.0, 1810]
        >>> f = Frame.from_list(l)

        """
        if len(values) == 12:
            values.extend([0.0, 0.0, 0.0, 1.0])
        if len(values) != 16:
            raise ValueError("Expected 12 or 16 floats but got %d" % len(values))

        matrix = [[0.0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                matrix[i][j] = float(values[i * 4 + j])

        return cls.from_matrix(matrix)

    @classmethod
    def from_quaternion(cls, quaternion, point=[0, 0, 0]):
        """Construct a frame from a rotation represented by quaternion coefficients.

        Parameters
        ----------
        quaternion : [float, float, float, float] | :class:`~compas.geometry.Quaternion`
            Four numbers that represent the four coefficient values of a quaternion.
        point : [float, float, float] | :class:`~compas.geometry.Point`, optional
            The point of the frame.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> q1 = [0.945, -0.021, -0.125, 0.303]
        >>> f = Frame.from_quaternion(q1, point=[1., 1., 1.])
        >>> q2 = f.quaternion
        >>> allclose(q1, q2, tol=1e-03)
        True

        """
        R = matrix_from_quaternion(quaternion)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_axis_angle_vector(cls, axis_angle_vector, point=[0, 0, 0]):
        """Construct a frame from an axis-angle vector representing the rotation.

        Parameters
        ----------
        axis_angle_vector : [float, float, float]
            Three numbers that represent the axis of rotation and angle of
            rotation by its magnitude.
        point : [float, float, float] | :class:`~compas.geometry.Point`, optional
            The point of the frame.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> aav1 = [-0.043, -0.254, 0.617]
        >>> f = Frame.from_axis_angle_vector(aav1, point=[0, 0, 0])
        >>> aav2 = f.axis_angle_vector
        >>> allclose(aav1, aav2)
        True

        """
        R = matrix_from_axis_angle_vector(axis_angle_vector)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_euler_angles(cls, euler_angles, static=True, axes="xyz", point=[0, 0, 0]):
        """Construct a frame from a rotation represented by Euler angles.

        Parameters
        ----------
        euler_angles : [float, float, float]
            Three numbers that represent the angles of rotations about the defined axes.
        static : bool, optional
            If True, the rotations are applied to a static frame.
            If False, to a rotational.
        axes : str, optional
            A 3 character string specifying the order of the axes.
        point : [float, float, float] | :class:`~compas.geometry.Point`, optional
            The point of the frame.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> ea1 = 1.4, 0.5, 2.3
        >>> f = Frame.from_euler_angles(ea1, static=True, axes='xyz')
        >>> ea2 = f.euler_angles(static=True, axes='xyz')
        >>> allclose(ea1, ea2)
        True

        """
        R = matrix_from_euler_angles(euler_angles, static, axes)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_plane(cls, plane):
        """Constructs a frame from a plane.

        Xaxis and yaxis are arbitrarily selected based on the plane's normal.

        Parameters
        ----------
        plane : [point, vector] | :class:`~compas.geometry.Plane`
            A plane.

        Returns
        -------
        :class:`~compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> plane = Plane([0,0,0], [0,0,1])
        >>> frame = Frame.from_plane(plane)
        >>> allclose(frame.normal, plane.normal)
        True

        """
        point, normal = plane
        # To construct a frame we need to find a vector v that is perpendicular
        # to the plane's normal. This means that the dot-product of v with the
        # normal must be equal to 0, which is true for the following vectors:
        vectors = [
            Vector(-normal[1], normal[0], 0),
            Vector(0, -normal[2], normal[1]),
            Vector(normal[2], 0, -normal[0]),
        ]
        # But if we are unlucky, one of these vectors is (0, 0, 0), so we
        # choose the vector with the longest length as xaxis.
        idx = argmax([v.length for v in vectors])
        xaxis = vectors[idx]
        yaxis = cross_vectors(normal, xaxis)
        return cls(point, xaxis, yaxis)

    # ==========================================================================
    # static
    # ==========================================================================

    @staticmethod
    def local_to_local_coordinates(frame1, frame2, object_in_frame1):
        """Returns the object's coordinates in frame1 in the local coordinates of frame2.

        Parameters
        ----------
        frame1 : [point, vector, vector] | :class:`~compas.geometry.Frame`
            A frame representing one local coordinate system.
        frame2 : [point, vector, vector] | :class:`~compas.geometry.Frame`
            A frame representing another local coordinate system.
        object_in_frame1 : [float, float, float] | :class:`~compas.geometry.Geometry`
            An object in the coordinate frame1.
            If you pass a list of float, it is assumed to represent a point.

        Returns
        -------
        :class:`~compas.geometry.Geometry`
            The object in the local coordinate system of frame2.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> frame1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> frame2 = Frame([2, 1, 3], [1., 0., 0.], [0., 1., 0.])
        >>> p1 = Point(2, 2, 2) # point in frame1
        >>> p2 = Frame.local_to_local_coordinates(frame1, frame2, p1) # point in frame2
        >>> Frame.local_to_local_coordinates(frame2, frame1, p2)
        Point(2.000, 2.000, 2.000)

        """
        T = Transformation.from_change_of_basis(frame1, frame2)
        if isinstance(object_in_frame1, (list, tuple)):
            return Point(*object_in_frame1).transformed(T)
        return object_in_frame1.transformed(T)

    # ==========================================================================
    # methods
    # ==========================================================================

    def euler_angles(self, static=True, axes="xyz"):
        """The Euler angles from the rotation given by the frame.

        Parameters
        ----------
        static : bool, optional
            If True the rotations are applied to a static frame.
            If False, to a rotational.
        axes : str, optional
            A 3 character string specifying the order of the axes.

        Returns
        -------
        list[float]
            Three numbers that represent the angles of rotations about the defined axes.

        Examples
        --------
        >>> ea1 = 1.4, 0.5, 2.3
        >>> f = Frame.from_euler_angles(ea1, static=True, axes='xyz')
        >>> ea2 = f.euler_angles(static=True, axes='xyz')
        >>> allclose(ea1, ea2)
        True

        """
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return euler_angles_from_matrix(R, static, axes)

    def to_local_coordinates(self, obj_in_wcf):
        """Returns the object's coordinates in the local coordinate system of the frame.

        Parameters
        ----------
        obj_in_wcf : [float, float, float] | :class:`~compas.geometry.Geometry`
            An object in the world coordinate frame.

        Returns
        -------
        :class:`~compas.geometry.Geometry`
            The object in the local coordinate system of the frame.

        Notes
        -----
        If you pass a list of floats, it is assumed to represent a point.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> pw = Point(2, 2, 2) # point in wcf
        >>> pl = frame.to_local_coordinates(pw) # point in frame
        >>> frame.to_world_coordinates(pl)
        Point(2.000, 2.000, 2.000)

        """
        T = Transformation.from_change_of_basis(Frame.worldXY(), self)
        if isinstance(obj_in_wcf, (list, tuple)):
            return Point(*obj_in_wcf).transformed(T)
        return obj_in_wcf.transformed(T)

    def to_world_coordinates(self, obj_in_lcf):
        """Returns the object's coordinates in the global coordinate frame.

        Parameters
        ----------
        obj_in_lcf : [float, float, float] | :class:`~compas.geometry.Geometry`
            An object in local coordinate system of the frame.

        Returns
        -------
        :class:`~compas.geometry.Geometry`
            The object in the world coordinate frame.

        Notes
        -----
        If you pass a list of floats, it is assumed to represent a point.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> pl = Point(1.632, -0.090, 0.573) # point in frame
        >>> pw = frame.to_world_coordinates(pl) # point in wcf
        >>> frame.to_local_coordinates(pw)
        Point(1.632, -0.090, 0.573)

        """
        T = Transformation.from_change_of_basis(self, Frame.worldXY())
        if isinstance(obj_in_lcf, list):
            return Point(*obj_in_lcf).transformed(T)
        return obj_in_lcf.transformed(T)

    def transform(self, T):
        """Transform the frame.

        Parameters
        ----------
        T : :class:`~compas.geometry.Transformation`
            The transformation.

        Examples
        --------
        >>> from compas.geometry import Transformation
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> f2 = Frame.worldXY()
        >>> f2.transform(T)
        >>> f1 == f2
        True

        """
        # replace this by function call
        X = T * Transformation.from_frame(self)
        point = X.translation_vector
        xaxis, yaxis = X.basis_vectors
        self.point = point
        self.xaxis = xaxis
        self.yaxis = yaxis
