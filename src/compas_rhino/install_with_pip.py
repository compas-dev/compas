import pathlib
import random
import string
import subprocess

import click

rhinocode = pathlib.Path().home() / ".rhinocode"
rhinopython = rhinocode / "py39-rh8" / "python3.9"
site_envs = rhinocode / "py39-rh8" / "site-envs"


def random_string(length=8) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def find_full_env_name(name: str) -> str:
    for filepath in site_envs.iterdir():
        if filepath.stem.startswith(name):
            return filepath.stem
    raise ValueError(f"No environment with this name exists: {name}")


def default_env_name() -> str:
    return find_full_env_name("default")


def ensure_site_env(name: str) -> str:
    try:
        fullname = find_full_env_name(name)
    except ValueError:
        fullname = f"{name}-{random_string()}"
    return fullname


@click.command()
@click.argument("package")
@click.option("--env", default="default", help="Name of the site env, without the random suffix...")
@click.option("--upgrade/--no-upgrade", default=False)
@click.option("--deps/--no-deps", default=True)
def install_package(
    package: str,
    env: str = "default",
    upgrade: bool = False,
    deps: bool = True,
):
    """Install a package with Rhino's CPython pip.

    Parameters
    ----------
    package : str
        If a package name is provided, the package will be installed from PyPI.
        If `.` or `..` is specified, the package will be installed from the source in the current or parent folder, respectively.
    env : str, optional
        The name of the virtual (site) environment in Rhino, without the random suffix.
        If no environment name is provided, the default environment will be used.
        If the environment doesn't exist, it will be created automatically.
    upgrade : bool, optional
        Attempt to upgrade packages that were already installed.
        The default is False.
    deps : bool, optional
        Attempt to install the package dependencies.
        Default is True.

    Returns
    -------
    str
        The output of the call to pip.

    Examples
    --------
    When COMPAS is installed, the function is registered as an executable command with the name `install_in_rhino`.

    $ cd path/to/local/compas/repo
    $ install_in_rhino .

    $ cd path/to/local/compas/repo
    $ install_in_rhino . --env=compas-dev

    $ cd path/to/local/compas/repo
    $ install_in_rhino . --env=compas-dev --upgrade --no-deps

    """
    if package == ".":
        package = str(pathlib.Path().cwd())
    elif package == "..":
        package = str(pathlib.Path().cwd().parent)

    target = site_envs / ensure_site_env(env or "default")
    target.mkdir(exist_ok=True)

    args = [
        str(rhinopython),
        "-m",
        "pip",
        "install",
        package,
        "--target",
        target,
        "--no-warn-script-location",
    ]

    if upgrade:
        args.append("--upgrade")

    if not deps:
        args.append("--no-deps")

    return subprocess.check_call(args)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    install_package()
