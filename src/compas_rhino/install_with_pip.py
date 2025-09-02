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
def install_package(package, env, upgrade, deps):
    if package == ".":
        package = pathlib.Path().cwd()
    elif package == "..":
        package = pathlib.Path().cwd().parent

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
