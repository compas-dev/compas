import pytest
import json
import compas
from random import random

from compas.geometry import Point  # noqa: F401
from compas.geometry import Vector  # noqa: F401
from compas.geometry import Frame
from compas.geometry import PlanarSurface
from compas.geometry import close


# =============================================================================
# Constructors
# =============================================================================


@pytest.mark.parametrize(
    "xsize,ysize",
    [
        (0, 0),
        (1, 0),
        (0, 1),
        (1, 1),
        (random(), random()),
    ],
)
def test_plane(xsize, ysize):
    plane = PlanarSurface(xsize=xsize, ysize=ysize)

    assert plane.xsize == xsize
    assert plane.ysize == ysize
    assert plane.frame == Frame.worldXY()

    other = eval(repr(plane))

    assert close(plane.xsize, other.xsize, tol=1e-12)
    assert close(plane.ysize, other.ysize, tol=1e-12)
    assert plane.frame == other.frame


# =============================================================================
# Data
# =============================================================================


def test_plane_data():
    xsize = random()
    ysize = random()
    plane = PlanarSurface(xsize=xsize, ysize=ysize)
    other = PlanarSurface.from_data(json.loads(json.dumps(plane.data)))

    assert plane.data == other.data
    assert plane.xsize == xsize
    assert plane.ysize == ysize
    assert plane.frame == Frame.worldXY()

    if not compas.IPY:
        assert PlanarSurface.validate_data(plane.data)
        assert PlanarSurface.validate_data(other.data)


# =============================================================================
# Properties and Geometry
# =============================================================================

# =============================================================================
# Accessors
# =============================================================================

# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================
