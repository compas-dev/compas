"""
********************************************************************************
compas
********************************************************************************

.. currentmodule:: compas

.. toctree::
    :maxdepth: 1
    :titlesonly:

    compas.data
    compas.datastructures
    compas.files
    compas.geometry
    compas.numerical
    compas.plugins
    compas.robots
    compas.rpc
    compas.topology
    compas.utilities

Utility functions
=================

JSON handling
-------------

.. autofunction:: json_dump

.. autofunction:: json_dumps

.. autofunction:: json_load

.. autofunction:: json_loads

Precision
---------

.. autofunction:: set_precision

.. autodata:: PRECISION

Execution context
-----------------

.. autofunction:: is_windows

.. autofunction:: is_linux

.. autofunction:: is_osx

.. autofunction:: is_mono

.. autofunction:: is_ironpython

.. autofunction:: is_rhino

.. autofunction:: is_blender

.. autodata:: WINDOWS

.. autodata:: LINUX

.. autodata:: OSX

.. autodata:: MONO

.. autodata:: IPY

.. autodata:: RHINO

.. autodata:: BLENDER

"""
from __future__ import print_function

import os
import decimal

from distutils.version import LooseVersion

import compas._os
from compas._os import is_windows, is_linux, is_osx, is_mono, is_ironpython, is_rhino, is_blender
from compas.data import json_dump, json_dumps, json_load, json_loads


__author__ = 'Tom Van Mele and many others (see AUTHORS.md)'
__copyright__ = 'Copyright 2014-2019 - Block Research Group, ETH Zurich'
__license__ = 'MIT License'
__email__ = 'vanmelet@ethz.ch'

__version__ = '1.6.3'

version = LooseVersion(compas.__version__)
versionstring = version.vstring.split('-')[0]

HERE = os.path.dirname(__file__)
"""str: Path to the location of the compas package."""

HOME = compas._os.absjoin(HERE, '../..')
"""str: Path to the root of the local repo."""

DATA = compas._os.absjoin(HERE, '../../data')
"""str: Path to the data folder of the local repo."""

TEMP = compas._os.absjoin(HERE, '../../temp')
"""str: Path to the temp folder of the local repo."""

APPDATA = compas._os.user_data_dir('COMPAS', 'compas-dev', roaming=True)
"""str: Path to the COMPAS directory in APPDATA."""

APPTEMP = compas._os.absjoin(APPDATA, 'temp')
"""str: Path to a temp folder in the COMPAS directory in APPDATA."""

PRECISION = '3f'
"""str:
The precision used by COMPAS for generation of geometric keys,
for the comparison of point locations,
for the parsing of geometry files,
and for the generation of human-readable representations of geometry objects.

The string is in the format used by the Python string formating mini language
for formatting numbers.
Float formatting (``'<x>f'``) and integer formatting (``'d'``) specifiers are supported.
"""

PY3 = compas._os.PY3
"""bool: True if the current Python version is 3.x, False otherwise."""

WINDOWS = is_windows()
"""bool: True if the current operating system is Windows, False otherwise."""

LINUX = is_linux()
"""bool: True if the current operating system is Linux, False otherwise."""

OSX = is_osx()
"""bool: True if the current operating system is OSX, False otherwise."""

MONO = is_mono()
"""bool: True if the current operating system is Mono, False otherwise."""

IPY = is_ironpython()
"""bool: True if the current Python implementation is IronPython, False otherwise."""

RHINO = is_rhino()
"""bool: True if the current context is Rhino, False otherwise."""

BLENDER = is_blender()
"""bool: True if the current context is Blender, False otherwise."""


# Check if COMPAS is installed from git
# If that's the case, try to append the current head's hash to __version__
try:
    git_head_file = compas._os.absjoin(HOME, '.git', 'HEAD')

    if os.path.exists(git_head_file):
        # git head file contains one line that looks like this:
        # ref: refs/heads/main
        with open(git_head_file, 'r') as git_head:
            _, ref_path = git_head.read().strip().split(' ')
            ref_path = ref_path.split('/')

            git_head_refs_file = compas._os.absjoin(HOME, '.git', *ref_path)

        if os.path.exists(git_head_refs_file):
            with open(git_head_refs_file, 'r') as git_head_ref:
                git_commit = git_head_ref.read().strip()
                __version__ += '-' + git_commit[:8]
