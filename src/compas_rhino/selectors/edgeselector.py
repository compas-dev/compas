from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

import compas

try:
    import rhinoscriptsyntax as rs
except ImportError:
    compas.raise_if_ironpython()


__all__ = ['EdgeSelector']


class EdgeSelector(object):

    @staticmethod
    def select_edge(self, message="Select an edge."):
        guid = rs.GetObject(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
        if guid:
            prefix = self.attributes['name']
            name = rs.ObjectName(guid).split('.')
            if 'edge' in name:
                if not prefix or prefix in name:
                    key = name[-1]
                    u, v = key.split('-')
                    u = ast.literal_eval(u)
                    v = ast.literal_eval(v)
                    return u, v
        return None

    @staticmethod
    def select_edges(self, message="Select edges."):
        keys = []
        guids = rs.GetObjects(message, preselect=True, filter=rs.filter.curve | rs.filter.textdot)
        if guids:
            prefix = self.attributes['name']
            seen = set()
            for guid in guids:
                name = rs.ObjectName(guid).split('.')
                if 'edge' in name:
                    if not prefix or prefix in name:
                        key = name[-1]
                        if not seen.add(key):
                            u, v = key.split('-')
                            u = ast.literal_eval(u)
                            v = ast.literal_eval(v)
                            keys.append((u, v))
        return keys


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
