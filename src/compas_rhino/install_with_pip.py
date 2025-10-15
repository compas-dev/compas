import argparse
import pathlib
import random
import shutil
import string
import subprocess
from typing import Optional

import compas

executable = "python" if compas.WINDOWS else "python3.9"
rhinocode = pathlib.Path().home() / ".rhinocode"
rhinopython = rhinocode / "py39-rh8" / executable
site_envs = rhinocode / "py39-rh8" / "site-envs"


def random_string(length=8) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def find_full_env_name(name: str) -> str:
    for filepath in site_envs.iterdir():
        if filepath.stem.startswith(name):
            return filepath.stem
    raise ValueError(f"No environment with this name exists: {name}")


def ensure_site_env(name: str) -> str:
    try:
        fullname = find_full_env_name(name)
    except ValueError:
        fullname = f"{name}-{random_string()}"
    return fullname


def install_package(
    packages: list[str],
    requirements: Optional[str] = None,
    env: str = "default",
    upgrade: bool = False,
    deps: bool = True,
    clear: bool = False,
):
    """Install a package with Rhino's CPython pip."""

    if requirements and packages:
        raise ValueError("You must provide either packages or a requirements file, not both.")

    if requirements:
        params = ["-r", str(pathlib.Path(requirements).resolve())]
    elif packages:
        params = []
        for p in packages:
            if p == ".":
                p = str(pathlib.Path().cwd())
            elif p == "..":
                p = str(pathlib.Path().cwd().parent)
            params.append(p)
    else:
        raise ValueError("You must provide either packages or a requirements file.")

    env = env or "default"

    if clear:
        try:
            fullname = find_full_env_name(env)
        except ValueError:
            pass
        else:
            target = site_envs / fullname
            shutil.rmtree(target, ignore_errors=True)

    target = site_envs / ensure_site_env(env)
    target.mkdir(exist_ok=True)

    args = [
        str(rhinopython),
        "-m",
        "pip",
        "install",
        *params,
        "--target",
        str(target),
        "--no-warn-script-location",
    ]

    if upgrade:
        args.append("--upgrade")
    if not deps:
        args.append("--no-deps")

    return subprocess.check_call(args)


def main():
    parser = argparse.ArgumentParser(description="Install a package with Rhino's CPython pip.")
    parser.add_argument("packages", help="The package(s) to install (PyPI names or local package paths)", nargs="*")
    parser.add_argument("-r", "--requirements", help="Path to a requirements file")
    parser.add_argument("--env", default="default", help="Name of the site env, without the random suffix")
    parser.add_argument("--upgrade", action="store_true", help="Attempt to upgrade packages already installed")
    parser.add_argument("--no-deps", dest="deps", action="store_false", help="Do not install dependencies")
    parser.add_argument("--clear", action="store_true", help="Clear the environment before installing")
    parser.set_defaults(deps=True)
    args = parser.parse_args()

    install_package(
        packages=args.packages,
        requirements=args.requirements,
        env=args.env,
        upgrade=args.upgrade,
        deps=args.deps,
        clear=args.clear,
    )


if __name__ == "__main__":
    main()
