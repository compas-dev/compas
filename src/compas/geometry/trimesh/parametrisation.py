from compas._typing import MeshType
from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_harmonic(mesh: MeshType) -> list[list[float]]:
    """Compute a harmonic parametrisation with a fixed circular boundary.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.

    Returns
    -------
    list[list[float]]
        The UV coordinates in mesh vertex order.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError


setattr(trimesh_harmonic, "__pluggable__", True)


@pluggable(category="trimesh")
def trimesh_lscm(mesh: MeshType) -> list[list[float]]:
    """Compute a least-squares conformal parametrisation.

    Parameters
    ----------
    mesh
        The mesh vertex coordinates and triangular faces.

    Returns
    -------
    list[list[float]]
        The UV coordinates in mesh vertex order.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError


setattr(trimesh_lscm, "__pluggable__", True)
