from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_geodistance(M, source, method="exact"):
    """Compute the geodesic distance from every vertex of the mesh to a source vertex.

    Parameters
    ----------
    M : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    source : int
        The index of the vertex from where the geodesic distances should be calculated.
    method : Literal['exact', 'heat'], optional
        The method for calculating the distances.

    Returns
    -------
    list[float]
        A list of geodesic distances from the source vertex.

    Raises
    ------
    NotImplementedError
        If `method` is not one of ``{'exact', 'heat'}``.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


trimesh_geodistance.__pluggable__ = True
