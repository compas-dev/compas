import io
import math
import os

import pytest

from compas.files import _iotools

BASE_FOLDER = os.path.dirname(__file__)
IMAGE_FILE_SIZE = 252391
TEXT_FILE_SIZE = 747
REMOTE_IMAGE_FILE_SIZE = 373


@pytest.fixture
def path_image():
    return os.path.join(BASE_FOLDER, 'fixtures', 'iotools', 'image.png')


@pytest.fixture
def path_text():
    return os.path.join(BASE_FOLDER, 'fixtures', 'iotools', 'text.txt')


@pytest.fixture
def url_text():
    return 'https://raw.githubusercontent.com/compas-dev/compas/master/README.md'


@pytest.fixture
def url_image():
    return 'https://via.placeholder.com/150'


def test_open_file_path_binary(path_image):
    with _iotools.open_file(path_image, mode='rb') as file:
        assert len(file.read()) == IMAGE_FILE_SIZE


def test_open_file_path_text(path_text):
    with _iotools.open_file(path_text, mode='r') as file:
        assert len(file.read()) == TEXT_FILE_SIZE


def test_open_file_object_binary(path_image):
    with open(path_image, mode='rb') as f:
        with _iotools.open_file(f) as file:
            assert len(file.read()) == IMAGE_FILE_SIZE


def test_open_file_object_text(path_text):
    with open(path_text, mode='r') as f:
        with _iotools.open_file(f) as file:
            assert len(file.read()) == TEXT_FILE_SIZE


def test_open_file_memory_stream():
    text = b"How many roads must a man walk down?"
    data = io.BytesIO(text)
    with _iotools.open_file(data, mode='rb') as f:
        assert f.read() == text


def test_open_file_url_image(url_image):
    with _iotools.open_file(url_image) as file:
        assert len(file.read()) == REMOTE_IMAGE_FILE_SIZE


def test_open_file_url_text(url_text):
    with _iotools.open_file(url_text) as file:
        assert b'COMPAS framework' in file.read()


def test_iter_file_chunks_path_image(path_image):
    CHUNK_SIZE = 30
    chunks = []

    with _iotools.open_file(path_image, 'rb') as file:
        for data in _iotools.iter_file(file, size=CHUNK_SIZE):
            chunks.append(data)

    assert len(chunks) == math.ceil(IMAGE_FILE_SIZE / CHUNK_SIZE)
