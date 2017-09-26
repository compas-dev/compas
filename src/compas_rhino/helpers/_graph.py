import compas_rhino

from compas.utilities.colors import color_to_colordict


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


# todo: align default attributes and use by/in helpers (or make this explicit)


# ==============================================================================
# label
# ==============================================================================


def display_graph_vertex_labels(graph,
                                attr_name=None,
                                layer=None,
                                clear_layer=False,
                                color=None,
                                formatter=None):
    """"""
    if not attr_name:
        attr_name = 'key'

    colordict = color_to_colordict(color,
                                   graph.vertices(),
                                   default=graph.attributes['color.vertex'],
                                   colorformat='rgb',
                                   normalize=False)

    if formatter:
        if not callable(formatter):
            raise Exception('The provided formatter is not callable.')
    else:
        formatter = str

    labels = []

    for index, key, attr in graph.vertices_enum(True):
        if 'key' == attr_name:
            value = key
        elif 'index' == attr_name:
            value = index
        else:
            value = attr[attr_name]

        name = '{0}.vertex.label.{1}'.format(graph.attriutes['name'], repr(key))

        labels.append({'pos'  : graph.vertex_coordinates(key),
                       'text' : formatter(value),
                       'name' : name,
                       'color': colordict[key], })

    compas_rhino.xdraw_labels(
        labels,
        layer=layer,
        clear=clear_layer,
        redraw=True
    )


def display_graph_edge_labels(graph,
                              attr_name=None,
                              layer=None,
                              clear_layer=False,
                              color=None,
                              formatter=None):
    """"""
    if not attr_name:
        attr_name = 'key'

    colordict = color_to_colordict(color,
                                   graph.edges(),
                                   default=graph.attributes['color.edge'],
                                   colorformat='rgb',
                                   normalize=False)

    if formatter:
        if not callable(formatter):
            raise Exception('The provided formatter is not callable.')
    else:
        formatter = str

    labels = []

    for index, u, v, attr in graph.edges_enum(True):

        if attr_name == 'key':
            value = '{0}-{1}'.format(u, v)
        elif attr_name == 'index':
            value = index
        else:
            value = attr[attr_name]

        labels.append({'pos'  : graph.edge_midpoint(u, v),
                       'text' : formatter(value),
                       'name' : '{0}.edge.label.{1}-{2}'.format(graph.attributes['name'], u, v),
                       'color': colordict[(u, v)], })

    compas_rhino.xdraw_labels(
        labels,
        layer=layer,
        clear=clear_layer,
        redraw=True
    )


def display_graph_face_labels(graph,
                              attr_name=None,
                              layer=None,
                              clear_layer=False,
                              color=None,
                              formatter=None):
    """"""
    if not attr_name:
        attr_name = 'key'

    colordict = color_to_colordict(color,
                                   graph.faces(),
                                   default=graph.attributes['color.face'],
                                   colorformat='rgb',
                                   normalize=False)

    if formatter:
        if not callable(formatter):
            raise Exception('The provided formatter is not callable.')
    else:
        formatter = str

    labels = []

    for index, fkey in graph.faces_enum():
        if attr_name == 'key':
            value = fkey
        elif attr_name == 'index':
            value = index
        else:
            value = graph.facedata[fkey][attr_name]

        labels.append({
            'pos'  : graph.face_centroid(fkey),
            'text' : formatter(value),
            'name' : '{0}.face.label.{1}'.format(graph.attributes['name'], fkey),
            'color': colordict[fkey]
        })

    compas_rhino.xdraw_labels(
        labels,
        layer=layer,
        clear=clear_layer,
        redraw=True
    )


# ==============================================================================
# select
# ==============================================================================


# ==============================================================================
# attributes
# ==============================================================================


# ==============================================================================
# geometry
# ==============================================================================


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
