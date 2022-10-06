import os
import shutil
import subprocess
import compas

from test_api_stability import get_names_in_module


def compas_api():
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


def compas_stubs():
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


def check_compas_stubs(api, stubs):
    for packmod in api:
        parts = packmod.split(".")
        if len(parts) != 2:
            continue
        assert packmod in stubs
        for name in api[packmod]:
            if name not in stubs[packmod]:
                print(packmod, name)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    check_compas_stubs(compas_api(), compas_stubs())
