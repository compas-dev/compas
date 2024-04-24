import compas_rhino

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        choices=compas_rhino.SUPPORTED_VERSIONS,
        default=compas_rhino.DEFAULT_VERSION,
        help="The version of Rhino.",
    )

    args = parser.parse_args()

    print(compas_rhino._get_default_rhino_cpython_path(version=args.version))
