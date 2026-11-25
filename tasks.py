from __future__ import print_function

import os

from compas_invocations2 import build
from compas_invocations2 import docs
from compas_invocations2 import style
from compas_invocations2 import tests
from compas_invocations2 import grasshopper
from invoke.collection import Collection
from invoke.tasks import task


@task(
    help={
        "blender": "Path to the Blender executable (defaults to $BLENDER, then PATH).",
        "from_pypi": "Bundle the released compas wheel from PyPI instead of building it from this checkout.",
    }
)
def build_blender_extension(ctx, blender=None, from_pypi=False):
    """Build the COMPAS Blender extension packages into dist/blender."""
    cmd = "python extensions/blender/build.py"
    if blender:
        cmd += ' --blender "{}"'.format(blender)
    if from_pypi:
        cmd += " --from-pypi"
    ctx.run(cmd, pty=False)


ns = Collection(
    docs.help,
    style.check,
    style.lint,
    style.format,
    docs.docs,
    docs.linkcheck,
    tests.test,
    tests.testdocs,
    tests.testcodeblocks,
    build.prepare_changelog,
    build.clean,
    build.release,
    build.build_ghuser_components,
    build.build_cpython_ghuser_components,
    build_blender_extension,
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
