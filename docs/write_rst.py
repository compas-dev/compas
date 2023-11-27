# from pathlib import Path
from compas import numerical as module

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
        items=classes,
    )

functions = ""
for name in sorted(__newall__["functions"]):
    functions += "    {name}\n".format(name=name)

if functions:
    functions = SECTION.format(
        title="Functions",
        line="=" * len("Functions"),
        items=functions,
    )

numpy = ""
for name in sorted(__newall__["numpy"]):
    numpy += "    {name}\n".format(name=name)

if numpy:
    numpy = SECTION.format(
        title="Numpy",
        line="=" * len("Numpy"),
        items=numpy,
    )

pluggables = ""
for name in sorted(__newall__["pluggables"]):
    pluggables += "    {name}\n".format(name=name)

if pluggables:
    pluggables = SECTION.format(
        title="Pluggables",
        line="=" * len("Pluggables"),
        items=pluggables,
    )

plugins = ""
for name in sorted(__newall__["plugins"]):
    plugins += "    {name}\n".format(name=name)

if plugins:
    plugins = SECTION.format(
        title="Plugins",
        line="=" * len("Plugins"),
        items=plugins,
    )

sections = "".join([classes, functions, numpy, pluggables, plugins])

# docs = Path(__file__).parent

with open("/Users/vanmelet/Code/compas/docs/reference/{name}.rst".format(name=module.__name__), "w") as f:
    f.write(
        TPL.format(
            currentmodule=currentmodule,
            lead=lead,
            sections=sections,
        )
    )
