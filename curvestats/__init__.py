#!/usr/bin/env python3
"""
Recording full statistics about the state of Curve pools
"""
from web3.exceptions import BadFunctionCallOutput
from .abi import ABI, TOKEN_ABI


class Pool:
    def __init__(self, pool, token, w3=None):
        if not w3:
            from web3.auto.infura import w3 as infura_w3
            self.w3 = infura_w3
        self.pool = self.w3.eth.contract(abi=ABI, address=pool).functions
        self.token = self.w3.eth.contract(abi=TOKEN_ABI, address=token).functions

        self.N = 0
        self.underlying_coins = []
        self.coins = []
        self.decimals = []
        for i in range(10):
            try:
                self.pool.balances(i).call()
                uc = self.pool.underlying_coins(i).call()
                uc = self.w3.eth.contract(abi=TOKEN_ABI, address=uc).functions
                self.underlying_coins.append(uc)
                c = self.pool.coins(i).call()
                self.coins.append(c)  # just address
                self.decimals.append(uc.decimals().call())
                self.N += 1
            except BadFunctionCallOutput:
                break

    @property
    def current_block(self):
        return self.w3.eth.getBlock('latest')['number']

    def get_rate(self, i, block=None):
        return 10 ** 18

    # XXX retry
    def fetch_stats(self, block=None):
        if not block:
            block = self.current_block
        kw = {'block_identifier': block}
        return {
            'A': self.pool.A().call(**kw),
            'fee': self.pool.fee().call(**kw),
            'admin_fee': self.pool.fee().call(**kw),
            'supply': self.token.totalSupply().call(**kw),
            'virtual_price': self.pool.get_virtual_price().call(**kw),
            'balances': [
                self.pool.balances(i).call(**kw) for i in range(self.N)],
            'rates': [self.get_rate(i, block=block) for i in range(self.N)]
        }
