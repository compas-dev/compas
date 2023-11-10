"""
********************************************************************************
compas_ghpython
********************************************************************************

.. currentmodule:: compas_ghpython

.. toctree::
    :maxdepth: 1

    compas_ghpython.artists
    compas_ghpython.utilities

"""
import io
import os
import urllib
import zipfile

import compas
import compas_rhino

__version__ = "1.17.9"

if compas.is_rhino():
    from .utilities import *  # noqa: F401 F403

__all__ = [
    "get_grasshopper_managedplugin_path",
    "get_grasshopper_library_path",
    "get_grasshopper_userobjects_path",
    "fetch_ghio_lib",
]
__all_plugins__ = [
    "compas_ghpython.install",
    "compas_ghpython.uninstall",
    "compas_ghpython.artists",
]


# =============================================================================
# General Helpers
# =============================================================================


def _get_grasshopper_special_folder(version, folder_name):
    grasshopper = compas_rhino._get_rhino_grasshopperplugin_path(version)
    return os.path.join(grasshopper, folder_name)


# =============================================================================
# Managed Plugin
# =============================================================================


def get_grasshopper_managedplugin_path(version):
    version = compas_rhino._check_rhino_version(version)
    managedplugins = compas_rhino._get_rhino_managedplugins_path(version)

    if compas.WINDOWS:
        gh_managedplugin_path = os.path.join(managedplugins, "Grasshopper")

    elif compas.OSX:
        gh_managedplugin_path = os.path.join(managedplugins, "GrasshopperPlugin.rhp")

    if not os.path.exists(gh_managedplugin_path):
        raise Exception(
            "The Grasshopper (managed) Plug-in folder does not exist in this location: {}".format(gh_managedplugin_path)
        )

    return gh_managedplugin_path


# =============================================================================
# GH Plugin Libraries path
# =============================================================================


def get_grasshopper_library_path(version):
    """Retrieve Grasshopper's library (components) path"""
    return _get_grasshopper_special_folder(version, "Libraries")


# =============================================================================
# GH Plugin UserObjects path
# =============================================================================


def get_grasshopper_userobjects_path(version):
    """Retrieve Grasshopper's user objects path"""
    return _get_grasshopper_special_folder(version, "UserObjects")


# =============================================================================
# GH_IO Dll
# =============================================================================


def fetch_ghio_lib(target_folder="temp"):
    """Fetch the GH_IO.dll library from the NuGet packaging system."""
    ghio_dll = "GH_IO.dll"
    filename = "lib/net48/" + ghio_dll

    response = urllib.request.urlopen("https://www.nuget.org/api/v2/package/Grasshopper/")
    dst_file = os.path.join(target_folder, ghio_dll)
    zip_file = zipfile.ZipFile(io.BytesIO(response.read()))

    with zip_file.open(filename, "r") as zipped_dll:
        with open(dst_file, "wb") as fp:
            fp.write(zipped_dll.read())

    return dst_file
