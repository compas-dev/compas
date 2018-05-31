"""
********************************************************************************
compas
********************************************************************************

.. module:: compas


.. toctree::
    :maxdepth: 1

    compas.com
    compas.datastructures
    compas.files
    compas.geometry
    compas.hpc
    compas.interop
    compas.numerical
    compas.plotters
    compas.topology
    compas.utilities
    compas.viewers

"""

from __future__ import print_function

import os
import sys


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2017 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'
__version__   = '0.0.1'


PY3 = sys.version_info.major == 3

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))
DOCS = os.path.abspath(os.path.join(HOME, 'docs'))
LIBS = os.path.abspath(os.path.join(HOME, 'libs'))
TEMP = os.path.abspath(os.path.join(HOME, 'temp'))


def get(filename):
    filename = filename.strip('/')
    return os.path.abspath(os.path.join(DATA, filename))


get_data = get


def get_bunny():
    import urllib
    import tarfile

    bunny = os.path.abspath(os.path.join(DATA, 'bunny/reconstruction/bun_zipper.ply'))

    if not os.path.exists(bunny):
        url = 'http://graphics.stanford.edu/pub/3Dscanrep/bunny.tar.gz'

        print('Getting the bunny from {} ...'.format(url))
        print('This will take a few seconds...')

        destination = os.path.abspath(os.path.join(DATA, 'bunny.tar.gz'))

        urllib.urlretrieve(url, destination)

        tar = tarfile.open(destination)
        tar.extractall(DATA)
        tar.close()

        os.remove(destination)

        print('Got it!\n')

    return bunny


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
    # import pkg_resources
    # from pkg_resources import DistributionNotFound
    # from pkg_resources import VersionConflict

    # # dependencies can be any iterable with strings,
    # # e.g. file line-by-line iterator
    # # here, if a dependency is not met, a DistributionNotFound or VersionConflict
    # # exception is thrown.
    # try:
    #     pkg_resources.require(dependencies)
    # except DistributionNotFound as e:
    #     print(e)
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
    import pip
    installed_packages = pip.get_installed_distributions()
    flat_installed_packages = [package.project_name for package in installed_packages]
    return sorted(flat_installed_packages, key=str.lower)


def requirements():
    with open(os.path.join(HERE, '../requirements.txt')) as f:
        for line in f:
            print(line.strip())


__all__ = ['HOME', 'DATA', 'DOCS', 'LIBS', 'TEMP', 'get_data', 'get_license', 'get_requirements', 'get_version']
