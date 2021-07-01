import io
import math
import os
import tempfile

import pytest

from compas import _iotools

BASE_FOLDER = os.path.dirname(__file__)
IMAGE_FILE_SIZE = 252391
TEXT_FILE_SIZE = 747
REMOTE_IMAGE_FILE_SIZE = 2734


@pytest.fixture
def path_image():
    return os.path.join(BASE_FOLDER, 'fixtures', 'iotools', 'image.png')


@pytest.fixture
def path_text():
    return os.path.join(BASE_FOLDER, 'fixtures', 'iotools', 'text.txt')


@pytest.fixture
def url_text():
    return 'https://raw.githubusercontent.com/compas-dev/compas/main/README.md'


@pytest.fixture
def url_image():
    return 'https://en.wikipedia.org/favicon.ico'


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
    text = b"All Gaul is divided into three parts, one of which the Belgae inhabit, the Aquitani another, those who in their own language are called Celts, in our Gauls, the third."
    data = io.BytesIO(text)
    with _iotools.open_file(data, mode='rb') as f:
        assert f.read() == text


def test_open_file_url_image(url_image):
    with _iotools.open_file(url_image) as file:
        assert len(file.read()) == REMOTE_IMAGE_FILE_SIZE


def test_open_file_url_text(url_text):
    with _iotools.open_file(url_text) as file:
        assert b'COMPAS framework' in file.read()


def test_open_file_url_as_write_fails(url_text):
    with pytest.raises(ValueError):
        with _iotools.open_file(url_text, mode='w') as _:
            pass


def test_iter_file_chunks_path_image(path_image):
    CHUNK_SIZE = 30
    chunks = []

    with _iotools.open_file(path_image, 'rb') as file:
        for data in _iotools.iter_file(file, size=CHUNK_SIZE):
            chunks.append(data)

    assert len(chunks) == math.ceil(IMAGE_FILE_SIZE / float(CHUNK_SIZE))


def test_open_file_write_path():
    path = os.path.join(tempfile.gettempdir(), 'test-file.txt')

    with _iotools.open_file(path, 'w') as file:
        file.write('Hello world')

    with _iotools.open_file(path, 'r') as file:
        assert file.read() == 'Hello world'


def test_open_file_write_file_object():
    path = os.path.join(tempfile.gettempdir(), 'test-file.txt')
    with open(path, mode='w') as f:
        with _iotools.open_file(f) as file:
            file.write('Hello world')

    with open(path, mode='r') as f:
        with _iotools.open_file(f) as file:
            assert file.read() == 'Hello world'


def test_open_file_does_not_close_file_objects(path_image):
    with open(path_image, mode='rb') as f:
        with _iotools.open_file(f):
            pass
        assert not f.closed
    assert f.closed


def test_open_file_closes_path_like(path_image):
    with _iotools.open_file(path_image, mode='rb') as file:
        assert not file.closed

    assert file.closed
