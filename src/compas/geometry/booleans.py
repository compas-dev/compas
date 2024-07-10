from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable


@pluggable(category="booleans")
def boolean_union_mesh_mesh(A, B):
    """Compute the boolean union of two triangle meshes.

    Parameters
    ----------
    A : tuple[sequence[point], sequence[[int, int, int]]]
        The vertices and faces of mesh A.
    B : tuple[sequence[point], sequence[[int, int, int]]]
        The vertices and faces of mesh B.

    Returns
    -------
    tuple[list[point], list[[int, int, int]]]
        The vertices and the faces of the boolean union.

    See Also
    --------
    boolean_difference_mesh_mesh
    boolean_intersection_mesh_mesh

    Notes
    -----
    This function is a "pluggable".
    This means that it doesn't provide an implementation, but receives an implementation from a corresponding "plugin".
    To use the plugin implementation, you have to install it in the same environment as COMPAS.
    One such plugin is available in ``compas_cgal``.

    Examples
    --------
    >>> from compas.geometry import Box, Sphere
    >>> from compas.geometry import boolean_union_mesh_mesh  # doctest: +SKIP
    >>> from compas.geometry import trimesh_remesh  # doctest: +SKIP
    >>> from compas.datastructures import Mesh

    >>> box = Box.from_width_height_depth(2, 2, 2)
    >>> box = Mesh.from_shape(box)
    >>> box.quads_to_triangles()

    >>> sphere = Sphere(1, point=[1, 1, 1])
    >>> sphere = Mesh.from_shape(sphere, u=30, v=30)
    >>> sphere.quads_to_triangles()

    >>> A = box.to_vertices_and_faces()
    >>> B = sphere.to_vertices_and_faces()
    >>> B = trimesh_remesh(B, 0.3, 10)  # doctest: +SKIP

    >>> V, F = boolean_union_mesh_mesh(A, B)  # doctest: +SKIP
    >>> union = Mesh.from_vertices_and_faces(V, F)  # doctest: +SKIP

    """
    raise PluginNotInstalledError("No plugin was found for the boolean_union_mesh_mesh pluggable. A plugin is available in compas_cgal...")


boolean_union_mesh_mesh.__pluggable__ = True


@pluggable(category="booleans")
def boolean_difference_mesh_mesh(A, B):
    """Compute the boolean difference of two triangle meshes.

    Parameters
    ----------
    A : tuple[sequence[point], sequence[[int, int, int]]]
        The vertices and faces of mesh A.
    B : tuple[sequence[point], sequence[[int, int, int]]]
        The vertices and faces of mesh B.

    Returns
    -------
    tuple[list[point], list[[int, int, int]]]
        The vertices and the faces of the boolean difference.

    See Also
    --------
    boolean_union_mesh_mesh
    boolean_intersection_mesh_mesh

    Notes
    -----
    This function is a "pluggable".
    This means that it doesn't provide an implementation, but receives an implementation from a corresponding "plugin".
    To use the plugin implementation, you have to install it in the same environment as COMPAS.
    One such plugin is available in ``compas_cgal``.

    """
    raise PluginNotInstalledError("No plugin was found for the boolean_difference_mesh_mesh pluggable. A plugin is available in compas_cgal...")


boolean_difference_mesh_mesh.__pluggable__ = True


@pluggable(category="booleans")
def boolean_intersection_mesh_mesh(A, B):
    """Compute the boolean intersection of two triangle meshes.

    Parameters
    ----------
    A : tuple[sequence[point], sequence[[int, int, int]]]
        The vertices and faces of mesh A.
    B : tuple[sequence[point], sequence[[int, int, int]]]
        The vertices and faces of mesh B.

    Returns
    -------
    tuple[list[point], list[[int, int, int]]]
        The vertices and the faces of the boolean intersection.

    See Also
    --------
    boolean_union_mesh_mesh
    boolean_difference_mesh_mesh

    Notes
    -----
    This function is a "pluggable".
    This means that it doesn't provide an implementation, but receives an implementation from a corresponding "plugin".
    To use the plugin implementation, you have to install it in the same environment as COMPAS.
    One such plugin is available in ``compas_cgal``.

    """
    raise PluginNotInstalledError("No plugin was found for the boolean_intersection_mesh_mesh pluggable. A plugin is available in compas_cgal...")


boolean_intersection_mesh_mesh.__pluggable__ = True


