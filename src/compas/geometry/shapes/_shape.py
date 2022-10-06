from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import abc
from ..geometry import Geometry


class Shape(Geometry):
    """Base class for geometric shapes."""

    @abc.abstractmethod
    def to_vertices_and_faces(self, triangulated=False):
        pass

    def __add__(self, other):
        """Compute the boolean union using the "+" operator of this shape and another.

        Parameters
        ----------
        other : :class:`~compas.geometry.Shape`
            The solid to add.

        Returns
        -------
        :class:`~compas.geometry.Polyhedron`
            The resulting solid.

        Examples
        --------
        >>> from compas.geometry import Box, Sphere
        >>> A = Box.from_width_height_depth(2, 2, 2)
        >>> B = Sphere([1, 1, 1], 1.0)
        >>> C = A + B                                   # doctest: +SKIP

        """
        from compas.geometry import boolean_union_mesh_mesh
        from compas.geometry import Polyhedron

        A = self.to_vertices_and_faces(triangulated=True)
        B = other.to_vertices_and_faces(triangulated=True)
        V, F = boolean_union_mesh_mesh(A, B)
        return Polyhedron(V, F)

    def __sub__(self, other):
        """Compute the boolean difference using the "-" operator of this shape and another.

        Parameters
        ----------
        other : :class:`~compas.geometry.Shape`
            The solid to subtract.

        Returns
        -------
        :class:`~compas.geometry.Polyhedron`
            The resulting solid.

        Examples
        --------
        >>> from compas.geometry import Box, Sphere
        >>> A = Box.from_width_height_depth(2, 2, 2)
        >>> B = Sphere([1, 1, 1], 1.0)
        >>> C = A - B                                   # doctest: +SKIP

        """
        from compas.geometry import boolean_difference_mesh_mesh
        from compas.geometry import Polyhedron

        A = self.to_vertices_and_faces(triangulated=True)
        B = other.to_vertices_and_faces(triangulated=True)
        V, F = boolean_difference_mesh_mesh(A, B)
        return Polyhedron(V, F)

    def __and__(self, other):
        """Compute the boolean intersection using the "&" operator of this shape and another.

        Parameters
        ----------
        other : :class:`~compas.geometry.Shape`
            The solid to intersect with.

        Returns
        -------
        :class:`~compas.geometry.Polyhedron`
            The resulting solid.

        Examples
        --------
        >>> from compas.geometry import Box, Sphere
        >>> A = Box.from_width_height_depth(2, 2, 2)
        >>> B = Sphere([1, 1, 1], 1.0)
        >>> C = A & B                                   # doctest: +SKIP

        """
        from compas.geometry import boolean_intersection_mesh_mesh
        from compas.geometry import Polyhedron

        A = self.to_vertices_and_faces(triangulated=True)
        B = other.to_vertices_and_faces(triangulated=True)
        V, F = boolean_intersection_mesh_mesh(A, B)
        return Polyhedron(V, F)

    def __or__(self, other):
        """Compute the boolean union using the "|" operator of this shape and another.

        Parameters
        ----------
        other : :class:`~compas.geometry.Shape`
            The solid to add.

        Returns
        -------
        :class:`~compas.geometry.Polyhedron`
            The resulting solid.

        Examples
        --------
        >>> from compas.geometry import Box, Sphere
        >>> A = Box.from_width_height_depth(2, 2, 2)
        >>> B = Sphere([1, 1, 1], 1.0)
        >>> C = A | B                                   # doctest: +SKIP

        """
        return self.__add__(other)
