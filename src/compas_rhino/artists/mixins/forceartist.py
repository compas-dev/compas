from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt

import compas_rhino

try:
    import rhinoscriptsyntax as rs
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__all__ = ['ForceArtist']


class ForceArtist(object):

    def clear_loads(self):
        compas_rhino.delete_objects_by_name(name='{}.load.*'.format(self.datastructure.name))

    def clear_reactions(self):
        compas_rhino.delete_objects_by_name(name='{}.reaction.*'.format(self.datastructure.name))

    def clear_residuals(self):
        compas_rhino.delete_objects_by_name(name='{}.residual.*'.format(self.datastructure.name))

    def draw_loads(self, color=None, scale=1.0, tol=1e-6):
        if not scale:
            self.clear_loads()
            return
        color = color or (255, 255, 0)
        lines = []
        for key, attr in self.datastructure.vertices(True):
            p = sqrt(attr['px'] ** 2 + attr['py'] ** 2 + attr['pz'] ** 2)
            if p < tol:
                continue
            sp = self.datastructure.vertex_coordinates(key)
            ep = sp[0] + scale * attr['px'], sp[1] + scale * attr['py'], sp[2] + scale * attr['pz']
            lines.append({
                'start': sp,
                'end'  : ep,
                'name' : '{}.load.{}:{:.3f}'.format(self.datastructure.name, key, p),
                'color': color,
                'arrow': 'end'
            })
        self.clear_loads()
        compas_rhino.xdraw_lines(lines, layer=self.layer)

    def draw_reactions(self, color=None, scale=1.0, tol=1e-6, identifier='is_support'):
        if not scale:
            self.clear_reactions()
            return
        color = color or (0, 255, 0)
        lines = []
        for key, attr in self.datastructure.vertices(True):
            if not attr[identifier]:
                continue
            r = sqrt(attr['rx'] ** 2 + attr['ry'] ** 2 + attr['rz'] ** 2)
            if r < tol:
                continue
            sp = self.datastructure.vertex_coordinates(key)
            ep = sp[0] - scale * attr['rx'], sp[1] - scale * attr['ry'], sp[2] - scale * attr['rz']
            lines.append({
                'start': sp,
                'end'  : ep,
                'name' : '{}.reaction.{}:{:.3f}'.format(self.datastructure.name, key, r),
                'color': color,
                'arrow': 'end'
            })
        self.clear_reactions()
        compas_rhino.xdraw_lines(lines, layer=self.layer)

    def draw_residuals(self, color=None, scale=1.0, tol=1e-6, identifier='is_support'):
        if not scale:
            self.clear_residuals()
            return
        color = color or (0, 255, 255)
        lines = []
        for key, attr in self.datastructure.vertices(True):
            if attr[identifier]:
                continue
            r = sqrt(attr['rx'] ** 2 + attr['ry'] ** 2 + attr['rz'] ** 2)
            if r < tol:
                continue
            sp = self.datastructure.vertex_coordinates(key)
            ep = sp[0] + scale * attr['rx'], sp[1] + scale * attr['ry'], sp[2] + scale * attr['rz']
            lines.append({
                'start': sp,
                'end'  : ep,
                'name' : '{}.residual.{}:{:.3f}'.format(self.datastructure.name, key, r),
                'color': color,
                'arrow': 'end'
            })
        self.clear_residuals()
        compas_rhino.xdraw_lines(lines, layer=self.layer)

    def draw_forces(self):
        pass

    def draw_stresses(self):
        pass

    def draw_bending(self):
        pass

    def draw_torsion(self):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass


# ==============================================================================
# forces
# ==============================================================================


# def network_display_axial_forces(network,
#                                  display=True,
#                                  layer=None,
#                                  clear_layer=False,
#                                  scale=1.0,
#                                  attr_name='f',
#                                  color_tension=(255, 0, 0),
#                                  color_compression=(0, 0, 255)):
#     """Display the axial forces in the edges of a network.

#     Parameters:
#         network (compas.datastructures.network.Network):
#             The network object.
#         display (bool): Optional.
#             If ``True``, display the axial forces.
#             If ``False``, don't display the axial forces.
#             Default is ``True``.
#         layer (str): Optional.
#             The layer to draw in. Default is ``None``.
#         clear_layer (bool): Optional.
#             Flag for clearing the layer.
#             Default is ``False``.
#         scale (float): Optional.
#             The scale of the forces.
#             Default is ``1.0``.
#         attr_name (str): Optional.
#             The name of the edge attribute storing the force value.
#             Default is ``'f'``.
#         color_tension (tuple): Optional.
#             The color to use for tension forces.
#             Default is ``(255, 0, 0)``.
#         color_compression (tuple): Optional.
#             The color to use for compression forces.
#             Default is ``(0, 0, 255)``.

#     Example:

#         .. code-block:: python

#             import random
#             import compas
#             import compas_rhino as compas_rhino

#             from compas.datastructures.network import Network

#             network = Network.from_obj(compas.get('lines.obj'))

#             for u, v, attr in network.edges(True):
#                 attr['f'] = random.choice([-1.0, 1.0]) * random.randint(1, 10)

#             compas_rhino.network_display_axial_forces(network)

#     See Also:
#         * :func:`network_display_reaction_forces`
#         * :func:`network_display_residual_forces`
#         * :func:`network_display_selfweight`

