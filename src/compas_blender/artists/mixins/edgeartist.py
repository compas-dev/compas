try:
    import bpy
except ImportError:
    pass

from compas_blender.utilities import set_objects_show_names
from compas_blender.utilities import create_collection
from compas_blender.utilities import draw_lines


__all__ = [
    'EdgeArtist',
]


class EdgeArtist(object):

    def clear_edges(self, keys=None):
        collection_name = "{}.edges".format(self.datastructure.name)
        collection = bpy.data.collections.get(collection_name)
        if not collection:
            return
        objects = collection.objects
        curves = [obj.data for obj in objects]
        bpy.ops.object.select_all(action="DESELECT")
        for obj in objects:
            obj.select_set(True)
        bpy.ops.object.delete()
        for curve in curves:
            bpy.data.curves.remove(curve)

    def clear_edgelabels(self):
        set_objects_show_names(objects=self.edge_objects, show=False)

    def draw_edges(self, width=0.05, keys=None, colors=None):
        self.clear_edges()
        self.clear_edgelabels()
        keys = keys or list(self.datastructure.edges())
        lines = [0] * len(keys)
        if colors is None:
            colors = {key: self.defaults['color.line'] for key in keys}
        for index, (u, v) in enumerate(keys):
            lines[index] = {
                'start': self.datastructure.vertex_coordinates(u),
                'end': self.datastructure.vertex_coordinates(v),
                'layer': self.layer,
                'color': colors[(u, v)],
                'width': width,
                'name': '{}.edge.{}-{}'.format(self.datastructure, u, v)}
        objects = draw_lines(lines)
        layer_collection = create_collection(self.layer)
        edge_collection_name = "{}.edges".format(self.datastructure.name)
        edge_collection = create_collection(edge_collection_name, parent=layer_collection)
        for obj in objects:
            for collection in obj.users_collection:
                collection.objects.unlink(obj)
            edge_collection.objects.link(obj)
        self.edge_objects = objects
        self.edge_collection = edge_collection

    def draw_edgelabels(self):
        set_objects_show_names(objects=self.edge_objects, show=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
