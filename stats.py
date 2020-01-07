#!/usr/bin/env python3

import time
import config
from retry import retry
from web3.auto.infura import w3

###
PRINT_FMT = r'[{0}] token_price: {1:.6f} | dai->usdc: {2:.6f} | usdc->dai: {3:.6f}'
FILE_FMT = '{0}, {1:.6f}, {2:.6f}, {3:.6f}\n'
swap = w3.eth.contract(abi=config.SWAP_ABI, address=config.SWAP_ADDRESS)


@retry(Exception, delay=5, tries=5, backoff=2)
def get_info():
    virtual_price = swap.caller.get_virtual_price() / 10 ** 18
    dai2usdc = swap.caller.get_dy_underlying(0, 1, 10 ** 18) / 10 ** 6
    usdc2dai = swap.caller.get_dy_underlying(1, 0, 10 ** 6) / 10 ** 18
    return [virtual_price, dai2usdc, usdc2dai]


if __name__ == '__main__':
    while True:
        results = get_info()
        t = int(time.time())
        results = [t] + results
        with open('swap-stats.csv', 'a') as f:
            f.write(FILE_FMT.format(*results))
        print(PRINT_FMT.format(*results))
        time.sleep(60)
