from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
from abc import abstractmethod
from collections import defaultdict

import compas
from compas.scene.exceptions import SceneObjectNotRegisteredError
from compas.scene.exceptions import NoSceneObjectContextError
from compas.plugins import PluginValidator
from compas.plugins import pluggable

from .descriptors.protocol import DescriptorProtocol


@pluggable(category="drawing-utils")
def clear():
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
    other_contexts = [v for v in SceneObject.ITEM_SCENEOBJECT.keys()]
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
        context = SceneObject.ITEM_SCENEOBJECT[context_name]

        for type_ in inspect.getmro(dtype):
            cls = context.get(type_, None)
            if cls is not None:
                break

    if cls is None:
        raise SceneObjectNotRegisteredError(
            "No scene object is registered for this data type: {} in this context: {}".format(dtype, context_name)
        )

    return cls


class SceneObject(object):
    """Base class for all scene objects.

    Parameters
    ----------
    item : Any
        The item which should be visualized using the created SceneObject.
    context : str, optional
        Explicit context to pick the SceneObject from.
        If not specified, an attempt will be made to automatically detect the appropriate context.

    Attributes
    ----------
    ITEM_SCENEOBJECT : dict[str, dict[Type[:class:`~compas.data.Data`], Type[:class:`~compas.scene.SceneObject`]]]
        Dictionary mapping data types to the corresponding scene objects types per visualization context.

    """

    # add this to support the descriptor protocol vor Python versions below 3.6
    __metaclass__ = DescriptorProtocol

    __SCENEOBJECTS_REGISTERED = False

    ITEM_SCENEOBJECT = defaultdict(dict)

    def __new__(cls, item, **kwargs):
        if not SceneObject.__SCENEOBJECTS_REGISTERED:
            cls.register_scene_objects()
            SceneObject.__SCENEOBJECTS_REGISTERED = True

        if item is None:
            raise ValueError(
                "Cannot create a scene object for None. Please ensure you pass a instance of a supported class."
            )

        cls = _get_sceneobject_cls(item, **kwargs)
        PluginValidator.ensure_implementations(cls)
        return super(SceneObject, cls).__new__(cls)

    def __init__(self, item, **kwargs):
        self._item = item
        self._transformation = None

    @property
    def transformation(self):
        """The transformation matrix of the scene object.

        Returns
        -------
        :class:`Transformation` or None
            The transformation matrix.

        """
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        self._transformation = transformation

    @staticmethod
    def build(item, **kwargs):
        """Build a scene object corresponding to the item type.

        Parameters
        ----------
        **kwargs : dict[str, Any], optional
            The keyword arguments (kwargs) collected in a dict.
            For relevant options, see the parameter lists of the matching scene object type.

        Returns
        -------
        :class:`~compas.scene.SceneObject`
            A scene object of the type matching the provided item according to the item-sceneobject map :attr:`~SceneObject.ITEM_SCENEOBJECT`.
            The map is created by registering item-sceneobject type pairs using :meth:`~SceneObject.register`.

        """
        sceneobject_type = _get_sceneobject_cls(item, **kwargs)
        sceneobject = sceneobject_type(item, **kwargs)
        return sceneobject

    @staticmethod
    def build_as(item, sceneobject_type, **kwargs):
        """Build a scene object with the given type.

        Parameters
        ----------
        sceneobject_type : :class:`~compas.scene.SceneObject`
        **kwargs : dict[str, Any], optional
            The keyword arguments (kwargs) collected in a dict.
            For relevant options, see the parameter lists of the matching sceneobject type.

        Returns
        -------
        :class:`~compas.scene.SceneObject`
            A scene object of the given type.

        """
        sceneobject = sceneobject_type(item, **kwargs)
        return sceneobject

    @staticmethod
    def clear():
        """Clear all objects from the view.

        Returns
        -------
        None

        """
        return clear()

    @staticmethod
    def redraw():
        """Redraw the view.

        Returns
        -------
        None

        """
        return redraw()

    @staticmethod
    def register_scene_objects():
        """Register SceneObjects using available plugins.

        Returns
        -------
        List[str]
            List containing names of discovered SceneObject plugins.

        """
        return register_scene_objects()

    @staticmethod
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
        SceneObject.ITEM_SCENEOBJECT[context][item_type] = sceneobject_type

    @abstractmethod
    def draw(self):
        """The main drawing method."""
        raise NotImplementedError

    @staticmethod
    def draw_collection(collection):
        """Drawing method for drawing an entire collection of objects."""
        raise NotImplementedError
