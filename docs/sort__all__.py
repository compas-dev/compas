import compas
from compas_blender import conversions as module

functions = []
classes = []
errors = []
numpy = []

__newall__ = {
    "classes": [],
    "errors": [],
    "functions": [],
    "numpy": [],
    "pluggables": [],
    "plugins": [],
}

for name in module.__all__:
    obj = getattr(module, name)

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


compas.json_dump(__newall__, f"docs/{module.__name__}__all__.json", pretty=True)
