from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ..datastructure import Datastructure
from ..network import Network


class Assembly(Datastructure):
    """A data structure for managing the connections between different parts of an assembly.

    Attributes
    ----------
    attributes: dict
        General attributes of the assembly that will be included in the data dict.
    network: :class:`compas.datastructures.Network`
        The network that is used under the hood to store the parts and their connections.
    """

    @property
    def DATASCHEMA(self):
        import schema
        return schema.Schema({
            "network": Network,
        })

    @property
    def JSONSCHEMANAME(self):
        return 'assembly'

    def __init__(self, *args, **kwargs):
        super(Assembly, None).__init__(*args, **kwargs)
        self.attributes = {}
        self.network = Network()

    def __str__(self):
        tpl = "<Assembly with {} parts and {} connections>"
        return tpl.format(self.network.number_of_nodes(), self.network.number_of_edges())

    @property
    def data(self):
        """dict : A data dict representing the assembly data structure for serialization.
        """
        data = {
            'attributes': self.attributes,
            'network': self.network,
        }
        return data

    @data.setter
    def data(self, data):
        self.attributes.update(data['attributes'] or {})
        self.network = data['network']

    def parts(self):
        """The parts of the assembly."""
        return self.network.nodes()

    def connections(self):
        """The connections between the parts."""
        return self.network.edges()

    def add_part(self, part, id=None, **kwargs):
        """Add a part to the assembly."""
        self.network.add_node(key=id, part=part, **kwargs)

    def add_connection(self, a, b, **kwargs):
        """Add a connection between two parts."""
        self.network.add_edge(a, b, **kwargs)
