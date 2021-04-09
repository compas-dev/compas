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

if compas.RHINO:
    from .utilities import *  # noqa: F401 F403


__version__ = '1.4.0'


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


__all_plugins__ = ['compas_ghpython.install']
__all__ = [name for name in dir() if not name.startswith('_')]
