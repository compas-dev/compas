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
import os
import compas
import compas_rhino

__version__ = '1.12.2'

if compas.is_rhino():
    from .utilities import *  # noqa: F401 F403

__all__ = [
    'get_grasshopper_managedplugin_path',
    'get_grasshopper_library_path',
    'get_grasshopper_userobjects_path'
]
__all_plugins__ = [
    'compas_ghpython.install',
    'compas_ghpython.uninstall',
    'compas_ghpython.artists',
]


# =============================================================================
# General Helpers
# =============================================================================


def _get_grasshopper_special_folder(version, folder_name):
    grasshopper = compas_rhino._get_grasshopper_plugin_path(version)
    return os.path.join(grasshopper, folder_name)


# =============================================================================
# Managed Plugin
# =============================================================================


def get_grasshopper_managedplugin_path(version):
    version = compas_rhino._check_rhino_version(version)
    managedplugins = compas_rhino._get_managedplugins_path(version)

    if compas.WINDOWS:
        gh_managedplugin_path = os.path.join(managedplugins, 'Grasshopper')

    elif compas.OSX:
        gh_managedplugin_path = os.path.join(managedplugins, 'GrasshopperPlugin.rhp')

    if not os.path.exists(gh_managedplugin_path):
        raise Exception("The Grasshopper (managed) Plug-in folder does not exist in this location: {}".format(gh_managedplugin_path))

    return gh_managedplugin_path


# =============================================================================
# GH Plugin Libraries path
# =============================================================================


def get_grasshopper_library_path(version):
    """Retrieve Grasshopper's library (components) path"""
    return _get_grasshopper_special_folder(version, 'Libraries')


# =============================================================================
# GH Plugin UserObjects path
# =============================================================================


def get_grasshopper_userobjects_path(version):
    """Retrieve Grasshopper's user objects path"""
    return _get_grasshopper_special_folder(version, 'UserObjects')
