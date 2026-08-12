from pathlib import Path
import math
import numpy
import pytest

import compas
from compas.geometry import allclose


def pytest_ignore_collect(collection_path: Path, config):
    # Skip anything under rhino/blender/ghpython, or files ending with _cli.py
    parts_lower = {p.lower() for p in collection_path.parts}
    if {"rhino", "blender", "ghpython"} & parts_lower:
        return True

    if collection_path.name.endswith("_cli.py"):
        return True

    # return None -> don't ignore
    return None


@pytest.fixture(autouse=True)
def add_compas(doctest_namespace):
    doctest_namespace["compas"] = compas


@pytest.fixture(autouse=True)
def add_math(doctest_namespace):
    doctest_namespace["math"] = math


@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace["np"] = numpy


@pytest.fixture(autouse=True)
def add_allclose(doctest_namespace):
    doctest_namespace["allclose"] = allclose
