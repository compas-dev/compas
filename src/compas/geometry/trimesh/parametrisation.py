from .._tessellation_plugin import tessellation_pluggable
from ..tessellation import Tessellation


@tessellation_pluggable(category="trimesh", inputs=("mesh",))
def trimesh_harmonic(mesh: "Tessellation") -> list[list[float]]:
    """Compute a harmonic parametrisation with a fixed circular boundary.

    Parameters
    ----------
    mesh
        The triangle tessellation.

    Returns
    -------
    list[list[float]]
        The UV coordinates in mesh vertex order.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError


@tessellation_pluggable(category="trimesh", inputs=("mesh",))
def trimesh_lscm(mesh: "Tessellation") -> list[list[float]]:
    """Compute a least-squares conformal parametrisation.

    Parameters
    ----------
    mesh
        The triangle tessellation.

    Returns
    -------
    list[list[float]]
        The UV coordinates in mesh vertex order.

    Notes
    -----
    This operation requires a registered plugin.

    """
    raise NotImplementedError
