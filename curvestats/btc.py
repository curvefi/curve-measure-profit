"""
Module for Bitcoin tokens where Ren, like Compound, uses exchangeRateCurrent
"""

from web3.exceptions import BadFunctionCallOutput
from . import Pool, TOKEN_ABI


COMPOUND_ABI = TOKEN_ABI.copy()
COMPOUND_ABI += [
    {
        "constant": True,
        "inputs": [],
        "name": "exchangeRateCurrent",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
        "signature": "0x182df0f5"
    },
]


class BtcPool(Pool):
    def __init__(self, *args, w3=None):
        super().__init__(*args, w3=w3)
        for i in range(self.N):
            c = self.w3.eth.contract(abi=COMPOUND_ABI, address=self.coins[i]).functions
            self.coins[i] = c

    def get_rate(self, i, block=None):
        if not block:
            block = self.w3.eth.getBlock('latest')['number']
        kw = {'block_identifier': block}

        try:
            rate = self.coins[i].exchangeRateCurrent().call(**kw)
        except BadFunctionCallOutput:
            rate = 10 ** 18
        return rate
