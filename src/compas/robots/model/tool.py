from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from compas.geometry import Frame
from compas.geometry import Transformation
from compas.robots.model.robot import RobotModel


class ToolModel(RobotModel):
    """Represents a tool to be attached to the robot's flange.

    Attributes
    ----------
    visual : :class:`compas.datastructures.Mesh`
        The visual mesh of the tool.
    frame : :class:`compas.geometry.Frame`
        The frame of the tool in tool0 frame.
    collision : :class:`compas.datastructures.Mesh`
        The collision mesh representation of the tool.
    name : :obj:`str`
        The name of the `ToolModel`. Defaults to 'attached_tool'.
    link_name : :obj:`str`
        The name of the `Link` to which the tool is attached.  Defaults to ``None``.

    Examples
    --------
    >>> import compas
    >>> from compas.datastructures import Mesh
    >>> from compas.geometry import Frame
    >>> mesh = Mesh.from_stl(compas.get('cone.stl'))
    >>> frame = Frame([0.14, 0, 0], [0, 1, 0], [0, 0, 1])
    >>> tool = ToolModel(mesh, frame)

    """

    def __init__(self, visual, frame_in_tool0_frame, collision=None,
                 name="attached_tool", link_name=None):
        collision = collision or visual
        super(ToolModel, self).__init__(name)
        self.add_link("attached_tool_link", visual_mesh=visual, collision_mesh=collision)

        self._rebuild_tree()
        self._create(self.root, Transformation())

        self.frame = frame_in_tool0_frame
        self.link_name = link_name

    @classmethod
    def from_robot_model(cls, robot, frame_in_tool0_frame, link_name=None):
        """Creates a ``ToolModel`` from a :class:`compas.robots.RobotModel` instance.

        Parameters
        ----------
        robot : :class:`compas.robots.RobotModel`
        frame_in_tool0_frame : :obj:`str`
            The frame of the tool in tool0 frame.
        link_name : :obj:`str`
            The name of the `Link` to which the tool is attached.  Defaults to ``None``.
        """
        data = robot.data
        data['frame'] = frame_in_tool0_frame.data
        data['link_name'] = link_name
        return cls.from_data(data)

    @property
    def data(self):
        """Returns the data dictionary that represents the tool.

        Returns
        -------
        :obj:`dict`
            The tool data.

        """
        return self._get_data()

    def _get_data(self):
        data = super(ToolModel, self)._get_data()
        data['frame'] = self.frame.data
        data['link_name'] = self.link_name
        return data

    @data.setter
    def data(self, data):
        self._set_data(data)

    def _set_data(self, data):
        super(ToolModel, self)._set_data(data)
        self.frame = Frame.from_data(data['frame'])
        self.name = self.name or 'attached_tool'
        self.link_name = data['link_name'] if 'link_name' in data else None

    def to_data(self):
        return self.data

    @classmethod
    def from_data(cls, data):
        """Construct a `ToolModel` from its data representation.  To be used
        in conjunction with the :meth:`to_data` method.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        :class:`ToolModel`
            The constructed `ToolModel`.

        """
        tool = cls(None, None)
        tool.data = data
        return tool

    @classmethod
    def from_json(cls, filepath):
        """Construct a `ToolModel` from the data contained in a JSON file.

        Parameters
        ----------
        filepath : str
            Path to the file containing the data.

        Returns
        -------
        :class:`ToolModel`
            The tool.

        Examples
        --------
        >>> import os
        >>> import compas
        >>> filepath = os.path.join(compas.DATA, "cone_tool.json")
        >>> tool = ToolModel.from_json(filepath)
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_data(data)

    def to_json(self, filepath):
        """Serialise the data dictionary representing the tool to JSON and store in a file.

        Parameters
        ----------
        filepath : :obj:`str`
            Path to the file.

        Returns
        -------
        None

        Examples
        --------
        >>> import os
        >>> import compas
        >>> from compas.datastructures import Mesh
        >>> from compas.geometry import Frame
        >>> mesh = Mesh.from_stl(compas.get('cone.stl'))
        >>> frame = Frame([0.14, 0, 0], [0, 1, 0], [0, 0, 1])
        >>> tool = ToolModel(mesh, frame)
        >>> filepath = os.path.join(compas.DATA, "cone_tool.json")
        >>> tool.to_json(filepath)
        """
        with open(filepath, 'w') as f:
            json.dump(self.data, f, indent=4, sort_keys=True)

    def from_tcf_to_t0cf(self, frames_tcf):
        """Converts a list of frames at the robot's tool tip (tcf frame) to frames at the robot's flange (tool0 frame).

        Parameters
        ----------
        frames_tcf : :obj:`list` of :class:`compas.geometry.Frame`
            Frames (in WCF) at the robot's tool tip (tcf).

        Returns
        -------
        :obj:`list` of :class:`compas.geometry.Frame`
            Frames (in WCF) at the robot's flange (tool0).

        Examples
        --------
        >>> import compas
        >>> from compas.datastructures import Mesh
        >>> from compas.geometry import Frame
        >>> mesh = Mesh.from_stl(compas.get('cone.stl'))
        >>> frame = Frame([0.14, 0, 0], [0, 1, 0], [0, 0, 1])
        >>> tool = ToolModel(mesh, frame)
        >>> frames_tcf = [Frame((-0.309, -0.046, -0.266), (0.276, 0.926, -0.256), (0.879, -0.136, 0.456))]
        >>> tool.from_tcf_to_t0cf(frames_tcf)
        [Frame(Point(-0.363, 0.003, -0.147), Vector(0.388, -0.351, -0.852), Vector(0.276, 0.926, -0.256))]
        """
        Te = Transformation.from_frame_to_frame(self.frame, Frame.worldXY())
        return [Frame.from_transformation(Transformation.from_frame(f) * Te) for f in frames_tcf]

    def from_t0cf_to_tcf(self, frames_t0cf):
        """Converts frames at the robot's flange (tool0 frame) to frames at the robot's tool tip (tcf frame).

        Parameters
        ----------
        frames_t0cf : :obj:`list` of :class:`compas.geometry.Frame`
            Frames (in WCF) at the robot's flange (tool0).

        Returns
        -------
        :obj:`list` of :class:`compas.geometry.Frame`
            Frames (in WCF) at the robot's tool tip (tcf).

        Examples
        --------
        >>> import compas
        >>> from compas.datastructures import Mesh
        >>> from compas.geometry import Frame
        >>> mesh = Mesh.from_stl(compas.get('cone.stl'))
        >>> frame = Frame([0.14, 0, 0], [0, 1, 0], [0, 0, 1])
        >>> tool = ToolModel(mesh, frame)
        >>> frames_t0cf = [Frame((-0.363, 0.003, -0.147), (0.388, -0.351, -0.852), (0.276, 0.926, -0.256))]
        >>> tool.from_t0cf_to_tcf(frames_t0cf)
        [Frame(Point(-0.309, -0.046, -0.266), Vector(0.276, 0.926, -0.256), Vector(0.879, -0.136, 0.456))]
        """
        Te = Transformation.from_frame_to_frame(Frame.worldXY(), self.frame)
        return [Frame.from_transformation(Transformation.from_frame(f) * Te) for f in frames_t0cf]
