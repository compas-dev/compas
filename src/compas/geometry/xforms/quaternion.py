from compas.geometry.transformations import quaternion_multiply
from compas.geometry.transformations import quaternion_conjugate
from compas.geometry.transformations import quaternion_unitize
from compas.geometry.transformations import quaternion_canonize
from compas.geometry.transformations import quaternion_norm
from compas.geometry.transformations import quaternion_is_unit

__all__ = ['Quaternion']


class Quaternion(object):

    """Creates a ``Quaternion`` object.

    Parameters
    ----------
    w (:obj:`float`): the scalar (real) part of a quaternion
    x, y, z (:obj:`float`): form the vector (complex, imaginary) part.
    """

    def __init__(self, w, x, y, z):

        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __iter__(self):
        return iter([self.w, self.x, self.y, self.z])

    def __str__(self):
        return "Quaternion = %s" % list(self)

    def __repr__(self):
        return 'Quaternion({:.{prec}f}, {:.{prec}f}, {:.{prec}f}, {:.{prec}f})'.format(*self, prec=6)

    def __mul__(self, other):
        """Multiply operator for two quaternions.

        Parameters
        ----------
        other
            A Quaternion object.

        Returns
        -------
        Quaternion
            The product P = R * Q of this quaternion (R) multiplied by other quaternion (Q).

        Examples
        --------
        >>> Q = Quaternion(1.0, 1.0, 1.0, 1.0).unitized
        >>> R = Quaternion(0.0,-0.1, 0.2,-0.3).unitized
        >>> P = R*Q
        >>> P.is_unit
        True

        Notes
        -----
        Multiplication of two quaternions R * Q can be interpreted as applying rotation R to an orientation Q,
        provided that both R and Q are unit-length.
        The result is also unit-length.
        Multiplication of quaternions is not commutative!

        """
        p = quaternion_multiply(list(self), list(other))
        return Quaternion(*p)

    @property
    def wxyz(self):
        """
        Returns the quaternion as a list in the "wxyz" convention.
        """
        return [self.w, self.x, self.y, self.z]

    @property
    def xyzw(self):
        """
        Returns the quaternion as a list in the "xyzw" convention.
        """
        return [self.x, self.y, self.z, self.w]

    @property
    def conjugate(self):
        """
        Returns a conjugate quaternion.
        """
        qc = quaternion_conjugate(list(self))
        return Quaternion(*qc)

    def unitize(self):
        """
        Scales the quaternion to make it unit-length.
        """
        qu = quaternion_unitize(list(self))
        self.w, self.x, self.y, self.z = qu

    @property
    def is_unit(self):
        """
        Returns ``True`` if the quaternion is unit-length or ``False`` if otherwise.
        """
        return quaternion_is_unit(list(self))

    @property
    def unitized(self):
        """
        Returns a quaternion with a unit-length.
        """
        qu = quaternion_unitize(list(self))
        return Quaternion(*qu)

    def canonize(self):
        """
        Makes the quaternion canonic.
        """
        qc = quaternion_canonize(list(self))
        self.w, self.x, self.y, self.z = qc

    @property
    def canonized(self):
        """
        Returns a quaternion in a canonic form.
        """
        qc = quaternion_canonize(list(self))
        return Quaternion(*qc)

    @property
    def norm(self):
        """
        Returns the length (euclidean norm) of the quaternion.
        """
        return quaternion_norm(list(self))


if __name__ == "__main__":
    import doctest
    doctest.testmod(globs=globals())
