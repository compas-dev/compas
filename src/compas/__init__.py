"""
********************************************************************************
compas
********************************************************************************

.. currentmodule:: compas


.. toctree::
    :maxdepth: 1

    compas.datastructures
    compas.files
    compas.geometry
    compas.numerical
    compas.remote
    compas.robots
    compas.rpc
    compas.topology
    compas.utilities

"""

from __future__ import print_function

import os
import sys
import decimal

import compas._os


__author__    = 'Tom Van Mele and many others (see AUTHORS.md)'
__copyright__ = 'Copyright 2014-2019 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'

__version__ = '0.9.1'


PY3 = sys.version_info[0] == 3

HERE = os.path.dirname(__file__)
HOME = compas._os.absjoin(HERE, '../..')
DATA = compas._os.absjoin(HERE, '../../data')
TEMP = compas._os.absjoin(HERE, '../../temp')

APPDATA = compas._os.user_data_dir('COMPAS', 'compas-dev', roaming=True)
APPTEMP = compas._os.absjoin(APPDATA, 'temp')

PRECISION = '3f'


__all__ = [
    'raise_if_windows',
    'raise_if_not_windows',
    'raise_if_ironpython',
    'raise_if_not_ironpython',
]


def is_windows():
    """Check if the operating system is Windows.

    Returns
    -------
    bool
        True if the OS is Windows. False otherwise

    """
    return os.name == 'nt'
WINDOWS = is_windows()


def is_linux():
    """Check if the operating system is Linux.

    Returns
    -------
    bool
        True if the OS is Linux. False otherwise

    """
    return os.name == 'posix'
LINUX = is_linux()


def is_mono():
    """Check if the operating system is running on Mono.

    Returns
    -------
    bool
        True if the OS is running on Mono. False otherwise

    """
    return 'mono' in sys.version.lower()
MONO = is_mono()


def is_ironpython():
    """Check if the Python implementation is IronPython.

    Returns
    -------
    bool
        True if the implementation is IronPython. False otherwise

    """
    return 'ironpython' in sys.version.lower()
IPY = is_ironpython()


def raise_if_not_windows():
    if not WINDOWS:
        raise


def raise_if_windows():
    if WINDOWS:
        raise


def raise_if_not_ironpython():
    if not IPY:
        raise


def raise_if_ironpython():
    if IPY:
        raise


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
        e = abs(d.exponent)
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
    In all other cases, the function will get the corresponding files direcly from
    the GitHub repo, at https://raw.githubusercontent.com/compas-dev/compas/master/data

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
        return "https://raw.githubusercontent.com/compas-dev/compas/master/data/{}".format(filename)


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
