# type: ignore
import io
import os
import compas

__version__ = "2.0.0-beta.2"


PURGE_ON_DELETE = True

INSTALLABLE_PACKAGES = ["compas", "compas_rhino8"]
SUPPORTED_VERSIONS = ["8.0"]
DEFAULT_VERSION = "8.0"

INSTALLATION_ARGUMENTS = None

# IRONPYTHON_PLUGIN_GUID = "814d908a-e25c-493d-97e9-ee3861957f49"
# GRASSHOPPER_PLUGIN_GUID = "b45a29b1-4343-4035-989e-044e8580d9cf"
# RHINOCYCLES_PLUGIN_GUID = "9bc28e9e-7a6c-4b8f-a0c6-3d05e02d1b97"


__all__ = [
    "PURGE_ON_DELETE",
    "INSTALLABLE_PACKAGES",
    "SUPPORTED_VERSIONS",
    "DEFAULT_VERSION",
    # "IRONPYTHON_PLUGIN_GUID",
    # "GRASSHOPPER_PLUGIN_GUID",
    # "RHINOCYCLES_PLUGIN_GUID",
    "clear",
    "redraw",
]

__all_plugins__ = [
    "compas_rhino8.scene",
    "compas_rhino8.install",
]

# =============================================================================
# =============================================================================
# =============================================================================
# General helpers
# =============================================================================
# =============================================================================
# =============================================================================


def clear(guids=None):
    import compas_rhino8.objects

    if guids is None:
        guids = compas_rhino8.objects.get_objects()  # noqa: F405
    compas_rhino8.objects.delete_objects(guids, purge=True)  # noqa: F405


def redraw():
    import rhinoscriptsyntax as rs

    rs.EnableRedraw(True)
    rs.Redraw()


def _check_rhino8_version(version):
    supported_versions = SUPPORTED_VERSIONS

    if not version:
        return DEFAULT_VERSION

    if version not in supported_versions:
        raise Exception("Unsupported rhino8 version: {}".format(version))

    return version


def _get_package_path(package):
    return os.path.abspath(os.path.dirname(package.__file__))


def _get_rhino_appdata_folder():
    if compas.WINDOWS:
        app = os.path.join(os.getenv("APPDATA"), "McNeel", "Rhinoceros")

    elif compas.OSX:
        app = os.path.join(os.getenv("HOME"), "Library", "Application Support", "McNeel", "Rhinoceros")

    else:
        raise Exception("Unsupported platform")

    if not os.path.exists(app):
        raise Exception("The appdata folder does not exist in this location: {}".format(app))

    return app


def _get_rhino_scripts_path(version):
    # appdata = _get_rhino_appdata_folder()
    # version = _check_rhino8_version(version)
    # scripts_path = os.path.join(appdata, "{}".format(version), "scripts")

    # if not os.path.exists(scripts_path):
    #     raise Exception("The scripts folder does not exist in this location: {}".format(scripts_path))

    # return scripts_path
    raise NotImplementedError


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
# rhino8 executable
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_rhino8_executable_path_mac():
    return "/Applications/rhino 8.app/Contents/MacOS/Rhinoceros"


def _get_default_rhino8_executable_path_windows():
    raise NotImplementedError


def _get_default_rhino8_executable_path_linux():
    raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# rhino8 Python
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_rhino8_python_path_mac(version):
    return "{}/.rhinocode/py39-rh8/python3.9".format(os.path.expanduser("~"))


def _get_default_rhino8_python_path_windows(version):
    raise NotImplementedError


def _get_default_rhino8_python_path_linux(version):
    raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# rhino8 Python site-packages
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_rhino8_sitepackages_path(version):
    version = _check_rhino8_version(version)

    if compas.OSX:
        path = _get_default_rhino8_sitepackages_path_mac(version)
    elif compas.WINDOWS:
        path = _get_default_rhino8_sitepackages_path_windows(version)
    elif compas.LINUX:
        path = _get_default_rhino8_sitepackages_path_linux(version)
    else:
        raise Exception("Unsupported platform.")

    if not os.path.exists(path):
        raise Exception("The default installation folder for rhino8 {} doesn't exist.".format(version))

    return path


def _get_default_rhino8_sitepackages_path_mac(version):
    return "{}/.rhinocode/py39-rh8/lib/python3.9//site-packages".format(os.path.expanduser("~"))


def _get_default_rhino8_sitepackages_path_windows(version):
    raise NotImplementedError


def _get_default_rhino8_sitepackages_path_linux(version):
    raise NotImplementedError
