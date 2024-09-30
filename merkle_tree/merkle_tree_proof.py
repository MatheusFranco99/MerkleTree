""" Merkle Tree """

from dataclasses import dataclass
from enum import Enum
from typing import Callable

def join_hashes(hash_a: str, hash_b: str, hash_f: Callable[[str, str], str]) -> str:
    """ Returns the hash of the combination of two hashes """
    return hash_f(hash_a + hash_b)

class MerkleJoinDirection(Enum):
    """ Direction to which perform the join operation for the Merkle proof """
    LEFT = 1
    RIGHT = 2

@dataclass
class MerkleProofOperation:
    """ Represents an operation for the Merkle proof """
    hash: str
    direction: MerkleJoinDirection

    def __repr__(self):
        return f"(Hash:{self.hash[:5]}, direction: {self.direction})"

    def __str__(self):
        return self.__repr__()

@dataclass
class MerkleProof:
    """ Represents the Merkle Proof with a sequence of operations that should result on the the root node's hash """
    operations: list[MerkleProofOperation]

    def __repr__(self):
        ret: str = ""
        for i, operation in enumerate(self.operations):
            ret += str(i) + ": " + str(operation) + "\n"
        return ret

    def __str__(self):
        return self.__repr__()

def verify_merkle_proof(target_hash: str, merkle_proof: MerkleProof, merkle_root: str, hash_function: callable) -> bool:
    """ Verifies if a proof is correct """

    curr_hash: str = target_hash

    for merkle_operation in merkle_proof.operations:
        if merkle_operation.direction == MerkleJoinDirection.LEFT:
            curr_hash = join_hashes(merkle_operation.hash, curr_hash, hash_function)
        elif merkle_operation.direction == MerkleJoinDirection.RIGHT:
            curr_hash = join_hashes(curr_hash, merkle_operation.hash, hash_function)
        else:
            raise ValueError("Invalid direction for proof operation")

    return curr_hash == merkle_root
