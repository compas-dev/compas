import compas


def test_compas_3_version_metadata():
    assert compas.__version__.split("-", 1)[0] == "3.0.0"
