import subprocess
import compas_rhino


def install(package, *args):
    subprocess.check_call([compas_rhino._get_default_rhino_cpython_path, "-m", "pip", "install", package] + list(args))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        choices=["8.0"],
        default="8.0",
        help="The version of Rhino to install the packages in.",
    )

    args = parser.parse_args()
    compas_rhino.INSTALLATION_ARGUMENTS = args

    install("compas")
