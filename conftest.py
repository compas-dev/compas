import pytest
import compas
import math
import numpy

from compas.geometry import allclose


def pytest_ignore_collect(path):
    if "rhino" in str(path):
        return True

    if "blender" in str(path):
        return True

    if "ghpython" in str(path):
        return True

    if "matlab" in str(path):
        return True

    if str(path).endswith("_cli.py"):
        return True


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
