"""
Module for Y (iearn) tokens being used under the hood
"""

from . import Pool, TOKEN_ABI
from .abi import IDLE_ABI as IDLE_POOL_ABI


IDLE_ABI = TOKEN_ABI.copy()
IDLE_ABI += [
    {
        "constant": True,
        "inputs": [],
        "name": "tokenPrice",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"}
]


class IDLEPool(Pool):
    def __init__(self, *args, w3=None):
        super().__init__(*args, w3=w3, abi=IDLE_POOL_ABI)
        for i in range(self.N):
            c = self.w3.eth.contract(abi=IDLE_ABI, address=self.coins[i]).functions
            self.coins[i] = c

    def get_rate(self, i, block=None):
        if not block:
            block = self.w3.eth.getBlock('latest')['number']
        kw = {'block_identifier': block}
        use_lending = (self.coins[i].address != self.underlying_coins[i].address)

        rate = 10 ** 18
        if use_lending:
            rate = self.coins[i].tokenPrice().call(**kw)
        return rate
