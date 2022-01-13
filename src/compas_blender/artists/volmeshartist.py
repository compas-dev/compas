from typing import Optional
from typing import Union
from typing import Any

import bpy

from compas.artists import MeshArtist
from .artist import BlenderArtist


class VolMeshArtist(BlenderArtist, MeshArtist):
    """An artist for drawing volumetric mesh data structures in Blender.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        The volmesh data structure.
    collection : str or :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`compas_blender.artists.BlenderArtist` and :class:`compas.artists.MeshArtist`.

    """

    def __init__(self, volmesh,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):

        super().__init__(volmesh=volmesh, collection=collection or volmesh.name, **kwargs)
