import inspect
import sys
import warnings
from collections import defaultdict

import compas
from compas.plugins import PluginValidator
from compas.plugins import pluggable
from compas.plugins import plugin_manager

from .exceptions import SceneObjectNotRegisteredError

ITEM_SCENEOBJECT = defaultdict(dict)

# registrations are made by plugins, so they are stale once the plugins are rediscovered
plugin_manager.add_reset_callback(ITEM_SCENEOBJECT.clear)


@pluggable(category="drawing-utils")
def clear(guids=None):
    """Pluggable to clear the current context of the scene or a list of objects through guids.

    Parameters
    ----------
    guids : list, optional
        A list of guids to clear.

    Returns
    -------
    None
    """
    raise NotImplementedError


clear.__pluggable__ = True


@pluggable(category="drawing-utils")
def before_draw():
    """Pluggable to perform operations before drawing the scene. This function is automatically called in the beginning of `compas.scene.Scene.draw()`.

    Returns
    -------
    None

    """
    pass


before_draw.__pluggable__ = True


@pluggable(category="drawing-utils")
def after_draw(drawn_objects):
    """Pluggable to perform operations after drawing the scene. This function is automatically called at the end of `compas.scene.Scene.draw()`.
    Parameters
    ----------
    drawn_objects : list
        A list of objects that were drawn.

    Returns
    -------
    None

    """
    pass


after_draw.__pluggable__ = True


@pluggable(category="factories", selector="collect_all")
def register_scene_objects():
    """Registers scene objects available in the current context."""
    raise NotImplementedError


register_scene_objects.__pluggable__ = True


def register(item_type, sceneobject_type, context=None):
    """Register a scene object type to a data type.

    Parameters
    ----------
    item_type : :class:`~compas.data.Data`
        The type of data item.
    sceneobject_type : :class:`~compas.scene.SceneObject`
        The type of the corresponding/compatible scene object.
    context : Literal['Viewer', 'Rhino', 'Grasshopper', 'Blender'], optional
        The visualization context in which the pair should be registered.

    Returns
    -------
    None

    """
    ITEM_SCENEOBJECT[context][item_type] = sceneobject_type


def detect_current_context():
    """Chooses an appropriate context depending on available contexts and open instances. with the following priority:
    1. Viewer
    2. Plotter
    3. Rhino / GH - checked explicitly since SceneObjects for both get registered when code is run from either.
    4. Other

    Returns
    -------
    str
        Name of an available context, used as key in :attr:`SceneObject.ITEM_SCENEOBJECT`

    """

    if compas.is_grasshopper():
        return "Grasshopper"
    if compas.is_rhino():
        return "Rhino"
    if compas.is_blender():
        return "Blender"
    # other_contexts = [v for v in ITEM_SCENEOBJECT.keys()]
    # if other_contexts:
    #     return other_contexts[0]

    return None


def _get_sceneobject_cls(data, **kwargs):
    # in any case user gets to override the choice
    context_name = kwargs.get("context") or detect_current_context()

    dtype = type(data)
    cls = None

    if "sceneobject_type" in kwargs:
        cls = kwargs["sceneobject_type"]
    else:
        context = ITEM_SCENEOBJECT[context_name]

        for type_ in inspect.getmro(dtype):
            cls = context.get(type_, None)
            if cls is not None:
                break

    if cls is None:
        message = "No scene object is registered for this data type: {} in this context: {}".format(dtype, context_name)
        reason = _diagnose_reloaded_type(dtype, ITEM_SCENEOBJECT[context_name])
        if reason:
            message += "\n" + reason
        raise SceneObjectNotRegisteredError(message)

    return cls


def _diagnose_reloaded_type(dtype, context):
    # A registered type with the same name as the item's type (or one of its bases) is a different definition of the same class,
    # i.e. one of them was created before its module was unloaded (e.g. using compas_rhino.unload_modules) and re-imported.
    for type_ in inspect.getmro(dtype):
        for registered in context:
            if registered.__module__ != type_.__module__ or registered.__name__ != type_.__name__:
                continue

            module = sys.modules.get(type_.__module__)
            if getattr(module, type_.__name__, None) is type_:
                return "A stale definition of {} is registered. This happens when a module is reloaded, but the module registering its scene object is not.".format(type_)
            return "The item is an instance of a stale definition of {}. Re-create the item after reloading modules.".format(type_)
    return None


def get_sceneobject_cls(item, **kwargs):
    if not ITEM_SCENEOBJECT:
        for result in register_scene_objects():
            # collect_all returns the exceptions of failed plugins instead of raising them
            if isinstance(result, Exception):
                warnings.warn("Failed to register scene objects: {!r}".format(result))

    if item is None:
        raise ValueError("Cannot create a scene object for None. Please ensure you pass a instance of a supported class.")

    cls = _get_sceneobject_cls(item, **kwargs)
    PluginValidator.ensure_implementations(cls)
    return cls
