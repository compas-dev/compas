import inspect
from collections import defaultdict

import compas
from compas.plugins import PluginValidator
from compas.plugins import pluggable

from .exceptions import SceneObjectNotRegisteredError

ITEM_SCENEOBJECT = defaultdict(dict)


@pluggable(category="drawing-utils")
def clear(guids=None):
    raise NotImplementedError


clear.__pluggable__ = True


@pluggable(category="drawing-utils")
def redraw():
    raise NotImplementedError


redraw.__pluggable__ = True


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


def is_viewer_open():
    """Returns True if an instance of the compas_view2 App is available.

    Returns
    -------
    bool

    """
    from compas.scene import Scene

    return Scene.viewerinstance is not None


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

    if not ITEM_SCENEOBJECT:
        register_scene_objects()

    if is_viewer_open():
        return "Viewer"
    if compas.is_grasshopper():
        return "Grasshopper"
    if compas.is_rhino():
        return "Rhino"
    if compas.is_blender():
        return "Blender"
    other_contexts = [v for v in ITEM_SCENEOBJECT.keys()]
    if other_contexts:
        return other_contexts[0]

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
        raise SceneObjectNotRegisteredError(
            "No scene object is registered for this data type: {} in this context: {}".format(dtype, context_name)
        )

    return cls


def get_sceneobject_cls(item, **kwargs):
    if item is None:
        raise ValueError(
            "Cannot create a scene object for None. Please ensure you pass a instance of a supported class."
        )

    cls = _get_sceneobject_cls(item, **kwargs)
    PluginValidator.ensure_implementations(cls)
    return cls
