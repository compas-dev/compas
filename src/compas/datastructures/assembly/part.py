from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ..datastructure import Datastructure
from ..graph import Graph
from ..mesh import Mesh


class Part(Datastructure):
    """A data structure for representing assembly parts."""

    @property
    def DATASCHEMA(self):
        import schema
        return schema.Schema({
            "attributes": dict,
            "graph": Graph,
            "mesh": Mesh
        })

    @property
    def JSONSCHEMANAME(self):
        return 'assembly'

    def __init__(self, name, **kwargs):
        super(Part, self).__init__()
        self._key = None
        self._mesh = None
        self._graph = None

    def __str__(self):
        tpl = "<Part with ...>"
        return tpl

    @property
    def data(self):
        """dict : A data dict representing the part attributes, internal data structure, and geometries for serialization.
        """
        data = {
            'attributes': self.attributes,
            'mesh': self.mesh.data,
            'graph': self.graph.data
        }
        return data

    @data.setter
    def data(self, data):
        self.attributes.update(data['attributes'] or {})
        self.mesh.data = data['mesh']
        self.graph.data = data['graph']

    @property
    def key(self):
        return self._key

    @property
    def mesh(self):
        if not self._mesh:
            self._mesh = Mesh()
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

    @property
    def graph(self):
        if not self._graph:
            self._graph = Graph()
        return self._graph

    @graph.setter
    def graph(self, graph):
        self._graph = graph
