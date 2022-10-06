import os
import sys
import compas

from compas._os import remove
from compas._os import remove_symlink
from compas._os import rename

import compas_blender

__all__ = ["uninstall"]


def uninstall(blender_path, version=None):
    """Uninstall COMPAS from Blender.

    Parameters
    ----------
    blender_path : str
        The path to the folder with the version number of Blender.
        For example, on Mac: ``'/Applications/Blender.app/Contents/Resources/2.83'``.
        On Windows: ``'%PROGRAMFILES%/Blender Foundation/Blender 2.83/2.83'``.
    version : {'2.83', '2.93', '3.1'}, optional
        The version number of Blender.
        Default is ``'2.93'``.

    Examples
    --------
    .. code-block:: bash

        $ python -m compas_blender.uninstall /Applications/blender.app/Contents/Resources/2.80

    """
    if not os.environ.get("CONDA_PREFIX"):
        print(
            "Conda environment not found. The installation into Blender requires an active conda environment with a matching Python version to continue."
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

    print("Uninstalling COMPAS for Blender {}".format(version))

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

    print()
    print("COMPAS has been uninstalled from Blender {}.".format(version))


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

    args = parser.parse_args()

    uninstall(args.blenderpath, version=args.version)
