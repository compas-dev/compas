from __future__ import print_function

import os

from compas_invocations2 import build
from compas_invocations2 import docs
from compas_invocations2 import style
from compas_invocations2 import tests
from invoke import Collection

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
)
ns.configure(
    {
        "base_folder": os.path.dirname(__file__),
        "ghuser": {
            "source_dir": "src/compas_ghpython/components",
            "target_dir": "src/compas_ghpython/components/ghuser",
            "prefix": "COMPAS: ",
        },
    }
)
