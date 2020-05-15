#!/usr/bin/env python3

import lmdb
import json
import time
import config_infura  # noqa
from time import sleep
from multiprocessing import Pool
from functools import partial

from curvestats.compound import CompoundPool
from curvestats.y import YPool
from curvestats.susd import SUSDPool

MPOOL_SIZE = 40

pools = {
        'compound': (CompoundPool, ("0xA2B47E3D5c44877cca798226B7B8118F9BFb7A56", "0x845838DF265Dcd2c412A1Dc9e959c7d08537f8a2"), 9554041),
        'usdt': (CompoundPool, ("0x52EA46506B9CC5Ef470C5bf89f17Dc28bB35D85C", "0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23"), 9456294),
        'y': (YPool, ("0x45F783CCE6B7FF23B2ab2D70e416cdb7D6055f51", "0xdF5e0e81Dff6FAF3A7e52BA697820c5e32D806A8"), 9476469),
        'busd': (YPool, ("0x79a8C46DeA5aDa233ABaFFD40F3A0A2B1e5A4F27", "0x3B3Ac5386837Dc563660FB6a0937DFAa5924333B"), 9567296),
        'susd': (CompoundPool, ('0xA5407eAE9Ba41422680e2e00537571bcC53efBfD', '0xC25a3A3b969415c80451098fa907EC722572917F'), 9906599),
        'pax': (YPool, ("0x06364f10B501e868329afBc005b3492902d6C763", "0xD905e2eaeBe188fc92179b6350807D8bd91Db0D8"), 10041041),
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


def pools_not_in_block(tx, b):
    out = []
    block = tx.get(int2uid(b))
    if block:
        block = json.loads(block)
    if block:
        for k in pools:
            if k not in block:
                out.append(k)
    else:
        out = list(pools)
    return out


mpool = Pool(MPOOL_SIZE)
init_pools()


if __name__ == '__main__':
    from web3.auto.infura import w3
    init_pools()

    db = lmdb.open(DB_NAME, map_size=(2 ** 32))

    start_block = 10040000
    # start_block = w3.eth.getBlock('latest')['number'] - 1000
    print('Monitor started')

    # Initial data
    with db.begin(write=True) as tx:
        if pools_not_in_block(tx, 0):
            tx.put(int2uid(0), json.dumps(
                        {k: {
                            'N': pool.N, 'decimals': pool.decimals,
                            'token': pool.token.address, 'pool': pool.pool.address,
                            'coins': [pool.coins[j].address for j in range(pool.N)],
                            'underlying_coins': [pool.underlying_coins[j].address for j in range(pool.N)]}
                         for k, pool in pools.items()}).encode())

    while True:
        while True:
            try:
                current_block = w3.eth.getBlock('latest')['number'] + 1
                break
            except Exception:
                time.sleep(10)

        if current_block - start_block > MPOOL_SIZE:
            blocks = range(start_block, start_block + MPOOL_SIZE)
            with db.begin(write=True) as tx:
                pools_to_fetch = pools_not_in_block(tx, blocks[-1])
                if pools_to_fetch:
                    stats = {}
                    for p in pools_to_fetch:
                        if blocks[0] >= start_blocks[p]:
                            newstats = mpool.map(partial(fetch_stats, i=p), blocks)
                            for b, s in zip(blocks, newstats):
                                if b not in stats:
                                    stats[b] = {}
                                stats[b][p] = s
                    for b, v in stats.items():
                        block = tx.get(int2uid(b))
                        if block:
                            block = json.loads(block)
                            v.update(block)
                        tx.put(int2uid(b), json.dumps(v).encode())
                    pools_fetched = [p for p in pools_to_fetch
                                     if blocks[-1] in stats and p in stats[blocks[-1]]]
                    print('...', start_block, pools_fetched)
                else:
                    print('... already in DB:', start_block)
            start_block += MPOOL_SIZE

        else:
            if current_block > start_block:
                for block in range(start_block, current_block):
                    with db.begin(write=True) as tx:
                        if pools_not_in_block(tx, block):
                            stats = {}
                            for p, pool in pools.items():
                                if block >= start_blocks[p]:
                                    stats[p] = pool.fetch_stats(block)
                            print(block, [len(s['trades']) for s in stats.values()])
                            tx.put(int2uid(block), json.dumps(stats).encode())
                start_block = current_block

            sleep(15)
