from compas.utilities import geometric_key

import compas_rhino

try:
    import Rhino
    import scriptcontext as sc
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'volmesh_from_polysurfaces',
    'volmesh_from_wireframe',
    'draw_volmesh',

]


# ==============================================================================
# constructors
# ==============================================================================


def volmesh_from_polysurfaces(cls, guids):
    """Construct a volumetric mesh from given polysurfaces.

    Essentially, this function does the following:

    * find each of the polysurfaces and check if they have a boundary representation (b-rep)
    * convert to b-rep and extract the edge loops
    * make a face of each loop by referring to vertices using their geometric keys
    * add a cell per brep
    * and add the faces of a brep to the cell
    * create a volmesh from the found vertices and cells

    Parameters:
        cls (compas.datastructures.volmesh.VolMesh):
            The class of volmesh.
        guids (sequence of str or System.Guid):
            The *globally unique identifiers* of the polysurfaces.

    Returns:
        compas.datastructures.volmesh.Volmesh: The volumetric mesh object.

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
            sp_gkey = geometric_key(sp)
            ep_gkey = geometric_key(ep)
            gkey_xyz[sp_gkey] = sp
            gkey_xyz[ep_gkey] = ep
            face.append(sp_gkey)
            face.append(ep_gkey)
            for segment in segments[1:-1]:
                ep = segment.PointAtEnd
                ep_gkey = geometric_key(ep)
                face.append(ep_gkey)
                gkey_xyz[ep_gkey] = ep
            cell.append(face)
        cells.append(cell)

    gkey_index = dict((gkey, index) for index, gkey in enumerate(gkey_xyz))
    vertices   = [list(xyz) for gkey, xyz in gkey_xyz.items()]
    cells      = [[[gkey_index[gkey] for gkey in face] for face in cell] for cell in cells]

    return cls.from_vertices_and_cells(vertices, cells)


def volmesh_from_wireframe(cls, edges):
    raise NotImplementedError


# ==============================================================================
# drawing
# ==============================================================================


def draw_volmesh(volmesh,
                 name=None,
                 layer=None,
                 clear=True,
                 redraw=True,
                 show_faces=True,
                 show_vertices=True,
                 show_edges=True,
                 vertex_color=None,
                 edge_color=None,
                 face_color=None):
    """"""
    # set default options
    if not isinstance(vertex_color, dict):
        vertex_color = {}
    if not isinstance(edge_color, dict):
        edge_color = {}
    if not isinstance(face_color, dict):
        face_color = {}
    if name:
        volmesh.attributes['name'] = name
    name = volmesh.setdefault('name', name)
    if layer:
        volmesh.attributes['layer'] = layer
    layer = volmesh.setdefault('layer', layer)
    # delete all relevant objects by name
    objects  = compas_rhino.get_objects(name='{0}.mesh'.format(name))
    objects += compas_rhino.get_objects(name='{0}.vertex.*'.format(name))
    objects += compas_rhino.get_objects(name='{0}.edge.*'.format(name))
    compas_rhino.delete_objects(objects)
    # clear the layer if requested
    if clear:
        compas_rhino.clear_layers([layer])
    # draw the requested components
    if show_faces:
        faces = []
        color = volmesh.attributes['color.face']
        for vertices in volmesh.faces():
            points = [volmesh.vertex_coordinates(vkey) for vkey in vertices + [vertices[0]]]
            faces.append({
                'points' : points,
                'name'   : '',
                'color'  : color,
            })
        compas_rhino.xdraw_faces(faces, layer=layer, clear=False, redraw=False)
    if show_edges:
        lines = []
        color = volmesh.attributes['color.edge']
        for u, v in volmesh.edges_iter():
            lines.append({
                'start': volmesh.vertex_coordinates(u),
                'end'  : volmesh.vertex_coordinates(v),
                'name' : '{0}.edge.{1}-{2}'.format(name, u, v),
                'color': edge_color.get((u, v), color),
            })
        compas_rhino.xdraw_lines(lines, layer=layer, clear=False, redraw=False)
    if show_vertices:
        points = []
        color  = volmesh.attributes['color.vertex']
        for key in volmesh.vertices_iter():
            points.append({
                'pos'  : volmesh.vertex_coordinates(key),
                'name' : '{0}.vertex.{1}'.format(name, key),
                'color': vertex_color.get(key, color),
            })
        compas_rhino.xdraw_points(points, layer=layer, clear=False, redraw=False)
    # redraw if requested
    if redraw:
        rs.Redraw()


# ==============================================================================
# labels
# ==============================================================================


# def display_volmesh_vertex_labels(volmesh, attr_name=None, layer=None, color=None, formatter=None):
    



# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
