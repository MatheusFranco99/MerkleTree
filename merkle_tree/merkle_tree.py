""" Merkle Tree """

import hashlib
from typing import Callable
from merkle_tree_proof import MerkleJoinDirection, MerkleProof, MerkleProofOperation
from transaction import Transaction
from tree_node import TreeNode

def join_hashes(hash_a: str, hash_b: str, hash_f: Callable[[str, str], str]) -> str:
    """ Returns the hash of the combination of two hashes """
    return hash_f(hash_a + hash_b)

class MerkleTree:
    """ Implements a Merkle Tree holding the transactions and providing proofs """

    def __init__(self, transactions: list[Transaction]):
        self.transactions: list[Transaction] = transactions
        self.root_node: TreeNode | None = None
        self.transaction_nodes: list[TreeNode] = []
        self.build_tree()

    @staticmethod
    def hash_object(obj) -> str:
        """ Hashes a generalized object """
        return hashlib.sha256(obj.encode('utf-8')).hexdigest()

    def merge_nodes(self, nodes: list[TreeNode]) -> list[TreeNode]:
        """ Merges nodes returning len(nodes)//2 nodes (+1 in case of an odd number of nodes) """
        merged_nodes: list[TreeNode] = []

        i = 0
        while i <= len(nodes) - 1:
            node_a = nodes[i]
            if i == len(nodes) - 1:
                merged_nodes.append(node_a)
            else:
                node_b = nodes[i+1]
                node = TreeNode(data = None, node_hash = join_hashes(node_a.hash, node_b.hash, self.hash_object), child_nodes = [node_a, node_b], parent = None)
                merged_nodes.append(node)
                node_a.parent = node
                node_b.parent = node
            i += 2

        return merged_nodes

    def build_tree(self) -> None:
        """ Creates the tree """

        nodes: list[TreeNode] = []

        for transaction in self.transactions:
            node = TreeNode(data = transaction, node_hash = self.hash_object(transaction.body()), child_nodes = [], parent = None)
            nodes.append(node)

        self.transaction_nodes = nodes

        while len(nodes) > 1:
            nodes = self.merge_nodes(nodes)

        assert len(nodes) == 1

        self.root_node = nodes[0]

    def run_dfs(self, transaction: Transaction) -> TreeNode:
        """ Runs a depth-first-search to find the transaction """

    def get_merkle_proof_operation(self, parent: TreeNode, child_target: TreeNode) -> MerkleProofOperation:
        """ Return a Merkle proof operation given a parent and a child target.
            The operation is constructed by finding the other node that is a child of the parent node,
            by getting its hash and by getting the connection direction (if it's on the left or right from the target node).
        """
        found_target: bool = False
        for child in parent.child_nodes:
            if child.equal(child_target):
                found_target = True
            else:
                if found_target:
                    return MerkleProofOperation(hash = child.hash, direction = MerkleJoinDirection.RIGHT)
                else:
                    return MerkleProofOperation(hash = child.hash, direction = MerkleJoinDirection.LEFT)

        raise ValueError("Couldn't construct Merkle proof operation")

    def proof_for_transaction(self, transaction: Transaction) -> MerkleProof | None:
        """ Returns a proof that the transaction belongs to the list of transactions, or None if it doesn't belong to it """

        transaction_node = None

        for node in self.transaction_nodes:
            if node.data.equal(transaction):
                transaction_node = node
                break

        if transaction_node is None:
            return None

        merkle_proof_operations: list[MerkleProofOperation] = []
        curr_node = transaction_node
        while not curr_node.equal(self.root_node):
            parent = curr_node.parent
            merkle_operation = self.get_merkle_proof_operation(parent = parent, child_target = curr_node)
            merkle_proof_operations.append(merkle_operation)
            curr_node = parent

        return MerkleProof(operations = merkle_proof_operations)
