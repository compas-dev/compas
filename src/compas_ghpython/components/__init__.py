
"""
********************************************************************************
components
********************************************************************************

.. currentmodule:: compas_ghpython.components

.. rst-class:: lead

Utilities to work with Grasshopper components.

Installation
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    install_userobjects
    uninstall_userobjects

"""
from __future__ import absolute_import

import argparse
import glob
import os

from compas._os import create_symlinks
from compas._os import remove_symlinks
from compas_ghpython import get_grasshopper_userobjects_path
from compas_rhino import _check_rhino_version


def get_version_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', choices=['5.0', '6.0', '7.0'], default='6.0')
    args = parser.parse_args()
    return _check_rhino_version(args.version)


def install_userobjects(source):
    """Installs Grasshopper user objects.

    Parameters
    ----------
    source : str
        Folder where the ghuser files to install are located.

    Returns
    -------
    list
        List of tuples (name, success) indicating whether each of the user objects was successfully installed.
    """
    version = get_version_from_args()

    dstdir = get_grasshopper_userobjects_path(version)
    userobjects = glob.glob(os.path.join(source, '*.ghuser'))

    symlinks_to_remove = []
    symlinks_to_add = []
    for src in userobjects:
        dst = os.path.join(dstdir, os.path.basename(src))
        symlinks_to_remove.append(dst)
        symlinks_to_add.append((src, dst))

    # Remove existing links first
    remove_symlinks(symlinks_to_remove)

    # And the create new ones
    created = create_symlinks(symlinks_to_add)

    return list(zip(symlinks_to_add, created))


def uninstall_userobjects(userobjects):
    """
    Uninstalls Grasshopper user objects.

    Parameters
    ----------
    userobjects : list of str
        List of user object names to uninstall, eg. ``['Compas_Info.ghuser']``

    Returns
    -------
    list
        List of tuples (name, success) indicating whether each of the user objects was successfully removed.
    """
    version = get_version_from_args()
    dstdir = get_grasshopper_userobjects_path(version)

    symlinks = []
    for src in userobjects:
        dst = os.path.join(dstdir, os.path.basename(src))
        symlinks.append(dst)

    removed = remove_symlinks(symlinks)

    return list(zip(symlinks, removed))


__all__ = [
    'install_userobjects',
    'uninstall_userobjects'
]
