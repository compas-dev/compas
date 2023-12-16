from compas.plugins import pluggable
from compas.plugins import PluginValidator
from .exceptions import NoSceneObjectContextError
from .exceptions import SceneObjectNotRegisteredError
import inspect
import compas
from collections import defaultdict

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
    # TODO: implement [without introducing compas_view2 as a dependency..?]
    # make the viewer app a singleton
    # check for the exitence of an instance of the singleton
    # if the instance exists, return True
    # in this case, the viewer is the current context
    # to do this without introducing compas_view2 as a dependency,
    # creating the singleton instance should modify a class attribute of the SceneObject
    # (or potentially a module level attribute of compas itself)
    return False


def _detect_current_context():
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
    raise NoSceneObjectContextError()


def _get_sceneobject_cls(data, **kwargs):
    # in any case user gets to override the choice
    context_name = kwargs.get("context") or _detect_current_context()

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


def build_scene_object(item, **kwargs):
    if not ITEM_SCENEOBJECT:
        register_scene_objects()

    if item is None:
        raise ValueError(
            "Cannot create a scene object for None. Please ensure you pass a instance of a supported class."
        )

    cls = _get_sceneobject_cls(item, **kwargs)
    PluginValidator.ensure_implementations(cls)
    return cls(item, **kwargs)
