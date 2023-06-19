import os
import sys
import subprocess

import compas
import compas_blender

from compas._os import remove
from compas._os import remove_symlink
from compas._os import rename


BOOTSTRAPPER_TEMPLATE = """
import os
import sys

import bpy

ENVIRONMENT_NAME = r"{}"
PYTHON_DIRECTORY = r"{}"

def register():
    pass

def unregister():
    pass

"""


def install_windows(blender_path, version=None, packages=None, force_reinstall=False, no_deps=False):
    """Install COMPAS for Blender on Windows.

    Parameters
    ----------
    blender_path : str
        The path to the folder with the version number of Blender.
        For example, on Mac: ``'/Applications/Blender.app/Contents/Resources/2.83'``.
        On Windows: ``'%PROGRAMFILES%/Blender Foundation/Blender 2.83/2.83'``.
    version : {'2.83', '2.93', '3.1'}, optional
        The version number of Blender.
        Default is ``'2.93'``.
    packages : list[str], optional
        Additional packages to install.
        Note that the packages should be available on the Python Package Index (PyPI).
    force_reinstall : bool, optional
        Force existing packages to be reinstalled.
    no_deps : bool, optional
        Ignore requirements of the specified packages during installation.

    Examples
    --------
    .. code-block:: bash

        $ python -m compas_blender.install

    .. code-block:: bash

        $ python -m compas_blender.install -v 2.93

    .. code-block:: bash

        $ python -m compas_blender.install /Applications/Blender.app/Contents/Resources/2.93

    """
    if not compas.WINDOWS:
        print(
            "This install procedure is only suited for installations on Windows. Please use the basic install instead..."
        )
        sys.exit(-1)

    if not version and not blender_path:
        version = "2.93"

    if version and blender_path:
        print(
            "Both options cannot be provided simultaneously. Provide the full installation path, or the version with flag -v."
        )
        sys.exit(-1)

    if version:
        if compas.LINUX:
            print(
                "Version-based installs are currently not supported for Linux. Please provide the full installation path with the -p option."
            )
            sys.exit(-1)

        blender_path = compas_blender._get_default_blender_installation_path(version)

    if not os.path.exists(blender_path):
        raise FileNotFoundError("Blender version folder not found.")

    path, version = os.path.split(blender_path)

    print("Installing COMPAS for Blender {}".format(version))

    startup = os.path.join(blender_path, "scripts", "startup")

    blenderpython_src = os.path.join(blender_path, "python")
    blenderpython_dst = os.path.join(blender_path, "original_python")
    compas_bootstrapper = os.path.join(startup, "compas_bootstrapper.py")

    if os.path.exists(blenderpython_dst):
        print("Found existing installation, restoring bundled python installation...")
        if os.path.exists(blenderpython_src):
            remove_symlink(blenderpython_src)

        print(
            "  Renaming original_python back to bundled python folder: {} => {}".format(
                blenderpython_dst, blenderpython_src
            )
        )
        rename(blenderpython_dst, blenderpython_src)

    if os.path.exists(compas_bootstrapper):
        print("  Removing compas bootstrapper...")
        remove(compas_bootstrapper)

    # Install COMPAS by running a subprocess triggering pip
    blenderpython = os.path.join(blender_path, "python", "bin", "python.exe")

    try:
        subprocess.run([blenderpython, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    except subprocess.CalledProcessError:
        print("Could not upgrade pip")
        sys.exit(-1)

    try:
        args = [blenderpython, "-m", "pip", "install", "compas"]
        if packages:
            args += packages
        if force_reinstall:
            args.append("--force-reinstall")
        if no_deps:
            args.append("--no-deps")

        subprocess.run(args, check=True)
    except subprocess.CalledProcessError:
        print("Could not install compas or some of the requested additional packages.")
        sys.exit(-1)

    # # Take either the CONDA environment directory or the current Python executable's directory
    # python_directory = os.environ.get("CONDA_PREFIX", None) or os.path.dirname(
    #     sys.executable
    # )
    # environment_name = os.environ.get("CONDA_DEFAULT_ENV", "")

    # Get current sys.version value, we will override it inside Blender
    # because it seems Blender overrides it as well, but doing so breaks many things after having replaced the Python interpreter

    # _handle, bootstrapper_temp_path = tempfile.mkstemp(suffix=".py", text=True)

    # with open(bootstrapper_temp_path, "w") as f:
    #     f.write(BOOTSTRAPPER_TEMPLATE.format(environment_name, python_directory))

    # print("  Creating bootstrap script: {}".format(compas_bootstrapper))
    # copy(bootstrapper_temp_path, compas_bootstrapper)

    print()
    print("COMPAS for Blender {} has been installed via pip.".format(version))
    print("Note that functionaliy of conda-only packages has to be run via the command server (RPC).")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "blenderpath",
        nargs="?",
        help="The path to the folder with the version number of Blender.",
    )
    parser.add_argument(
        "-v",
        "--version",
        choices=["2.83", "2.93", "3.1"],
        help="The version of Blender to install COMPAS in.",
    )
    parser.add_argument("-p", "--packages", nargs="+", help="The packages to install.")
    parser.add_argument("--force-reinstall", dest="force_reinstall", default=False, action="store_true")
    parser.add_argument("--no-deps", dest="no_deps", default=False, action="store_true")

    args = parser.parse_args()

    install_windows(
        args.blenderpath,
        version=args.version,
        packages=args.packages,
        force_reinstall=args.force_reinstall,
        no_deps=args.no_deps,
    )
