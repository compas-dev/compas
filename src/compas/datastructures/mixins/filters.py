__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'VertexFilter',
    'EdgeFilter',
    'FaceFilter',
]


class VertexFilter(object):

    def vertices_where(self, conditions, data=False):
        """Get vertices for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            Yield the vertices and their data attributes.
            Default is ``False``.

        Yields
        ------
        key: hashable
            The next vertex that matches the condition.
        2-tuple
            The next vertex and its attributes, if ``data=True``.
    
        """
        # keys = []
        for key, attr in self.vertices(True):
            is_match = True
            for name, value in conditions.items():
                if name not in attr:
                    is_match = False
                    break
                if isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if attr[name] < minval or attr[name] > maxval:
                        is_match = False
                        break
                else:
                    if value != attr[name]:
                        is_match = False
                        break
            if is_match:
                if data:
                    yield key, attr
                else:
                    yield key
        #         keys.append(key)
        # return keys


class EdgeFilter(object):

    def edges_where(self, conditions):
        """Get edges for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.

        Returns
        -------
        list
            A list of edge keys that satisfy the condition(s).

        """
        keys = []
        for u, v, attr in self.edges(True):
            is_match = True
            for name, value in conditions.items():
                if name not in attr:
                    is_match = False
                    break
                if isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if attr[name] < minval or attr[name] > maxval:
                        is_match = False
                        break
                else:
                    if value != attr[name]:
                        is_match = False
                        break
            if is_match:
                keys.append((u, v))
        return keys


class FaceFilter(object):

    def faces_where(self, conditions):
        raise NotImplementedError


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":
    pass
