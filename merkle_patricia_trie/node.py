""" Patricia Merkle Trie """

from dataclasses import dataclass
from typing import Any

@dataclass
class Node:
    """ Merkle Patricia Trie Node """
    prefix_key: str

    class Empty:
        """ Empty node """

    class Leaf:
        """ Leaf node """
        def __init__(self, keyend: str, data: Any, prefix_key: str):
            self.keyend = keyend
            self.data = data
            self.prefix_key = prefix_key

    class Extension:
        """ Extension node """
        def __init__(self, shared_nibble: str, next_branch_node, prefix_key: str):
            self.shared_nibble = shared_nibble
            self.next_branch_node = next_branch_node
            self.prefix_key = prefix_key

    class Branch:
        """ Branch node """
        def __init__(self, branches: list, data: Any, prefix_key: str):
            assert len(branches) == 16
            self.branches = branches
            self.data = data
            self.prefix_key = prefix_key
