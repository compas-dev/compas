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


@pytest.fixture
def binary_stl_with_ascii_header():
    return os.path.join(BASE_FOLDER, 'fixtures', 'binary-1.stl')


@pytest.fixture
def binary_stl():
    return os.path.join(BASE_FOLDER, 'fixtures', 'binary-2.stl')


@pytest.fixture
def ascii_stl():
    return os.path.join(BASE_FOLDER, 'fixtures', 'ascii.stl')


@pytest.fixture
def pathobj_boxes_obj():
    return Path.cwd().joinpath('data/boxes.obj')


@pytest.fixture
def binary_ply():
    return os.path.join(BASE_FOLDER, 'fixtures', 'triangle_binary.ply')


def test_iterate_over_ascii_file(ascii_ply):
    ply = BaseReader(ascii_ply)
    assert len(list(ply.iter_lines())) == 23598


def test_iterate_over_downloaded_file(url_to_faces_obj, first_five_lines_of_faces_obj):
    url_faces = BaseReader(url_to_faces_obj)
    five_lines_from_url = []

    for i, line in enumerate(url_faces.iter_lines()):
        five_lines_from_url.append(line)
        if i >= 4:
            break

    assert five_lines_from_url == first_five_lines_of_faces_obj


def test_iterate_over_binary_file(binary_stl):
    binary_file = BaseReader(binary_stl)

    two_chunks = []

    for i, chunk in enumerate(binary_file.iter_chunks(chunk_size=80)):
        two_chunks.append(chunk)
        if i >= 1:
            break

    assert two_chunks[0] == b'dilos link_6                                                                    '
    assert two_chunks[1][:5] == b'\x9a%\x00\x00\x8b'


def open_nonexistant_file():
    not_a_file = BaseReader('not_a_file')
    print(not_a_file.location)


def test_open_nonexistant_file():
    with pytest.raises(FileNotFoundError):
        open_nonexistant_file()


def test_location_from_string_adress(ascii_ply):
    file = BaseReader(ascii_ply)
    assert isinstance(file.location, Path)


def test_location_from_url(url_to_faces_obj):
    file = BaseReader(url_to_faces_obj)
    assert isinstance(file.location, Path)


def test_location_from_pathobj(pathobj_boxes_obj):
    file = BaseReader(pathobj_boxes_obj)
    assert file.location == pathobj_boxes_obj


def test_file_signature_check(binary_ply):
    ply = BaseReader(binary_ply)

    # Default offset is zero
    ply.FILE_SIGNATURE['content'] = b'ply'

    assert ply.is_file_signature_correct() is True


def test_is_binary_positive(binary_stl):
    stl = BaseReader(binary_stl)
    assert stl.is_binary is True


def test_is_binary_negative(ascii_stl):
    stl = BaseReader(ascii_stl)
    assert stl.is_binary is False


def test_is_binary_binary_w_ascii_header(binary_stl_with_ascii_header):
    stl = BaseReader(binary_stl_with_ascii_header)
    assert stl.is_binary is True
