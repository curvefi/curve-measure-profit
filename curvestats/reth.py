"""
Module for Y (iearn) tokens being used under the hood
"""

from . import Pool, TOKEN_ABI
from .abi import NEW_ABI


RETH_ABI = TOKEN_ABI.copy()
RETH_ABI += [
    {
        "inputs": [],
        "name": "getExchangeRate",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view", "type": "function"}
]


class RETHPool(Pool):
    def __init__(self, *args, w3=None):
        super().__init__(*args, w3=w3, abi=NEW_ABI)
        for i in range(self.N):
            c = self.w3.eth.contract(abi=RETH_ABI, address=self.coins[i]).functions
            self.coins[i] = c

    def get_rate(self, i, block=None):
        if not block:
            block = self.w3.eth.getBlock('latest')['number']
        kw = {'block_identifier': block}
        use_lending = (self.coins[i].address != "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE")
        rate = 10 ** 18
        if use_lending:
            rate = self.coins[i].getExchangeRate().call(**kw)
        return rate
