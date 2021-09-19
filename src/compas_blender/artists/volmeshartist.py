from .meshartist import MeshArtist


class VolMeshArtist(MeshArtist):

    def __init__(self, volmesh):
        super().__init__()
        self.volmesh = volmesh

    @property
    def volmesh(self):
        return self.datastructure

    @volmesh.setter
    def volmesh(self, volmesh):
        self.datastructure = volmesh
