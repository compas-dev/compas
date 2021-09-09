from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ..datastructure import Datastructure
from ..graph import Graph


class Assembly(Datastructure):
    """A data structure for managing the connections between different parts of an assembly.

    Attributes
    ----------
    attributes: dict
        General attributes of the assembly that will be included in the data dict.
    graph: :class:`compas.datastructures.Graph`
        The graph that is used under the hood to store the parts and their connections.
    """

    @property
    def DATASCHEMA(self):
        import schema
        return schema.Schema({
            "graph": Graph,
        })

    @property
    def JSONSCHEMANAME(self):
        return 'assembly'

    def __init__(self, name=None, **kwargs):
        super(Assembly, None).__init__(name=name, **kwargs)
        self.graph = Graph()
        self.parts = {}

    def __str__(self):
        tpl = "<Assembly with {} parts and {} connections>"
        return tpl.format(self.graph.number_of_nodes(), self.graph.number_of_edges())

    @property
    def data(self):
        """dict : A data dict representing the assembly data structure for serialization.
        """
        data = {
            'attributes': self.attributes,
            'graph': self.graph.data,
        }
        return data

    @data.setter
    def data(self, data):
        self.attributes.update(data['attributes'] or {})
        self.graph.data = data['graph']

    def add_part(self, part, key=None, **kwargs):
        """Add a part to the assembly.

        Parameters
        ----------
        part: :class:`compas.datastructures.Part`
            The part to add.
        key: int or str, optional
            The identifier of the part in the assembly.
            Note that the key is unique only in the context of the current assembly.
            Nested assemblies may have the same ``key`` value for one of their parts.
            Default is ``None`` in which case the key will be automatically assigned integer value.
        kwargs: dict
            Additional named parameters collected in a dict.

        Returns
        -------
        int or str
            The identifier of the part in the current assembly graph.

        """
        key = self.graph.add_node(key=key, part=part, **kwargs)
        part.key = key
        self.parts[part.guid] = part
        return key

    def add_connection(self, a, b, **kwargs):
        """Add a connection between two parts.

        Parameters
        ----------
        a: int or str
            The identifier of the "from" part in the assembly.
        b: int or str
            The identifier of the "to" part in the assembly.
        kwargs: dict
            Additional named parameters collected in a dict.

        Returns
        -------
        tuple of str or int
            The tuple of node identifiers that identifies the connection.

        """
        return self.graph.add_edge(a, b, **kwargs)

    def parts(self):
        """The parts of the assembly.

        Yields
        ------
        :class:`compas.datastructures.Part`
            The individual parts of the assembly.
        """
        for node in self.graph.nodes():
            yield self.graph.node_attribute(node, 'part')

    def connections(self):
        """The connections between the parts."""
        return self.graph.edges()

    def find(self, guid):
        """Find a part in the assembly by its GUID.

        Parameters
        ----------
        guid: str
            A globally unique identifier.
            This identifier is automatically assigned when parts are created.

        Returns
        -------
        :class:`compas.datastructures.Part` or None
            The identified part, if any.

        """
        return self.parts.get(guid)
