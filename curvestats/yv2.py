"""
Module for Y (iearn) tokens being used under the hood
"""

from . import Pool, TOKEN_ABI
from .abi import YV2_ABI


YV2_TOKEN_ABI = TOKEN_ABI.copy()
YV2_TOKEN_ABI += [
    {
        "constant": True,
        "inputs": [],
        "name": "exchangeRateStored",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"}
]


class YV2Pool(Pool):
    def __init__(self, *args, w3=None):
        super().__init__(*args, w3=w3, abi=YV2_ABI)
        for i in range(self.N):
            c = self.w3.eth.contract(abi=YV2_TOKEN_ABI, address=self.coins[i]).functions
            self.coins[i] = c

    def get_rate(self, i, block=None):
        if not block:
            block = self.w3.eth.getBlock('latest')['number']
        kw = {'block_identifier': block}
        use_lending = (self.coins[i].address != self.underlying_coins[i].address)

        rate = 10 ** 18
        if use_lending:
            rate = self.coins[i].exchangeRateStored().call(**kw)
        return rate
