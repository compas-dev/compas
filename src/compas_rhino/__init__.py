"""
********************************************************************************
compas_rhino
********************************************************************************

.. currentmodule:: compas_rhino


.. toctree::
    :maxdepth: 1

    compas_rhino.artists
    compas_rhino.conduits
    compas_rhino.forms
    compas_rhino.geometry
    compas_rhino.helpers
    compas_rhino.inspectors
    compas_rhino.modifiers
    compas_rhino.selectors
    compas_rhino.ui
    compas_rhino.utilities

"""
from __future__ import absolute_import

import os

import compas

from .utilities import *
from . import utilities

__version__ = '0.3.3'


def _get_ironpython_lib_path(version):
    if version not in ('5.0', '6.0'):
        version = '5.0'

    appdata = os.getenv('APPDATA')
    ironpython_settings_path = os.path.join(appdata,
                                            'McNeel',
                                            'Rhinoceros',
                                            '{}'.format(version),
                                            'Plug-ins',
                                            'IronPython (814d908a-e25c-493d-97e9-ee3861957f49)',
                                            'settings')
    ironpython_lib_path = os.path.join(ironpython_settings_path, 'lib')

    if not os.path.exists(ironpython_lib_path):
        raise Exception("The lib folder for IronPython does not exist in this location: {}".format(
            ironpython_lib_path))

    return ironpython_lib_path


__all__ = utilities.__all__ + ['__version__']
