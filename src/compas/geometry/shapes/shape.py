from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import abc
from compas.geometry import Geometry
from compas.geometry import Frame
from compas.geometry import Transformation


class Shape(Geometry):
    """Base class for geometric shapes."""

    def __init__(self, frame=None, **kwargs):
        super(Shape, self).__init__(**kwargs)
        self._frame = None
        self.frame = frame

    @abc.abstractmethod
    def to_vertices_and_faces(self, triangulated=False):
        pass

    @property
    def frame(self):
        if not self._frame:
            raise ValueError("The shape has no coordinate frame.")
        return self._frame

    @frame.setter
    def frame(self, frame):
        if frame is None:
            self._frame = Frame.worldXY()
        else:
            self._frame = Frame(frame[0], frame[1], frame[2])

    @property
    def transformation(self):
        return Transformation.from_frame(self.frame)

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
        V, F = boolean_union_mesh_mesh(A, B)  # type: ignore
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
        V, F = boolean_difference_mesh_mesh(A, B)  # type: ignore
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
        V, F = boolean_intersection_mesh_mesh(A, B)  # type: ignore
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
