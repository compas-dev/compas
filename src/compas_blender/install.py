import os
import sys
import tempfile

import compas
import compas_blender

from compas._os import copy
from compas._os import create_symlinks
from compas._os import remove
from compas._os import remove_symlink
from compas._os import rename


__all__ = ['install']


BOOTSTRAPPER_TEMPLATE = """
import os
import sys

import bpy

ENVIRONMENT_NAME = r"{}"
PYTHON_DIRECTORY = r"{}"

PREVIOUS_ENVIRON = os.environ.copy()

# Blender uses `register` and `unregister` functions now for the startup scripts
def register():
    sys.version = '{}'

    # We delay the import of compas._os because
    # it depends this very same compas_bootstrapper
    import compas._os

    # Update current env variables
    compas._os.prepare_environment(os.environ)

def unregister():
    # Restore environment state to before registration
    os.environ = PREVIOUS_ENVIRON

"""


def install(blender_path, version=None):
    """Install COMPAS for Blender.

    Parameters
    ----------
    blender_path : str
        The path to the folder with the version number of Blender.
        For example, on Mac: ``'/Applications/Blender.app/Contents/Resources/2.83'``.
        On Windows: ``'%PROGRAMFILES%/Blender Foundation/Blender 2.83/2.83'``.
    version : {'2.83', '2.93', '3.1'}, optional
        The version number of Blender.
        Default is ``'2.93'``.

    Examples
    --------
    .. code-block:: bash

        $ python -m compas_blender.install

    .. code-block:: bash

        $ python -m compas_blender.install -v 2.93

    .. code-block:: bash

        $ python -m compas_blender.install /Applications/Blender.app/Contents/Resources/2.93

    """
    if not os.environ.get('CONDA_PREFIX'):
        print('Conda environment not found. The installation into Blender requires an active conda environment with a matching Python version to continue.')
        sys.exit(-1)

    if not version and not blender_path:
        version = '2.93'

    if version and blender_path:
        print('Both options cannot be provided simultaneously. Provide the full installation path, or the version with flag -v.')
        sys.exit(-1)

    if version:
        if compas.LINUX:
            print('Version-based installs are currently not supported for Linux. Please provide the full installation path with the -p option.')
            sys.exit(-1)

        blender_path = compas_blender._get_default_blender_installation_path(version)

    if not os.path.exists(blender_path):
        raise FileNotFoundError('Blender version folder not found.')

    path, version = os.path.split(blender_path)

    print('Installing COMPAS for Blender {}'.format(version))

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

    print('Installing current conda environment into Blender...')
    print('  Renaming bundled python folder to original_python: {} => {}'.format(blenderpython_src, blenderpython_dst))
    rename(blenderpython_src, blenderpython_dst)
    create_symlinks([(os.environ['CONDA_PREFIX'], blenderpython_src)])

    # Take either the CONDA environment directory or the current Python executable's directory
    python_directory = os.environ.get('CONDA_PREFIX', None) or os.path.dirname(sys.executable)
    environment_name = os.environ.get('CONDA_DEFAULT_ENV', '')

    # Get current sys.version value, we will override it inside Blender
    # because it seems Blender overrides it as well, but doing so breaks many things after having replaced the Python interpreter
    sys_version = "\\n".join(sys.version.split("\n"))

    _handle, bootstrapper_temp_path = tempfile.mkstemp(suffix='.py', text=True)

    with open(bootstrapper_temp_path, 'w') as f:
        f.write(BOOTSTRAPPER_TEMPLATE.format(environment_name, python_directory, sys_version))

    print('  Creating bootstrap script: {}'.format(compas_bootstrapper))
    copy(bootstrapper_temp_path, compas_bootstrapper)

    print()
    print('COMPAS for Blender {} has been installed.'.format(version))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('blenderpath', nargs='?', help="The path to the folder with the version number of Blender.")
    parser.add_argument('-v', '--version', choices=['2.83', '2.93', '3.1'], help="The version of Blender to install COMPAS in.")

    args = parser.parse_args()

    install(args.blenderpath, version=args.version)