#     """
#     tol = compas_rhino.get_tolerance()
#     objects = compas_rhino.get_objects(name='{0}.force:axial.*'.format(network.attributes['name']))
#     compas_rhino.delete_objects(objects)

#     if not display:
#         return

#     lines = []

#     for u, v, attr in network.edges(True):
#         start  = network.vertex_coordinates(u)
#         end    = network.vertex_coordinates(v)
#         force  = attr['f']
#         color  = color_tension if force > 0.0 else color_compression
#         radius = scale * ((force ** 2) ** 0.5 / 3.14159) ** 0.5
#         name   = '{0}.force:axial.{1}-{2}'.format(network.attributes['name'], u, v)

#         if radius < tol:
#             continue

#         lines.append({
#             'start' : start,
#             'end'   : end,
#             'name'  : name,
#             'color' : color,
#             'radius': radius,
#         })

#     compas_rhino.xdraw_cylinders(lines, layer=layer, clear=clear_layer)


# def network_display_reaction_forces(network,
#                                     display=True,
#                                     layer=None,
#                                     clear_layer=False,
#                                     scale=1.0,
#                                     color=(0, 255, 0),
#                                     attr_name='is_anchor'):

#     tol = compas_rhino.get_tolerance()
#     objects = compas_rhino.get_objects(name='{0}.force:reaction.*'.format(network.attributes['name']))
#     compas_rhino.delete_objects(objects)

#     if not display:
#         return

#     lines = []

#     for key, attr in network.vertices(True):

#         if not attr[attr_name]:
#             continue

#         force  = attr['rx'], attr['ry'], attr['rz']
#         start  = network.vertex_coordinates(key)
#         end    = [start[i] - scale * force[i] for i in range(3)]
#         length = sum((end[i] - start[i]) ** 2 for i in range(3)) ** 0.5
#         arrow  = 'end'
#         name   = '{0}.force:reaction.{1}'.format(network.attributes['name'], key)

#         if length < tol:
#             continue

#         lines.append({
#             'start': start,
#             'end'  : end,
#             'name' : name,
#             'color': color,
#             'arrow': arrow,
#         })

#     compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer)


# def network_display_residual_forces(network,
#                                     display=True,
#                                     layer=None,
#                                     clear_layer=False,
#                                     scale=1.0,
#                                     color=(0, 255, 255),
#                                     attr_name='is_anchor'):

#     tol = compas_rhino.get_tolerance()
#     guids = compas_rhino.get_objects(name='{0}.force:residual.*'.format(network.attributes['name']))
#     compas_rhino.delete_objects(guids)

#     if not display:
#         return

#     lines = []

#     for key, attr in network.vertices(True):

#         if attr[attr_name]:
#             continue

#         force  = attr['rx'], attr['ry'], attr['rz']
#         start  = network.vertex_coordinates(key)
#         end    = [start[i] + scale * force[i] for i in range(3)]
#         length = distance_point_point(start, end)
#         arrow  = 'end'
#         name   = '{0}.force:residual.{1}'.format(network.attributes['name'], key)

#         if length < tol:
#             continue

#         lines.append({
#             'start' : start,
#             'end'   : end,
#             'name'  : name,
#             'color' : color,
#             'arrow' : arrow,
#         })

#     compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer)


# def network_display_selfweight(network,
#                                display=True,
#                                layer=None,
#                                clear_layer=False,
#                                scale=1.0,
#                                color=(0, 255, 0)):

#     tol = compas_rhino.get_tolerance()
#     guids = compas_rhino.get_objects(name='{0}.force:selfweight.*'.format(network.attributes['name']))
#     compas_rhino.delete_objects(guids)

#     if not display:
#         return

#     lines = []

#     for key, attr in network.vertices(True):
#         load   = 0, 0, network.vertex_area(key)
#         start  = network.vertex_coordinates(key)
#         end    = [start[i] - scale * load[i] for i in range(3)]
#         name   = '{0}.force:selfweight.{1}'.format(network.attributes['name'], key)
#         arrow  = 'end'
#         length = distance_point_point(start, end)

#         if length < tol:
#             continue

#         lines.append({
#             'start': start,
#             'end'  : end,
#             'name' : name,
#             'color': color,
#             'arrow': arrow,
#         })

#     compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer)


# def network_display_applied_loads(network,
#                                   display=True,
#                                   layer=None,
#                                   clear_layer=False,
#                                   scale=1.0,
#                                   color=(0, 0, 255)):

#     tol = compas_rhino.get_tolerance()
#     guids = compas_rhino.get_objects(name='{0}.force:load.*'.format(network.attributes['name']))
#     compas_rhino.delete_objects(guids)

#     if not display:
#         return

#     lines = []

#     for key, attr in network.vertices(True):
#         load   = attr['px'], attr['py'], attr['pz']
#         end    = network.vertex_coordinates(key)
#         start  = [end[i] - scale * load[i] for i in range(3)]
#         length = distance_point_point(start, end)
#         arrow  = 'end'
#         name   = '{0}.force:load.{1}'.format(network.attributes['name'], key)

#         if length < tol:
#             continue

#         lines.append({
#             'start': start,
#             'end'  : end,
#             'name' : name,
#             'color': color,
#             'arrow': arrow,
#         })

#     compas_rhino.xdraw_lines(lines, layer=layer, clear=clear_layer)