except Exception:
    pass


__all__ = [
    'WINDOWS', 'LINUX', 'OSX', 'MONO', 'IPY', 'RHINO', 'BLENDER',
    'is_windows', 'is_linux', 'is_osx', 'is_mono', 'is_ironpython', 'is_rhino', 'is_blender',
    'set_precision',
    'get',
    'json_dump', 'json_load', 'json_dumps', 'json_loads'
]


def set_precision(precision):
    """Set the precision used by geometric maps.

    Parameters
    ----------
    precision : float
        The precision as a floating point number.
        For example, ``0.0001``.

    Notes
    -----
    This function converts the floating point number to a string formatting
    specifier and assigns the specifier to ``compas.PRECISION``.

    Examples
    --------
    >>> compas.set_precision(0.001)
    >>> compas.PRECISION
    '3f'

    """
    global PRECISION
    precision = str(precision)
    d = decimal.Decimal(precision).as_tuple()
    if d.exponent < 0:
        e = - d.exponent
        PRECISION = "{}f".format(e)


# ==============================================================================
# data
# ==============================================================================

def get(filename):
    """Get the full path to one of the sample data files.

    Parameters
    ----------
    filename : str
        The name of the data file.
        The following are available.

        * boxes.obj
        * faces.obj
        * fink.obj
        * hypar.obj
        * lines.obj
        * saddle.obj

    Returns
    -------
    str
        The full path to the specified file.

    Notes
    -----
    The file name should be specified relative to the **COMPAS** sample data folder.
    This folder is only locally available if you installed **COMPAS** from source,
    or if you are working directly with the source.
    In all other cases, the function will get the corresponding files directly from
    the GitHub repo, at https://raw.githubusercontent.com/compas-dev/compas/main/data

    Examples
    --------
    The ``compas.get`` function is meant to be used in combination with the static
    constructors of the data structures.

    .. code-block:: python

        import compas
        from compas.datastructures import Mesh

        mesh = Mesh.from_obj(compas.get('faces.obj'))

    """
    filename = filename.strip('/')

    if filename.endswith('bunny.ply'):
        return get_bunny()

    localpath = compas._os.absjoin(DATA, filename)

    if os.path.exists(localpath):
        return localpath
    else:
        return "https://github.com/compas-dev/compas/raw/main/data/{}".format(filename)


def get_bunny(localstorage=None):
    """Get the *Stanford Bunny* directly from the Stanford repository.

    Parameters
    ----------
    localstorage : str, optional
        Path to a local storage folder for saving the downloaded data.
        Default is ``None``, in which case the data will be stored in a local
        user data directory. See https://pypi.org/project/appdirs/ for more info.

    Returns
    -------
    str
        Full path to the local file.

    Examples
    --------
    The *Stanford Bunny* is a `PLY` file.
    Therefore, the returned path should be used in combination with the ``PLY``
    file reader, or with the ``from_ply`` constructor function for meshes.

    .. code-block:: python

        import compas
        from compas.datastructures import Mesh

        mesh = Mesh.from_ply(compas.get_bunny())

    """
    import tarfile

    try:
        from urllib.request import urlretrieve
    except ImportError:
        from urllib import urlretrieve

    if not localstorage:
        localstorage = APPDATA

    if not os.path.exists(localstorage):
        os.makedirs(localstorage)

    if not os.path.isdir(localstorage):
        raise Exception('Local storage location does not exist: {}'.format(localstorage))

    if not os.access(localstorage, os.W_OK):
        raise Exception('Local storage location is not writable: {}'.format(localstorage))

    bunny = compas._os.absjoin(localstorage, 'bunny/reconstruction/bun_zipper.ply')
    destination = compas._os.absjoin(localstorage, 'bunny.tar.gz')

    if not os.path.exists(bunny):
        url = 'http://graphics.stanford.edu/pub/3Dscanrep/bunny.tar.gz'

        print('Getting the bunny from {} ...'.format(url))
        print('This will take a few seconds...')

        urlretrieve(url, destination)

        with tarfile.open(destination) as file:
            file.extractall(localstorage)

        os.remove(destination)

        print('Got it!\n')

    return bunny
