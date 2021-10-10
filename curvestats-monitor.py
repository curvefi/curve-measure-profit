#!/usr/bin/env python3

import lmdb
import json
import time
from time import sleep
from multiprocessing import Pool
from functools import partial

from curvestats.newpool import NewPool
from curvestats.cryptometastable import Pool as CryptoPool  # noqa

MPOOL_SIZE = 25

pools = {
        '3pool': (NewPool, ("0xC5cfaDA84E902aD92DD40194f0883ad49639b023", "0xC5cfaDA84E902aD92DD40194f0883ad49639b023"), 18000572),
}
start_blocks = {}

DB_NAME = 'harmony.lmdb'  # <- DB [block][pool#]{...}


def init_pools():
    for i, p in pools.items():
        if isinstance(p, tuple):
            pools[i] = p[0](*p[1])
            start_blocks[i] = p[2]


def fetch_stats(block, i='compound'):
    try:
        init_pools()
        return pools[i].fetch_stats(block)
    except ValueError as e:
        if 'missing trie node' in str(e):
            print('missing trie node for', block)
            return {}
        else:
            raise


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
    from curvestats.w3 import w3 as our_w3
    w3 = our_w3()
    init_pools()

    db = lmdb.open(DB_NAME, map_size=(2 ** 35))

    # start_block = 18000572
    start_block = w3.eth.getBlock('latest')['number'] - 100
    print('Monitor started')

    # Initial data
    with db.begin(write=True) as tx:
        if pools_not_in_block(tx, 0) or True:  # XXX
            tx.put(int2uid(0), json.dumps(
                        {k: {
                            'N': pool.N,
                            'underlying_N': pool.underlying_N if hasattr(pool, 'underlying_N') else pool.N,
                            'decimals': pool.decimals,
                            'underlying_decimals': pool.underlying_decimals if hasattr(pool, 'underlying_decimals') else pool.decimals,
                            'token': pool.token.address, 'pool': pool.pool.address,
                            'coins': [pool.coins[j].address for j in range(pool.N)],
                            'underlying_coins': [pool.underlying_coins[j].address for j in range(getattr(pool, 'underlying_N', pool.N))]}
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
