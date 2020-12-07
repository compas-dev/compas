from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import geometric_key

import Rhino
import scriptcontext as sc


__all__ = ['volmesh_from_polysurfaces']


def volmesh_from_polysurfaces(cls, guids, precision=None):
    """Construct a volumetric mesh from given polysurfaces.

    Essentially, this function does the following:

    * find each of the polysurfaces and check if they have a boundary representation (b-rep)
    * convert to b-rep and extract the edge loops
    * make a face of each loop by referring to vertices using their geometric keys
    * add a cell per brep
    * and add the faces of a brep to the cell
    * create a volmesh from the found vertices and cells

    Parameters
    ----------
    cls : :class:`compas.datastructures.VolMesh`
        The class of volmesh.
    guids : sequence of str or System.Guid
        The *globally unique identifiers* of the polysurfaces.
    precision: string
        Precision of the polysurface connectivity.

    Returns
    -------
    :class:`compas.datastructures.Volmesh`
        The volumetric mesh object.

    """
    gkey_xyz = {}
    cells = []
    for guid in guids:
        cell = []
        obj = sc.doc.Objects.Find(guid)
        if not obj.Geometry.HasBrepForm:
            continue
        brep = Rhino.Geometry.Brep.TryConvertBrep(obj.Geometry)
        for loop in brep.Loops:
            curve = loop.To3dCurve()
            segments = curve.Explode()
            face = []
            sp = segments[0].PointAtStart
            ep = segments[0].PointAtEnd
            sp_gkey = geometric_key(sp, precision)
            ep_gkey = geometric_key(ep, precision)
            gkey_xyz[sp_gkey] = sp
            gkey_xyz[ep_gkey] = ep
            face.append(sp_gkey)
            face.append(ep_gkey)
            for segment in segments[1:-1]:
                ep = segment.PointAtEnd
                ep_gkey = geometric_key(ep, precision)
                face.append(ep_gkey)
                gkey_xyz[ep_gkey] = ep
            cell.append(face)
        cells.append(cell)
    gkey_index = dict((gkey, index) for index, gkey in enumerate(gkey_xyz))
    vertices = [list(xyz) for gkey, xyz in gkey_xyz.items()]
    cells = [[[gkey_index[gkey] for gkey in face] for face in cell] for cell in cells]
    return cls.from_vertices_and_cells(vertices, cells)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
