from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys

import compas_rhino
import compas_rhino.install

from compas._os import remove_symlink

__all__ = []


def uninstall(version='5.0', packages=None):
    """Uninstall COMPAS from Rhino.

    Parameters
    ----------
    version : {'5.0', '6.0'}
        The version number of Rhino.
    packages : list of str
        List of packages to uninstall or None to use default package list.

    Examples
    --------
    .. code-block:: python

        >>> import compas_rhino
        >>> compas_rhino.uninstall('5.0')

    .. code-block:: python

        $ python -m compas_rhino.uninstall 5.0

    """

    print('Uninstalling COMPAS packages from Rhino IronPython lib:')

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
            results.append(
                (package, 'Cannot remove symlink, try to run as administrator.'))

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

    import sys

    print('\nusage: python -m compas_rhino.uninstall [version]\n')
    print('  version       Rhino version (5.0 or 6.0)\n')

    try:
        version = sys.argv[1]
    except IndexError:
        version = '5.0'
    else:
        try:
            version = str(version)
        except Exception:
            version = '5.0'

    uninstall(version=version, packages=compas_rhino.install.INSTALLABLE_PACKAGES)
