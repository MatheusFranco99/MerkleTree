# Summary

This summary is based on this [publication](https://www.researchgate.net/publication/358740207_An_Overview_of_Trees_in_Blockchain_Technology_Merkle_Trees_and_Merkle_Patricia_Tries) and some extra resources.

## Merkle Trees
- Define the Merkle Tree’s content and how it’s built.
    - Merkle Tree is a binary tree that stores a hash value for each node. The parent node is the hash output of a combination from its child nodes.
    - To construct the tree, you start with the list of hashes, and keep computing the combination of hashes (and new nodes) until the root node is reached.
    - The cool property is that changing a single cell breaks all the tree.
- What is the purpose of Merkle Trees?
    - It’s purpose is to provide a small proof that some object belong to a list of object.
    - For example, once the tree is built, you may ask whether some object belongs to the list that created such tree.
    - If so, one can return all operations (combination of hashes) that should be performed until the root hash is reached.
- What is the complexity for proofs with Merkle Trees?
    - The Merkle Tree provides a logarithmic complexity for the size of proofs since the size is bounded by the degree of the tree.
- How Bitcoin uses Merkle Trees?
    - In Bitcoin, Merkle Trees serves for holding a fingerprint of all transactions in a block.

## Merkle Patricia Tries
- What is the motivation for the Merkle Patricia Trie?
    - Merkle Trees are limited in the sense that it can only provide a query for the existence of an object, but you can’t access the object’s properties, for example.
    - This possibility is useful in Ethereum, e.g. to fetch the account balance for a certain address
- How Ethereum uses it?
    - Ethereum defined three kinds of trees:
        - transactions trees: similar to the Bitcoin use case
        - Receipts trees: retrieve instances about a given event (e.g. amount of gas)
        - State tree: to check the current balance of an account, if the account exists, or even running transactions
    - The trees should be able to quickly update after some object is changed, inserted or deleted.
    - The name Patricia comes from: Practical Algorithm To Retrieve Information Coded in Alphanumeric
- How Merkle Patricia Tries works?
    - It is more similar to a radix tree, while the Merkle Tree was similar to a binary tree.
    - It's goal is to store data (e.g. accounts) indexed by keys.
    - It contains 4 types of nodes:
        - Extension: you can see it as the first node of a subtree (also the type for the root node). It contains a `shared_nibble` field with the biggest common prefix (possible empty) for all keys in its subtree. It has a link to a Branch node.
        - Branch: it has a list with 16 entries (one for each hex char). Following the upper Extension `shared_nibble`, each entry in the list represents the next character for the keys. In a list cell, there may be empty nodes (if there's no key for such key prefix), a leaf node (if there's only one key for such prefix), or a new Extension node (if there's more than one key for such prefix).
        - Empty: used just to fulfil space.
        - Leaf: represent a data, e.g. an Ethereum account, indexed by a key.
