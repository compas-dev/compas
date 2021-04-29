import sys


__all__ = [
    'unload_modules',
]


def unload_modules(top_level_module_name):
    """Unloads all modules named starting with the specified string.

    This function eases the development workflow when editing a library that is
    used from Blender.

    Parameters
    ----------
    top_level_module_name : :obj:`str`
        Name of the top-level module to unload.

    Returns
    -------
    list
        List of unloaded module names.
    """
    modules = list(filter(lambda m: m.startswith(top_level_module_name), sys.modules))

    for module in modules:
        sys.modules.pop(module)

    return modules
