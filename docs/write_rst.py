# from pathlib import Path
from compas import datastructures as module

TPL = """
********************************************************************************
{currentmodule}
********************************************************************************

.. currentmodule:: {currentmodule}

.. rst-class:: lead

{lead}
{sections}

"""

SECTION = """
{title}
{line}

{summary}

.. autosummary::
    :toctree: generated/
    :nosignatures:

{items}
"""

__newall__ = {
    "functions": [],
    "classes": [],
    "errors": [],
    "numpy": [],
    "pluggables": [],
    "plugins": [],
}

for name in module.__all__:
    obj = getattr(module, name)

    if name.endswith("_numpy"):
        __newall__["numpy"].append(name)
        continue

    if issubclass(type(obj), Exception):
        __newall__["errors"].append(name)
        continue

    if hasattr(obj, "__pluggable__"):
        __newall__["pluggables"].append(name)
        continue

    if hasattr(obj, "__plugin__"):
        __newall__["plugins"].append(name)
        continue

    if isinstance(obj, type):
        __newall__["classes"].append(name)
    else:
        __newall__["functions"].append(name)


currentmodule = module.__name__

lead = module.__doc__

classes = ""
for name in sorted(__newall__["classes"]):
    classes += "    {name}\n".format(name=name)

if classes:
    classes = SECTION.format(
        title="Classes",
        line="=" * len("Classes"),
        summary="",
        items=classes,
    )

errors = ""
for name in sorted(__newall__["errors"]):
    errors += "    {name}\n".format(name=name)

if errors:
    errors = SECTION.format(
        title="Exceptions",
        line="=" * len("Exceptions"),
        summary="",
        items=errors,
    )

functions = ""
for name in sorted(__newall__["functions"]):
    functions += "    {name}\n".format(name=name)

if functions:
    functions = SECTION.format(
        title="Functions",
        line="=" * len("Functions"),
        summary="",
        items=functions,
    )

numpy = ""
for name in sorted(__newall__["numpy"]):
    numpy += "    {name}\n".format(name=name)

if numpy:
    numpy = SECTION.format(
        title="Functions using Numpy",
        line="=" * len("Functions using Numpy"),
        summary="In environments where numpy is not available, these functions can still be accessed through RPC.",
        items=numpy,
    )

pluggables = ""
for name in sorted(__newall__["pluggables"]):
    pluggables += "    {name}\n".format(name=name)

if pluggables:
    pluggables = SECTION.format(
        title="Pluggables",
        line="=" * len("Pluggables"),
        summary="Pluggables are functions that don't have an actual implementation, but receive an implementation from a plugin.",
        items=pluggables,
    )

plugins = ""
for name in sorted(__newall__["plugins"]):
    plugins += "    {name}\n".format(name=name)

if plugins:
    plugins = SECTION.format(
        title="Plugins",
        line="=" * len("Plugins"),
        summary="Plugins provide implementations for pluggables. You can use the plugin directly, or through the pluggable.",
        items=plugins,
    )

sections = "".join([classes, errors, functions, numpy, pluggables, plugins])

# docs = Path(__file__).parent

with open("/Users/vanmelet/Code/compas/docs/api/{name}.rst".format(name=module.__name__), "w") as f:
    f.write(
        TPL.format(
            currentmodule=currentmodule,
            lead=lead,
            sections=sections,
        )
    )
