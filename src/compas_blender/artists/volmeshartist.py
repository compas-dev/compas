from compas_blender.artists.meshartist import MeshArtist


__all__ = [
    'VolMeshArtist',
]


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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
