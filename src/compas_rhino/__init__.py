"""
********************************************************************************
compas_rhino
********************************************************************************

.. currentmodule:: compas_rhino


.. toctree::
    :maxdepth: 1

    compas_rhino.artists
    compas_rhino.constructors
    compas_rhino.conduits
    compas_rhino.forms
    compas_rhino.geometry
    compas_rhino.helpers
    compas_rhino.modifiers
    compas_rhino.selectors
    compas_rhino.ui
    compas_rhino.utilities

"""
from __future__ import absolute_import

import os
import compas._os
from .utilities import *


__version__ = '0.9.1'


PURGE_ON_DELETE = True


def _check_rhino_version(version):
    supported_versions = ['5.0', '6.0']

    if not version:
        return '6.0'

    if version not in supported_versions:
        raise Exception('Unsupported Rhino version: {}'.format(version))

    return version


def _get_ironpython_lib_path(version):
    version = _check_rhino_version(version)

    if compas._os.system == 'win32':
        ironpython_lib_path = _get_ironpython_lib_path_win32(version)
    elif compas._os.system == 'darwin':
        ironpython_lib_path = _get_ironpython_lib_path_mac(version)
    else:
        raise Exception('Unsupported platform')

    if not os.path.exists(ironpython_lib_path):
        raise Exception("The lib folder for IronPython does not exist in this location: {}".format(ironpython_lib_path))

    return ironpython_lib_path


def _get_ironpython_lib_path_win32(version):
    appdata = os.getenv('APPDATA')
    return os.path.join(appdata,
                        'McNeel',
                        'Rhinoceros',
                        '{}'.format(version),
                        'Plug-ins',
                        'IronPython (814d908a-e25c-493d-97e9-ee3861957f49)',
                        'settings',
                        'lib')


def _get_ironpython_lib_path_mac(version):
    lib_paths = {
        '5.0': [''],
        '6.0': ['Frameworks', 'RhCore.framework', 'Versions', 'A']
    }
    return os.path.join(*['/',
                          'Applications',
                          'Rhinoceros.app',
                          'Contents']
                        + lib_paths.get(version) +
                        ['Resources',
                         'ManagedPlugIns',
                         'RhinoDLR_Python.rhp',
                         'Lib'])


def _get_python_plugins_path(version):
    version = _check_rhino_version(version)

    if compas._os.system == 'win32':
        python_plugins_path = _get_python_plugins_path_win32(version)
    elif compas._os.system == 'darwin':
        python_plugins_path = _get_python_plugins_path_mac()
    else:
        raise Exception('Unsupported platform')

    return python_plugins_path


def _get_python_plugins_path_win32(version):
    appdata = os.getenv('APPDATA')
    return os.path.join(appdata,
                        'McNeel',
                        'Rhinoceros',
                        '{}'.format(version),
                        'Plug-ins',
                        'PythonPlugins')


def _get_python_plugins_path_mac(version):
    if version == '6.0':
        path = os.path.join(
            os.environ['HOME'],
            'Library',
            'Application Support',
            'McNeel',
            'Rhinoceros',
            '6.0',
            'Plug-ins',
            'PythonPlugIns')
    else:
        path = os.path.join(
            os.environ['HOME'],
            'Library',
            'Application Support',
            'McNeel',
            'Rhinoceros',
            'MacPlugIns',
            'PythonPlugIns')
    return path


__all__ = [name for name in dir() if not name.startswith('_')]
