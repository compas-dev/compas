from pathlib import Path
from compas import geometry

TPL = """
********************************************************************************
{currentmodule}
********************************************************************************

.. currentmodule:: {currentmodule}

.. rst-class:: lead

{lead}

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

{classes}

Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

{functions}

Functions using NumPy
=====================

.. autosummary::
    :toctree: generated/
    :nosignatures:

{numpy}

Pluggables
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

{pluggables}

"""

__newall__ = {
    "functions": [],
    "classes": [],
    "errors": [],
    "numpy": [],
}

for name in geometry.__all__:
    obj = getattr(geometry, name)

    if name.endswith("_numpy"):
        __newall__["numpy"].append(name)
        continue

    if isinstance(obj, type):
        __newall__["classes"].append(name)
    else:
        __newall__["functions"].append(name)


currentmodule = "compas.geometry"

lead = """
This package provides a wide range of geometry objects and geometric algorithms
independent from the geometry kernels of CAD software.
"""

classes = ""
for name in sorted(__newall__["classes"]):
    classes += f"    {name}\n"

functions = ""
for name in sorted(__newall__["functions"]):
    functions += f"    {name}\n"

numpy = ""
for name in sorted(__newall__["numpy"]):
    numpy += f"    {name}\n"

pluggables = ""
# for name in sorted(__newall__["pluggables"]):
#     pluggables += f"    {name}\n"

# print(
#     TPL.format(
#         currentmodule=currentmodule,
#         lead=lead,
#         classes=classes,
#         functions=functions,
#         numpy="",
#     )
# )

docs = Path(__file__).parent

with open(docs / "reference/compas.geometry.rst", "w") as f:
    f.write(
        TPL.format(
            currentmodule=currentmodule,
            lead=lead,
            classes=classes,
            functions=functions,
            numpy=numpy,
            pluggables=pluggables,
        )
    )
