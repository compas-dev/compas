from __future__ import absolute_import

import io
import os

import compas
import compas._os
from compas_rhino.devtools import DevTools

__version__ = "2.11.0"


PURGE_ON_DELETE = True

INSTALLABLE_PACKAGES = ["compas", "compas_rhino", "compas_ghpython"]
SUPPORTED_VERSIONS = ["5.0", "6.0", "7.0", "8.0"]
DEFAULT_VERSION = "8.0"
INSTALLED_VERSION = None

INSTALLATION_ARGUMENTS = None

IRONPYTHON_PLUGIN_GUID = "814d908a-e25c-493d-97e9-ee3861957f49"
GRASSHOPPER_PLUGIN_GUID = "b45a29b1-4343-4035-989e-044e8580d9cf"
RHINOCYCLES_PLUGIN_GUID = "9bc28e9e-7a6c-4b8f-a0c6-3d05e02d1b97"

unload_modules = DevTools.unload_modules

__all__ = [
    "PURGE_ON_DELETE",
    "INSTALLABLE_PACKAGES",
    "SUPPORTED_VERSIONS",
    "DEFAULT_VERSION",
    "INSTALLED_VERSION",
    "IRONPYTHON_PLUGIN_GUID",
    "GRASSHOPPER_PLUGIN_GUID",
    "RHINOCYCLES_PLUGIN_GUID",
    "clear",
    "redraw",
    "unload_modules",
]

__all_plugins__ = [
    "compas_rhino.geometry.booleans",
    "compas_rhino.geometry.trimesh_curvature",
    "compas_rhino.geometry.trimesh_slicing",
    "compas_rhino.install",
    "compas_rhino.uninstall",
    "compas_rhino.scene",
    "compas_rhino.geometry.curves",
    "compas_rhino.geometry.surfaces",
    "compas_rhino.geometry.brep",
]


# =============================================================================
# =============================================================================
# =============================================================================
# General helpers
# =============================================================================
# =============================================================================
# =============================================================================


def clear(guids=None):
    import compas_rhino.objects

    if guids is None:
        guids = compas_rhino.objects.get_objects()
    compas_rhino.objects.delete_objects(guids, purge=True)


def redraw():
    import rhinoscriptsyntax as rs  # type: ignore

    rs.EnableRedraw(True)
    rs.Redraw()


def _check_rhino_version(version):
    if not version:
        return DEFAULT_VERSION

    if version not in SUPPORTED_VERSIONS:
        raise Exception("Unsupported Rhino version: {}".format(version))

    return version


def _get_package_path(package):
    return os.path.abspath(os.path.dirname(package.__file__))


# =============================================================================
# =============================================================================
# =============================================================================
# Bootstrapper
# =============================================================================
# =============================================================================
# =============================================================================


def _get_bootstrapper_path(install_path):
    return os.path.join(install_path, "compas_bootstrapper.py")


def _get_bootstrapper_data(compas_bootstrapper):
    data = {}

    if not os.path.exists(compas_bootstrapper):
        return data

    content = io.open(compas_bootstrapper, encoding="utf8").read()
    exec(content, data)

    return data


def _try_remove_bootstrapper(path):
    """Try to remove bootstrapper.

    Returns
    -------
    bool: True if the operation did not cause errors, False otherwise.
    """

    bootstrapper = _get_bootstrapper_path(path)

    if os.path.exists(bootstrapper):
        try:
            os.remove(bootstrapper)
            return True
        except:  # noqa: E722
            return False
    return True


# =============================================================================
# =============================================================================
# =============================================================================
# Rhino executable
# =============================================================================
# =============================================================================
# =============================================================================


# def _get_default_rhino_executable_path(version):
#     version = _check_rhino_version(version)

#     if compas.WINDOWS:
#         path = _get_default_rhino_executable_path_windows(version)

#     elif compas.OSX:
#         path = _get_default_rhino_executable_path_mac(version)

#     else:
#         raise Exception("Unsupported platform")

#     if not os.path.exists(path):
#         path = None

#     return path


# def _get_default_rhino_executable_path_mac(version):
#     if version == "8.0":
#         return "/Applications/Rhino 8.app/Contents/MacOS/Rhinoceros"
#     raise NotImplementedError


# def _get_default_rhino_executable_path_windows(version):
#     raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# Base Application folder (Program Files on Windows and Applications on Mac)
# =============================================================================
# =============================================================================
# =============================================================================


