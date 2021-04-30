import pytest
import compas
import math
import numpy


def pytest_ignore_collect(path):
    if str(path).endswith('_rhino.py'):
        return True

    if str(path).endswith('_cli.py'):
        return True

    if str(path).endswith('matlab/client.py'):
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
