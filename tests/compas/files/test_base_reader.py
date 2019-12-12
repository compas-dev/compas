import os
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

import pytest

from compas.files.base_reader import BaseReader

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def ascii_ply():
    return os.path.join(BASE_FOLDER, 'fixtures', 'bigX_sphere.ply')


def test_iterate_over_ascii_file(ascii_ply):
    ply = BaseReader(ascii_ply)
    assert len(list(ply.iter_lines())) == 23598