@pluggable(category="booleans")
def boolean_union_polygon_polygon(A, B):
    """Compute the boolean union of two polygons.

    For this operation, the polygons are assumed to lie in the XY plane.
    Therefore, the Z components of the points defining the polygons are simply ignored.
    If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
    Otherwise the results are meaningless.

    Parameters
    ----------
    A : sequence[point]
        The vertices of polygon A.
    B : sequence[point]
        The vertices of polygon B.

    Returns
    -------
    list[point]
        The vertices of the boolean union.

    See Also
    --------
    boolean_difference_polygon_polygon
    boolean_intersection_polygon_polygon
    boolean_symmetric_difference_polygon_polygon

    Notes
    -----
    This function is a "pluggable".
    This means that it doesn't provide an implementation, but receives an implementation from a corresponding "plugin".
    To use the plugin implementation, you have to install it in the same environment as COMPAS.
    One such plugin is available through ``shapely``.

    """
    raise PluginNotInstalledError("No plugin was found for the boolean_union_polygon_polygon pluggable. Installing Shapely should solve the problem.")


boolean_union_polygon_polygon.__pluggable__ = True


@pluggable(category="booleans")
def boolean_difference_polygon_polygon(A, B):
    """Compute the boolean difference of two polygons.

    For this operation, the polygons are assumed to lie in the XY plane.
    Therefore, the Z components of the points defining the polygons are simply ignored.
    If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
    Otherwise the results are meaningless.

    Parameters
    ----------
    A : sequence[point]
        The vertices of polygon A.
    B : sequence[point]
        The vertices of polygon B.

    Returns
    -------
    list[point]
        The vertices of the boolean difference.

    See Also
    --------
    boolean_union_polygon_polygon
    boolean_intersection_polygon_polygon
    boolean_symmetric_difference_polygon_polygon

    Notes
    -----
    This function is a "pluggable".
    This means that it doesn't provide an implementation, but receives an implementation from a corresponding "plugin".
    To use the plugin implementation, you have to install it in the same environment as COMPAS.
    One such plugin is available through ``shapely``.

    """
    raise PluginNotInstalledError("No plugin was found for the boolean_difference_polygon_polygon pluggable. Installing Shapely should solve the problem.")


boolean_difference_polygon_polygon.__pluggable__ = True


@pluggable(category="booleans")
def boolean_symmetric_difference_polygon_polygon(A, B):
    """Compute the boolean symmetric difference of two polygons.

    For this operation, the polygons are assumed to lie in the XY plane.
    Therefore, the Z components of the points defining the polygons are simply ignored.
    If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
    Otherwise the results are meaningless.

    Parameters
    ----------
    A : sequence[point]
        The vertices of polygon A.
    B : sequence[point]
        The vertices of polygon B.

    Returns
    -------
    list[point]
        The vertices of the boolean symmetric difference.

    See Also
    --------
    boolean_union_polygon_polygon
    boolean_intersection_polygon_polygon
    boolean_difference_polygon_polygon

    Notes
    -----
    This function is a "pluggable".
    This means that it doesn't provide an implementation, but receives an implementation from a corresponding "plugin".
    To use the plugin implementation, you have to install it in the same environment as COMPAS.
    One such plugin is available through ``shapely``.

    """
    raise PluginNotInstalledError("No plugin was found for the boolean_symmetric_difference_polygon_polygon pluggable. Installing Shapely should solve the problem.")


boolean_symmetric_difference_polygon_polygon.__pluggable__ = True


@pluggable(category="booleans")
def boolean_intersection_polygon_polygon(A, B):
    """Compute the boolean intersection of two polygons.

    For this operation, the polygons are assumed to lie in the XY plane.
    Therefore, the Z components of the points defining the polygons are simply ignored.
    If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
    Otherwise the results are meaningless.

    Parameters
    ----------
    A : sequence[point]
        The vertices of polygon A.
    B : sequence[point]
        The vertices of polygon B.

    Returns
    -------
    list[point]
        The vertices of the boolean difference.

    See Also
    --------
    boolean_union_polygon_polygon
    boolean_difference_polygon_polygon
    boolean_symmetric_difference_polygon_polygon

    Notes
    -----
    This function is a "pluggable".
    This means that it doesn't provide an implementation, but receives an implementation from a corresponding "plugin".
    To use the plugin implementation, you have to install it in the same environment as COMPAS.
    One such plugin is available through ``shapely``.

    """
    raise PluginNotInstalledError("No plugin was found for the boolean_intersection_polygon_polygon pluggable. Installing Shapely should solve the problem.")


boolean_intersection_polygon_polygon.__pluggable__ = True
