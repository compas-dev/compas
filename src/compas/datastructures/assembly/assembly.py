from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Datastructure
from compas.datastructures import Network
from .exceptions import AssemblyError


class Assembly(Datastructure):
    """A data structure for managing the connections between different parts of an assembly.

    Parameters
    ----------
    name : str, optional
        The name of the assembly.

    Attributes
    ----------
    attributes : dict[str, Any]
        General attributes of the data structure that will be included in the data dict and serialization.
    network : :class:`compas.datastructures.Network`
        The network that is used under the hood to store the parts and their connections.

    See Also
    --------
    :class:`compas.datastructures.Network`
    :class:`compas.datastructures.Mesh`
    :class:`compas.datastructures.VolMesh`

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "attributes": {"type": "object"},
            "network": Network.DATASCHEMA,
        },
        "required": ["network"],
    }

    def __init__(self, name=None, **kwargs):
        super(Assembly, self).__init__()
        self.attributes = {"name": name or "Assembly"}
        self.attributes.update(kwargs)
        self.network = Network()
        self._parts = {}

    def __str__(self):
        tpl = "<Assembly with {} parts and {} connections>"
        return tpl.format(self.network.number_of_nodes(), self.network.number_of_edges())

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def data(self):
        return {
            "attributes": self.attributes,
            "network": self.network.data,
        }

    @classmethod
    def from_data(cls, data):
        assembly = cls()
        assembly.attributes.update(data["attributes"] or {})
        assembly.network = Network.from_data(data["network"])
        assembly._parts = {part.guid: part.key for part in assembly.parts()}  # type: ignore
        return assembly

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def name(self):
        return self.attributes.get("name") or self.__class__.__name__

    @name.setter
    def name(self, value):
        self.attributes["name"] = value

    # ==========================================================================
    # Constructors
    # ==========================================================================

    # ==========================================================================
    # Methods
    # ==========================================================================

    def add_part(self, part, key=None, **kwargs):
        """Add a part to the assembly.

        Parameters
        ----------
        part : :class:`compas.datastructures.Part`
            The part to add.
        key : int | str, optional
            The identifier of the part in the assembly.
            Note that the key is unique only in the context of the current assembly.
            Nested assemblies may have the same `key` value for one of their parts.
            Default is None in which case the key will be an automatically assigned integer value.
        **kwargs: dict[str, Any], optional
            Additional named parameters collected in a dict.

        Returns
        -------
        int | str
            The identifier of the part in the current assembly network.

        """
        if part.guid in self._parts:
            raise AssemblyError("Part already added to the assembly")
        key = self.network.add_node(key=key, part=part, **kwargs)
        part.key = key
        self._parts[part.guid] = part.key
        return key

    def add_connection(self, a, b, **kwargs):
        """Add a connection between two parts.

        Parameters
        ----------
        a : :class:`compas.datastructures.Part`
            The "from" part.
        b : :class:`compas.datastructures.Part`
            The "to" part.
        **kwargs : dict[str, Any], optional
            Attribute dict compiled from named arguments.

        Returns
        -------
        tuple[int | str, int | str]
            The tuple of node identifiers that identifies the connection.

        Raises
        ------
        :class:`AssemblyError`
            If `a` and/or `b` are not in the assembly.

        """
        error_msg = "Both parts have to be added to the assembly before a connection can be created."
        if a.key is None or b.key is None:
            raise AssemblyError(error_msg)
        if not self.network.has_node(a.key) or not self.network.has_node(b.key):
            raise AssemblyError(error_msg)
        return self.network.add_edge(a.key, b.key, **kwargs)

    def delete_part(self, part):
        """Remove a part  from the assembly.

        Parameters
        ----------
        part : :class:`compas.datastructures.Part`
            The part to add.

        Returns
        -------
        None

        """
        del self._parts[part.guid]
        self.network.delete_node(key=part.key)

    def delete_connection(self, edge):
        """Delete a connection between two parts.

        Parameters
        ----------
        edge : :class:`compas.datastructures.Part`
            The part to add.

        Returns
        -------
        None

        """
        self.network.delete_edge(edge=edge)

    def parts(self):
        """The parts of the assembly.

        Yields
        ------
        :class:`compas.datastructures.Part`
            The individual parts of the assembly.

        """
        for node in self.network.nodes():
            yield self.network.node_attribute(node, "part")

    def connections(self, data=False):
        """Iterate over the connections between the parts.

        Parameters
        ----------
        data : bool, optional
            If True, yield the connection attributes in addition to the connection identifiers.

        Yields
        ------
        tuple[int | str, int | str] | tuple[tuple[int | str, int | str], dict[str, Any]]
            If `data` is False, the next connection identifier (u, v).
            If `data` is True, the next connector identifier and its attributes as a ((u, v), attr) tuple.

        """
        return self.network.edges(data)

    def find(self, guid):
        """Find a part in the assembly by its GUID.

        Parameters
        ----------
        guid : str
            A globally unique identifier.
            This identifier is automatically assigned when parts are created.

        Returns
        -------
        :class:`compas.datastructures.Part` | None
            The identified part,
            or None if the part can't be found.

        """
        key = self._parts.get(guid)

        if key is None:
            return None

        return self.network.node_attribute(key, "part")

    def find_by_key(self, key):
        """Find a part in the assembly by its key.

        Parameters
        ----------
        key : int | str, optional
            The identifier of the part in the assembly.

        Returns
        -------
        :class:`compas.datastructures.Part` | None
            The identified part,
            or None if the part can't be found.

        """
        if key not in self.network.node:
            return None

        return self.network.node_attribute(key, "part")
