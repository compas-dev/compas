from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
    'VertexFilter',
    'EdgeFilter',
    'FaceFilter',
]


class VertexFilter(object):

    __module__ = 'compas.datastructures._mixins'

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
        for key, attr in self.vertices(True):
            is_match = True

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if callable(method):
                    val = method(key)

                    if isinstance(val, list):
                       if value not in val:
                          is_match = False
                          break
                       break

                    if isinstance(value, (tuple, list)):
                        minval, maxval = value

                        if val < minval or val > maxval:
                            is_match = False
                            break
                    else:
                        if value != val:
                            is_match = False
                            break

                else:
                    if name not in attr:
                        is_match = False
                        break

                    if isinstance(attr[name], list):
                       if value not in attr[name]:
                          is_match = False
                          break
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

    def vertices_where_predicate(self, predicate, data=False):
        """Get vertices for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : function
            The condition you want to evaluate
        data : bool, optional
            Yield the vertices and their data attributes.
            Default is ``False``.

        Yields
        ------
        key: hashable
            The next vertex that matches the condition.
        2-tuple
            The next vertex and its attributes, if ``data=True``.

        Examples
        --------
        .. code-block:: python

            from compas.datastructures import Mesh

            mesh = Mesh()

            v0 = mesh.add_vertex( x = 0.0, y = 0.0, z = 0.0, extra_attr1 = 0, extra_attr2 = [])
            v1 = mesh.add_vertex( x = 100.0, y = 0.0, z = 0.0, extra_attr1 = 2, extra_attr2 = [3,5,9])
            v2 = mesh.add_vertex( x = 100.0, y = 100.0, z = 0.0, extra_attr1 = 1, extra_attr2 = ['value1', 'value2'])
            v3 = mesh.add_vertex( x = 0.0, y = 100.0, z = 0.0, extra_attr1 = 2, extra_attr2 = [3,7,12])

            mesh.add_face([v0,v1,v3])
            mesh.add_face([v1,v2,v3])

            for v_key in mesh.vertices_where_predicate(lambda _, attr: attr['x'] == 100.0):
                print v_key

            for v_key, v_data in mesh.vertices_where_predicate(lambda _, attr: 50.0 <= attr['y'] <= 150.0, True):
                print v_key, v_data

            for v_key in mesh.vertices_where_predicate(lambda _, attr: 'extra_attr2' in attr):
                print v_key

            for v_key in mesh.vertices_where_predicate(lambda _, attr: 3 in attr['extra_attr2']):
                print v_key

            for v_key in mesh.vertices_where_predicate(lambda _, attr: 'value2' in attr['extra_attr2']):
                print v_key
        """
        for key, attr in self.vertices(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key


class EdgeFilter(object):

    __module__ = 'compas.datastructures._mixins'

    def edges_where(self, conditions, data=False):
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
        for u, v, attr in self.edges(True):
            is_match = True

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if callable(method):
                    val = method(u, v)

                    if isinstance(value, (tuple, list)):
                        minval, maxval = value

                        if val < minval or val > maxval:
                            is_match = False
                            break
                    else:
                        if value != val:
                            is_match = False
                            break

                else:
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
                    yield u, v, attr
                else:
                    yield u, v


class FaceFilter(object):

    __module__ = 'compas.datastructures._mixins'

    def faces_where(self, conditions, data=False):
        for fkey, attr in self.faces(True):
            is_match = True

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if callable(method):
                    val = method(fkey)

                    if isinstance(value, (tuple, list)):
                        minval, maxval = value

                        if val < minval or val > maxval:
                            is_match = False
                            break
                    else:
                        if value != val:
                            is_match = False
                            break

                else:
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
                    yield fkey, attr
                else:
                    yield fkey


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
