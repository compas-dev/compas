from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import importlib
import os
import sys

import compas_rhinomac

from compas._os import create_symlink
from compas._os import remove_symlink


__all__ = ['install']


INSTALLABLE_PACKAGES = ['compas', 'compas_rhino']


def _get_package_path(package):
    return os.path.abspath(os.path.dirname(package.__file__))


def install(packages=None):
    """Install COMPAS for Rhino.

    Parameters
    ----------
    packages : list of str, optional
        List of packages to install.
        Default is to install ``['compas', 'compas_rhino']``.

    Examples
    --------
    .. code-block:: python

        >>> import compas_rhino
        >>> compas_rhinomac.install()

    .. code-block:: python

        $ python -m compas_rhinomac.install

    """
    if not packages:
        packages = INSTALLABLE_PACKAGES

    print('Installing COMPAS packages to RhinoMac IronPython Lib.')

    ipylib_path = compas_rhinomac._get_ironpython_lib_path()

    results = []
    exit_code = 0

    for package in packages:
        package_path = _get_package_path(importlib.import_module(package))
        symlink_path = os.path.join(ipylib_path, package)

        if os.path.exists(symlink_path):
            try:
                remove_symlink(symlink_path)
            except OSError:
                results.append((package, 'ERROR: Cannot remove symlink, try to run as administrator.'))

        try:
            create_symlink(package_path, symlink_path)
            results.append((package, 'OK'))
        except OSError:
            results.append((package, 'ERROR: Cannot create symlink. You may not have permission.'))

    for _, status in results:
        if status is not 'OK':
            exit_code = -1

    if exit_code == -1:
        results.append(('compas_bootstrapper', 'WARNING: One or more packages failed, will not install bootstrapper. Try uninstalling first.'))
    else:
        conda_prefix = os.environ.get('CONDA_PREFIX', None)
        compas_bootstrapper = os.path.join(ipylib_path, 'compas_bootstrapper.py')
        try:
            with open(compas_bootstrapper, 'w') as f:
                f.write('CONDA_PREFIX = r"{0}"'.format(conda_prefix))
                results.append(('compas_bootstrapper', 'OK'))
        except:
            results.append(('compas_bootstrapper', 'ERROR: Could not create compas_bootstrapper to auto-determine Python environment'))

    for package, status in results:
        print('   {} {}'.format(package.ljust(20), status))

        if status is not 'OK':
            exit_code = -1

    print('\nCompleted.')
    sys.exit(exit_code)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--packages', nargs='+', help="The packages to install.")

    args = parser.parse_args()

    install(packages=args.packages)
