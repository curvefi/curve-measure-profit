"""
Module for Compound tokens being used under the hood
"""

from retry import retry
from web3.exceptions import BadFunctionCallOutput, ABIFunctionNotFound, ABIEventFunctionNotFound
from . import Pool, TOKEN_ABI
from .abi import NEW_ABI

ABI = NEW_ABI.copy()
ABI += [{"name":"base_pool","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2291}]


class MetaPool:
    def __init__(self, pool, token, w3=None, abi=ABI):
        if not w3:
            from web3.auto.infura import w3 as infura_w3
            self.w3 = infura_w3
        self.pool_contract = self.w3.eth.contract(abi=abi, address=pool)
        self.pool = self.pool_contract.functions
        self.token_contract = self.w3.eth.contract(abi=TOKEN_ABI, address=token)
        self.token = self.token_contract.functions
        self.base_pool = self.w3.eth.contract(abi=ABI, address=self.pool.base_pool().call()).functions

        self.coins = []
        for i in range(10):
            try:
                self.pool.balances(i).call()
                c = self.pool.coins(i).call()
                self.coins.append(c)
            except (BadFunctionCallOutput, ValueError):
                break
        self.N = len(self.coins)
        self.coins = [self.w3.eth.contract(abi=TOKEN_ABI, address=addr).functions for addr in self.coins]
        self.decimals = [c.decimals().call() for c in self.coins]

        self.underlying_coins = self.coins[:-1]
        self.underlying_decimals = self.decimals[:-1]
        self.underlying_N = self.N - 1
        for i in range(10):
            try:
                self.base_pool.balances(i).call()
                uc = self.base_pool.coins(i).call()
                uc = self.w3.eth.contract(abi=TOKEN_ABI, address=uc).functions
                self.underlying_coins.append(uc)
                self.underlying_decimals.append(uc.decimals().call())
                self.underlying_N += 1
            except (BadFunctionCallOutput, ValueError):
                break

    def get_rate(self, i, underlying=False, block=None):
        if not block:
            block = self.w3.eth.getBlock('latest')['number']
        kw = {'block_identifier': block}
        use_lending = (i == self.N - 1) and not underlying

        rate = 10 ** 18
        if use_lending:
            rate = self.base_pool.get_virtual_price().call(**kw)
        return rate

    @retry(Exception, delay=5, tries=5, backoff=2)
    def fetch_stats(self, block='latest'):
        full_block = self.w3.eth.getBlock(block)
        block = full_block['number']
        timestamp = full_block['timestamp']
        kw = {'block_identifier': block}
        rates = [self.get_rate(i, block=block) for i in range(self.N)]
        underlying_rate = 10 ** 18
        balances = [self.pool.balances(i).call(**kw) for i in range(self.N)]
        is_deposited = True
        for b in balances:
            is_deposited *= (b > 0)
        trades = []

        try:
            for e in self.pool_contract.events.TokenExchangeUnderlying.getLogs(fromBlock=block, toBlock=block):
                ev = e['args']
                trades.append({
                    'sold_id': ev['sold_id'],
                    'tokens_sold': ev['tokens_sold'],
                    'bought_id': ev['bought_id'],
                    'tokens_bought': ev['tokens_bought'],
                    'underlying': True})
        except ABIEventFunctionNotFound:
            pass

        for e in self.pool_contract.events.TokenExchange.getLogs(fromBlock=block, toBlock=block):
            ev = e['args']
            trades.append({
                'sold_id': ev['sold_id'],
                'tokens_sold': ev['tokens_sold'] * rates[ev['sold_id']] // 1e18,
                'bought_id': ev['bought_id'],
                'tokens_bought': ev['tokens_bought'] * rates[ev['bought_id']] // 1e18})

        return {
            'A': self.pool.A().call(**kw),
            'fee': self.pool.fee().call(**kw),
            'admin_fee': self.pool.admin_fee().call(**kw),
            'supply': self.token.totalSupply().call(**kw),
            'virtual_price': is_deposited and self.pool.get_virtual_price().call(**kw),
            'timestamp': timestamp,
            'balances': balances,
            'rates': rates,
            'underlying_rate': underlying_rate,
            'trades': trades
        }
