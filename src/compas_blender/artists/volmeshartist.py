from compas_blender.artists.meshartist import MeshArtist


__all__ = [
    'VolMeshArtist',
]


class VolMeshArtist(MeshArtist):

    def __init__(self, volmesh, layer=None):
        super().__init__(layer=layer)
        self.volmesh = volmesh
        self.defaults.update({
            'color.vertex': [255, 255, 255],
            'color.edge':   [0, 0, 0],
            'color.face':   [110, 110, 110],
        })

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
