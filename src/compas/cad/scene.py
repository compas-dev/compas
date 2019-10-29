from compas.cad import Object3D


__all__ = ["Scene"]


class Scene(Object3D):

    """
    Scence class serves as a container to store object3ds for visualization
    """

    __module__ = "compas.cad"

    def __init__(self):
        super(Scene, self).__init__()

    @property
    def parent(self):
        return None


if __name__ == "__main__":

    from compas.geometry import Point
    from compas.cad import Object3D

    scene = Scene()
    scene.add(Object3D(geometry=Point(0, 0, 0)))
    print(scene.get_children())
