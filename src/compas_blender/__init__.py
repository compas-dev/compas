# type: ignore
import io
import os
import compas

try:
    import bpy
    import compas_blender.data

except ImportError:
    pass


__version__ = "2.11.0"


INSTALLABLE_PACKAGES = ["compas", "compas_blender"]
SUPPORTED_VERSIONS = ["3.3", "3.6", "4.2"]
DEFAULT_VERSION = "4.2"

INSTALLATION_ARGUMENTS = None


__all__ = [
    "INSTALLABLE_PACKAGES",
    "SUPPORTED_VERSIONS",
    "DEFAULT_VERSION",
    "clear",
    "redraw",
]

__all_plugins__ = [
    "compas_blender.geometry.booleans",
    "compas_blender.install",
    "compas_blender.scene",
]

# =============================================================================
# =============================================================================
# =============================================================================
# General helpers
# =============================================================================
# =============================================================================
# =============================================================================


def clear(guids=None):
    """Clear all scene objects."""
    if guids is None:
        # delete all objects
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=True, confirm=False)
        # delete data
        compas_blender.data.delete_unused_data()
        # delete collections
        for collection in bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.unlink(collection)
        for block in bpy.data.collections:
            objects = [o for o in block.objects if o.users]
            while objects:
                bpy.data.objects.remove(objects.pop())
            for collection in block.children:
                block.children.unlink(collection)
            if block.users == 0:
                bpy.data.collections.remove(block)
    else:
        for obj in guids:
            bpy.data.objects.remove(obj, do_unlink=True)


def redraw():
    """Trigger a redraw."""
    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)


def _check_blender_version(version):
    supported_versions = SUPPORTED_VERSIONS

    if not version:
        return DEFAULT_VERSION

    if version not in supported_versions:
        raise Exception("Unsupported Blender version: {}".format(version))

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
# Blender executable
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_blender_executable_path(version):
    version = _check_blender_version(version)

    if compas.OSX:
        path = _get_default_blender_executable_path_mac(version)
    elif compas.WINDOWS:
        path = _get_default_blender_executable_path_windows(version)
    elif compas.LINUX:
        path = _get_default_blender_executable_path_linux(version)
    else:
        raise Exception("Unsupported platform.")

    if not os.path.exists(path):
        raise Exception("The default installation folder for Blender doesn't exist.")

    return path


def _get_default_blender_executable_path_mac(version):
    return "/Applications/Blender.app/Contents/MacOS/Blender"


def _get_default_blender_executable_path_windows(version):
    return "C:\\Program Files\\Blender Foundation\\Blender {}".format(version)


def _get_default_blender_executable_path_linux(version):
    raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# Blender Python
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_blender_python_path(version):
    version = _check_blender_version(version)

    if compas.OSX:
        path = _get_default_blender_python_path_mac(version)
    elif compas.WINDOWS:
        path = _get_default_blender_python_path_windows(version)
    elif compas.LINUX:
        path = _get_default_blender_python_path_linux(version)
    else:
        raise Exception("Unsupported platform.")

    if not os.path.exists(path):
        raise Exception("The default installation folder for Blender {} doesn't exist.".format(version))

    return path


def _get_default_blender_python_path_mac(version):
    if version == "4.2":
        return "/Applications/Blender.app/Contents/Resources/{}/python/bin/python3.11".format(version)
    return "/Applications/Blender.app/Contents/Resources/{}/python/bin/python3.10".format(version)


def _get_default_blender_python_path_windows(version):
    return "C:\\Program Files\\Blender Foundation\\Blender {}\\{}\\python\\bin\\python.exe".format(version, version)


def _get_default_blender_python_path_linux(version):
    raise NotImplementedError


# =============================================================================
# =============================================================================
# =============================================================================
# Blender Python site-packages
# =============================================================================
# =============================================================================
# =============================================================================


def _get_default_blender_sitepackages_path(version):
    version = _check_blender_version(version)

    if compas.OSX:
        path = _get_default_blender_sitepackages_path_mac(version)
    elif compas.WINDOWS:
        path = _get_default_blender_sitepackages_path_windows(version)
    elif compas.LINUX:
        path = _get_default_blender_sitepackages_path_linux(version)
    else:
        raise Exception("Unsupported platform.")

    if not os.path.exists(path):
        raise Exception("The default installation folder for Blender {} doesn't exist.".format(version))

    return path


def _get_default_blender_sitepackages_path_mac(version):
    return "/Applications/Blender.app/Contents/Resources/{}/python/lib/python3.10/site-packages".format(version)


def _get_default_blender_sitepackages_path_windows(version):
    return "C:\\Program Files\\Blender Foundation\\Blender {}\\{}\\python\\lib\\site-packages".format(version, version)


def _get_default_blender_sitepackages_path_linux(version):
    raise NotImplementedError
