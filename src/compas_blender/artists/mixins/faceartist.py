try:
    import bpy
except ImportError:
    pass

from compas_blender.utilities import set_objects_show_names
from compas_blender.utilities import create_collection
from compas_blender.utilities import draw_faces


__all__ = ['FaceArtist']


class FaceArtist(object):

    def clear_faces(self, keys=None):
        collection_name = "{}.faces".format(self.datastructure.name)
        collection = bpy.data.collections.get(collection_name)
        if not collection:
            return
        objects = collection.objects
        meshes = [obj.data for obj in objects]
        bpy.ops.object.select_all(action="DESELECT")
        for obj in objects:
            obj.select_set(True)
        bpy.ops.object.delete()
        for mesh in meshes:
            bpy.data.meshes.remove(mesh)

    def clear_facelabels(self):
        set_objects_show_names(objects=self.face_objects, show=False)

    def draw_faces(self, keys=None, colors=None):
        self.clear_faces()
        self.clear_facelabels()
        keys = keys or list(self.datastructure.faces())
        faces = [0] * len(keys)
        if colors is None:
            colors = {key: self.defaults['color.face'] for key in keys}
        for index, key in enumerate(keys):
            faces[index] = {
                "points": self.datastructure.face_coordinates(key),
                "name": "{}.face.{}".format(self.datastructure.name, key),
                "color": colors[key],
                "layer": self.layer}
        objects = draw_faces(faces)
        layer_collection = create_collection(self.layer)
        face_collection_name = "{}.faces".format(self.datastructure.name)
        face_collection = create_collection(face_collection_name, parent=layer_collection)
        for obj in objects:
            for collection in obj.users_collection:
                collection.objects.unlink(obj)
            face_collection.objects.link(obj)
        self.face_objects = objects
        self.face_collection = face_collection

    def draw_facelabels(self, text=None, color=None):
        set_objects_show_names(objects=self.face_objects, show=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
