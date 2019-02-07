from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys

import compas_rhino
import compas_rhino.install

from compas._os import remove_symlink


__all__ = ['uninstall']


def uninstall(version=None, packages=None):
    """Uninstall COMPAS from Rhino.

    Parameters
    ----------
    version : {'5.0', '6.0'}, optional
        The version number of Rhino.
        Default is ``'6.0'``.
    packages : list of str, optional
        List of packages to uninstall.
        Default is to uninstall all COMPAS packages.

    Examples
    --------
    .. code-block:: python

        >>> import compas_rhino
        >>> compas_rhino.uninstall('6.0')

    .. code-block:: python

        $ python -m compas_rhino.uninstall -v 6.0

    """
    if version not in ('5.0', '6.0'):
        version = '6.0'

    print('Uninstalling COMPAS packages to Rhino {0} IronPython lib:'.format(version))

    if not packages:
        # should this not default to all installed compas packages?
        packages = compas_rhino.install.INSTALLABLE_PACKAGES

    ipylib_path = compas_rhino._get_ironpython_lib_path(version)

    results = []
    exit_code = 0

    for package in packages:
        symlink_path = os.path.join(ipylib_path, package)

        if not os.path.exists(symlink_path):
            continue

        try:
            remove_symlink(symlink_path)
            results.append((package, 'OK'))
        except OSError:
            results.append((package, 'ERROR: Cannot remove symlink, try to run as administrator.'))

    for _, status in results:
        if status is not 'OK':
            exit_code = -1

    if exit_code == -1:
        results.append(('compas_bootstrapper', 'WARNING: One or more packages failed, will not uninstall bootstrapper.'))
    else:
        compas_bootstrapper = os.path.join(ipylib_path, 'compas_bootstrapper.py')
        try:
            if os.path.exists(compas_bootstrapper):
                os.remove(compas_bootstrapper)
                results.append(('compas_bootstrapper', 'OK'))
        except:
            results.append(('compas_bootstrapper', 'ERROR: Could not delete compas_bootstrapper'))

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

    parser.add_argument('-v', '--version', choices=['5.0', '6.0'], default='5.0', help="The version of Rhino to install the packages in.")
    parser.add_argument('-p', '--packages', nargs='+', help="The packages to uninstall.")

    args = parser.parse_args()

    uninstall(version=args.version, packages=args.packages)
