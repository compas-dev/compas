import importlib
import itertools
import os
import sys

import compas._os
import compas.plugins
import compas_blender

INSTALLED_VERSION = None


def install(version=None, packages=None, clean=False):
    """Install COMPAS for Blender.

    Parameters
    ----------
    version : str, optional
        The version number of Blender.
        Default is ``'4.0'``.
    packages : list of str, optional
        List of packages to install or None to use default package list.
        Default is the result of ``installable_blender_packages``,
        which collects all installable packages in the current environment.
    clean : bool, optional
        If True, this will clean up the site packages folder and remove
        also existing symlinks that are not importable in the current environment.

    Examples
    --------
    .. code-block:: python

        import compas_blender.install

        compas_blender.install.install()

    .. code-block:: bash

        python -m compas_blender.install

    """
    version = compas_blender._check_blender_version(version)

    # We install COMPAS packages in the site packages folder
    sitepackages_path = compas_blender._get_default_blender_sitepackages_path(version)

    # Filter the provided list of packages
    # If no packages are provided
    # this first collects all installable packages from the environment.
    packages = _filter_installable_packages(version, packages)

    results = []
    symlinks_to_install = []
    symlinks_to_uninstall = []
    exit_code = 0

    # check all installable packages
    # add the packages that can't be imported from the current env to the list of symlinks to uninstall
    # and remove the package name from the list of installable packages
    # make a copy of the list to avoid problems with removing items
    # note: perhaps this should already happen in the filter function...
    for name in packages[:]:
        try:
            importlib.import_module(name)
        except ImportError:
            path = os.path.join(sitepackages_path, name)
            symlinks_to_uninstall.append(dict(name=name, link=path))
            packages.remove(name)

    # Also remove all broken symlinks from the scripts folder
    # because ... they're broken!
    # If it is an actual folder or a file, leave it alone
    # because probably someone put it there on purpose.
    for name in os.listdir(sitepackages_path):
        path = os.path.join(sitepackages_path, name)
        if os.path.islink(path):
            if not os.path.exists(path):
                symlinks_to_uninstall.append(dict(name=name, link=path))
                try:
                    importlib.import_module(name)
                except ImportError:
                    pass
                else:
                    if name not in packages:
                        packages.append(name)

    # If the scripts folder is supposed to be cleaned
    # also remove all existing symlinks that cannot be imported
    # and reinstall symlinks that can be imported
    if clean:
        for name in os.listdir(sitepackages_path):
            path = os.path.join(sitepackages_path, name)
            if os.path.islink(path):
                if os.path.exists(path):
                    try:
                        importlib.import_module(name)
                    except ImportError:
                        path = os.path.join(sitepackages_path, name)
                        symlinks_to_uninstall.append(dict(name=name, link=path))
                    else:
                        if name not in packages:
                            packages.append(name)

    # add all of the packages in the list of installable packages
    # to the list of symlinks to uninstall
    # and to the list of symlinks to install
    for package in packages:
        symlink_path = os.path.join(sitepackages_path, package)
        symlinks_to_uninstall.append(dict(name=package, link=symlink_path))

        package_path = compas_blender._get_package_path(importlib.import_module(package))
        symlinks_to_install.append(dict(name=package, source_path=package_path, link=symlink_path))

    # -------------------------
    # Uninstall first
    # -------------------------

    symlinks = [link["link"] for link in symlinks_to_uninstall]
    uninstall_results = compas._os.remove_symlinks(symlinks)

    # Let the user know if some symlinks could not be removed.
    for uninstall_data, success in zip(symlinks_to_uninstall, uninstall_results):
        if not success:
            results.append(
                (
                    uninstall_data["name"],
                    "ERROR: Cannot remove symlink, try to run as administrator.",
                )
            )

    # -------------------------
    # Ready to start installing
    # -------------------------

    # create new symlinks and register the results
    symlinks = [(link["source_path"], link["link"]) for link in symlinks_to_install]
    install_results = compas._os.create_symlinks(symlinks)

    # set the exit code based on the installation results
    if not all(install_results):
        exit_code = -1

    # make a list of installed packages
    # based on the installation results
    # and update the general results list
    installed_packages = []
    for install_data, success in zip(symlinks_to_install, install_results):
        if success:
            installed_packages.append(install_data["name"])
            result = "OK"
        else:
            result = "ERROR: Cannot create symlink, try to run as administrator."
        results.append((install_data["name"], result))

    # finalize the general results list with info about the bootstrapper
    if exit_code == -1:
        results.append(
            (
                "compas_bootstrapper",
                "WARNING: One or more packages failed, will not install bootstrapper, try uninstalling first",
            )
        )
    else:
        try:
            _update_bootstrapper(sitepackages_path, packages)
            results.append(("compas_bootstrapper", "OK"))
        except:  # noqa: E722
            results.append(
                (
                    "compas_bootstrapper",
                    "ERROR: Could not create compas_bootstrapper to auto-determine Python environment",
                )
            )

    # output the outcome of the installation process
    # perhaps we should more info here
    print("\nInstalling COMPAS packages to Blender {0} site-packages folder:".format(version))
    print("{}\n".format(sitepackages_path))

    for package, status in results:
        print("   {} {}".format(package.ljust(20), status))
        if status != "OK":
            exit_code = -1

    if exit_code == 0 and len(installed_packages):
        print("\nRunning post-installation steps...\n")
        if not _run_post_execution_steps(after_blender_install(installed_packages)):
            exit_code = -1

    print("\nInstall completed.")
    if exit_code != 0:
        sys.exit(exit_code)

    global INSTALLED_VERSION
    INSTALLED_VERSION = version


