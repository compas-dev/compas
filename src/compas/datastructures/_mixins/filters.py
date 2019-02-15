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
        predicate : callable
            The condition you want to evaluate. The callable takes 2 parameters: ``key``, ``attr`` and should return ``True`` or ``False``.
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

            v0 = mesh.add_vertex(x=0.0, y=0.0, z=0.0, extra_attr1=0, extra_attr2=[])
            v1 = mesh.add_vertex(x=100.0, y=0.0, z=0.0, extra_attr1=2, extra_attr2=[3,5,9])
            v2 = mesh.add_vertex(x=100.0, y=100.0, z=0.0, extra_attr1=1, extra_attr2=['value1', 'value2'])
            v3 = mesh.add_vertex(x=0.0, y=100.0, z=0.0, extra_attr1=2, extra_attr2=[3,7,12])

            mesh.add_face([v0,v1,v3])
            mesh.add_face([v1,v2,v3])

            for v_key in mesh.vertices_where_predicate(lambda key, attr: attr['x'] == 100.0):
                print v_key

            for v_key, v_data in mesh.vertices_where_predicate(lambda key, attr: 50.0 <= attr['y'] <= 150.0, True):
                print v_key, v_data

            for v_key in mesh.vertices_where_predicate(lambda key, attr: 'extra_attr2' in attr):
                print v_key

            for v_key in mesh.vertices_where_predicate(lambda key, attr: 3 in attr['extra_attr2']):
                print v_key

            for v_key in mesh.vertices_where_predicate(lambda key, attr: 'value2' in attr['extra_attr2']):
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
        data : bool, optional
            Yield the edges and their data attributes.
            Default is ``False``.

        Yields
        ------
        2-tuple
            The next edge as a (u, v) tuple, if ``data=False``.
        3-tuple
            The next edge as a (u, v, data) tuple, if ``data=True``.
        """
        for u, v, attr in self.edges(True):
            is_match = True

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if callable(method):
                    val = method(u, v)

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
                    yield u, v, attr
                else:
                    yield u, v

    def edges_where_predicate(self, predicate, data=False):
        """Get edges for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate. The callable takes 3 parameters: ``u``, ``v``, ``attr`` and should return ``True`` or ``False``.
        data : bool, optional
            Yield the vertices and their data attributes.
            Default is ``False``.

        Yields
        ------
        2-tuple
            The next edge as a (u, v) tuple, if ``data=False``.
        3-tuple
            The next edge as a (u, v, data) tuple, if ``data=True``.

        Examples
        --------
        .. code-block:: python

            from compas.datastructures import Mesh

            mesh = Mesh()

            v0 = mesh.add_vertex(x=0.0, y=0.0, z=0.0)
            v1 = mesh.add_vertex(x=100.0, y=0.0, z=0.0)
            v2 = mesh.add_vertex(x=100.0, y=100.0, z=0.0)
            v3 = mesh.add_vertex(x=0.0, y=100.0, z=0.0)

            mesh.add_face([v0,v1,v3])
            mesh.add_face([v1,v2,v3])

            mesh.update_default_edge_attributes({'extra_attr1':None, "extra_attr2":[]})

            random_edge = mesh.get_any_edge()
            mesh.set_edge_attributes(random_edge, ['extra_attr1', 'extra_attr2'], [2, [3,5,9]])


            for u, v, e_data in mesh.edges_where_predicate(lambda u, v, attr: attr['extra_attr1'] == 2, True):
                print u, v, e_data

            for u, v in mesh.edges_where_predicate(lambda u, v, attr: 'extra_attr1' in attr):
                print u, v

            for u, v in mesh.edges_where_predicate(lambda u, v, attr: 3 in attr['extra_attr2']):
                print u, v
        """
        for u, v, attr in self.edges(True):
            if predicate(u, v, attr):
                if data:
                    yield u, v, attr
                else:
                    yield u, v


class FaceFilter(object):

    __module__ = 'compas.datastructures._mixins'

    def faces_where(self, conditions, data=False):
        """Get faces for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            Yield the faces and their data attributes.
            Default is ``False``.

        Yields
        ------
        key: hashable
            The next face that matches the condition.
        2-tuple
            The next face and its attributes, if ``data=True``.

        """
        for fkey, attr in self.faces(True):
            is_match = True

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if callable(method):
                    val = method(fkey)

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
                    yield fkey, attr
                else:
                    yield fkey

    def faces_where_predicate(self, predicate, data=False):
        """Get faces for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate. The callable takes 2 parameters: ``key``, ``attr`` and should return ``True`` or ``False``.
        data : bool, optional
            Yield the faces and their data attributes.
            Default is ``False``.

        Yields
        ------
        key: hashable
            The next face that matches the condition.
        2-tuple
            The next face and its attributes, if ``data=True``.

        Examples
        --------
        .. code-block:: python

            from compas.datastructures import Mesh

            mesh = Mesh()

            v0 = mesh.add_vertex(x=0.0, y=0.0, z=0.0)
            v1 = mesh.add_vertex(x=100.0, y=0.0, z=0.0)
            v2 = mesh.add_vertex(x=100.0, y=100.0, z=0.0)
            v3 = mesh.add_vertex(x=0.0, y=100.0, z=0.0)

            mesh.add_face([v0,v1,v3], extra_attr1=5, extra_attr2=[3,5,9])
            mesh.add_face([v1,v2,v3], extra_attr1=1, extra_attr2=[3,7,12])


            for f_key in mesh.faces_where_predicate(lambda f_key, attr: attr['extra_attr1'] == 5):
                print f_key

            for f_key, f_data in mesh.faces_where_predicate(lambda f_key, attr: 3 <= attr['extra_attr1'] <= 6, True):
                print f_key, f_data

            for f_key in mesh.faces_where_predicate(lambda f_key, attr: 'extra_attr2' in attr):
                print f_key

            for f_key in mesh.faces_where_predicate(lambda f_key, attr: 3 in attr['extra_attr2']):
                print f_key
        """
        for fkey, attr in self.faces(True):
            if predicate(fkey, attr):
                if data:
                    yield fkey, attr
                else:
                    yield fkey


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
