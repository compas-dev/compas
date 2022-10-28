from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools

from compas.geometry import Frame
from compas.geometry import Scale
from compas.geometry import Transformation
from compas.robots import Geometry
from compas.robots.model.link import LinkItem

from .artist import Artist


class AbstractRobotModelArtist(object):
    def transform(self, geometry, transformation):
        """Transforms a CAD-specific geometry using a Transformation.

        Parameters
        ----------
        geometry : object
            A CAD-specific (i.e. native) geometry object as returned by :meth:`create_geometry`.
        transformation : :class:`~compas.geometry.Transformation`
            Transformation to update the geometry object.

        """
        raise NotImplementedError

    def create_geometry(self, geometry, name=None, color=None):
        """Draw geometry in the respective CAD environment.

        Note
        ----
        This is an abstract method that needs to be implemented by derived classes.

        Parameters
        ----------
        geometry : :class:`~compas.datastructures.Mesh`
            Instance of a mesh data structure
        name : str, optional
            The name of the mesh to draw.

        Returns
        -------
        object
            CAD-specific geometry

        """
        raise NotImplementedError


class RobotModelArtist(AbstractRobotModelArtist, Artist):
    """Provides common functionality to most robot model artist implementations.

    In COMPAS, "artists" are classes that assist with the visualization of
    datastructures and models, in a way that maintains the data separated from the
    specific CAD interfaces, while providing a way to leverage native performance
    of the CAD environment.

    There are two methods that implementers of this base class should provide, one
    is concerned with the actual creation of geometry in the native format of the
    CAD environment (:meth:`create_geometry`) and the other is one to apply a transformation
    to geometry (:meth:`transform`).

    Attributes
    ----------
    model : :class:`~compas.robots.RobotModel`
        Instance of a robot model.

    """

    def __init__(self, model):
        super(RobotModelArtist, self).__init__()
        self.model = model
        self.create()
        self.scale_factor = 1.0
        self.attached_tool_models = {}
        self.attached_items = {}

    @property
    def attached_tool_model(self):
        """
        For backwards compatibility. Returns the tool attached to the first end effector link or,
        if not available, the first tool from the dictionary.
        Returns None if no tool are attached.

        Returns
        -------
        :class: `~compas.robots.model.ToolModel`

        """
        tool_model = None
        if self.attached_tool_models:
            link_name = self.model.get_end_effector_link()
            tool_model = self.attached_tool_models.get(link_name) or list(self.attached_tool_models.values())[0]
        return tool_model

    def attach_tool_model(self, tool_model):
        """Attach a tool to the robot artist for visualization.

        Parameters
        ----------
        tool_model : :class:`~compas.robots.ToolModel`
            The tool that should be attached to the robot's flange.

        """
        self.create(tool_model.root, "attached_tool")

        if not tool_model.link_name:
            link = self.model.get_end_effector_link()
            tool_model.link_name = link.name
        else:
            link = self.model.get_link_by_name(tool_model.link_name)

        # don't attach twice on the same link
        self.attached_tool_models[tool_model.link_name] = tool_model

        ee_frame = link.parent_joint.origin.copy()
        initial_transformation = Transformation.from_frame_to_frame(Frame.worldXY(), ee_frame)

        sample_geometry = link.collision[0] if link.collision else link.visual[0] if link.visual else None

        if hasattr(sample_geometry, "current_transformation"):
            relative_transformation = sample_geometry.current_transformation
        else:
            relative_transformation = Transformation()

        transformation = relative_transformation.concatenated(initial_transformation)

        self.update_tool(tool=tool_model, transformation=transformation)

        tool_model.parent_joint_name = link.parent_joint.name

    def detach_tool_model(self, tool_model=None):
        """
        Detach tool_model from this robot model.
        If tool_model is None, all attached tools are detached.

        Parameters
        ----------
        tool_model : :class:`~compas.robots.ToolModel`
            The tool that should be detached from the robot's flange.
            If None, all attached tools tools are removed.
        """
        if tool_model:
            del self.attached_tool_models[tool_model.link_name]
        else:
            self.attached_tool_models.clear()

    def attach_mesh(self, mesh, name, link=None, frame=None):
        """Rigidly attaches a compas mesh to a given link for visualization.

        Parameters
        ----------
        mesh : :class:`~compas.datastructures.Mesh`
            The mesh to attach to the robot model.
        name : str
            The identifier of the mesh.
        link : :class:`~compas.robots.Link`
            The link within the robot model or tool model to attach the mesh to. Optional.
            Defaults to the model's end effector link.
        frame : :class:`~compas.geometry.Frame`
            The frame of the mesh. Defaults to :meth:`compas.geometry.Frame.worldXY`.

        Returns
        -------
        None

        """
        if not link:
            link = self.model.get_end_effector_link()
        transformation = Transformation.from_frame(frame) if frame else Transformation()

        sample_geometry = None

        while sample_geometry is None:
            sample_geometry = link.collision[0] if link.collision else link.visual[0] if link.visual else None
            link = self.model.get_link_by_name(link.parent_joint.parent.link)

        native_mesh = self.create_geometry(mesh)
        init_transformation = transformation * sample_geometry.init_transformation
        self.transform(native_mesh, sample_geometry.current_transformation * init_transformation)

        item = LinkItem()
        item.native_geometry = [native_mesh]
        item.init_transformation = init_transformation
        item.current_transformation = sample_geometry.current_transformation

        self.attached_items.setdefault(link.name, {})[name] = item

    def detach_mesh(self, name):
        """Removes attached collision meshes with a given name.

        Parameters
        ----------
        name : str
            The identifier of the mesh.

        Returns
        -------
        None

        """
        for _, items in self.attached_items:
            items.pop(name, None)

    def create(self, link=None, context=None):
        """Recursive function that triggers the drawing of the robot model's geometry.

        This method delegates the geometry drawing to the :meth:`create_geometry`
        method. It transforms the geometry based on the saved initial
        transformation from the robot model.

        Parameters
        ----------
        link : :class:`~compas.robots.Link`, optional
            Link instance to create. Defaults to the robot model's root.
        context : str, optional
            Subdomain identifier to insert in the mesh names.

        Returns
        -------
        None

        """
        if link is None:
            link = self.model.root

        for item in itertools.chain(link.visual, link.collision):
            meshes = Geometry._get_item_meshes(item)

            if meshes:
                is_visual = hasattr(item, "get_color")
                color = item.get_color() if is_visual else None

                native_geometry = []
                for i, mesh in enumerate(meshes):
                    mesh_type = "visual" if is_visual else "collision"
                    if not context:
                        mesh_name_components = [
                            self.model.name,
                            mesh_type,
                            link.name,
                            str(i),
                        ]
                    else:
                        mesh_name_components = [
                            self.model.name,
                            mesh_type,
                            context,
                            link.name,
                            str(i),
                        ]
                    mesh_name = ".".join(mesh_name_components)
                    native_mesh = self.create_geometry(mesh, name=mesh_name, color=color)

                    self.transform(native_mesh, item.init_transformation)

                    native_geometry.append(native_mesh)

                item.native_geometry = native_geometry
                item.current_transformation = Transformation()

        for child_joint in link.joints:
            self.create(child_joint.child_link)

    def meshes(self, link=None, visual=True, collision=False, attached_meshes=True):
        """Returns all compas meshes of the model.

        Parameters
        ----------
        link : :class:`~compas.robots.Link`, optional
            Base link instance.
            Defaults to the robot model's root.
        visual : bool, optional
            Whether to include the robot's visual meshes.
        collision : bool, optional
            Whether to include the robot's collision meshes.
        attached_meshes : bool, optional
            Whether to include the robot's attached meshes.

        Returns
        -------
        list[:class:`~compas.datastructures.Mesh`]

        """
        if link is None:
            link = self.model.root

        meshes = []
        items = []
        if visual:
            items += link.visual
        if collision:
            items += link.collision
        if attached_meshes:
            items += list(self.attached_items.get(link.name, {}).values())
        for item in items:
            new_meshes = Geometry._get_item_meshes(item)
            for mesh in new_meshes:
                mesh.transform(item.current_transformation)
            meshes += new_meshes
        for child_joint in link.joints:
            meshes += self.meshes(child_joint.child_link, visual, collision, attached_meshes)
        return meshes

    def scale(self, factor):
        """Scales the robot model's geometry by factor (absolute).

        Parameters
        ----------
        factor : float
            The factor to scale the robot with.

        Returns
        -------
        None

        """
        self.model.scale(factor)

        relative_factor = factor / self.scale_factor
        transformation = Scale.from_factors([relative_factor] * 3)
        self.scale_link(self.model.root, transformation)
        self.scale_factor = factor

    def scale_link(self, link, transformation):
        """Recursive function to apply the scale transformation on each link.

        Parameters
        ----------
        link : :class:`~compas.robots.Link`
            A link.
        transformation : :class:`~compas.geometry.Transformation`
            A transformation to apply to th link's geometry.

        Returns
        -------
        None

        """
        self._scale_link_helper(link, transformation)

        for tool in self.attached_tool_models.values():
            self._scale_link_helper(tool.root, transformation)

    def _scale_link_helper(self, link, transformation):
        for item in itertools.chain(link.visual, link.collision):
            # Some links have only collision geometry, not visual. These meshes
            # have not been loaded.
            if item.native_geometry:
                for geometry in item.native_geometry:
                    self.transform(geometry, transformation)

        for child_joint in link.joints:
            self._scale_link_helper(child_joint.child_link, transformation)

    def _apply_transformation_on_transformed_link(self, item, transformation):
        """Applies a transformation on a link that is already transformed.

        Calculates the relative transformation and applies it to the link
        geometry. This is to prevent the recreation of large meshes.

        Parameters
        ----------
        item: :class:`~compas.robots.Visual` | :class:`~compas.robots.Collision`
            The visual or collidable object of a link.
        transformation: :class:`~compas.geometry.Transformation`
            The (absolute) transformation to apply onto the link's geometry.

        Returns
        -------
        None

        """
        if getattr(item, "current_transformation"):
            relative_transformation = transformation * item.current_transformation.inverse()
        else:
            relative_transformation = transformation
        for native_geometry in item.native_geometry or []:
            self.transform(native_geometry, relative_transformation)
        item.current_transformation = transformation

    def update(self, joint_state, visual=True, collision=True):
        """Triggers the update of the robot geometry.

        Parameters
        ----------
        joint_state : :class:`~compas.robots.Configuration` | dict[str, float]
            A dictionary with joint names as keys and joint positions as values.
        visual : bool, optional
            If True, the visual geometry will also be updated.
        collision : bool, optional
            If True, the collision geometry will also be updated.

        Returns
        -------
        None

        """
        _ = self._update(self.model, joint_state, visual, collision)
        for tool in self.attached_tool_models.values():
            frame = self.model.forward_kinematics(joint_state, link_name=tool.link_name)
            self.update_tool(
                tool=tool,
                visual=visual,
                collision=collision,
                transformation=Transformation.from_frame_to_frame(Frame.worldXY(), frame),
            )

    def _update(
        self,
        model,
        joint_state,
        visual=True,
        collision=True,
        parent_transformation=None,
    ):
        transformations = model.compute_transformations(joint_state, parent_transformation=parent_transformation)
        for j in model.iter_joints():
            self._transform_link_geometry(j.child_link, transformations[j.name], collision)
        return transformations

    def _transform_link_geometry(self, link, transformation, collision=True):
        for item in link.visual:
            self._apply_transformation_on_transformed_link(item, transformation)
        if collision:
            for item in link.collision:
                # some links have only collision geometry, not visual. These meshes have not been loaded.
                if item.native_geometry:
                    self._apply_transformation_on_transformed_link(item, transformation)
        for item in self.attached_items.get(link.name, {}).values():
            self._apply_transformation_on_transformed_link(item, transformation)

    def update_tool(self, tool, joint_state=None, visual=True, collision=True, transformation=None):
        """Triggers the update of the robot geometry of the tool.

        Parameters
        ----------
        joint_state : :class:`~compas.robots.Configuration` | dict[str, float], optional
            A dictionary with joint names as keys and joint positions as values.
            Defaults to an empty dictionary.
        transformation : :class:`~compas.geometry.Transformation`, optional
            The (absolute) transformation to apply to the entire tool's geometry.
            If None is given, no additional transformation will be applied.
            Defaults to None.
        visual : bool, optional
            If True, the visual geometry will also be updated.
        collision : bool, optional
            If True, the collision geometry will also be updated.

        Returns
        -------
        None

        """
        joint_state = joint_state or {}

        if transformation is None:
            transformation = tool.current_transformation
        self._transform_link_geometry(tool.root, transformation, collision)
        self._update(tool, joint_state, visual, collision, transformation)
        tool.current_transformation = transformation

    def draw_visual(self):
        """Draws all visual geometry of the robot model.

        Returns
        -------
        list[object]
            A list of context-specific mesh representations.

        """
        visual = []
        for native_geometry in self._iter_geometry(self.model, "visual"):
            visual.append(native_geometry)
        for tool in self.attached_tool_models.values():
            for native_geometry in self._iter_geometry(tool, "visual"):
                visual.append(native_geometry)
        return visual

    def draw_collision(self):
        """Draws all collision geometry of the robot model.

        Returns
        -------
        list[object]
            A list of context-specific mesh representations.

        """
        visual = []
        for native_geometry in self._iter_geometry(self.model, "collision"):
            visual.append(native_geometry)
        for tool in self.attached_tool_models.values():
            for native_geometry in self._iter_geometry(tool, "collision"):
                visual.append(native_geometry)

        return visual

    def draw_attached_meshes(self):
        """Draws all meshes attached to the robot model.

        Returns
        -------
        list[object]
            A list of context-specific mesh representations.

        """
        visual = []
        for items in self.attached_items.values():
            for item in items.values():
                for native_mesh in item.native_geometry:
                    visual.append(native_mesh)
        return visual

    @staticmethod
    def _iter_geometry(model, geometry_type):
        for link in model.iter_links():
            for item in getattr(link, geometry_type):
                if item.native_geometry:
                    for native_geometry in item.native_geometry:
                        yield native_geometry
