"""
.. _compas:

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
    compas.utilities
    compas.topology
    compas.visualization

"""

from __future__ import print_function

import os
import sys

import urllib
import tarfile


__version__ = '0.0.1'

PY3 = sys.version_info.major == 3

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'samples'))
DOCS = os.path.abspath(os.path.join(HOME, 'docs'))
LIBS = os.path.abspath(os.path.join(HOME, 'libs'))
TEMP = os.path.abspath(os.path.join(HOME, '__temp'))


def _find_resource(filename):
    filename = filename.strip('/')
    return os.path.abspath(os.path.join(DATA, filename))


def get_data(filename):
    return _find_resource(filename)


def get(filename):
    return _find_resource(filename)


def get_bunny():
    bunny = os.path.abspath(os.path.join(DATA, 'bunny/reconstruction/bun_zipper.ply'))

    if not os.path.exists(bunny):
        print('Getting the bunny from http://graphics.stanford.edu/pub/3Dscanrep/bunny.tar.gz ...')
        print('This will take a few seconds...')

        destination = os.path.abspath(os.path.join(DATA, 'bunny.tar.gz'))

        urllib.urlretrieve('http://graphics.stanford.edu/pub/3Dscanrep/bunny.tar.gz', destination)

        tar = tarfile.open(destination)
        tar.extractall(DATA)
        tar.close()

        os.remove(destination)

        print('Got it!\n')

    return bunny


def get_license():
    with open(os.path.join(HOME, 'LICENSE')) as fp:
        return fp.read()


def get_requirements(rtype='list'):
    pass


def get_version():
    return __version__


def requirements():
    with open(os.path.join(HERE, '../requirements.txt')) as f:
        for line in f:
            print(line.strip())


__all__ = ['HOME', 'DATA', 'DOCS', 'LIBS', 'TEMP', 'get_data', 'get_license', 'get_requirements', 'get_version']
