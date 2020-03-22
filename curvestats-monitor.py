#!/usr/bin/env python3

import lmdb
import json
import os
from time import sleep
from multiprocessing import Pool
from functools import partial
from pprint import pprint

os.environ['WEB3_INFURA_PROJECT_ID'] = 'efd35366fc0445f98df93cc418832774'

from curvestats.compound import CompoundPool

MPOOL_SIZE = 25

pools = [
    (CompoundPool, ("0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56", "0x845838DF265Dcd2c412A1Dc9e959c7d08537f8a2"))
]

DB_NAME = 'curvestats.lmdb'  # <- DB [block][pool#]{...}


def init_pools():
    for i, p in enumerate(pools):
        if isinstance(p, tuple):
            pools[i] = p[0](*p[1])


def fetch_stats(block, i=0):
    init_pools()
    return pools[i].fetch_stats(block)


def int2uid(value):
    return int.to_bytes(value, 4, 'big')


mpool = Pool(MPOOL_SIZE)
init_pools()


if __name__ == '__main__':
    from web3.auto.infura import w3
    init_pools()

    db = lmdb.open(DB_NAME)
    db.set_mapsize(2 ** 29)

    start_block = w3.eth.getBlock('latest')['number'] - 100  # XXX pull from DB
    print('Monitor started')

    # Initial data
    with db.begin(write=True) as tx:
        if not tx.get(int2uid(0)):
            tx.put(int2uid(0), json.dumps(
                        [{'N': pool.N, 'decimals': pool.decimals,
                          'token': pool.token.address, 'pool': pool.pool.address,
                          'coins': [pool.coins[j].address for j in range(pool.N)],
                         'underlying_coins': [pool.underlying_coins[j].address for j in range(pool.N)]}
                         for pool in pools]).encode())

    while True:
        current_block = w3.eth.getBlock('latest')['number'] + 1

        if current_block - start_block > MPOOL_SIZE:
            blocks = range(start_block, start_block + MPOOL_SIZE)
            with db.begin(write=True) as tx:
                if not tx.get(int2uid(blocks[-1])):
                    stats = {}
                    for i in range(len(pools)):
                        newstats = mpool.map(partial(fetch_stats, i=i), blocks)
                        for b, s in zip(blocks, newstats):
                            if b not in stats:
                                stats[b] = [None] * len(pools)
                            stats[b][i] = s
                    for b, v in stats.items():
                        tx.put(int2uid(b), json.dumps(v).encode())
                    print('...', start_block)
                else:
                    print('... already in DB:', start_block)
            start_block += MPOOL_SIZE

        else:
            if current_block > start_block:
                for block in range(start_block, current_block):
                    with db.begin(write=True) as tx:
                        if not tx.get(int2uid(block)):
                            stats = [None] * len(pools)
                            for i, pool in enumerate(pools):
                                stats[i] = pool.fetch_stats(block)
                            print(block)
                            if stats[i]['trades']:
                                pprint(stats[i]['trades'])
                            tx.put(int2uid(block), json.dumps(stats).encode())
                start_block = current_block

            sleep(15)
