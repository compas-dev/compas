from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable
from compas.typing import VerticesFaces


def trimesh_harmonic(mesh: VerticesFaces) -> list[list[float]]:
    """Compute a harmonic parametrisation with a fixed circular boundary.

    Parameters
    ----------
    mesh
        The triangle mesh as vertices and triangles.

    Returns
    -------
    list[list[float]]
        The UV coordinates in mesh vertex order.

    Notes
    -----
    This operation requires a registered plugin.

    """
    return _trimesh_harmonic(mesh)


@pluggable(category="trimesh")
def _trimesh_harmonic(mesh: VerticesFaces) -> list[list[float]]:
    raise PluginNotInstalledError


def trimesh_lscm(mesh: VerticesFaces) -> list[list[float]]:
    """Compute a least-squares conformal parametrisation.

    Parameters
    ----------
    mesh
        The triangle mesh as vertices and triangles.

    Returns
    -------
    list[list[float]]
        The UV coordinates in mesh vertex order.

    Notes
    -----
    This operation requires a registered plugin.

    """
    return _trimesh_lscm(mesh)


@pluggable(category="trimesh")
def _trimesh_lscm(mesh: VerticesFaces) -> list[list[float]]:
    raise PluginNotInstalledError
