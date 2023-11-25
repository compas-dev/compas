import compas
from compas import geometry

functions = []
classes = []
errors = []
numpy = []

__newall__ = {
    "functions": [],
    "classes": [],
    "errors": [],
    "numpy": [],
}

for name in geometry.__all__:
    obj = getattr(geometry, name)

    if name.endswith("_numpy"):
        numpy.append(name)
        continue

    if isinstance(obj, type):
        classes.append(name)
    else:
        functions.append(name)

for name in sorted(classes):
    __newall__["classes"].append(name)

for name in sorted(functions):
    __newall__["functions"].append(name)

for name in sorted(numpy):
    __newall__["numpy"].append(name)


compas.json_dump(__newall__, "docs/geometry__all__.json", pretty=True)
