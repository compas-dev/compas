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

# TODO: I believe this should be removed, as it pulls all utilities funcs
# into first-level instead of the usual second-level namespace
if compas.RHINO:
    from .utilities import *  # noqa: F401 F403


__version__ = '1.6.2'


def get_grasshopper_plugin_path(version):
    version = compas_rhino._check_rhino_version(version)

    if compas.WINDOWS:
        version = version.split('.')[0]   # take the major only
        grasshopper_plugin_path = os.path.join(os.getenv('ProgramFiles'), 'Rhino {}'.format(version), 'Plug-ins', 'Grasshopper')
    elif compas.OSX:
        lib_paths = {
            '6.0': ['/', 'Applications', 'Rhinoceros.app'],
            '7.0': ['/', 'Applications', 'Rhino 7.app', ]
        }

        if version not in lib_paths:
            raise Exception('Unsupported Rhino version')

        grasshopper_plugin_path = os.path.join(*lib_paths.get(version) +
                                               ['Contents', 'Frameworks', 'RhCore.framework', 'Versions', 'A',
                                                'Resources', 'ManagedPlugIns', 'GrasshopperPlugin.rhp'])
    else:
        raise Exception('Unsupported platform')
    return grasshopper_plugin_path


def get_grasshopper_library_path(version):
    """Retrieve Grasshopper's library (components) path"""
    return _get_grasshopper_special_folder(version, 'Libraries')


def get_grasshopper_userobjects_path(version):
    """Retrieve Grasshopper's user objects path"""
    return _get_grasshopper_special_folder(version, 'UserObjects')


def _get_grasshopper_special_folder(version, folder_name):
    if compas.WINDOWS:
        grasshopper_library_path = os.path.join(os.getenv('APPDATA'), 'Grasshopper', folder_name)
    elif compas.OSX:
        grasshopper_library_path = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', 'McNeel', 'Rhinoceros', '{}'.format(version),
                                                'Plug-ins', 'Grasshopper (b45a29b1-4343-4035-989e-044e8580d9cf)', folder_name)
    else:
        raise Exception('Unsupported platform')
    return grasshopper_library_path


__all_plugins__ = ['compas_ghpython.install', 'compas_ghpython.uninstall']
__all__ = [name for name in dir() if not name.startswith('_')]
