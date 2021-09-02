from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ..datastructure import Datastructure
from ..network import Network


class Assembly(Datastructure):

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
