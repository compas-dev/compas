try:
    import bpy
except ImportError:
    pass

from compas_blender.utilities import set_objects_show_names
from compas_blender.utilities import create_collection
from compas_blender.utilities import draw_spheres


__all__ = [
    'VertexArtist',
]


class VertexArtist(object):

    def clear_vertices(self, keys=None):
        collection_name = "{}.vertices".format(self.datastructure.name)
        collection = bpy.data.collections.get(collection_name)
        if not collection:
            return
        objects = collection.objects
        mesh = objects[0].data
        bpy.ops.object.select_all(action="DESELECT")
        for obj in objects:
            obj.select_set(True)
        bpy.ops.object.delete()
        bpy.data.meshes.remove(mesh)

    def clear_vertexlabels(self):
        set_objects_show_names(objects=self.vertex_objects, show=False)

    def draw_vertices(self, keys=None, radius=0.05):
        self.clear_vertices()
        self.clear_vertexlabels()
        keys = keys or list(self.datastructure.vertices())
        points = [0] * len(keys)
        for index, key in enumerate(keys):
            points[index] = {
                'pos': self.datastructure.vertex_coordinates(key),
                'radius': radius,
                'name': '{}.vertex.{}'.format(self.datastructure.name, key)}
        objects = draw_spheres(points)
        layer_collection = create_collection(self.layer)
        vertex_collection_name = "{}.vertices".format(self.datastructure.name)
        vertex_collection = create_collection(vertex_collection_name, parent=layer_collection)
        for obj in objects:
            for collection in obj.users_collection:
                collection.objects.unlink(obj)
            vertex_collection.objects.link(obj)
        self.vertex_objects = objects
        self.vertex_collection = vertex_collection

    def draw_vertexlabels(self):
        set_objects_show_names(objects=self.vertex_objects, show=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
