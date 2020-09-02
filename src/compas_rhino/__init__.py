"""
************
compas_rhino
************

.. currentmodule:: compas_rhino

.. toctree::
    :maxdepth: 1

    compas_rhino.artists
    compas_rhino.conduits
    compas_rhino.forms
    compas_rhino.geometry
    compas_rhino.objects
    compas_rhino.utilities

"""
from __future__ import absolute_import

import os
import compas
import compas._os

if compas.RHINO:
    import rhinoscriptsyntax as rs  # noqa: F401
    from .utilities import *  # noqa: F401 F403


__version__ = '0.16.2'


PURGE_ON_DELETE = True


def _check_rhino_version(version):
    supported_versions = ['5.0', '6.0', '7.0']

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
        '5.0': ['/', 'Applications', 'Rhinoceros.app', 'Contents'],
        '6.0': ['/', 'Applications', 'Rhinoceros.app', 'Contents', 'Frameworks', 'RhCore.framework', 'Versions', 'A'],
        '7.0': ['/', 'Applications', 'RhinoWIP.app', 'Contents', 'Frameworks', 'RhCore.framework', 'Versions', 'A']
    }
    return os.path.join(*lib_paths.get(version) + ['Resources', 'ManagedPlugIns', 'RhinoDLR_Python.rhp', 'Lib'])


def _get_python_plugins_path(version):
    version = _check_rhino_version(version)

    if compas._os.system == 'win32':
        python_plugins_path = _get_python_plugins_path_win32(version)
    elif compas._os.system == 'darwin':
        python_plugins_path = _get_python_plugins_path_mac(version)
    else:
        raise Exception('Unsupported platform')

    return python_plugins_path


def _get_python_plugins_path_win32(version):
    return os.path.join(
        os.getenv('APPDATA'),
        'McNeel',
        'Rhinoceros',
        '{}'.format(version),
        'Plug-ins',
        'PythonPlugins')


def _get_python_plugins_path_mac(version):
    if version == '5.0':
        return os.path.join(
            os.environ['HOME'],
            'Library',
            'Application Support',
            'McNeel',
            'Rhinoceros',
            'MacPlugIns',
            'PythonPlugIns')

    return os.path.join(
        os.environ['HOME'],
        'Library',
        'Application Support',
        'McNeel',
        'Rhinoceros',
        '{}'.format(version),
        'Plug-ins',
        'PythonPlugIns')


def _get_scripts_path(version):
    version = _check_rhino_version(version)

    if compas._os.system == 'win32':
        scripts_path = _get_scripts_path_win32(version)
    elif compas._os.system == 'darwin':
        scripts_path = _get_scripts_path_mac(version)
    else:
        raise Exception('Unsupported platform')

    if not os.path.exists(scripts_path):
        raise Exception("The folder for RhinoPython scripts does not exist in this location: {}".format(scripts_path))

    return scripts_path


def _get_scripts_path_win32(version):
    return os.path.join(
        os.getenv('APPDATA'), 'McNeel', 'Rhinoceros', '{}'.format(version), 'scripts')


def _get_scripts_path_mac(version):
    return os.path.join(
        os.getenv('HOME'), 'Library', 'Application Support', 'McNeel', 'Rhinoceros', '{}'.format(version), 'scripts')


__all_plugins__ = ['compas_rhino.geometry.booleans']
__all__ = [name for name in dir() if not name.startswith('_')]
