from compas.plugins import PluginNotInstalledError
from compas.plugins import pluggable
from compas.typing import FloatSequenceLike
from compas.typing import VerticesFaces


def trimesh_isolines(
    mesh: VerticesFaces,
    scalarfield: FloatSequenceLike,
    number_of_isolines: int = 50,
) -> tuple[list[list[float]], list[list[int]]]:
    """Compute isolines of a scalar field on a triangle mesh.

    Parameters
    ----------
    mesh
        The triangle mesh as vertices and triangles.
    scalarfield
        Scalar value at every mesh vertex.
    number_of_isolines
        Number of isolines.

    Returns
    -------
    tuple[list[list[float]], list[list[int]]]
        The generated point coordinates and the isoline segments as pairs of
        point indices.

    Notes
    -----
    This operation requires a registered plugin.

    """
    return _trimesh_isolines(mesh, scalarfield, number_of_isolines)


@pluggable(category="trimesh")
def _trimesh_isolines(
    mesh: VerticesFaces,
    scalarfield: FloatSequenceLike,
    number_of_isolines: int = 50,
) -> tuple[list[list[float]], list[list[int]]]:
    raise PluginNotInstalledError
