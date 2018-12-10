from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import sys

import compas_rhino
import compas_rhino.install

from compas._os import remove_symlink

__all__ = []


def uninstall(version='6.0', packages=None):
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
        >>> compas_rhino.uninstall('6.0')

    .. code-block:: python

        $ python -m compas_rhino.uninstall 6.0

    """

    print('Uninstalling COMPAS packages to Rhino {0} IronPython lib:'.format(version))

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

    for _, status in results:
        if status is not 'OK':
            exit_code = -1

    if exit_code == -1:
        results.append(('compas_bootstrapper', 'One or more packages failed, will not uninstall bootstrapper.'))
    else:
        compas_bootstrapper = os.path.join(ipylib_path, 'compas_bootstrapper.py')
        try:
            if os.path.exists(compas_bootstrapper):
                os.remove(compas_bootstrapper)
                results.append(('compas_bootstrapper', 'OK'))
        except:
            results.append(
                ('compas_bootstrapper', 'Could not delete compas_bootstrapper'))

    for package, status in results:
        print('   {} {}'.format(package.ljust(20), status))

        # Re-check just in case bootstrapper failed
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
        version = '6.0'
    else:
        try:
            version = str(version)
        except Exception:
            version = '6.0'

    uninstall(version=version, packages=compas_rhino.install.INSTALLABLE_PACKAGES)
