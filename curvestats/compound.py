"""
Module for Compound tokens being used under the hood
"""

from . import Pool, TOKEN_ABI


COMPOUND_ABI = TOKEN_ABI.copy()
COMPOUND_ABI += [
    {
        "constant": True,
        "inputs": [],
        "name": "exchangeRateStored",
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
    {
        "constant": True,
        "inputs": [],
        "name": "supplyRatePerBlock",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
        "signature": "0xae9d70b0"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "accrualBlockNumber",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
        "signature": "0x6c540baf"
    },
]


class CompoundPool(Pool):
    def __init__(self, *args, w3=None):
        super().__init__(*args, w3=w3)
        for i in range(self.N):
            c = self.w3.eth.contract(abi=COMPOUND_ABI, address=self.coins[i]).functions
            self.coins[i] = c

    def get_rate(self, i, block=None):
        if not block:
            block = self.current_block
        kw = {'block_identifier': block}
        use_lending = (self.coins[i].address != self.underlying_coins[i].address)

        result = 10 ** 18 // 10 ** self.decimals[i]
        rate = 10 ** 18
        if use_lending:
            rate = self.coins[i].exchangeRateStored().call(**kw)
            supply_rate = self.coins[i].supplyRatePerBlock().call(**kw)
            old_block = self.coins[i].accrualBlockNumber().call(**kw)
            rate += rate * supply_rate * (block - old_block) // 10 ** 18
        result *= rate
        return result

        if self.coins[i].address != self.underlying_coins[i].address:
            rate = self.coins[i].exchangeRateStored().call(**kw)
            return rate

        else:
            return 10 ** 18
