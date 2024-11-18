"""
This package provides a small set of functions to easily install and uninstall user-defined GH Components.
"""

from __future__ import absolute_import

import glob
import os

from compas._os import remove_symlinks
from compas._os import copy as _copy
from compas_ghpython import get_grasshopper_userobjects_path
from compas_rhino import _check_rhino_version
import compas_rhino


def get_version_from_args():
    args = compas_rhino.INSTALLATION_ARGUMENTS
    return _check_rhino_version(args.version)  # type: ignore


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

    # this dstdir potentially doesn't exist
    dstdir = get_grasshopper_userobjects_path(version)
    userobjects = glob.glob(os.path.join(source, "*.ghuser"))

    symlinks_to_remove = []
    symlinks_to_add = []
    for src in userobjects:
        dst = os.path.join(dstdir, os.path.basename(src))
        symlinks_to_remove.append(dst)
        symlinks_to_add.append((src, dst))

    # Remove existing links first
    remove_symlinks(symlinks_to_remove)

    # And the create new ones
    created = []
    for src, dst in symlinks_to_add:
        try:
            _copy(src, dst)
        except Exception:
            created.append(False)
        else:
            created.append(True)

    return list(zip(symlinks_to_add, created))


def uninstall_userobjects(userobjects=None):
    """
    Uninstalls Grasshopper user objects.

    Parameters
    ----------
    userobjects : list of str, optional
        List of user object names to uninstall, eg. ``['Compas_Info.ghuser']``
        Defaults to ``None``, in which case the uninstaller will search for user objects
        whose name starts with the string 'compas'.

    Returns
    -------
    list
        List of tuples (name, success) indicating whether each of the user objects was successfully removed.
    """
    version = get_version_from_args()
    dstdir = get_grasshopper_userobjects_path(version)

    if not userobjects:
        userobjects = []
        for name in os.listdir(dstdir):
            if name.lower().startswith("compas"):
                userobjects.append(name)

    symlinks = []
    for obj in userobjects:
        path = os.path.join(dstdir, os.path.basename(obj))
        symlinks.append(path)

    removed = remove_symlinks(symlinks)

    return list(zip(symlinks, removed))


__all__ = ["install_userobjects", "uninstall_userobjects"]
