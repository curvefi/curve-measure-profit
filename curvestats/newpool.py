"""
Module for Compound tokens being used under the hood
"""

from . import Pool, TOKEN_ABI
from .abi import NEW_ABI


class NewPool(Pool):
    def __init__(self, *args, w3=None):
        super().__init__(*args, w3=w3, abi=NEW_ABI)
        for i in range(self.N):
            c = self.w3.eth.contract(abi=TOKEN_ABI, address=self.coins[i]).functions
            self.coins[i] = c

    def get_rate(self, i, block=None):
        if not block:
            block = self.w3.eth.getBlock('latest')['number']
        kw = {'block_identifier': block}

        rate = 10 ** 18
        return rate
