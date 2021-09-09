from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data.encoders import cls_from_dtype

from ..datastructure import Datastructure
# from ..graph import Graph


class Part(Datastructure):
    """Class representing assembly parts."""

    @property
    def DATASCHEMA(self):
        import schema
        return schema.Schema({
            "attributes": dict,
            # "graph": Graph,
            "geometries": list
        })

    @property
    def JSONSCHEMANAME(self):
        return 'assembly'

    def __init__(self, name, **kwargs):
        super(Part, self).__init__(name=name, **kwargs)
        # self.graph = Graph()
        self.geometries = []

    def __str__(self):
        tpl = "<Part with {} geometries and {} sub-parts with {} connections>"
        return tpl.format(len(self.geometries), self.graph.number_of_nodes(), self.graph.number_of_edges())

    @property
    def data(self):
        """dict : A data dict representing the part attributes, internal data structure, and geometries for serialization.
        """
        data = {
            'attributes': self.attributes,
            # 'graph': self.graph.data,
            'geometries': [(g.dtype, g.data) for g in self.geometries]
        }
        return data

    @data.setter
    def data(self, data):
        self.attributes.update(data['attributes'] or {})
        # self.graph.data = data['graph']
        self.geometries = []
        for dt, dd in data['geometries']:
            d = cls_from_dtype(dt).from_data(dd)
            self.geometries.append(d)
