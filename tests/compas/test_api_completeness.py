from __future__ import absolute_import

import os
import pytest
import shutil
import subprocess
import importlib
import inspect
import compas


def get_names_in_module(module_name):
    exceptions = ["absolute_import", "division", "print_function"]
    module = importlib.import_module(module_name)
    all_names = module.__all__ if hasattr(module, "__all__") else dir(module)
    return sorted(
        [
            i
            for i in all_names
            if not i.startswith("_") and i not in exceptions and not inspect.ismodule(getattr(module, i))
        ]
    )


@pytest.fixture
def compas_api():
    if compas.IPY:
        return

    modules = [
        "compas.data",
        "compas.datastructures",
        "compas.files",
        "compas.geometry",
        "compas.numerical",
        "compas.plugins",
        "compas.robots",
        "compas.rpc",
        "compas.topology",
        "compas.utilities",
    ]
    api = {}
    for module_name in modules:
        api[module_name] = get_names_in_module(module_name)
    return api


@pytest.fixture
def compas_stubs():
    if compas.IPY:
        return

    env = compas._os.prepare_environment()

    HERE = os.path.dirname(__file__)
    HOME = os.path.abspath(os.path.join(HERE, "../.."))
    TEMP = os.path.abspath(os.path.join(HOME, "temp/stubs"))
    DOCS = os.path.abspath(os.path.join(HOME, "docs"))
    API = os.path.abspath(os.path.join(DOCS, "api"))

    shutil.rmtree(TEMP, ignore_errors=True)

    _, _, filenames = next(os.walk(API))
    stubs = []
    for name in filenames:
        if name == "compas.rst" or not name.startswith("compas."):
            continue
        stub = os.path.abspath(os.path.join(API, name))
        subprocess.call("sphinx-autogen -o {} {}".format(TEMP, stub), shell=True, env=env)

    _, _, filenames = next(os.walk(TEMP))

    shutil.rmtree(TEMP, ignore_errors=True)

    stubs = {}
    for name in filenames:
        parts = name.split(".")
        if len(parts) != 4:
            continue
        package = parts[0]
        module = parts[1]
        item = parts[2]
        if package == "compas":
            packmod = "{}.{}".format(package, module)
            if packmod not in stubs:
                stubs[packmod] = []
            stubs[packmod].append(item)

    return stubs


def test_compas_api_stubs(compas_api, compas_stubs):
    if compas.IPY:
        return

    for packmod in compas_api:
        parts = packmod.split(".")
        if len(parts) != 2:
            continue
        assert packmod in compas_stubs
        for name in compas_api[packmod]:
            if name in [
                "BaseMesh",
                "BaseNetwork",
                "BaseVolMesh",
                "Datastructure",
                "Graph",
                "HalfEdge",
                "HalfFace",
            ]:
                continue
            if parts[1] == "plugins":
                continue
            if parts[1] == "utilities":
                continue
            assert name in compas_stubs[packmod]
