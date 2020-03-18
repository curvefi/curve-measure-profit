#!/usr/bin/env python3

import os
from time import sleep

os.environ['WEB3_INFURA_PROJECT_ID'] = 'efd35366fc0445f98df93cc418832774'

from web3.auto.infura import w3
from curvestats.compound import CompoundPool

pools = [
    CompoundPool("0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56", "0x845838DF265Dcd2c412A1Dc9e959c7d08537f8a2")
]

stats = [{} for _ in pools]  # <- DB instead of this


if __name__ == '__main__':
    start_block = w3.eth.getBlock('latest')['number'] - 10  # XXX pull from DB
    print('Monitor started')

    # Initial data
    for i, pool in enumerate(pools):
        stats[i] = {
                    'N': pool.N, 'decimals': pool.decimals,
                    'token': pool.token.address, 'pool': pool.pool.address,
                    'coins': [pool.coins[j].address for j in range(pool.N)],
                    'underlying_coins': [pool.underlying_coins[j].address for j in range(pool.N)]}

    while True:
        current_block = w3.eth.getBlock('latest')['number']

        if current_block > start_block:
            for block in range(start_block + 1, current_block + 1):
                for i, pool in enumerate(pools):
                    stats[i][block] = pool.fetch_stats()
                print(block)
            start_block = current_block

        sleep(15)