def _get_rhino_application_folder(version):
    version = _check_rhino_version(version)
    version = version.split(".")[0]  # take the major only

    if compas.WINDOWS:
        app = os.path.join(os.getenv("ProgramFiles"), "Rhino {}".format(version))  # type: ignore

    elif compas.OSX:
        paths = {
            "5": ["/", "Applications", "Rhinoceros.app"],
            "6": ["/", "Applications", "Rhinoceros.app"],
            "7": [
                "/",
                "Applications",
                "Rhino 7.app",
            ],
            "8": [
                "/",
                "Applications",
                "Rhino 8.app",
            ],
        }
        app = os.path.join(*paths[version])

    else:
        raise Exception("Unsupported platform")

    if not os.path.exists(app):
        raise Exception("The application folder does not exist in this location: {}".format(app))

    return app


# =============================================================================
# =============================================================================
# =============================================================================
# Base AppData folder (APPDATA on Windows and Application Support on Mac)
# =============================================================================
# =============================================================================
# =============================================================================


def _get_rhino_appdata_folder():
    if compas.WINDOWS:
        app = os.path.join(os.getenv("APPDATA"), "McNeel", "Rhinoceros")  # type: ignore

    elif compas.OSX:
        app = os.path.join(os.getenv("HOME"), "Library", "Application Support", "McNeel", "Rhinoceros")  # type: ignore

    else:
        raise Exception("Unsupported platform")

    if not os.path.exists(app):
        raise Exception("The appdata folder does not exist in this location: {}".format(app))

    return app


# =============================================================================
# =============================================================================
# =============================================================================
# Scripts folder
# =============================================================================
# =============================================================================
# =============================================================================


def _get_rhino_scripts_path(version):
    appdata = _get_rhino_appdata_folder()
    version = _check_rhino_version(version)
    scripts_path = os.path.join(appdata, "{}".format(version), "scripts")

    if not os.path.exists(scripts_path):
        raise Exception("The scripts folder does not exist in this location: {}".format(scripts_path))

    return scripts_path


# =============================================================================
# =============================================================================
# =============================================================================
# Managed Plugins folder
# =============================================================================
# =============================================================================
# =============================================================================


def _get_rhino_managedplugins_path(version):
    app = _get_rhino_application_folder(version)

    if compas.WINDOWS:
        managedplugins_path = os.path.join(app, "Plug-ins")

    elif compas.OSX:
        managedplugins_path = os.path.join(
            app,
            "Contents",
            "Frameworks",
            "RhCore.framework",
            "Versions",
            "A",
            "Resources",
            "ManagedPlugIns",
        )
    else:
        raise Exception("Unsupported platform")

    if not os.path.exists(managedplugins_path):
        raise Exception("The Managed Plug-ins folder does not exist in this location: {}".format(managedplugins_path))

    return managedplugins_path


# =============================================================================
# =============================================================================
# =============================================================================
# Plugins folder
# =============================================================================
# =============================================================================
# =============================================================================


def _get_rhino_plugins_path(version):
    appdata = _get_rhino_appdata_folder()
    version = _check_rhino_version(version)

    if compas.WINDOWS:
        plugins_path = os.path.join(appdata, "{}".format(version), "Plug-ins")

    elif compas.OSX:
        if version == "5.0":
            plugins_path = os.path.join(appdata, "MacPlugIns")
        else:
            plugins_path = os.path.join(appdata, "{}".format(version), "Plug-ins")

    else:
        raise Exception("Unsupported platform")

    if not os.path.exists(plugins_path):
        raise Exception("The plugins folder does not exist in this location: {}".format(plugins_path))

    return plugins_path


# =============================================================================
# =============================================================================
# =============================================================================
# PythonPlugins folder
# =============================================================================
# =============================================================================
# =============================================================================


def _get_rhino_pythonplugins_path(version):
    version = _check_rhino_version(version)
    return os.path.join(_get_rhino_plugins_path(version), "PythonPlugins")


# =============================================================================
# =============================================================================
# =============================================================================
# IronPython Plugin
# =============================================================================
# =============================================================================
# =============================================================================


def _get_rhino_ironpythonplugin_path(version):
    version = _check_rhino_version(version)
    return os.path.join(
        _get_rhino_plugins_path(version),
        "IronPython ({})".format(IRONPYTHON_PLUGIN_GUID),
    )


# =============================================================================
# =============================================================================
# =============================================================================
# Grasshopper
# =============================================================================
# =============================================================================
# =============================================================================


def _get_rhino_grasshopperplugin_path(version):
    version = _check_rhino_version(version)

    if compas.WINDOWS:
        gh_path = os.path.join(os.getenv("APPDATA"), "Grasshopper")  # type: ignore

    elif compas.OSX:
        gh_path = os.path.join(
            _get_rhino_plugins_path(version),
            "Grasshopper ({})".format(GRASSHOPPER_PLUGIN_GUID),
        )

    else:
        raise Exception("Unsupported platform")

    if not os.path.exists(gh_path):
        raise Exception("The grasshopper folder does not exist in this location: {}".format(gh_path))

    return gh_path


