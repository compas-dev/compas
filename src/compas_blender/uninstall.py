import os
import sys

from compas._os import remove
from compas._os import remove_symlink
from compas._os import rename

__all__ = ['uninstall']


def uninstall(blender_path):
    """Uninstall COMPAS from Blender.

    Parameters
    ----------
    blender_path : str
        The path to the folder with the version number of Blender.
        For example, on Mac: ``'/Applications/blender.app/Contents/Resources/2.80'``.
        On Windows: ``'%PROGRAMFILES%\\Blender Foundation\\Blender\\2.80'``.

    Examples
    --------
    .. code-block:: bash

        $ python -m compas_blender.uninstall /Applications/blender.app/Contents/Resources/2.80

    """
    if not os.environ.get('CONDA_PREFIX'):
        print('Conda environment not found. The installation into Blender requires an active conda environment with a matching Python version to continue.')
        sys.exit(-1)

    path, version = os.path.split(blender_path)

    print('Uninstalling COMPAS for Blender {}'.format(version))

    startup = os.path.join(blender_path, 'scripts', 'startup')

    blenderpython_src = os.path.join(blender_path, 'python')
    blenderpython_dst = os.path.join(blender_path, 'original_python')
    compas_bootstrapper = os.path.join(startup, 'compas_bootstrapper.py')

    if os.path.exists(blenderpython_dst):
        print('Found existing installation, restoring bundled python installation...')
        if os.path.exists(blenderpython_src):
            remove_symlink(blenderpython_src)

        print('  Renaming original_python back to bundled python folder: {} => {}'.format(blenderpython_dst, blenderpython_src))
        rename(blenderpython_dst, blenderpython_src)

    if os.path.exists(compas_bootstrapper):
        print('  Removing compas bootstrapper...')
        remove(compas_bootstrapper)

    print()
    print('COMPAS has been uninstalled from Blender {}.'.format(version))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('versionpath', help="The path to the folder with the version number of Blender.")
    args = parser.parse_args()

    uninstall(args.versionpath)
