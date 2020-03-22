#!/usr/bin/env python3

import lmdb
import json
import config  # noqa
from time import sleep
from multiprocessing import Pool
from functools import partial

from curvestats.compound import CompoundPool
from curvestats.y import YPool

MPOOL_SIZE = 10

pools = {
        'compound': (CompoundPool, ("0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56", "0x845838DF265Dcd2c412A1Dc9e959c7d08537f8a2"), 9554041),
        'usdt': (CompoundPool, ("0x52EA46506B9CC5Ef470C5bf89f17Dc28bB35D85C", "0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23"), 9456294),
        'y': (YPool, ("0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51", "0xdF5e0e81Dff6FAF3A7e52BA697820c5e32D806A8"), 9476469),
        'busd': (YPool, ("0x79a8C46DeA5aDa233ABaFFD40F3A0A2B1e5A4F27", "0x3B3Ac5386837Dc563660FB6a0937DFAa5924333B"), 9567296)
}
start_blocks = {}

DB_NAME = 'curvestats.lmdb'  # <- DB [block][pool#]{...}


def init_pools():
    for i, p in pools.items():
        if isinstance(p, tuple):
            pools[i] = p[0](*p[1])
            start_blocks[i] = p[2]


def fetch_stats(block, i='compound'):
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
                        {k: {
                            'N': pool.N, 'decimals': pool.decimals,
                            'token': pool.token.address, 'pool': pool.pool.address,
                            'coins': [pool.coins[j].address for j in range(pool.N)],
                            'underlying_coins': [pool.underlying_coins[j].address for j in range(pool.N)]}
                         for k, pool in pools.items()}).encode())

    while True:
        current_block = w3.eth.getBlock('latest')['number'] + 1

        if current_block - start_block > MPOOL_SIZE:
            blocks = range(start_block, start_block + MPOOL_SIZE)
            with db.begin(write=True) as tx:
                if not tx.get(int2uid(blocks[-1])):
                    stats = {}
                    for p in pools:
                        if blocks[0] >= start_blocks[p]:
                            newstats = mpool.map(partial(fetch_stats, i=p), blocks)
                            for b, s in zip(blocks, newstats):
                                if b not in stats:
                                    stats[b] = {}
                                stats[b][p] = s
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
                            stats = {}
                            for p, pool in pools.items():
                                if block >= start_blocks[p]:
                                    stats[p] = pool.fetch_stats(block)
                            print(block, [len(s['trades']) for s in stats.values()])
                            tx.put(int2uid(block), json.dumps(stats).encode())
                start_block = current_block

            sleep(15)
