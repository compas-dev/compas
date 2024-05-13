import subprocess

import compas_rhino


def install(args):
    subprocess.check_call([compas_rhino._get_default_rhino_cpython_path("8.0"), "-m", "pip", "install"] + args)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("pipargs", help="Arguments to be passed on to pip as a string")

    args = parser.parse_args()
    pipargs = args.pipargs.split()

    install(pipargs)
