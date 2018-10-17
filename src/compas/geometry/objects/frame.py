from __future__ import print_function

import math

from compas.geometry.basic import cross_vectors
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import allclose

from compas.geometry.objects import Point
from compas.geometry.objects import Vector

from compas.geometry.xforms import Transformation
from compas.geometry.xforms import Rotation

from compas.geometry.transformations import matrix_from_basis_vectors
from compas.geometry.transformations import basis_vectors_from_matrix
from compas.geometry.transformations import quaternion_from_matrix
from compas.geometry.transformations import matrix_from_quaternion
from compas.geometry.transformations import axis_angle_vector_from_matrix
from compas.geometry.transformations import matrix_from_axis_angle_vector
from compas.geometry.transformations import euler_angles_from_matrix
from compas.geometry.transformations import matrix_from_euler_angles
from compas.geometry.transformations import decompose_matrix
from compas.geometry.transformations import inverse
from compas.geometry.transformations import matrix_from_frame


__all__ = ['Frame']


class Frame(object):
    """A frame is defined by a base point and two orthonormal base vectors.

    Parameters
    ----------
    point : point
        The origin of the frame.
    xaxis : vector
        The x-axis of the frame.
    yaxis : vector
        The y-axis of the frame.

    Examples
    --------
    >>> f = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    >>> f = Frame.from_points([1, 1, 1], [2, 4, 5], [4, 2, 3])
    >>> f = Frame.from_euler_angles([0.5, 1., 0.2])
    >>> f = Frame.worldXY()

    Notes
    -----
    All input vectors are orthonormalized when creating a frame, with the first
    vector as starting point.

    """

    def __init__(self, point, xaxis, yaxis):
        self._point = None
        self._xaxis = None
        self._yaxis = None
        self.point = point
        self.xaxis = xaxis
        self.yaxis = yaxis

    # ==========================================================================
    # factory
    # ==========================================================================

    @classmethod
    def worldXY(cls):
        """Construct the world XY frame.

        Returns
        -------
        Frame
            The world XY frame.

        """
        return cls([0, 0, 0], [1, 0, 0], [0, 1, 0])

    @classmethod
    def worldZX(cls):
        """Construct the world ZX frame.

        Returns
        -------
        Frame
            The world ZX frame.

        """
        return cls([0, 0, 0], [0, 0, 1], [1, 0, 0])

    @classmethod
    def worldYZ(cls):
        """Construct the world YZ frame.

        Returns
        -------
        Frame
            The world YZ frame.

        """
        return cls([0, 0, 0], [0, 1, 0], [0, 0, 1])

    @classmethod
    def from_points(cls, point, point_xaxis, point_xyplane):
        """Constructs a frame from 3 points.

        Parameters
        ----------
        point : point
            The origin of the frame.
        point_xaxis : point
            A point on the x-axis of the frame.
        point_xyplane : point
            A point within the xy-plane of the frame.

        Returns
        -------
        Frame
            The constructed frame.

        Examples
        --------
        >>> f = Frame.from_points([1, 1, 1], [2, 4, 5], [4, 2, 3])

        """
        xaxis = subtract_vectors(point_xaxis, point)
        xyvec = subtract_vectors(point_xyplane, point)
        yaxis = cross_vectors(cross_vectors(xaxis, xyvec), xaxis)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_rotation(cls, rotation, point=[0, 0, 0]):
        """Constructs a frame from a ``Rotation``.

        Parameters
        ----------
        rotation : :class:`Rotation`
            The rotation defines the orientation of the frame.
        point : :obj:`list` of :obj:`float`, optional
            The origin of the frame.
            Defaults to [0, 0, 0].

        Returns
        -------
        Frame
            The constructed frame.

        Examples
        --------
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> R = Rotation.from_frame(f1)
        >>> f2 = Frame.from_rotation(R, point = f1.point)
        >>> f1 == f2
        True

        """
        xaxis, yaxis = rotation.basis_vectors
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_transformation(cls, transformation):
        """Constructs a frame from a ``Transformation``.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation defines the orientation of the frame through the
            rotation and the origin through the translation.

        Returns
        -------
        Frame
            The constructed frame.

        Examples
        --------
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> f2 = Frame.from_transformation(T)
        >>> f1 == f2
        True

        """
        xaxis, yaxis = transformation.basis_vectors
        point = transformation.translation
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_matrix(cls, matrix):
        """Construct a frame from a matrix.

        Parameters
        ----------
        matrix : :obj:`list` of :obj:`list` of :obj:`float`
            The 4x4 transformation matrix in row-major order.

        Returns
        -------
        Frame
            The constructed frame.

        Examples
        --------
        >>> ea1 = [0.5, 0.4, 0.8]
        >>> M = matrix_from_euler_angles(ea1)
        >>> f = Frame.from_matrix(M)
        >>> ea2 = f.euler_angles()
        >>> allclose(ea1, ea2)
        True

        """
        sc, sh, a, point, p = decompose_matrix(matrix)
        R = matrix_from_euler_angles(a, static=True, axes='xyz')
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_list(cls, values):
        """Construct a frame from a list of 12 or 16 :obj:`float` values.

        Parameters
        ----------
        values : :obj:`list` of :obj:`float`
            The list of 12 or 16 values representing a 4x4 matrix.

        Returns
        -------
        Frame
            The constructed frame.

        Raises
        ------
        ValueError
            If the length of the list is neither 12 nor 16.

        Examples
        --------
        >>> f = Frame.from_list([-1.0,  0.0,  0.0, 8110,
                                  0.0,  0.0, -1.0, 7020,
                                  0.0, -1.0,  0.0, 1810])

        Notes
        -----
        Since the transformation matrix follows the row-major order, the
        translational components must be at the list's indices 3, 7, 11.

        """

        if len(values) == 12:
            values.extend([0., 0., 0., 1.])
        if len(values) != 16:
            raise ValueError(
                'Expected 12 or 16 floats but got %d' %
                len(values))

        matrix = [[0. for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                matrix[i][j] = float(values[i * 4 + j])

        return cls.from_matrix(matrix)

    @classmethod
    def from_quaternion(cls, quaternion, point=[0, 0, 0]):
        """Construct a frame from a rotation represented by quaternion coefficients.

        Parameters
        ----------
        quaternion : :obj:`list` of :obj:`float`
            Four numbers that represent the four coefficient values of a quaternion.
        point : :obj:`list` of :obj:`float`, optional
            The point of the frame.
            Defaults to [0, 0, 0].

        Returns
        -------
        Frame
            The constructed frame.

        Examples
        --------
        >>> q1 = [0.945, -0.021, -0.125, 0.303]
        >>> f = Frame.from_quaternion(q1, point = [1., 1., 1.])
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
        axis_angle_vector : :obj:`list` of :obj:`float`
            Three numbers that represent the axis of rotation and angle of
            rotation by its magnitude.
        point : :obj:`list` of :obj:`float`, optional
            The point of the frame.
            Defaults to [0, 0, 0].

        Returns
        -------
        Frame
            The constructed frame.

        Examples
        --------
        >>> aav1 = [-0.043, -0.254, 0.617]
        >>> f = Frame.from_axis_angle_vector(aav1, point = [0, 0, 0])
        >>> aav2 = f.axis_angle_vector
        >>> allclose(aav1, aav2)
        True

        """
        R = matrix_from_axis_angle_vector(axis_angle_vector)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_euler_angles(cls, euler_angles, static=True,
                          axes='xyz', point=[0, 0, 0]):
        """Construct a frame from a rotation represented by Euler angles.

        Parameters
        ----------
        euler_angles : :obj:`list` of :obj:`float`
            Three numbers that represent the angles of rotations about the defined axes.
        static : :obj:`bool`, optional
            If true the rotations are applied to a static frame.
            If not, to a rotational.
            Defaults to true.
        axes : :obj:`str`, optional
            A 3 character string specifying the order of the axes.
            Defaults to 'xyz'.
        point : :obj:`list` of :obj:`float`, optional
            The point of the frame.
            Defaults to [0, 0, 0].

        Returns
        -------
        Frame
            The constructed frame.

        Examples
        --------
        >>> ea1 = 1.4, 0.5, 2.3
        >>> f = Frame.from_euler_angles(ea1, static = True, axes = 'xyz')
        >>> ea2 = f.euler_angles(static = True, axes = 'xyz')
        >>> allclose(ea1, ea2)
        True

        """
        R = matrix_from_euler_angles(euler_angles, static, axes)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_data(cls, data):
        """Construct a frame from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        Frame
            The constructed frame.

        Examples
        --------
        >>>

        """
        frame = cls()
        frame.data = data
        return frame

    # ==========================================================================
    # descriptors
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
        self._yaxis = Vector.cross(zaxis, self.xaxis)

    @property
    def data(self):
        """:obj:`dict` : The data dictionary that represents the frame."""
        return {'point': self.point,
                'xaxis': self.xaxis,
                'yaxis': self.yaxis}

    @data.setter
    def data(self, data):
        self.point = data['point']
        self.xaxis = data['xaxis']
        self.yaxis = data['yaxis']

    def to_data(self):
        """Return the data dictionary that represents the frame.

        Returns
        -------
        dict
            The frame data.

        """
        return self.data

    @property
    def normal(self):
        """:class:`Vector` : The frame's normal (z-axis)."""
        return Vector(*cross_vectors(self.xaxis, self.yaxis))

    @property
    def zaxis(self):
        """:class:`Vector` : The frame's z-axis (normal)."""
        return self.normal

    @property
    def quaternion(self):
        """:obj:`list` of :obj:`float` : The 4 quaternion coefficients from the rotation given by the frame.
        """
        rotation = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return quaternion_from_matrix(rotation)

    @property
    def axis_angle_vector(self):
        """vector : The axis-angle vector from the rotation given by the frame."""
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return axis_angle_vector_from_matrix(R)

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return "Frame({0}, {1}, {2})".format(self.point, self.xaxis, self.yaxis)

    def __len__(self):
        return 3

    # ==========================================================================
    # access
    # ==========================================================================

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

    # ==========================================================================
    # comparison
    # ==========================================================================

    def __eq__(self, other, tol=1e-05):
        for v1, v2 in zip(self, other):
            for a, b in zip(v1, v2):
                if math.fabs(a - b) > tol:
                    return False
        return True

    # ==========================================================================
    # operators
    # ==========================================================================

    # ==========================================================================
    # inplace operators
    # ==========================================================================

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Make a copy of this ``Frame``.

        Returns
        -------
        Frame
            The copy.

        """
        cls = type(self)
        return cls(self.point.copy(), self.xaxis.copy(), self.yaxis.copy())

    # ==========================================================================
    # methods
    # ==========================================================================

    def euler_angles(self, static=True, axes='xyz'):
        """The Euler angles from the rotation given by the frame.

        Parameters
        ----------
        static : :obj:`bool`, optional
            If true the rotations are applied to a static frame.
            If not, to a rotational.
            Defaults to True.
        axes : :obj:`str`, optional
            A 3 character string specifying the order of the axes.
            Defaults to 'xyz'.

        Returns
        -------
        :obj:`list` of :obj:`float`
            Three numbers that represent the angles of rotations about the defined axes.

        Examples
        --------
        >>> ea1 = 1.4, 0.5, 2.3
        >>> f = Frame.from_euler_angles(ea1, static = True, axes = 'xyz')
        >>> ea2 = f.euler_angles(static = True, axes = 'xyz')
        >>> allclose(ea1, ea2)
        True

        """
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return euler_angles_from_matrix(R, static, axes)

    def represent_in_local_coordinates(self, point):
        """Represents a point in the frame's local coordinate system.

        Parameters
        ----------
        point : :obj:`list` of :obj:`float`
            A point in world XY.

        Returns
        -------
        :obj:`list` of :obj:`float`
            A point in the local coordinate system of the frame.

        Examples
        --------
        >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> pw1 = [2, 2, 2]
        >>> pf = f.represent_in_local_coordinates(pw1)
        >>> pw2 = f.represent_in_global_coordinates(pf)
        >>> allclose(pw1, pw2)
        True

        """
        pt = Point(*subtract_vectors(point, self.point))
        T = inverse(matrix_from_basis_vectors(self.xaxis, self.yaxis))
        pt.transform(T)
        return pt

    def represent_in_global_coordinates(self, point):
        """Represents a point from local coordinates in the world coordinate system.

        Parameters
        ----------
        point : :obj:`list` of :obj:`float`
            A point in local coordinates.

        Returns
        -------
        :obj:`list` of :obj:`float`
            A point in the world coordinate system.

        Examples
        --------
        >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> pw1 = [2, 2, 2]
        >>> pf = f.represent_in_local_coordinates(pw1)
        >>> pw2 = f.represent_in_global_coordinates(pf)
        >>> allclose(pw1, pw2)
        True

        """
        T = matrix_from_frame(self)
        pt = Point(*point)
        pt.transform(T)
        return pt

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, transformation):
        """Transform the frame.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the Frame.

        Examples
        --------
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> f2 = Frame.worldXY()
        >>> f2.transform(T)
        >>> f1 == f2
        True

        """
        T = transformation * Transformation.from_frame(self)
        point = T.translation
        xaxis, yaxis = T.basis_vectors
        self.point = point
        self.xaxis = xaxis
        self.yaxis = yaxis

    def transformed(self, transformation):
        """Returns a transformed copy of the current frame.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the Frame.

        Returns
        -------
        :class:`Frame`
            The transformed frame.

        Examples
        --------
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> f2 = Frame.worldXY()
        >>> f1 == f2.transformed(T)
        True

        """
        frame = self.copy()
        frame.transform(transformation)
        return frame


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    R = Rotation.from_frame(f1)
    f2 = Frame.from_rotation(R, point=f1.point)
    print(f1 == f2)

    print(f2)

    f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f1)
    f2 = Frame.from_transformation(T)
    print(f1 == f2)

    ea1 = [0.5, 0.4, 0.8]
    M = matrix_from_euler_angles(ea1)
    f = Frame.from_matrix(M)
    ea2 = f.euler_angles()
    print(allclose(ea1, ea2))

    q1 = [0.945, -0.021, -0.125, 0.303]
    f = Frame.from_quaternion(q1, point=[1., 1., 1.])
    q2 = f.quaternion
    print(allclose(q1, q2, tol=1e-03))

    aav1 = [-0.043, -0.254, 0.617]
    f = Frame.from_axis_angle_vector(aav1, point=[0, 0, 0])
    aav2 = f.axis_angle_vector
    print(allclose(aav1, aav2))

    ea1 = 1.4, 0.5, 2.3
    f = Frame.from_euler_angles(ea1, static=True, axes='xyz')
    ea2 = f.euler_angles(static=True, axes='xyz')
    print(allclose(ea1, ea2))

    f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f1)
    f2 = Frame.worldXY()
    f2.transform(T)
    print(f1 == f2)

    f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    pw1 = [2, 2, 2]
    pw1 = Point(*pw1)
    pf = f.represent_in_local_coordinates(pw1)
    pw2 = f.represent_in_global_coordinates(pf)
    print(allclose(pw1, pw2))
