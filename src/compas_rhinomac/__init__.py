"""
********************************************************************************
compas_rhinomac
********************************************************************************

.. currentmodule:: compas_rhinomac


"""
from __future__ import absolute_import

import os


__version__ = '0.4.8'


def _get_ironpython_lib_path():
    ironpython_lib_path = os.path.join(
        '/',
        'Applications',
        'Rhinoceros.app',
        'Contents',
        'Resources',
        'ManagedPlugIns',
        'RhinoDLR_Python.rhp',
        'Lib'
    )

    if not os.path.exists(ironpython_lib_path):
        raise Exception("The Lib folder for IronPython does not exist in this location: {}".format(ironpython_lib_path))

    return ironpython_lib_path


def _get_python_plugins_path():
    python_plugins_path = os.path.join(
        os.environ['HOME'],
        'Library',
        'Application Support',
        'McNeel',
        'Rhinoceros',
        'MacPlugIns',
        'PythonPlugIns'
    )

    if not os.path.exists(python_plugins_path):
        raise Exception("The PythonPlugins folder does not exist in this location: {}".format(python_plugins_path))

    return python_plugins_path


__all__ = [name for name in dir() if not name.startswith('_')]
