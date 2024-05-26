from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable


@pluggable(category="contours")
def scalarfield_contours(xy, s, levels=50, density=100):
    r"""Compute the contour lines of a scalarfield.

    Parameters
    ----------
    xy : array-like
        The xy-coordinates at which the scalar field is defined.
    s : array-like
        The values of the scalar field.
    levels : int, optional
        The number of contour lines to compute.
        Default is ``50``.

    Returns
    -------
    tuple
        A tuple of a list of levels and a list of contour geometry.

        The list of levels contains the values of the scalarfield at each of
        the contours. The second item in the tuple is a list of contour lines.
        Each contour line is a list of paths, and each path is a list polygons.

    """
    raise PluginNotInstalledError()


scalarfield_contours.__pluggable__ = True
