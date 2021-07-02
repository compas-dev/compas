# -*- coding: utf-8 -*-
from __future__ import print_function

import contextlib
import glob
import os
import shutil
import sys
import tempfile

from invoke import Exit
from invoke import task

BASE_FOLDER = os.path.dirname(__file__)


class Log(object):
    def __init__(self, out=sys.stdout, err=sys.stderr):
        self.out = out
        self.err = err

    def flush(self):
        self.out.flush()
        self.err.flush()

    def write(self, message):
        self.flush()
        self.out.write(message + '\n')
        self.out.flush()

    def info(self, message):
        self.write('[INFO] %s' % message)

    def warn(self, message):
        self.write('[WARN] %s' % message)


log = Log()


def confirm(question):
    while True:
        response = input(question).lower().strip()

        if not response or response in ('n', 'no'):
            return False

        if response in ('y', 'yes'):
            return True

        print('Focus, kid! It is either (y)es or (n)o', file=sys.stderr)


@task(default=True)
def help(ctx):
    """Lists available tasks and usage."""
    ctx.run('invoke --list')
    log.write('Use "invoke -h <taskname>" to get detailed help for a task.')


@task(help={
    'docs': 'True to clean up generated documentation, otherwise False',
    'bytecode': 'True to clean up compiled python files, otherwise False.',
    'builds': 'True to clean up build/packaging artifacts, otherwise False.'})
def clean(ctx, docs=True, bytecode=True, builds=True, ghuser=True):
    """Cleans the local copy from compiled artifacts."""

    with chdir(BASE_FOLDER):
        if builds:
            ctx.run('python setup.py clean')

        if bytecode:
            for root, dirs, files in os.walk(BASE_FOLDER):
                for f in files:
                    if f.endswith('.pyc'):
                        os.remove(os.path.join(root, f))
                if '.git' in dirs:
                    dirs.remove('.git')

        folders = []

        if docs:
            folders.append('docs/api/generated')

        folders.append('dist/')

        if bytecode:
            for t in ('src', 'tests'):
                folders.extend(glob.glob('{}/**/__pycache__'.format(t), recursive=True))

        if builds:
            folders.append('build/')
            folders.append('src/compas.egg-info/')

        if ghuser:
            folders.append('src/compas_ghpython/components/ghuser')

        for folder in folders:
            shutil.rmtree(os.path.join(BASE_FOLDER, folder), ignore_errors=True)


@task(help={
      'rebuild': 'True to clean all previously built docs before starting, otherwise False.',
      'doctest': 'True to run doctests, otherwise False.',
      'check_links': 'True to check all web links in docs for validity, otherwise False.'})
def docs(ctx, doctest=False, rebuild=False, check_links=False):
    """Builds package's HTML documentation."""

    if rebuild:
        clean(ctx)

    with chdir(BASE_FOLDER):
        if doctest:
            testdocs(ctx, rebuild=rebuild)

        opts = '-E' if rebuild else ''
        ctx.run('sphinx-build {} -b html docs dist/docs'.format(opts))

        if check_links:
            linkcheck(ctx, rebuild=rebuild)


@task()
def lint(ctx):
    """Check the consistency of coding style."""
    log.write('Running flake8 python linter...')
    ctx.run('flake8 src')


@task()
def testdocs(ctx, rebuild=False):
    """Test the examples in the docstrings."""
    log.write('Running doctest...')
    ctx.run('pytest --doctest-modules')


@task()
def linkcheck(ctx, rebuild=False):
    """Check links in documentation."""
    log.write('Running link check...')
    opts = '-E' if rebuild else ''
    ctx.run('sphinx-build {} -b linkcheck docs dist/docs'.format(opts))


@task()
def check(ctx):
    """Check the consistency of documentation, coding style and a few other things."""

    with chdir(BASE_FOLDER):
        lint(ctx)

        log.write('Checking MANIFEST.in...')
        ctx.run('check-manifest')

        log.write('Checking metadata...')
        ctx.run('python setup.py check --strict --metadata')


@task(help={
      'checks': 'True to run all checks before testing, otherwise False.',
      'doctest': 'True to run doctest on all modules, otherwise False.'})
def test(ctx, checks=False, doctest=False):
    """Run all tests."""
    if checks:
        check(ctx)

    with chdir(BASE_FOLDER):
        cmd = ['pytest']
        if doctest:
            cmd.append('--doctest-modules')

        ctx.run(' '.join(cmd))


@task
def prepare_changelog(ctx):
    """Prepare changelog for next release."""
    UNRELEASED_CHANGELOG_TEMPLATE = '## Unreleased\n\n### Added\n\n### Changed\n\n### Removed\n\n\n## '

    with chdir(BASE_FOLDER):
        # Preparing changelog for next release
        with open('CHANGELOG.md', 'r+') as changelog:
            content = changelog.read()
            changelog.seek(0)
            changelog.write(content.replace(
                '## ', UNRELEASED_CHANGELOG_TEMPLATE, 1))

        ctx.run('git add CHANGELOG.md && git commit -m "Prepare changelog for next release"')


@task(help={
      'gh_io_folder': 'Folder where GH_IO.dll is located. Defaults to the Rhino 6.0 installation folder (platform-specific).',
      'ironpython': 'Command for running the IronPython executable. Defaults to `ipy`.'})
def build_ghuser_components(ctx, gh_io_folder=None, ironpython=None):
    """Build Grasshopper user objects from source"""
    clean(ctx, docs=False, bytecode=False, builds=False, ghuser=True)
    with chdir(BASE_FOLDER):
        with tempfile.TemporaryDirectory('actions.ghcomponentizer') as action_dir:
            source_dir = os.path.abspath('src/compas_ghpython/components')
            target_dir = os.path.join(source_dir, 'ghuser')
            ctx.run('git clone https://github.com/compas-dev/compas-actions.ghpython_components.git {}'.format(action_dir))
            if not gh_io_folder:
                import compas_ghpython
                gh_io_folder = compas_ghpython.get_grasshopper_plugin_path('6.0')

            if not ironpython:
                ironpython = 'ipy'

            gh_io_folder = os.path.abspath(gh_io_folder)
            componentizer_script = os.path.join(action_dir, 'componentize.py')

            ctx.run('{} {} {} {} --ghio "{}"'.format(ironpython, componentizer_script, source_dir, target_dir, gh_io_folder))


@task(help={
      'release_type': 'Type of release follows semver rules. Must be one of: major, minor, patch.'})
def release(ctx, release_type):
    """Releases the project in one swift command!"""
    if release_type not in ('patch', 'minor', 'major'):
        raise Exit('The release type parameter is invalid.\nMust be one of: major, minor, patch')

    # Run checks
    ctx.run('invoke check test')

    # Bump version and git tag it
    ctx.run('bump2version %s --verbose' % release_type)

    # Build project
    ctx.run('python setup.py clean --all sdist bdist_wheel')

    # Prepare changelog for next release
    prepare_changelog(ctx)

    # Clean up local artifacts
    clean(ctx)

    # Upload to pypi
    if confirm('Everything is ready. You are about to push to git which will trigger a release to pypi.org. Are you sure? [y/N]'):
        ctx.run('git push --tags && git push')
    else:
        raise Exit('You need to manually revert the tag/commits created.')


@contextlib.contextmanager
def chdir(dirname=None):
    current_dir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(current_dir)
