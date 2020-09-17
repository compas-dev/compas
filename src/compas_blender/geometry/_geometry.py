import bpy


__all__ = ['BaseBlenderGeometry']


class BaseBlenderGeometry:

    def __init__(self, obj):
        self.object = obj
        self.name = obj.name
        self.geometry = obj.data
        self.type = obj.type
        self.attributes = {}

    @property
    def location(self):
        return list(self.object.location)

    @classmethod
    def from_selection(cls):
        raise NotImplementedError

    @classmethod
    def from_name(cls, name):
        return cls(bpy.data.objects[name])

    def delete(self):
        raise NotImplementedError

    def purge(self):
        raise NotImplementedError

    def hide(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def select(self):
        raise NotImplementedError

    def unselect(self):
        raise NotImplementedError

    def closest_point(self, *args, **kwargs):
        raise NotImplementedError

    def closest_points(self, *args, **kwargs):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
