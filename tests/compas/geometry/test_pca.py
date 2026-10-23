import numpy as np
import pytest

from compas.geometry import pca


def test_pca():
    mean, directions, variances = pca([[0, 0], [1, 0], [2, 0]])

    assert np.allclose(mean, [1, 0])
    assert np.allclose(np.abs(directions), [[1, 0], [0, 1]])
    assert np.allclose(variances, [1, 0])


def test_pca_requires_at_least_as_many_observations_as_variables():
    with pytest.raises(ValueError):
        pca([[0, 0, 0], [1, 1, 1]])
