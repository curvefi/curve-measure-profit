#!/usr/bin/env python3

import time
import config
from web3.auto.infura import w3

###
swap = w3.eth.contract(abi=config.SWAP_ABI, address=config.SWAP_ADDRESS)


def get_info():
    virtual_price = swap.caller.get_virtual_price() / 10 ** 18
    dai2usdc = swap.caller.get_dy_underlying(0, 1, 10 ** 18) / 10 ** 6
    usdc2dai = swap.caller.get_dy_underlying(1, 0, 10 ** 6) / 10 ** 18
    return virtual_price, dai2usdc, usdc2dai


if __name__ == '__main__':
    while True:
        results = get_info()
        print(results)
        time.sleep(5)
