from __future__ import print_function

import os

from compas_invocations2 import build
from compas_invocations2 import style
from compas_invocations2 import tests
from compas_invocations2 import grasshopper
from invoke import task
from invoke.collection import Collection


@task
def docs(ctx):
    """Build documentation with MkDocs."""
    ctx.run("mkdocs build --strict")


@task
def serve(ctx):
    """Serve documentation locally with live reload."""
    ctx.run("mkdocs serve")


ns = Collection(
    docs,
    serve,
    style.check,
    style.lint,
    style.format,
    tests.test,
    tests.testdocs,
    tests.testcodeblocks,
    build.prepare_changelog,
    build.clean,
    build.release,
    build.build_ghuser_components,
    build.build_cpython_ghuser_components,
    grasshopper.yakerize,
    grasshopper.publish_yak,
    grasshopper.update_gh_header,
)
ns.configure(
    {
        "base_folder": os.path.dirname(__file__),
        "ghuser": {
            "source_dir": "src/compas_ghpython/components",
            "target_dir": "src/compas_ghpython/components/ghuser",
            "prefix": "COMPAS: ",
        },
        "ghuser_cpython": {
            "source_dir": "src/compas_ghpython/components_cpython",
            "target_dir": "src/compas_ghpython/components_cpython/ghuser",
            "prefix": "COMPAS: ",
        },
    }
)
