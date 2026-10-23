import os
import sys

from compas_invocations2 import build
from compas_invocations2 import docs
from compas_invocations2 import mkdocs
from compas_invocations2 import style
from compas_invocations2 import tests
from invoke import task
from invoke.collection import Collection


@task
def typecheck(ctx):
    """Run static type checking."""
    ctx.run(f'pyright --pythonpath "{sys.executable}" src/compas')


ns = Collection(
    docs.help,
    style.check,
    style.lint,
    style.format,
    typecheck,
    mkdocs.docs,
    tests.test,
    tests.testdocs,
    build.clean,
)
ns.configure(
    {
        "base_folder": os.path.dirname(__file__),
    }
)
