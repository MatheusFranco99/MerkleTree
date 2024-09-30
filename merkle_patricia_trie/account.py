""" Patricia Merkle Trie """


from dataclasses import dataclass

@dataclass
class Account:
    """ Represents an account to be stored in the Merkle Patricia Trie """
    key: str # Account key, e.g. could be the Validator's public key
    balance: float

    def __init__(self, key: str, balance: float):
        self.key = key
        self.balance = balance

    def __repr__(self):
        return f"(Account Key: {self.key}, Balance: {self.balance})"

    def __str__(self):
        return self.__repr__()
