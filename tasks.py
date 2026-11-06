import os
import sys

from compas_invocations2 import build
from compas_invocations2 import docs
from compas_invocations2 import mkdocs
from compas_invocations2 import tests
from invoke.collection import Collection
from invoke.tasks import task


@task
def typecheck(ctx):
    """Run static type checking."""
    ctx.run(f'"{sys.executable}" -m pyright --pythonpath "{sys.executable}"')


@task
def lint(ctx):
    """Run the non-mutating Ruff lint check."""
    ctx.run(f'"{sys.executable}" -m ruff check .')


@task
def format(ctx):
    """Format the configured repository files."""
    ctx.run(f'"{sys.executable}" -m ruff format .')


@task
def check(ctx):
    """Run the non-mutating Ruff lint and format checks."""
    ctx.run(f'"{sys.executable}" -m ruff check .')
    ctx.run(f'"{sys.executable}" -m ruff format --check .')


ns = Collection(
    docs.help,
    check,
    lint,
    format,
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
