from importlib import import_module

modules = [
    'compas',
    'compas.com',
    'compas.datastructures',
    'compas.files',
    'compas.geometry',
    'compas.hpc',
    'compas.interop',
    'compas.numerical',
    'compas.visualization',
    'compas.utilities',

    'compas_rhino',
    'compas_rhino.conduits',
    'compas_rhino.forms',
    'compas_rhino.geometry',
    'compas_rhino.helpers',
    'compas_rhino.ui',
    'compas_rhino.utilities',

    'compas_blender',
    'compas_blender.forms',
    'compas_blender.geometry',
    'compas_blender.helpers',
    'compas_blender.ui',
    'compas_blender.utilities',

    'compas_maya',

    'compas_grasshopper',
    'compas_dynamo',

]


for name in modules:
    obj = import_module(name)

    print obj

    with open('reference/{0}.rst'.format(name), 'wb+') as fp:
        fp.write(obj.__doc__)
