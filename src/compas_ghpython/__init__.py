import io
import os
import urllib
import zipfile

import compas
import compas_rhino

from compas_rhino import unload_modules  # noqa: F401


__version__ = "2.11.0"

__all__ = [
    "get_grasshopper_managedplugin_path",
    "get_grasshopper_library_path",
    "get_grasshopper_userobjects_path",
    "fetch_ghio_lib",
]
__all_plugins__ = [
    "compas_ghpython.install",
    "compas_ghpython.uninstall",
    "compas_ghpython.scene",
]


# =============================================================================
# General Helpers
# =============================================================================


def _get_grasshopper_special_folder(version, folder_name):
    grasshopper = compas_rhino._get_rhino_grasshopperplugin_path(version)
    return os.path.join(grasshopper, folder_name)


def create_id(component, name):
    """Creates an identifier string using `name` and the ID of the component passed to it.

    The resulting string can be used to store data elements in the global sticky dictionary.
    This can be useful when setting variable in a condition activated by a button.

    Parameters
    ----------
    components : `ghpythonlib.componentbase.executingcomponent`
        The components instance. Use `self` in advanced (SDK) mode and `ghenv.Components` otherwise.
    name : str
        A user chosen prefix for the identifier.

    Returns
    -------
    str
        For example: `somename55dd-c7cc-43c8-9d6a-65e4c8503abd`

    """
    return "{}_{}".format(name, component.InstanceGuid)


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

    else:
        raise NotImplementedError

    if not os.path.exists(gh_managedplugin_path):
        raise Exception("The Grasshopper (managed) Plug-in folder does not exist in this location: {}".format(gh_managedplugin_path))

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

    response = urllib.request.urlopen("https://www.nuget.org/api/v2/package/Grasshopper/")  # type: ignore
    dst_file = os.path.join(target_folder, ghio_dll)
    zip_file = zipfile.ZipFile(io.BytesIO(response.read()))

    with zip_file.open(filename, "r") as zipped_dll:
        with open(dst_file, "wb") as fp:
            fp.write(zipped_dll.read())

    return dst_file
