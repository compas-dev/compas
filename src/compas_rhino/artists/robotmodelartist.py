from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import Rhino.Geometry
import scriptcontext as sc
from System.Drawing import Color
from Rhino.DocObjects.ObjectColorSource import ColorFromObject
from Rhino.DocObjects.ObjectColorSource import ColorFromLayer
from Rhino.DocObjects.ObjectMaterialSource import MaterialFromObject

from compas.artists import RobotModelArtist

import compas_rhino
from compas_rhino.artists import RhinoArtist
from compas_rhino.geometry.transformations import xform_from_transformation


class RobotModelArtist(RhinoArtist, RobotModelArtist):
    """Artist for drawing robot models.

    Parameters
    ----------
    model : :class:`~compas.robots.RobotModel`
        Robot model.
    layer : str, optional
        The name of the layer that will contain the robot meshes.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info, see :class:`RhinoArtist` and :class:`RobotModelArtist`.

    """

    def __init__(self, model, layer=None, **kwargs):
        super(RobotModelArtist, self).__init__(model=model, layer=layer, **kwargs)

    def transform(self, native_mesh, transformation):
        T = xform_from_transformation(transformation)
        native_mesh.Transform(T)

    def create_geometry(self, geometry, name=None, color=None):
        """Create a Rhino mesh corresponding to the geometry of the model.

        Parameters
        ----------
        geometry : :class:`~compas.datastructures.Mesh`
            A COMPAS mesh data structure.
        name : str, optional
            Name of the mesh object.
        color : tuple[int, int, int], optional
            Color of the mesh object.

        Returns
        -------
        :rhino:`Rhino.Geometry.Mesh`

        """
        # Imported colors take priority over a the parameter color
        if "mesh_color.diffuse" in geometry.attributes:
            color = geometry.attributes["mesh_color.diffuse"]

        vertices, faces = geometry.to_vertices_and_faces(triangulated=False)

        mesh = Rhino.Geometry.Mesh()

        if name:
            mesh.UserDictionary.Set("MeshName", name)

        if color:
            r, g, b, a = color
            mesh.UserDictionary.Set("MeshColor.R", r)
            mesh.UserDictionary.Set("MeshColor.G", g)
            mesh.UserDictionary.Set("MeshColor.B", b)
            mesh.UserDictionary.Set("MeshColor.A", a)

        for v in vertices:
            mesh.Vertices.Add(*v)
        for face in faces:
            mesh.Faces.AddFace(*face)

        mesh.Normals.ComputeNormals()
        mesh.Compact()

        # Try to fix invalid meshes
        if not mesh.IsValid:
            mesh.FillHoles()

        return mesh

    def _enter_layer(self):
        self._previous_layer = None

        if self.layer:
            if not compas_rhino.rs.IsLayer(self.layer):
                compas_rhino.create_layers_from_path(self.layer)
            self._previous_layer = compas_rhino.rs.CurrentLayer(self.layer)

        compas_rhino.rs.EnableRedraw(False)

    def _exit_layer(self):
        if self.layer and self._previous_layer:
            compas_rhino.rs.CurrentLayer(self._previous_layer)

        self.redraw()

    def draw_collision(self):
        """Draw all the collision geometries of the robot model.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        collisions = super(RobotModelArtist, self).draw_collision()
        self._enter_layer()

        new_guids = []
        for mesh in collisions:
            guids = self._add_mesh_to_doc(mesh)
            new_guids.extend(guids)

        self._exit_layer()
        return new_guids

    def draw_visual(self):
        """Draw all the visual geometries of the robot model.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        visuals = super(RobotModelArtist, self).draw_visual()
        self._enter_layer()

        new_guids = []
        for mesh in visuals:
            guids = self._add_mesh_to_doc(mesh)
            new_guids.extend(guids)

        self._exit_layer()
        return new_guids

    def draw_attached_meshes(self):
        """Draw all the geometries attached to the robot model.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        acms = super(RobotModelArtist, self).draw_attached_meshes()
        self._enter_layer()

        new_guids = []
        for mesh in acms:
            guids = self._add_mesh_to_doc(mesh)
            new_guids.extend(guids)

        self._exit_layer()
        return new_guids

    def draw(self):
        """Draw the geometry of the model.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        return self.draw_visual()

    def redraw(self, timeout=None):
        """Redraw the Rhino view.

        Parameters
        ----------
        timeout : float, optional
            The amount of time the artist waits before updating the Rhino view.
            The time should be specified in seconds.

        Returns
        -------
        None

        """
        if timeout:
            time.sleep(timeout)

        compas_rhino.rs.EnableRedraw(True)
        compas_rhino.rs.Redraw()

    def clear_layer(self):
        """Clear the main layer of the artist.

        Returns
        -------
        None

        """
        if self.layer:
            compas_rhino.clear_layer(self.layer)
        else:
            compas_rhino.clear_current_layer()

    def _add_mesh_to_doc(self, mesh):
        guid = sc.doc.Objects.AddMesh(mesh)

        color = None
        if "MeshColor.R" in mesh.UserDictionary:
            color = [
                mesh.UserDictionary["MeshColor.R"],
                mesh.UserDictionary["MeshColor.G"],
                mesh.UserDictionary["MeshColor.B"],
                mesh.UserDictionary["MeshColor.A"],
            ]
        name = mesh.UserDictionary["MeshName"] if "MeshName" in mesh.UserDictionary else None

        obj = sc.doc.Objects.Find(guid)

        if obj:
            attr = obj.Attributes
            if color:
                r, g, b, a = [i * 255 for i in color]
                attr.ObjectColor = Color.FromArgb(a, r, g, b)
                attr.ColorSource = ColorFromObject

                material_name = "robotmodelartist.{:.2f}_{:.2f}_{:.2f}_{:.2f}".format(r, g, b, a)
                material_index = sc.doc.Materials.Find(material_name, True)

                # Material does not exist, create it
                if material_index == -1:
                    material_index = sc.doc.Materials.Add()
                    material = sc.doc.Materials[material_index]
                    material.Name = material_name
                    material.DiffuseColor = attr.ObjectColor
                    material.CommitChanges()

                attr.MaterialIndex = material_index
                attr.MaterialSource = MaterialFromObject
            else:
                attr.ColorSource = ColorFromLayer

            if name:
                attr.Name = name

            obj.CommitChanges()
        return [guid]
