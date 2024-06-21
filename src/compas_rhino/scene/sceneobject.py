from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore
import System  # type: ignore

import compas_rhino.layers
from compas.scene import SceneObject

from .helpers import ensure_layer


class RhinoSceneObject(SceneObject):
    """Base class for all Rhino scene objects.

    Parameters
    ----------
    layer : str, optional
        A layer name.
    group : str, optional
        The name of the group to add the mesh components. The group will be created if not already present.
        Default is ``None``.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    layer : str
        The name of the layer.
    group : str
        The name of the group.

    """

    def __init__(self, layer=None, group=None, **kwargs):
        super(RhinoSceneObject, self).__init__(**kwargs)
        self.layer = layer
        self.group = group

    def get_group(self, name):
        """Find the group with the given name, or create a new one.

        Parameters
        ----------
        name : str
            The name of the group.

        Returns
        -------
        :rhino:`Rhino.DocObjects.Group`

        """
        group = sc.doc.Groups.FindName(name)
        if not group:
            if sc.doc.Groups.Add(name) < 0:
                raise Exception("Failed to add group: {}".format(name))
            group = sc.doc.Groups.FindName(name)
        return group

    def add_to_group(self, name, guids):
        """Add the objects to the group.

        Parameters
        ----------
        name : str
            The name of the group.
        guids : list[System.Guid]
            A list of GUIDs.

        Returns
        -------
        None

        """
        group = self.get_group(name)
        if group:
            sc.doc.Groups.AddToGroup(group.Index, guids)

    def clear_layer(self):
        """Clear the layer of the scene object.

        Returns
        -------
        None

        """
        if self.layer:
            compas_rhino.layers.clear_layer(self.layer)

    def compile_attributes(self, name=None, color=None, arrow=None):
        """Compile Rhino DocObject Attributes.

        Parameters
        ----------
        name : str, optional
            The name of the object.
        color : :class:`compas.colors.Color`, optional
            The color of the object.
        arrow : {'end', 'start'}, optional
            Add an arrow at the start or end of the object.

        Returns
        -------
        :rhino:`Rhino.DocObjects.ObjectAttributes`

        """
        name = name or self.item.name
        color = color or self.color

        attributes = Rhino.DocObjects.ObjectAttributes()

        if name:
            attributes.Name = name

        if color:
            attributes.ObjectColor = System.Drawing.Color.FromArgb(*color.rgb255)
            attributes.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject

        if self.layer:
            attributes.LayerIndex = ensure_layer(self.layer)

        if arrow:
            if arrow == "end":
                attributes.ObjectDecoration = Rhino.DocObjects.ObjectDecoration.EndArrowhead
            elif arrow == "start":
                attributes.ObjectDecoration = Rhino.DocObjects.ObjectDecoration.StartArrowhead

        return attributes
