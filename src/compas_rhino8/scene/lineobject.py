import scriptcontext as sc  # type: ignore

from compas.scene import GeometryObject
from compas.colors import Color
from compas_rhino8.conversions import line_to_rhino
from compas_rhino8.conversions import transformation_to_rhino
from .sceneobject import RhinoSceneObject
from ._helpers import attributes


class LineObject(RhinoSceneObject, GeometryObject):
    """Scene object for drawing lines.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
        A COMPAS line.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, line, **kwargs):
        super(LineObject, self).__init__(geometry=line, **kwargs)

    def draw(self, color=None):
        """Draw the line.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`compas.colors.Color`, optional
            The RGB color of the line.

        Returns
        -------
        System.Guid
            The GUID of the created Rhino object.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        geometry = line_to_rhino(self.geometry)
        geometry.Transform(transformation_to_rhino(self.worldtransformation))

        self._guids = [sc.doc.Objects.AddLine(geometry, attr)]
        return self.guids
