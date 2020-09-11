import compas.plugins


@compas.plugins.plugin(category='install')
def installable_rhino_packages(category='install'):
    return ['compas_ghpython']
