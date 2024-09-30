""" Patricia Merkle Trie """

import queue
from node import Node

HEX = 16

# Hex manipulation

def hexchar_to_int(char: str) -> int:
    """ Transforms a hex char to int """
    return int(char, base = HEX)

def int_to_hexchar(value: int) -> str:
    """ Transforms a hex char to int """
    return hex(value)[-1]

def all_key_chars() -> list[str]:
    """ Get all key chars possible in the hexadecimal base """
    return [int_to_hexchar(value)[-1] for value in range(0,HEX)]

# Prefix

def get_biggest_common_prefix(word1: str, word2: str) -> str:
    """ Returns the biggest common prefix """
    ret: str = ""
    for i in range(min(len(word1), len(word2))):
        if word1[i] == word2[i]:
            ret += word1[i]
        else:
            return ret
    return ret

def get_biggest_shared_nibble_for_keys(keys: list[str]) -> str:
    """ Returns the biggest common prefix between all elements """
    ret: str = keys[0]
    for key in keys:
        ret = get_biggest_common_prefix(ret, key)
    return ret

def has_key_prefix(total_key: str, key_prefix: str) -> bool:
    """ Returns whether a total key has a key prefix or not """
    assert len(key_prefix) <= len(total_key)
    for i, v in enumerate(key_prefix):
        if total_key[i] != v:
            return False
    return True

def get_key_end(total_key: str, key_prefix: str) -> str:
    """ Get the key end, i.e. the part of total key that is not in key prefix """
    return total_key[len(key_prefix):]

# Print tree

def print_merkle_patricia_tree(root_node: Node.Extension) -> None:
    """ Prints a tree """

    def print_extension_node(node: Node.Extension, prefix: str):
        print(f"{prefix}Extension Node: (Prefix key: {node.prefix_key}, Shared nibble: {node.shared_nibble})")

    def print_empty_node(prefix: str):
        print(f"{prefix}Empty Node")

    def print_leaf_node(node: Node.Leaf, prefix: str):
        print(f"{prefix}Leaf Node: (Prefix key: {node.prefix_key}, Key end: {node.keyend}, Data: {node.data})")

    def print_branch_node(node: Node.Branch, prefix: str):
        print(f"{prefix}Branch Node: (Prefix key: {node.prefix_key})")
        for i, next_node in enumerate(node.branches):
            if isinstance(next_node, Node.Leaf):
                print(f"{prefix}\t{i} ->",end="")
                print_leaf_node(next_node, prefix = "")
            elif isinstance(next_node, Node.Empty):
                print(f"{prefix}\t{i} ->",end="")
                print_empty_node(prefix = "")

    def print_node(node, prefix: str):
        if isinstance(node, Node.Extension):
            print_extension_node(node, prefix)
        elif isinstance(node, Node.Empty):
                print_empty_node(prefix)
        elif isinstance(node, Node.Leaf):
            print_leaf_node(node, prefix)
        elif isinstance(node, Node.Branch):
            print_branch_node(node, prefix)

    node_queue = queue.LifoQueue() # Queue with elements (node, prefix)
    node_queue.put((root_node, ""))

    while not node_queue.empty():
        queue_element: tuple[Node, str] = node_queue.get()

        curr_node = queue_element[0]
        prefix = queue_element[1]
        print_node(curr_node, prefix)

        if isinstance(curr_node, Node.Extension):
            node_queue.put((curr_node.next_branch_node, prefix + "\t"))
        elif isinstance(curr_node, Node.Branch):
            for next_node in curr_node.branches:
                if isinstance(next_node, Node.Extension):
                    node_queue.put((next_node, prefix + "\t"))
                if isinstance(next_node, Node.Branch):
                    node_queue.put((next_node, prefix + "\t"))
