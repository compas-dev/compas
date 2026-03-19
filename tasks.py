from __future__ import print_function

import os
import shutil
import sys

from compas_invocations2 import build
from compas_invocations2 import docs
from compas_invocations2 import style
from compas_invocations2 import tests
from compas_invocations2 import grasshopper
from invoke import task
from invoke.collection import Collection


@task
def build_blender_addon(ctx, version="2.15.0", destination="dist"):
    """Build the COMPAS Blender addon."""
    
    # Define paths
    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "temp_build_blender")
    addon_dir = os.path.join(build_dir, "compas_blender")
    wheels_dir = os.path.join(addon_dir, "wheels")
    
    # Clean previous build
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    
    print("Building Blender addon version {}...".format(version))
    
    # Copy compas_blender source
    src_compas_blender = os.path.join(root_dir, "src", "compas_blender")
    shutil.copytree(src_compas_blender, addon_dir)
    
    # Create wheels directory
    os.makedirs(wheels_dir)
    
    # Build compas wheel
    print("Building compas wheel...")
    ctx.run("{} -m pip wheel . --no-deps -w {}".format(sys.executable, wheels_dir))
    
    # Note: We do NOT bundle dependencies (networkx, jsonschema, watchdog, scipy).
    # We let pip install them from PyPI on the user's machine to ensure:
    # 1. Cross-platform compatibility (getting the correct binary wheels for their OS).
    # 2. Smaller addon size.
    
    # Clean up __pycache__
    print("Cleaning up...")
    for root, dirs, files in os.walk(build_dir):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
        for f in files:
            if f.endswith(".pyc"):
                os.remove(os.path.join(root, f))

    # Clean up __pycache__
    print("Cleaning up...")
    for root, dirs, files in os.walk(build_dir):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
        for f in files:
            if f.endswith(".pyc"):
                os.remove(os.path.join(root, f))

    # Create zip
    if not os.path.exists(destination):
        os.makedirs(destination)
    zip_name = os.path.join(destination, "compas_blender-{}".format(version))
    shutil.make_archive(zip_name, 'zip', build_dir)
    
    print("Addon created at {}.zip".format(zip_name))
    
    # Cleanup build dir
    shutil.rmtree(build_dir)


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
    grasshopper.yakerize,
    grasshopper.publish_yak,
    grasshopper.update_gh_header,
    build_blender_addon,
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
