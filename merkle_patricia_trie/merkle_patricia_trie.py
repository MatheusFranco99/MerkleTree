""" Patricia Merkle Trie """


import queue
from account import Account
from node import Node
from util import HEX, has_key_prefix, all_key_chars, get_key_end, get_biggest_shared_nibble_for_keys, hexchar_to_int

class MerklePatriciaTrie:
    """ Implements the Merkle Patricia Trie """

    def __init__(self, accounts: list[Account]):
        self.accounts = accounts
        self.root = None
        self.build_tree()

    def filter_accounts_by_key_prefix(self, accounts: list[Account], key_prefix: str) -> list[Account]:
        """ Filter given accounts by prefix key """
        ret: list[Account] = []
        for account in accounts:
            if has_key_prefix(account.key, key_prefix):
                ret.append(account)
        return ret

    def build_tree(self) -> None:
        """ Builds the Markle Patricia Trie """
        accounts_to_be_added = {account.key: account for account in self.accounts}

        extension_nodes_to_be_fulfilled: queue.Queue[Node.Extension] = queue.Queue()

        def create_extension_node(accounts: list[Account], prefix_key: str) -> tuple[Node.Extension, Node.Branch]:
            accounts_keys = [account.key for account in accounts]
            common_prefix = get_biggest_shared_nibble_for_keys(accounts_keys)
            shared_nibble = get_key_end(common_prefix, prefix_key)

            extension_node = Node.Extension(shared_nibble = shared_nibble, next_branch_node = None, prefix_key = prefix_key)
            branch_node = Node.Branch(branches = [Node.Empty for _ in range(HEX)], data = None, prefix_key = common_prefix)

            extension_node.next_branch_node = branch_node

            return extension_node

        first_extension_node = create_extension_node(list(accounts_to_be_added.values()), "")

        extension_nodes_to_be_fulfilled.put(first_extension_node)

        self.root = first_extension_node

        while not extension_nodes_to_be_fulfilled.empty() and len(accounts_to_be_added) > 0:
            next_entension_node = extension_nodes_to_be_fulfilled.get()
            next_branch_node: Node.Branch = next_entension_node.next_branch_node

            for key_digit in all_key_chars():

                # Get current prefix
                current_key_prefix = next_branch_node.prefix_key + key_digit

                # Get remaining accounts related for this key
                matched_remaining_accounts = list(self.filter_accounts_by_key_prefix(list(accounts_to_be_added.values()), current_key_prefix))

                if len(matched_remaining_accounts) == 0:
                    continue
                elif len(matched_remaining_accounts) == 1:
                    account = matched_remaining_accounts[0]
                    leaf = Node.Leaf(keyend = get_key_end(account.key, current_key_prefix), data = account, prefix_key = current_key_prefix)
                    next_branch_node.branches[hexchar_to_int(key_digit)] = leaf
                    del accounts_to_be_added[account.key]
                else:
                    new_extension_node = create_extension_node(matched_remaining_accounts, prefix_key = current_key_prefix)

                    next_branch_node.branches[hexchar_to_int(key_digit)] = new_extension_node

                    extension_nodes_to_be_fulfilled.put(new_extension_node)
