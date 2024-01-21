import scriptcontext as sc  # type: ignore

from compas.scene import SceneObject


class RhinoSceneObject(SceneObject):
    """Base class for all Rhino scene objects.

    Parameters
    ----------
    layer : str, optional
        A layer name.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, layer=None, **kwargs):
        super(RhinoSceneObject, self).__init__(**kwargs)
        self.layer = layer

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
        # if self.layer:
        #     compas_rhino.clear_layer(self.layer)
