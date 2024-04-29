from compas.plugins import pluggable


@pluggable(category="trimesh")
def trimesh_remesh(mesh, target_edge_length, number_of_iterations=10, do_project=True):
    """Remeshing of a triangle mesh.

    Parameters
    ----------
    mesh : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    target_edge_length : float
        The target edge length.
    number_of_iterations : int, optional
        Number of remeshing iterations.
    do_project : bool, optional
        Reproject vertices onto the input surface when they are created or displaced.

    Returns
    -------
    list[[float, float, float]]
        Vertices of the remeshed mesh.
    list[[int, int, int]]
        Faces of the remeshed mesh.

    Notes
    -----
    This remeshing function only constrains the edges on the boundary of the mesh.
    To protect specific features or edges, please use :func:`remesh_constrained`.

    """
    raise NotImplementedError


trimesh_remesh.__pluggable__ = True


@pluggable(category="trimesh")
def trimesh_remesh_constrained(mesh, target_edge_length, protected_edges, number_of_iterations=10, do_project=True):
    """Constrained remeshing of a triangle mesh.

    Parameters
    ----------
    mesh : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    target_edge_length : float
        The target edge length.
    protected_edges : list[[int, int]]
        A list of vertex pairs that identify protected edges of the mesh.
    number_of_iterations : int, optional
        Number of remeshing iterations.
    do_project : bool, optional
        Reproject vertices onto the input surface when they are created or displaced.

    Returns
    -------
    list[[float, float, float]]
        Vertices of the remeshed mesh.
    list[[int, int, int]]
        Faces of the remeshed mesh.

    """
    raise NotImplementedError


trimesh_remesh_constrained.__pluggable__ = True


@pluggable(category="trimesh")
def trimesh_remesh_along_isoline(mesh, scalarfield, scalar):
    """Remesh a mesh along an isoline of a scalarfield over the vertices.

    Parameters
    ----------
    mesh : tuple[sequence[[float, float, float] | :class:`compas.geometry.Point`], sequence[[int, int, int]]]
        A mesh represented by a list of vertices and a list of faces.
    scalarfield : sequence[float]
        A scalar value per vertex of the mesh.
    scalar : float
        A value within the range of the scalarfield.

    Returns
    -------
    list[[float, float, float]]
        Vertices of the remeshed mesh.
    list[[int, int, int]]
        Faces of the remeshed mesh.

    Examples
    --------
    >>>

    """
    raise NotImplementedError


trimesh_remesh_along_isoline.__pluggable__ = True
