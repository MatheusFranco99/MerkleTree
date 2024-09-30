# Merkle Tree

This directory contains an implementation for the Merkle Tree data structure.

## Components

We define a [`Transaction`](transaction.py) class as an abstraction of a general transaction.

For the tree, we define a [`TreeNode`](tree_node.py) class that holds some data, its hash, its child nodes and parent node.

The main class is the [`MerkleTree`](merkle_tree.py) that receives a list of transactions and builds the tree. This class provides a method to produce a proof that a transaction belongs to the list of transactions.

The proof is an object of the class [`MerkleProof`](merkle_tree_proof.py) that contains hash operations to be performed in order to reach the Merkle tree's root hash.

## Usage

To check out how it can be used, check out the [merkle_tree_usage.ipynb](./merkle_tree_usage.ipynb) file.

## Complexity test

A complexity test on the size of the proof is performed in the [merkle_tree_complexity_test.ipynb](./merkle_tree_complexity_test.ipynb) file.