from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .core import BaseMesh
from .core import mesh_collapse_edge
from .core import mesh_split_edge
from .core import mesh_split_face
from .core import mesh_merge_faces

from .bbox import mesh_bounding_box
from .bbox import mesh_bounding_box_xy
from .combinatorics import mesh_is_connected
from .combinatorics import mesh_connected_components
from .duality import mesh_dual
from .orientation import mesh_face_adjacency
from .orientation import mesh_flip_cycles
from .orientation import mesh_unify_cycles
from .slice import mesh_slice_plane
from .smoothing import mesh_smooth_centroid
from .smoothing import mesh_smooth_area
from .subdivision import mesh_subdivide
from .transformations import mesh_transform
from .transformations import mesh_transformed
from .triangulation import mesh_quads_to_triangles


__all__ = ['Mesh']


class Mesh(BaseMesh):
    """Data structure for the representation of and operation on polygonal meshes.

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)

    """

    def bounding_box(self):
        """Compute the axis-aligned bounding box of the mesh.

        Returns
        -------
        box: tuple of 8 points.
            The corners of the bounding box.
            The first 4 points are the corners of the bottom face, in counter clockwise direction wrt the positive Z-axis.
            The last 4 points are the corners of the top face, in counter clockwise direction wrt the positive Z-axis.

        """
        return mesh_bounding_box(self)

    def bounding_box_xy(self):
        """Compute the axis-aligned bounding box of the mesh in the XY plane.

        Returns
        -------
        box: tuple of 4 points.
            The corners of the bounding rectangle in the XY plane.
        """
        return mesh_bounding_box_xy(self)

    def collapse_edge(self, u, v, t=0.5, allow_boundary=False, fixed=None):
        """Collapse an edge to its first or second vertex, or to an intermediate point.

        Parameters
        ----------
        u : int
            The first vertex of the (half-) edge.
        v : int
            The second vertex of the (half-) edge.
        t : float, optional
            Default is ``0.5``.
            Determines where to collapse to.
            If ``t == 0.0`` collapse to ``u``.
            If ``t == 1.0`` collapse to ``v``.
            If ``0.0 < t < 1.0``, collapse to a point between ``u`` and ``v``.
        allow_boundary : bool, optional
            Default is ``False``.
            Allow collapses involving boundary vertices.
        fixed : list, optional
            A list of identifiers of vertices that should stay fixed.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If `u` and `v` are not neighbors.

        """
        return mesh_collapse_edge(self, u, v, t=t, allow_boundary=allow_boundary, fixed=fixed)

    connected_components = mesh_connected_components
    dual = mesh_dual
    face_adjacency = mesh_face_adjacency
    flip_cycles = mesh_flip_cycles
    is_connected = mesh_is_connected
    merge_faces = mesh_merge_faces
    slice_plane = mesh_slice_plane
    smooth_centroid = mesh_smooth_centroid
    smooth_area = mesh_smooth_area
    split_edge = mesh_split_edge
    split_face = mesh_split_face
    subdivide = mesh_subdivide
    transform = mesh_transform
    transformed = mesh_transformed
    unify_cycles = mesh_unify_cycles
    quads_to_triangles = mesh_quads_to_triangles


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod(globs=globals())
