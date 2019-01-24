from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import importlib
import os
import sys

import compas_rhinomac

from compas._os import create_symlink


__all__ = ['install']


INSTALLABLE_PACKAGES = ('compas', 'compas_rhino')


def _get_package_path(package):
    return os.path.abspath(os.path.dirname(package.__file__))


def install(packages=None):
    """Install COMPAS for Rhino.

    Parameters
    ----------
    packages : list of str
        List of packages to install or None to use default package list.

    Examples
    --------
    .. code-block:: python

        >>> import compas_rhino
        >>> compas_rhino.install('6.0')

    .. code-block:: python

        $ python -m compas_rhino.install 6.0

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
            results.append(
                (package,
                 'WARNING: Package "{}" already found in RhinoMac Lib, try uninstalling first'.format(package)))

            continue

        try:
            create_symlink(package_path, symlink_path)
            results.append((package, 'OK'))
        except OSError:
            results.append((package, 'ERROR: Cannot create symlink. You may not have permission.'))

    for _, status in results:
        if status is not 'OK':
            exit_code = -1

    if exit_code == -1:
        results.append(
            ('compas_bootstrapper',
             'ERROR: One or more packages failed, will not install bootstrapper. Try uninstalling first.')
        )
    else:
        conda_prefix = os.environ.get('CONDA_PREFIX', None)
        try:
            with open(os.path.join(ipylib_path, 'compas_bootstrapper.py'), 'w') as f:
                f.write('CONDA_PREFIX = r"{0}"'.format(conda_prefix))
                results.append(('compas_bootstrapper', 'OK'))

        except:
            results.append(
                ('compas_bootstrapper',
                 'ERROR: Could not create compas_bootstrapper to auto-determine Python environment'))

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
