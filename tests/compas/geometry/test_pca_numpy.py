import compas


def _sliver_points():
    """An exactly planar but near-collinear cloud: long axis ~1, short in-plane
    axis ~1e-8, rotated off-axis. The plane (and its normal) are perfectly
    well defined; only an ill-conditioned fit loses them."""
    import numpy as np

    rng = np.random.default_rng(7)
    n = 200
    t = rng.uniform(-1.0, 1.0, n)
    s = rng.uniform(-1e-8, 1e-8, n)
    pts_local = np.column_stack([t, s, np.zeros(n)])

    a, b = 0.6, -1.1
    Rx = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    Rz = np.array([[np.cos(b), -np.sin(b), 0], [np.sin(b), np.cos(b), 0], [0, 0, 1]])
    R = Rz.dot(Rx)
    points = pts_local.dot(R.T) + np.array([100.0, -40.0, 7.0])
    normal = R.dot(np.array([0.0, 0.0, 1.0]))
    return points, normal


def test_pca_numpy_well_conditioned_matches_covariance_route():
    if compas.IPY:
        return

    import numpy as np

    from compas.geometry import pca_numpy

    rng = np.random.default_rng(42)
    points = rng.uniform(-10.0, 10.0, (100, 3))

    mean, eigenvectors, eigenvalues = pca_numpy(points)

    # eigenvalues must still be the variances along the principal directions
    Y = points - points.mean(axis=0)
    C = Y.T.dot(Y) / (len(points) - 1)
    expected = np.sort(np.linalg.eigvalsh(C))[::-1]
    assert np.allclose(eigenvalues, expected)

    # eigenvectors diagonalize the covariance matrix
    V = np.asarray(eigenvectors)
    assert np.allclose(V.dot(C).dot(V.T), np.diag(eigenvalues), atol=1e-12)

    assert np.allclose(mean, points.mean(axis=0))


def test_pca_numpy_near_collinear_recovers_smallest_direction():
    if compas.IPY:
        return

    import numpy as np

    from compas.geometry import pca_numpy

    points, normal = _sliver_points()

    _, eigenvectors, eigenvalues = pca_numpy(points)

    # the smallest principal direction is the plane normal (the cloud is
    # exactly planar); with the covariance route this was off by ~12 degrees
    smallest = np.asarray(eigenvectors)[2]
    angle = np.degrees(np.arccos(np.clip(abs(smallest.dot(normal)), -1.0, 1.0)))
    assert angle < 1e-4

    # eigenvalues are returned in descending order and non-negative
    assert eigenvalues[0] >= eigenvalues[1] >= eigenvalues[2] >= 0.0


def test_bestfit_plane_numpy_near_collinear():
    if compas.IPY:
        return

    import numpy as np

    from compas.geometry import bestfit_plane_numpy

    points, normal = _sliver_points()

    _, fitted_normal = bestfit_plane_numpy(points)

    fitted = np.asarray(fitted_normal, dtype=float)
    fitted = fitted / np.linalg.norm(fitted)
    angle = np.degrees(np.arccos(np.clip(abs(fitted.dot(normal)), -1.0, 1.0)))
    assert angle < 1e-4
