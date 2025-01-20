from __future__ import print_function

import os

from compas_invocations2 import build
from compas_invocations2 import docs
from compas_invocations2 import style
from compas_invocations2 import tests
from compas_invocations2 import grasshopper
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
    grasshopper.build_ghuser_components,
    grasshopper.build_cpython_ghuser_components,
    grasshopper.yakerize,
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
