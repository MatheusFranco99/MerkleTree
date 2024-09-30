""" Adds the code for a general tree """

from dataclasses import dataclass
import queue
from typing import Any

@dataclass
class TreeNode:
    """ A general node tree """
    data: Any
    hash: str
    child_nodes: list # list of pointers to TreeNode
    parent: Any # pointer to TreeNode

    def __init__(self, data: Any, node_hash: str, child_nodes: list, parent: Any):
        self.data = data
        self.hash = node_hash
        self.child_nodes = child_nodes
        self.parent = parent

    def add_child_nodes(self, child_nodes: list) -> None:
        """ Add child nodes """
        for node in child_nodes:
            self.child_nodes.append(node)

    def clear(self) -> None:
        """ Clear all data and child nodes """
        self.data = None
        self.child_nodes = []

    def equal(self, other) -> bool:
        """ Returns if it's equal to the other object """
        if not isinstance(other, TreeNode):
            return False
        return self.hash == other.hash

def print_tree(root_node: TreeNode) -> None:
    """ Prints a tree """

    def print_node(node: TreeNode, prefix: str):
        if node.data is None:
            print(f"{prefix}({node.hash[:5]}...)")
        else:
            print(f"{prefix}({node.hash[:5]}...) -> {node.data}")

    node_queue = queue.LifoQueue() # Queue with elements (node, prefix)
    node_queue.put((root_node, ""))

    while not node_queue.empty():
        queue_element: tuple[TreeNode, str] = node_queue.get()
        curr_node = queue_element[0]
        prefix = queue_element[1]
        print_node(curr_node, prefix)

        new_prefix = prefix + "\t"
        for child in curr_node.child_nodes:
            node_queue.put((child, new_prefix))

