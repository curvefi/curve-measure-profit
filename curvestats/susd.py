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

CRV_ABI = [
    {
      "name": "get_virtual_price",
      "outputs": [
       {
        "type": "uint256",
        "name": "out"
       }
      ],
      "inputs": [],
      "constant": True,
      "payable": False,
      "type": "function",
      "gas": 1074737
     }
]


class SUSDPool(Pool):
    def __init__(self, pool, token, rate_contracts, w3=None):
        super().__init__(pool, token, w3=w3)
        self.rate_contracts = []

        for i in range(self.N):
            c = self.w3.eth.contract(abi=Y_ABI, address=self.coins[i]).functions
            self.coins[i] = c
            if rate_contracts[i]:
                r = self.w3.eth.contract(abi=CRV_ABI, address=rate_contracts[i]).functions
            else:
                r = None
            self.rate_contracts.append(r)

    def get_rate(self, i, block=None):
        if not block:
            block = self.w3.eth.getBlock('latest')['number']
        kw = {'block_identifier': block}
        use_lending = (self.coins[i].address != self.underlying_coins[i].address)

        rate = 10 ** 18
        if use_lending:
            rate = self.coins[i].getPricePerFullShare().call(**kw)
        elif self.rate_contracts[i] is not None:
            rate = self.rate_contracts[i].get_virtual_price().call(**kw)
        return rate
