from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import itertools

from compas.datastructures import Mesh
from compas.geometry import Frame
from compas.geometry import Scale
from compas.geometry import Shape
from compas.geometry import Transformation

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


__all__ = [
    'BaseRobotModelArtist'
]


class AbstractRobotModelArtist(ABC):
    @abc.abstractmethod
    def transform(self, geometry, transformation):
        """Transforms a CAD-specific geometry using a **COMPAS** transformation.

        Parameters
        ----------
        geometry : object
            A CAD-specific (i.e. native) geometry object as returned by :meth:`draw_geometry`.
        transformation : `Transformation`
            **COMPAS** transformation to update the geometry object.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def draw_geometry(self, geometry, name=None, color=None):
        """Draw a **COMPAS** geometry in the respective CAD environment.

        Note
        ----
        This is an abstract method that needs to be implemented by derived classes.

        Parameters
        ----------
        geometry : :class:`Mesh`
            Instance of a **COMPAS** mesh
        name : str, optional
            The name of the mesh to draw.

        Returns
        -------
        object
            CAD-specific geometry
        """
        raise NotImplementedError


class BaseRobotModelArtist(AbstractRobotModelArtist):
    """Provides common functionality to most robot model artist implementations.

    In **COMPAS**, the `artists` are classes that assist with the visualization of
    datastructures and models, in a way that maintains the data separated from the
    specific CAD interfaces, while providing a way to leverage native performance
    of the CAD environment.

    There are two methods that implementers of this base class should provide, one
    is concerned with the actual creation of geometry in the native format of the
    CAD environment (:meth:`draw_geometry`) and the other is one to apply a transformation
    to geometry (:meth:`transform`).

    Attributes
    ----------
    model : :class:`compas.robots.RobotModel`
        Instance of a robot model.
    """

    def __init__(self, model):
        super(BaseRobotModelArtist, self).__init__()
        self.model = model
        self.create()
        self.scale_factor = 1.
        self.attached_tool = None

    def attach_tool(self, tool):
        """Attach a tool to the robot artist.

        Parameters
        ----------
        tool : :class:`compas_fab.robots.Tool`
            The tool that should be attached to the robot's flange.
        """
        name = '{}.visual.attached_tool'.format(self.model.name)
        native_geometry = self.draw_geometry(tool.visual, name=name)  # TODO: only visual, collision would be great

        link = self.model.get_link_by_name(tool.attached_collision_mesh.link_name)
        ee_frame = link.parent_joint.origin.copy()
        parent_joint_name = link.parent_joint.name

        T = Transformation.from_frame_to_frame(Frame.worldXY(), ee_frame)
        self.transform(native_geometry, T)
        tool.native_geometry = [native_geometry]
        tool.current_transformation = Transformation()
        tool.parent_joint_name = parent_joint_name
        self.attached_tool = tool

    def detach_tool(self):
        """Detach the tool.
        """
        self.attached_tool = None

    def create(self, link=None):
        """Recursive function that triggers the drawing of the robot model's geometry.

        This method delegates the geometry drawing to the :meth:`draw_geometry`
        method. It transforms the geometry based on the saved initial
        transformation from the robot model.

        Parameters
        ----------
        link : :class:`compas.robots.Link`, optional
            Link instance to create. Defaults to the robot model's root.

        Returns
        -------
        None
        """
        if link is None:
            link = self.model.root

        for item in itertools.chain(link.visual, link.collision):
            # NOTE: Currently, shapes assign their meshes to an
            # attribute called `geometry`, but this will change soon to `meshes`.
            # This code handles the situation in a forward-compatible
            # manner. Eventually, this can be simplified to use only `meshes` attr
            if hasattr(item.geometry.shape, 'meshes'):
                meshes = item.geometry.shape.meshes
            else:
                meshes = item.geometry.shape.geometry

            if isinstance(meshes, Shape):
                meshes = [Mesh.from_shape(meshes)]

            if meshes:
                # Coerce meshes into an iterable (a tuple if not natively iterable)
                if not hasattr(meshes, '__iter__'):
                    meshes = (meshes,)

                is_visual = hasattr(item, 'get_color')
                color = item.get_color() if is_visual else None

                native_geometry = []
                for i, mesh in enumerate(meshes):
                    # create native geometry
                    mesh_type = 'visual' if is_visual else 'collision'
                    mesh_name = '{}.{}.{}.{}'.format(self.model.name, mesh_type, link.name, i)
                    native_mesh = self.draw_geometry(mesh, name=mesh_name, color=color)
                    # transform native geometry based on saved init transform
                    self.transform(native_mesh, item.init_transformation)
                    # append to list
                    native_geometry.append(native_mesh)

                item.native_geometry = native_geometry
                item.current_transformation = Transformation()

        for child_joint in link.joints:
            self.create(child_joint.child_link)

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
        self.model.scale(factor)  # scale the model

        relative_factor = factor / self.scale_factor  # relative scaling factor
        transformation = Scale.from_factors([relative_factor] * 3)
        self.scale_link(self.model.root, transformation)
        self.scale_factor = factor

    def scale_link(self, link, transformation):
        """Recursive function to apply the scale transformation on each link.
        """
        for item in itertools.chain(link.visual, link.collision):
            # Some links have only collision geometry, not visual. These meshes
            # have not been loaded.
            if item.native_geometry:
                for geometry in item.native_geometry:
                    self.transform(geometry, transformation)

        for child_joint in link.joints:
            # Recursive call
            self.scale_link(child_joint.child_link, transformation)

    def _apply_transformation_on_transformed_link(self, item, transformation):
        """Applies a transformation on a link that is already transformed.

        Calculates the relative transformation and applies it to the link
        geometry. This is to prevent the recreation of large meshes.

        Parameters
        ----------
        item: :class:`compas.robots.Visual` or :class:`compas.robots.Collision`
            The visual or collidable object of a link.
        transformation: :class:`Transformation`
            The (absolute) transformation to apply onto the link's geometry.

        Returns
        -------
        None
        """
        relative_transformation = transformation * item.current_transformation.inverse()
        for native_geometry in item.native_geometry:
            self.transform(native_geometry, relative_transformation)
        item.current_transformation = transformation

    def update(self, configuration, visual=True, collision=True):
        """Triggers the update of the robot geometry.

        Parameters
        ----------
        configuration : :obj:`tuple` of :obj:`list`
            A tuple of 2 elements containing a list of joint positions and a list of matching joint names.
            If ``None`` is passed as the second element, the default will be the output of
            :meth:`compas.robots.RobotModel.get_configurable_joint_names`.
        visual : bool, optional
            ``True`` if the visual geometry should be also updated, otherwise ``False``.
            Defaults to ``True``.
        collision : bool, optional
            ``True`` if the collision geometry should be also updated, otherwise ``False``.
            Defaults to ``True``.
        """
        positions = configuration[0]
        names = configuration[1] or self.model.get_configurable_joint_names()
        if len(names) != len(configuration.values):
            raise ValueError("Please pass a configuration with %d joint_names." % len(positions))
        joint_state = dict(zip(names, positions))
        transformations = self.model.compute_transformations(joint_state)
        for j in self.model.iter_joints():
            link = j.child_link
            for item in link.visual:
                self._apply_transformation_on_transformed_link(item, transformations[j.name])
            if collision:
                for item in link.collision:
                    # some links have only collision geometry, not visual. These meshes have not been loaded.
                    if item.native_geometry:
                        self._apply_transformation_on_transformed_link(item, transformations[j.name])

        if self.attached_tool:
            self._apply_transformation_on_transformed_link(self.attached_tool, transformations[self.attached_tool.parent_joint_name])

    def draw_visual(self):
        """Draws all visual geometry of the robot model."""
        for link in self.model.iter_links():
            for item in link.visual:
                if item.native_geometry:
                    for native_geometry in item.native_geometry:
                        yield native_geometry
        if self.attached_tool:
            for native_geometry in self.attached_tool.native_geometry:
                yield native_geometry

    def draw_collision(self):
        """Draws all collision geometry of the robot model."""
        for link in self.model.iter_links():
            for item in link.collision:
                if item.native_geometry:
                    for native_geometry in item.native_geometry:
                        yield native_geometry
        if self.attached_tool:
            for native_geometry in self.attached_tool.native_geometry:
                yield native_geometry
