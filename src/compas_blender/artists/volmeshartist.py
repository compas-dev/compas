from typing import Optional
from typing import Union
from typing import Any

import bpy
from compas.artists import MeshArtist
from .artist import BlenderArtist


class VolMeshArtist(BlenderArtist, MeshArtist):

    def __init__(self, volmesh,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):
        super().__init__(volmesh=volmesh, collection=collection or volmesh.name, **kwargs)
