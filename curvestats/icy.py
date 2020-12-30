"""
Module for Compound tokens being used under the hood
"""

from . import Pool, TOKEN_ABI
from .abi import NEW_ABI

ABI = NEW_ABI.copy()
ABI += [{"name":"get_coin_rates","outputs":[{"type":"uint256[6]","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":20572}]


class IcyPool(Pool):
    def __init__(self, *args, w3=None):
        super().__init__(*args, w3=w3, abi=ABI)
        for i in range(self.N):
            c = self.w3.eth.contract(abi=TOKEN_ABI, address=self.coins[i]).functions
            self.coins[i] = c

    def get_rate(self, i, block=None):
        if not block:
            block = self.w3.eth.getBlock('latest')['number']
        kw = {'block_identifier': block}
        use_lending = (i < self.N - 1)

        rate = 10 ** 18
        if use_lending:
            rate = self.pool.get_coin_rates().call(**kw)[i]
        return rate
