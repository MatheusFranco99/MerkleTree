""" Transaction """

from dataclasses import dataclass
import random

MAX_NONCE = 1e9

class TransactionID(int):
    """ Identifier for transaction """

@dataclass
class Transaction:
    """ Transaction class with identifier and nonce """
    identifier: TransactionID
    nonce: float # A random nonce is used so that the content of the transaction seems to vary between implementations

    def __init__(self, identifier: TransactionID):
        self.identifier = identifier
        self.nonce = random.randint(1, MAX_NONCE)

    def body(self) -> str:
        """ Returns the body of the transaction """
        return f"(ID: {self.identifier}, Nonce: {self.nonce})"

    def equal(self, other) -> bool:
        """ Returns if it's equal to the other object """
        if not isinstance(other, Transaction):
            return False
        return (self.identifier == other.identifier) and (self.nonce == other.nonce)

    def __repr__(self):
        return self.body()

    def __str__(self):
        return self.body()