# =============================================================================
# =============================================================================
# =============================================================================
# Rhino IronPython
# =============================================================================
# =============================================================================
# =============================================================================


# def _get_default_rhino_ironpython_path(version):
#     version = _check_rhino_version(version)

#     if compas.WINDOWS:
#         path = _get_default_rhino_ironpython_path_windows(version)

#     elif compas.OSX:
#         path = _get_default_rhino_ironpython_path_mac(version)

#     else:
#         raise Exception("Unsupported platform")

#     if not os.path.exists(path):
#         path = None

#     return path


# def _get_default_rhino_ironpython_path_mac(version):
#     raise NotImplementedError


# def _get_default_rhino_ironpython_path_windows(version):
#     raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# Rhino CPython
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_rhino_cpython_path(version):
    version = _check_rhino_version(version)

    if version != "8.0":
        raise NotImplementedError

    if compas.WINDOWS:
        path = _get_default_rhino_cpython_path_windows(version)

    elif compas.OSX:
        path = _get_default_rhino_cpython_path_mac(version)

    else:
        raise Exception("Unsupported platform")

    if not os.path.exists(path):
        path = None

    return path


def _get_default_rhino_cpython_path_windows(version):
    if version == "8.0":
        return os.path.abspath("{}/.rhinocode/py39-rh8/python.exe".format(os.path.expanduser("~")))
    raise NotImplementedError


def _get_default_rhino_cpython_path_mac(version):
    if version == "8.0":
        return os.path.abspath("{}/.rhinocode/py39-rh8/python3.9".format(os.path.expanduser("~")))
    raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# Rhino IronPython site-packages
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_rhino_ironpython_sitepackages_path(version):
    version = _check_rhino_version(version)

    if version != "8.0":
        raise NotImplementedError

    if compas.OSX:
        path = _get_default_rhino_ironpython_sitepackages_path_mac(version)

    elif compas.WINDOWS:
        path = _get_default_rhino_ironpython_sitepackages_path_windows(version)

    else:
        raise Exception("Unsupported platform.")

    if not os.path.exists(path):
        raise Exception("The default installation folder for rhino8 {} doesn't exist.".format(version))

    return path


def _get_default_rhino_ironpython_sitepackages_path_mac(version):
    if version == "8.0":
        return "{}/.rhinocode/py27-rh8/Lib/site-packages".format(os.path.expanduser("~"))
    raise NotImplementedError


def _get_default_rhino_ironpython_sitepackages_path_windows(version):
    if version == "8.0":
        return "{}/.rhinocode/py27-rh8/Lib/site-packages".format(os.path.expanduser("~"))
    raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# Rhino CPython site-packages
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_rhino_cpython_sitepackages_path(version):
    version = _check_rhino_version(version)

    if version != "8.0":
        raise NotImplementedError

    if compas.OSX:
        path = _get_default_rhino_cpython_sitepackages_path_mac(version)

    elif compas.WINDOWS:
        path = _get_default_rhino_cpython_sitepackages_path_windows(version)

    else:
        raise Exception("Unsupported platform.")

    if not os.path.exists(path):
        raise Exception("The default installation folder for rhino8 {} doesn't exist.".format(version))

    return path


def _get_default_rhino_cpython_sitepackages_path_mac(version):
    if version == "8.0":
        return "{}/.rhinocode/py39-rh8/lib/python3.9/site-packages".format(os.path.expanduser("~"))
    raise NotImplementedError


def _get_default_rhino_cpython_sitepackages_path_windows(version):
    if version == "8.0":
        return "{}/.rhinocode/py39-rh8/lib/python3.9/site-packages".format(os.path.expanduser("~"))
    raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# IronPython lib folder
# =============================================================================
# =============================================================================
# =============================================================================


def _get_rhino_ironpython_lib_path(version):
    version = _check_rhino_version(version)

    if compas.WINDOWS:
        ipy_lib_path = _get_rhino_ironpython_lib_path_win32(version)

    elif compas.OSX:
        ipy_lib_path = _get_rhino_ironpython_lib_path_mac(version)

    else:
        raise Exception("Unsupported platform")

    if not os.path.exists(ipy_lib_path):
        ipy_lib_path = None
        # print("The lib folder for IronPython does not exist in this location: {}".format(ipy_lib_path))

    return ipy_lib_path


def _get_rhino_ironpython_lib_path_win32(version):
    return os.path.join(_get_rhino_ironpythonplugin_path(version), "settings", "lib")


# For 5.0 this is correct
# For +6 we should switch to the same path as on windows
# which is not in the managed plugins but in the appdata plugins
def _get_rhino_ironpython_lib_path_mac(version):
    return os.path.join(_get_rhino_managedplugins_path(version), "RhinoDLR_Python.rhp", "Lib")
