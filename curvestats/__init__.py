#!/usr/bin/env python3
"""
Recording full statistics about the state of Curve pools
"""
from retry import retry
from web3.exceptions import BadFunctionCallOutput, ABIFunctionNotFound, ABIEventFunctionNotFound
from .abi import ABI, TOKEN_ABI


class Pool:
    @retry(Exception, delay=5, tries=5, backoff=2)
    def __init__(self, pool, token, w3=None, abi=ABI):
        if not w3:
            from .w3 import w3 as our_w3
            self.w3 = our_w3()
        self.pool_contract = self.w3.eth.contract(abi=abi, address=pool)
        self.pool = self.pool_contract.functions
        self.token_contract = self.w3.eth.contract(abi=TOKEN_ABI, address=token)
        self.token = self.token_contract.functions

        self.N = 0
        self.underlying_coins = []
        self.coins = []
        self.decimals = []
        for i in range(10):
            try:
                self.pool.balances(i).call()
                c = self.pool.coins(i).call()
                self.coins.append(c)  # just address
                try:
                    uc = self.pool.underlying_coins(i).call()
                except (BadFunctionCallOutput, ABIFunctionNotFound, ValueError):
                    uc = c
                uc = self.w3.eth.contract(abi=TOKEN_ABI, address=uc).functions
                self.underlying_coins.append(uc)
                try:
                    self.decimals.append(uc.decimals().call())
                except Exception:
                    self.decimals.append(18)
                self.N += 1
            except (BadFunctionCallOutput, ValueError):
                if i == 0:
                    raise
                else:
                    break

    def get_rate(self, i, block=None):
        return 10 ** 18

    @retry(Exception, delay=5, tries=5, backoff=2)
    def fetch_stats(self, block='latest'):
        full_block = self.w3.eth.getBlock(block)
        block = full_block['number']
        timestamp = full_block['timestamp']
        kw = {'block_identifier': block}
        rates = [self.get_rate(i, block=block) for i in range(self.N)]
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
                    'tokens_bought': ev['tokens_bought']})
        except ABIEventFunctionNotFound:
            pass

        for e in self.pool_contract.events.TokenExchange.getLogs(fromBlock=block, toBlock=block):
            ev = e['args']
            trades.append({
                'sold_id': ev['sold_id'],
                'tokens_sold': ev['tokens_sold'] * rates[ev['sold_id']] // 1e18,
                'bought_id': ev['bought_id'],
                'tokens_bought': ev['tokens_bought'] * rates[ev['bought_id']] // 1e18})

        try:
            vprice = is_deposited and self.pool.get_virtual_price().call(**kw)
        except Exception as e:
            print(block, e)
            vprice = 0

        return {
            'A': self.pool.A().call(**kw),
            'fee': self.pool.fee().call(**kw),
            'admin_fee': self.pool.admin_fee().call(**kw),
            'supply': self.token.totalSupply().call(**kw),
            'virtual_price': vprice,
            'timestamp': timestamp,
            'balances': balances,
            'rates': rates,
            'trades': trades
        }
