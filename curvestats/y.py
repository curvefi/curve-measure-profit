"""
Module for Y (iearn) tokens being used under the hood
"""

from . import Pool, TOKEN_ABI


Y_ABI = TOKEN_ABI.copy()
Y_ABI += [
    {
        "constant": True,
        "inputs": [],
        "name": "getPricePerFullShare",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"}
]


class YPool(Pool):
    def __init__(self, *args, w3=None):
        super().__init__(*args, w3=w3)
        for i in range(self.N):
            c = self.w3.eth.contract(abi=Y_ABI, address=self.coins[i]).functions
            self.coins[i] = c

    def get_rate(self, i, block=None):
        if not block:
            block = self.w3.eth.getBlock('latest')['number']
        kw = {'block_identifier': block}
        use_lending = (self.coins[i].address != self.underlying_coins[i].address)

        rate = 10 ** 18
        if use_lending:
            rate = self.coins[i].getPricePerFullShare().call(**kw)
        return rate
