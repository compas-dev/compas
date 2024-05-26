import compas_blender

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--version",
        choices=compas_blender.SUPPORTED_VERSIONS,
        default=compas_blender.DEFAULT_VERSION,
        help="The version of Blender.",
    )

    args = parser.parse_args()

    print(compas_blender._get_default_blender_python_path(args.version))
