#!/usr/bin/env python3

import lmdb
import json
import time
from time import sleep
from multiprocessing import Pool
from functools import partial

from curvestats.newpool import NewPool
from curvestats.meta_andre import MetaPool
from curvestats.tricrypto import Pool as CryptoPool
from curvestats.yv2 import YV2Pool

MPOOL_SIZE = 100

pools = {
        '2pool': (NewPool, ("0x27E611FD27b276ACbd5Ffd632E5eAEBEC9761E40", "0x27E611FD27b276ACbd5Ffd632E5eAEBEC9761E40"), 2320910),
        'fusdt': (MetaPool, ("0x92D5ebF3593a92888C25C0AbEF126583d4b5312E", "0x92D5ebF3593a92888C25C0AbEF126583d4b5312E",
                             "0x27E611FD27b276ACbd5Ffd632E5eAEBEC9761E40"), 3182906),
        'ren': (NewPool, ("0x3eF6A01A0f81D6046290f3e2A8c5b843e738E604", "0x5B5CFE992AdAC0C9D48E05854B2d91C73a003858"), 9464131),
        'tricrypto': (CryptoPool, ("0x3a1659Ddcf2339Be3aeA159cA010979FB49155FF", "0x58e57cA18B7A47112b877E31929798Cd3D703b0f"), 17198626),
        'ibftm': (YV2Pool, ("0x4FC8D635c3cB1d0aa123859e2B2587d0FF2707b1", "0xDf38ec60c0eC001142a33eAa039e49E9b84E64ED"), 19000245),
        'geist': (NewPool, ("0x0fa949783947Bf6c1b171DB13AEACBB488845B3f", "0xD02a30d33153877BC20e5721ee53DeDEE0422B2F"), 19420478)
}
start_blocks = {}

DB_NAME = 'fantom.lmdb'  # <- DB [block][pool#]{...}


def init_pools():
    for i, p in pools.items():
        if isinstance(p, tuple):
            pools[i] = p[0](*p[1])
            start_blocks[i] = p[2]


def fetch_stats(block, i='compound'):
    try:
        init_pools()
        return pools[i].fetch_stats(block)
    except Exception as e:
        if 'missing trie node' in str(e) or 'not found' in str(e):
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

    start_block = 19420478
    # start_block = w3.eth.getBlock('latest')['number'] - 1000
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
