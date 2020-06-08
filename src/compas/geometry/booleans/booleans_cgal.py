from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    from compas_cgal.booleans import boolean_union
    from compas_cgal.booleans import boolean_difference
    from compas_cgal.booleans import boolean_intersection
except ImportError:
    pass


from compas.exceptions import PluginNotInstalledError


__all__ = [
    'boolean_union_mesh_mesh',
    'boolean_difference_mesh_mesh',
    'boolean_intersection_mesh_mesh',
]


def boolean_union_mesh_mesh(A, B, remesh=False):
    """Compute the boolean union of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Raises
    ------
    PluginNotInstalledError
        If :mod:`compas_cgal` is not installed.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean union.

    Examples
    --------
    >>>
    """
    try:
        boolean_union
    except NameError:
        raise PluginNotInstalledError('Plugin compas_cgal is not installed.')
    return boolean_union(A, B, remesh=remesh)


def boolean_difference_mesh_mesh(A, B, remesh=False):
    """Compute the boolean difference of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Raises
    ------
    PluginNotInstalledError
        If :mod:`compas_cgal` is not installed.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean difference.

    Examples
    --------
    >>>
    """
    try:
        boolean_difference
    except NameError:
        raise PluginNotInstalledError('Plugin compas_cgal is not installed.')
    return boolean_difference(A, B, remesh=remesh)


def boolean_intersection_mesh_mesh(A, B, remesh=False):
    """Compute the boolean intersection of two triangle meshes.

    Parameters
    ----------
    A : tuple
        The vertices and faces of mesh A.
    B : tuple
        The vertices and faces of mesh B.
    remesh : bool, optional
        Remesh the result if ``True``.
        Default is ``False``.

    Raises
    ------
    PluginNotInstalledError
        If :mod:`compas_cgal` is not installed.

    Returns
    -------
    tuple
        The vertices and the faces of the boolean intersection.

    Examples
    --------
    >>>
    """
    try:
        boolean_intersection
    except NameError:
        raise PluginNotInstalledError('Plugin compas_cgal is not installed.')
    return boolean_intersection(A, B, remesh=remesh)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
