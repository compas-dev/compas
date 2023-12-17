from compas.datastructures import Tree
from compas.datastructures import TreeNode
from compas.data import json_dumps
import hashlib


def sha256(content):
    return hashlib.sha256(json_dumps(content).encode()).hexdigest()


class HashNode(TreeNode):
    def __init__(self, path, value=None):
        super().__init__()
        self.path = path
        self.value = value
        self._signature = None

    def __repr__(self):
        path = self.path or "ROOT"
        if self.value is not None:
            return "{}:{} @ {}".format(path, self.value, self.signature[:5])
        else:
            return "{} @ {}".format(path, self.signature[:5])

    @property
    def absolute_path(self):
        if self.parent is None:
            return self.path
        return self.parent.absolute_path + self.path

    @property
    def is_value(self):
        return self.value is not None

    @property
    def signature(self):
        return self._signature

    @property
    def children_dict(self):
        return {child.path: child for child in self.children}

    @property
    def children_paths(self):
        return [child.path for child in self.children]

    @classmethod
    def from_dict(cls, data_dict, path=""):
        node = cls(path)
        for key in data_dict:
            path = ".{}".format(key)
            if isinstance(data_dict[key], dict):
                child = cls.from_dict(data_dict[key], path=path)
                node.add(child)
            else:
                node.add(cls(path, value=data_dict[key]))

        return node


class HashTree(Tree):
    def __init__(self):
        super().__init__()
        self.signatures = {}

    @classmethod
    def from_dict(cls, data_dict):
        tree = cls()
        root = HashNode.from_dict(data_dict)
        tree.add(root)
        tree.calculate_signatures()
        return tree

    def calculate_signatures(self):
        self.node_signature(self.root)

    def node_signature(self, node, parent_path=""):
        absolute_path = parent_path + node.path
        if absolute_path in self.signatures:
            return self.signatures[absolute_path]

        signature = sha256(
            {
                "path": node.path,
                "value": node.value,
                "children": [self.node_signature(child, absolute_path) for child in node.children],
            }
        )

        self.signatures[absolute_path] = signature
        node._signature = signature

        return signature

    def diff(self, other):
        added = []
        removed = []
        modified = []

        def _diff(node1, node2):
            if node1.signature == node2.signature:
                return
            else:
                if node1.is_value or node2.is_value:
                    modified.append({"path": node1.absolute_path, "old": node2.value, "new": node1.value})

                for path in node1.children_paths:
                    if path in node2.children_dict:
                        _diff(node1.children_dict[path], node2.children_dict[path])
                    else:
                        added.append(
                            {"path": node1.children_dict[path].absolute_path, "value": node1.children_dict[path].value}
                        )

                for path in node2.children_paths:
                    if path not in node1.children_dict:
                        removed.append(
                            {"path": node2.children_dict[path].absolute_path, "value": node2.children_dict[path].value}
                        )

        _diff(self.root, other.root)

        return {"added": added, "removed": removed, "modified": modified}

    def print_diff(self, other):
        diff = self.diff(other)
        print("Added:")
        for item in diff["added"]:
            print(item)
        print("Removed:")
        for item in diff["removed"]:
            print(item)
        print("Modified:")
        for item in diff["modified"]:
            print(item)


if __name__ == "__main__":

    print("\nCOMPARE DICTS:")
    tree1 = HashTree.from_dict({"a": {"b": 1, "c": 3}, "d": [1, 2, 3], "e": 2})
    tree2 = HashTree.from_dict({"a": {"b": 1, "c": 2}, "d": [1, 2, 3], "f": 2})

    tree1.print_hierarchy()
    tree2.print_hierarchy()

    tree2.print_diff(tree1)

    print("\nCOMPARE MESH CHANGE:")

    from compas.datastructures import Mesh

    mesh = Mesh.from_polyhedron(4)
    tree1 = HashTree.from_dict(mesh.data)
    mesh.vertex_attribute(0, "x", 1.0)
    tree2 = HashTree.from_dict(mesh.data)
    tree1.print_hierarchy()
    tree2.print_hierarchy()
    tree2.print_diff(tree1)
