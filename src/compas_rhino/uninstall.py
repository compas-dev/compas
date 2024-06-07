from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import os
import sys

import compas._os
import compas.plugins
import compas_rhino
from compas_rhino.install import _run_post_execution_steps
from compas_rhino.install import installable_rhino_packages


def uninstall(version=None, packages=None):
    """Uninstall COMPAS from Rhino.

    Parameters
    ----------
    version : {'5.0', '6.0', '7.0', '8.0'}, optional
        The version number of Rhino.
        Default is ``'7.0'``.
    packages : list of str, optional
        List of packages to uninstall.
        Default is to uninstall all packages installed by the COMPAS installer.

    Examples
    --------
    .. code-block:: python

        import compas_rhino

        compas_rhino.uninstall()

    .. code-block:: bash

        python -m compas_rhino.uninstall

    """
    version = compas_rhino._check_rhino_version(version)

    # We install COMPAS packages in the scripts folder
    # instead of directly as IPy module.
    scripts_path = compas_rhino._get_rhino_scripts_path(version)

    # This is for old installs
    ipylib_path = compas_rhino._get_rhino_ironpython_lib_path(version)

    # Filter the provided list of packages
    # If no packages are provided
    # this first collects all installable packages from the environment.
    packages = _filter_installed_packages(version, packages)

    # Also remove all broken symlinks
    # because ... they're broken!
    for name in os.listdir(scripts_path):
        path = os.path.join(scripts_path, name)
        if os.path.islink(path):
            if not os.path.exists(path):
                if name not in packages:
                    packages.append(name)

    # Collect paths for removal based on package names
    symlinks_to_uninstall = []

    for package in packages:
        symlink_path = os.path.join(scripts_path, package)
        symlinks_to_uninstall.append(dict(name=package, link=symlink_path))

        # Handle legacy install location
        # This does not always work,
        # and especially not in cases where it is in any case not necessary :)
        if ipylib_path:
            legacy_path = os.path.join(ipylib_path, package)
            if os.path.exists(legacy_path):
                symlinks_to_uninstall.append(dict(name=package, link=legacy_path))

    # There is nothing to uninstall
    if not symlinks_to_uninstall:
        print("\nNo packages to uninstall from Rhino {0} scripts folder: \n{1}.".format(version, scripts_path))
        return

    # -------------------------
    # Start uninstalling
    # -------------------------

    uninstalled_packages = []
    results = []
    exit_code = 0

    symlinks = [link["link"] for link in symlinks_to_uninstall]
    uninstall_results = compas._os.remove_symlinks(symlinks)

    for uninstall_data, success in zip(symlinks_to_uninstall, uninstall_results):
        if success:
            uninstalled_packages.append(uninstall_data["name"])
            result = "OK"
        else:
            result = "ERROR: Cannot remove symlink, try to run as administrator."

        results.append((uninstall_data["name"], result))

    if not all(uninstall_results):
        exit_code = -1

    if exit_code == -1:
        results.append(
            (
                "compas_bootstrapper",
                "WARNING: One or more packages failed, will not uninstall bootstrapper.",
            )
        )

    else:
        if compas_rhino._try_remove_bootstrapper(scripts_path):
            results.append(("compas_bootstrapper", "OK"))
        else:
            results.append(
                (
                    "compas_bootstrapper",
                    "ERROR: Cannot remove compas_bootstrapper, try to run as administrator.",
                )
            )

        # Handle legacy bootstrapper
        # Again, only if possible...
        if ipylib_path:
            if not compas_rhino._try_remove_bootstrapper(ipylib_path):
                results.append(
                    (
                        "compas_bootstrapper",
                        "ERROR: Cannot remove legacy compas_bootstrapper, try to run as administrator.",
                    )
                )

    # -------------------------
    # Output results
    # -------------------------

    print("Uninstalling COMPAS packages from Rhino {0} scripts folder: \n{1}".format(version, scripts_path))
    print("\nThe following packages have been detected and will be uninstalled:\n")

    for package, status in results:
        print("   {} {}".format(package.ljust(20), status))

        if status != "OK":
            exit_code = -1

    if exit_code == 0 and uninstalled_packages:
        print("\nRunning post-uninstallation steps...\n")

        if not _run_post_execution_steps(after_rhino_uninstall(uninstalled_packages)):
            exit_code = -1

    print("\nUninstall completed.")

    if exit_code != 0:
        sys.exit(exit_code)


def _filter_installed_packages(version, packages):
    ipylib_path = compas_rhino._get_rhino_ironpython_lib_path(version)
    scripts_path = compas_rhino._get_rhino_scripts_path(version)

    compas_bootstrapper = compas_rhino._get_bootstrapper_path(scripts_path)
    bootstrapper_data = compas_rhino._get_bootstrapper_data(compas_bootstrapper)

    # Don't modify the original list if we have one
    if packages:
        packages = packages[:]
    else:
        packages = bootstrapper_data.get("INSTALLED_PACKAGES", None)

        # No info, fall back to installable packages list
        if packages is None:
            packages = list(itertools.chain.from_iterable(installable_rhino_packages()))  # type: ignore

    # Handle legacy install
    if ipylib_path:
        legacy_bootstrapper = compas_rhino._get_bootstrapper_path(ipylib_path)
        if os.path.exists(legacy_bootstrapper):
            bootstrapper_data = compas_rhino._get_bootstrapper_data(legacy_bootstrapper)
            legacy_packages = bootstrapper_data.get("INSTALLED_PACKAGES", None)

            if legacy_packages:
                packages.extend(legacy_packages)

    return packages


@compas.plugins.pluggable(category="install", selector="collect_all")
def after_rhino_uninstall(uninstalled_packages):
    """Allows extensions to execute actions after uninstall from Rhino is done.

    Extensions providing Rhino or Grasshopper features
    can implement this pluggable interface to perform
    additional steps after the uninstall from Rhino has
    been completed.

    Parameters
    ----------
    uninstalled_packages : :obj:`list` of :obj:`str`
        List of packages that have been uninstalled.

    Examples
    --------
    >>> import compas.plugins
    >>> @compas.plugins.plugin(category="install")
    ... def after_rhino_uninstall(uninstalled_packages):
    ...     # Do something cleanup, eg remove copied files.
    ...     return [("compas_ghpython", "GH Components uninstalled", True)]

    Returns
    -------
    :obj:`list` of 3-tuple (str, str, bool)
        List containing a 3-tuple with component name, message and True/False success flag.
    """
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        choices=compas_rhino.SUPPORTED_VERSIONS,
        default=compas_rhino.DEFAULT_VERSION,
        help="The version of Rhino to install the packages in.",
    )
    parser.add_argument("-p", "--packages", nargs="+", help="The packages to uninstall.")

    args = parser.parse_args()
    compas_rhino.INSTALLATION_ARGUMENTS = args

    uninstall(version=args.version, packages=args.packages)
