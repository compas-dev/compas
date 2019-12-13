import os
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

import pytest

import compas
from compas.files.base_reader import BaseReader

REPO_ROOT = os.path.dirname(compas.__file__)
BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def ascii_ply():
    return os.path.join(BASE_FOLDER, 'fixtures', 'bigX_sphere.ply')


@pytest.fixture
def faces_obj():
    return os.path.join(REPO_ROOT, 'data', 'faces.obj')


@pytest.fixture
def url_to_faces_obj():
    return "https://raw.githubusercontent.com/compas-dev/compas/master/data/faces.obj"


@pytest.fixture
def first_five_lines_of_faces_obj():
    return ['# Rhino', '', 'v 0 0 0', 'v 2 0 0', 'v 4 0 0']


def test_iterate_over_ascii_file(ascii_ply):
    ply = BaseReader(ascii_ply)
    assert len(list(ply.iter_lines())) == 23598


def test_iterate_over_downloaded_ascii_file(url_to_faces_obj, first_five_lines_of_faces_obj):
    url_faces = BaseReader(url_to_faces_obj)
    five_lines_from_url = []

    for i, line in enumerate(url_faces.iter_lines()):
        five_lines_from_url.append(line)
        if i >= 4:
            break

    assert five_lines_from_url == first_five_lines_of_faces_obj


def test_file_signature_check():
    pass


def test_iterate_over_binary_file():
    pass


def test_iterate_over_downloaded_binary_file():
    pass
