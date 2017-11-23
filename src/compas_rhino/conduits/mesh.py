from compas_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Line

    from System.Collections.Generic import List
    from System.Drawing.Color import FromArgb

except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['MeshConduit', ]


class MeshConduit(Conduit):
    """A Rhino display conduit for meshes.

    Parameters:
        mesh (compas.datastructures.mesh.Mesh): The mesh object.
        color (tuple): Optional.
            The conduit color.
            Default is ``(255, 0, 0)``.

    Example:

        .. code-block:: python

            import compas
            import compas_rhino as compas_rhino

            from compas.datastructures.mesh import Mesh
            from compas.topology import smooth_mesh_centroid

            mesh = Mesh.from_obj(compas.get_data('faces.obj'))

            conduit = MeshConduit(mesh)
            conduit.enable()

            def update_conduit(mesh, k):
                if k % 10 == 0:
                    conduit.redraw()

            try:
                smooth_mesh_centroid(mesh, callback=update_conduit)
            except:
                raise

            finally:
                conduit.disable()
                del conduit

    """
    def __init__(self, mesh, color=None, **kwargs):
        super(MeshConduit, self).__init__(**kwargs)
        self.mesh = mesh
        color = color or (255, 255, 255)
        self.color = FromArgb(*color)

    def DrawForeground(self, e):
        edges = list(self.mesh.wireframe())
        lines = List[Line](len(edges))
        for u, v in edges:
            sp = self.mesh.vertex_coordinates(u)
            ep = self.mesh.vertex_coordinates(v)
            lines.Add(Line(Point3d(*sp), Point3d(*ep)))
        e.Display.DrawLines(lines, self.color)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
