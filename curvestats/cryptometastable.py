import json
from retry import retry
from web3.exceptions import BadFunctionCallOutput


def load_abi(fname):
    import os.path
    fname = os.path.join(os.path.dirname(__file__), 'abis', fname + '.json')
    with open(fname) as f:
        result = json.load(f)
        if isinstance(result, list):
            return result
        else:
            return result['abi']


class Pool:
    # @retry(Exception, delay=5, tries=5, backoff=2)
    def __init__(self, pool, token, stable_pool, w3=None):
        if not w3:
            from .w3 import w3 as our_w3
            self.w3 = our_w3()
        erc20 = load_abi("CurveTokenV4")

        self.pool_contract = self.w3.eth.contract(abi=load_abi("CurveCryptoSwap"), address=pool)
        self.pool = self.pool_contract.functions
        self.token_contract = self.w3.eth.contract(abi=erc20, address=token)
        self.token = self.token_contract.functions

        self.stableswap = self.w3.eth.contract(abi=load_abi("Stableswap"), address=stable_pool).functions

        self.N = 0
        self.UN = 0
        self.underlying_coins = []
        self.coins = []
        self.decimals = []
        self.underlying_decimals = []

        for i in range(10):
            try:
                c = self.pool.coins(i).call()
                c = self.w3.eth.contract(abi=erc20, address=c).functions
                self.coins.append(c)
                self.decimals.append(int(c.decimals().call()))
                self.N += 1
                if i == 0:
                    for j in range(10):
                        try:
                            addr = self.stableswap.coins(j).call()
                        except (BadFunctionCallOutput, ValueError):
                            break
                        uc = self.w3.eth.contract(abi=erc20, address=addr).functions
                        self.underlying_coins.append(uc)
                        self.underlying_decimals.append(int(uc.decimals().call()))
                        self.UN += 1
                else:
                    self.UN += 1
                    self.underlying_coins.append(c)
                    self.underlying_decimals.append(self.decimals[-1])
            except (BadFunctionCallOutput, ValueError):
                if i == 0:
                    raise
                else:
                    break

    # @retry(Exception, delay=5, tries=5, backoff=2)
    def fetch_stats(self, block='latest'):
        full_block = self.w3.eth.getBlock(block)
        block = full_block['number']
        timestamp = full_block['timestamp']
        kw = {'block_identifier': block}
        vprice = self.stableswap.get_virtual_price().call(**kw)
        price_oracle = [self.pool.price_oracle(i).call(**kw) for i in range(self.N-1)]
        rates = [vprice/1e18] + [vprice*p / 1e36 for p in price_oracle]
        balances = [self.pool.balances(i).call(**kw) for i in range(self.N)]
        is_deposited = True
        for b in balances:
            is_deposited *= (b > 0)
        trades = []

        for e in self.pool_contract.events.TokenExchange.getLogs(fromBlock=block, toBlock=block):
            ev = e['args']
            # Volumes assume everything in the same price
            trades.append({
                'sold_id': ev['sold_id'],
                'tokens_sold': int(ev['tokens_sold'] * rates[ev['sold_id']]),
                'bought_id': ev['bought_id'],
                'tokens_bought': int(ev['tokens_bought'] * rates[ev['bought_id']])})

        try:
            vprice = is_deposited and self.pool.get_virtual_price().call(**kw)
        except Exception as e:
            print(block, e)
            vprice = 0

        return {
            'A': self.pool.A().call(**kw),
            'gamma': self.pool.gamma().call(**kw),
            'mid_fee': self.pool.mid_fee().call(**kw),
            'out_fee': self.pool.out_fee().call(**kw),
            'admin_fee': self.pool.admin_fee().call(**kw),
            'price_threshold': self.pool.price_threshold().call(**kw),
            'fee_gamma': self.pool.fee_gamma().call(**kw),
            'price_scale': [self.pool.price_scale(i).call(**kw) for i in range(self.N-1)],
            'supply': self.token.totalSupply().call(**kw),
            'virtual_price': vprice,
            'timestamp': timestamp,
            'balances': balances,
            'rates': rates,
            'trades': trades
        }
