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
    compas.plotters
    compas.robots
    compas.topology
    compas.utilities

..
    compas.viewers


In addition to the above packages, :mod:`compas` provides the following convenience functions.

.. autosummary::
    :toctree: generated/

    get
    get_bunny
    is_windows
    is_linux
    is_mono
    is_ironpython
    raise_if_not_ironpython
    raise_if_ironpython
    verify
    installed
    requirements

"""

from __future__ import print_function

import os
import sys

import appdirs


__author__    = 'Tom Van Mele and many others (see CONTRIBUTORS)'
__copyright__ = 'Copyright 2014-2018 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'
__version__   = '0.3.0'


PY3 = sys.version_info.major == 3


def absjoin(*parts):
    return os.path.abspath(os.path.join(*parts))


HERE = os.path.dirname(__file__)
HOME = absjoin(HERE, '../..')
DATA = absjoin(HERE, '../../data')
TEMP = absjoin(HERE, '../../temp')

APPDATA = appdirs.user_data_dir('COMPAS', 'compas-dev', roaming=True)
APPTEMP = absjoin(APPDATA, 'temp')


# install the app dirs during general install
# add data files
# add config files?
# download all data to user data dir, unless otherwise specified with localstorage
# add example scripts from/for docs
# add template files
# add other stuff that doesn't go into site packages folder
def install_appdirs():
    pass


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
    localpath = os.path.abspath(os.path.join(DATA, filename))

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
        from urllib.requests import urlretrieve
    except ImportError:
        from urllib import urlretrieve

    if not localstorage:
        localstorage = appdirs.user_data_dir('COMPAS', 'compas-dev', roaming=True)

    if not os.path.exists(localstorage):
        os.makedirs(localstorage)

    if not os.path.isdir(localstorage):
        raise Exception('Local storage location does not exist: {}'.format(localstorage))

    if not os.access(localstorage, os.W_OK):
        raise Exception('Local storage location is not writable: {}'.format(localstorage))

    bunny = absjoin(localstorage, 'bunny/reconstruction/bun_zipper.ply')
    destination = absjoin(localstorage, 'bunny.tar.gz')

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


# def get_armadillo():
#     import urllib
#     import gzip
#     import shutil

#     armadillo = os.path.abspath(os.path.join(DATA, 'armadillo/Armadillo.ply'))

#     if not os.path.exists(armadillo):
#         url = 'http://graphics.stanford.edu/pub/3Dscanrep/armadillo/Armadillo.ply.gz'
#         print('Getting the armadillo from {} ...'.format(url))
#         print('This will take a few seconds...')
#         destination = os.path.abspath(os.path.join(DATA, 'Armadillo.ply.gz'))
#         urllib.urlretrieve(url, destination)
#         with gzip.open(destination, 'rb') as ifile, open(armadillo, 'wb+') as ofile:
#             shutil.copyfileobj(ifile, ofile)
#         os.remove(destination)
#         print('Got it!\n')
#     return armadillo


def is_windows():
    return os.name == 'nt'


def is_linux():
    return os.name == 'posix'


def is_mono():
    return 'mono' in sys.version.lower()


def is_ironpython():
    return 'ironpython' in sys.version.lower()


def raise_if_not_ironpython():
    if not is_ironpython():
        raise


def raise_if_ironpython():
    if is_ironpython():
        raise


def license():
    with open(os.path.join(HOME, 'LICENSE')) as fp:
        return fp.read()


def version():
    return __version__


def help():
    return 'http://compas-dev.github.io'


def copyright():
    return __copyright__


def credits():
    pass


def verify():
    requirements = [
        'numpy',
        'scipy',
        'matplotlib',
    ]
    optional = [
        'cvxopt',
        'cvxpy',
        'Cython',
        'imageio',
        'networkx',
        'numba',
        'pandas',
        'paramiko',
        'pycuda',
        'PyOpenGL',
        'PySide',
        'Shapely',
        'sympy',
    ]
    current = installed()

    print('=' * 80)
    print('Checking required packages...\n')
    issues = []
    for package in requirements:
        if package not in current:
            issues.append(package)
    if issues:
        print('The following required packages are not installed:')
        for package in issues:
            print('- {}'.format(package))
    else:
        print('All required packages are installed.')

    print('\nChecking optional packages...\n')
    issues = []
    for package in optional:
        if package not in current:
            issues.append(package)
    if issues:
        print('The following optional packages are not installed:')
        for package in issues:
            print('- {}'.format(package))
    else:
        print('All optional packages are installed.')
    print('=' * 80)
    print()


def installed():
    import pkg_resources
    installed_packages = pkg_resources.working_set
    flat_installed_packages = [package.project_name for package in installed_packages]
    return sorted(flat_installed_packages, key=str.lower)


def requirements():
    with open(os.path.join(HERE, '../requirements.txt')) as f:
        for line in f:
            print(line.strip())


__all__ = [
    'get',
    'license',
    'version',
    'help',
    'copyright',
    'credits',
    'verify',
    'installed',
    'requirements',
    'raise_if_ironpython',
    'raise_if_not_ironpython',
]