def _run_post_execution_steps(steps_generator):
    all_steps_succeeded = True
    post_execution_errors = []

    for result in steps_generator:
        if isinstance(result, Exception):
            post_execution_errors.append(result)
            continue

        for item in result:
            try:
                package, message, success = item
                status = "OK" if success else "ERROR"
                if not success:
                    all_steps_succeeded = False
                print("   {} {}: {}".format(package.ljust(20), status, message))
            except ValueError:
                post_execution_errors.append(ValueError("Step ran without errors but result is wrongly formatted: {}".format(str(item))))

    if post_execution_errors:
        print("\nOne or more errors occurred:\n")
        for error in post_execution_errors:
            print("   - {}".format(repr(error)))

        all_steps_succeeded = False

    return all_steps_succeeded


@compas.plugins.plugin(category="install", pluggable_name="installable_blender_packages", tryfirst=True)
def default_installable_blender_packages():
    # While this list could obviously be hard-coded, I think
    # eating our own dogfood and using plugins to define this, just like
    # any other extension/plugin would be is a better way to ensure consistent behavior.
    return compas_blender.INSTALLABLE_PACKAGES


@compas.plugins.pluggable(category="install", selector="collect_all")
def installable_blender_packages():
    """Provide a list of packages to make available inside Blender.

    Extensions providing Blender features
    can implement this pluggable interface to automatically
    have their packages made available inside Blender when
    COMPAS is installed into it.

    Examples
    --------
    >>> import compas.plugins
    >>> @compas.plugins.plugin(category="install")
    ... def installable_blender_packages():
    ...     return ["compas_fab"]

    Returns
    -------
    :obj:`list` of :obj:`str`
        List of package names to make available inside Blender.
    """
    pass


@compas.plugins.pluggable(category="install", selector="collect_all")
def after_blender_install(installed_packages):
    """Allows extensions to execute actions after install to Blender is done.

    Extensions providing Blender features
    can implement this pluggable interface to perform
    additional steps after an installation to Blender has
    been completed.

    Parameters
    ----------
    installed_packages : :obj:`list` of :obj:`str`
        List of packages that have been installed successfully.

    Examples
    --------
    >>> import compas.plugins
    >>> @compas.plugins.plugin(category="install")
    ... def after_blender_install(installed_packages):
    ...     # Do something after package is installed to Blender, e.g. install the COMPAS UI, etc
    ...     return [("compas_blender", "COMPAS Blender UI installed", True)]

    Returns
    -------
    :obj:`list` of 3-tuple (str, str, bool)
        List containing a 3-tuple with component name, message and True/False success flag.

    """
    pass


def _update_bootstrapper(install_path, packages):
    # Take either the CONDA environment directory or the current Python executable's directory
    python_directory = os.environ.get("CONDA_PREFIX", None) or os.path.dirname(sys.executable)
    environment_name = os.environ.get("CONDA_DEFAULT_ENV", "")
    conda_exe = os.environ.get("CONDA_EXE", "")

    compas_bootstrapper = compas_blender._get_bootstrapper_path(install_path)

    bootstrapper_data = compas_blender._get_bootstrapper_data(compas_bootstrapper)
    installed_packages = bootstrapper_data.get("INSTALLED_PACKAGES", [])
    installed_packages = list(set(installed_packages + list(packages)))

    with open(compas_bootstrapper, "w") as f:
        f.write('ENVIRONMENT_NAME = r"{}"\n'.format(environment_name))
        f.write('PYTHON_DIRECTORY = r"{}"\n'.format(python_directory))
        f.write('CONDA_EXE = r"{}"\n'.format(conda_exe))
        f.write("INSTALLED_PACKAGES = {}".format(repr(installed_packages)))


def _filter_installable_packages(version, packages):
    if not packages:
        # Flatten list of results (resulting from collect_all pluggable)
        packages = sorted(set(itertools.chain.from_iterable(installable_blender_packages())))  # type: ignore
    return packages


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        choices=compas_blender.SUPPORTED_VERSIONS,
        default=compas_blender.DEFAULT_VERSION,
        help="The version of Blender to install the packages in.",
    )
    parser.add_argument("-p", "--packages", nargs="+", help="The packages to install.")
    parser.add_argument("-c", "--clean", default=False, action="store_true", help="Clean up the installation directory")

    args = parser.parse_args()
    compas_blender.INSTALLATION_ARGUMENTS = args

    install(version=args.version, packages=args.packages, clean=args.clean)
